from bs4 import BeautifulSoup
from converter import nlp, image_converter
import re, os


# finds which type of header the file is using for sections
def get_type_of_header_tags_used(soup):
    h1_count = 0
    h2_count = 0

    for h in soup.findAll('h1'):
        h1_count += 1

    for h in soup.findAll('h2'):
        h2_count += 1

    if h1_count > h2_count:
        return 'h1'
    if h1_count < h2_count:
        return 'h2'
    if h1_count == 0 and h2_count == 0:
        return 'none'
    return 'both'


# need to create a function that can universally strip tags specified
def remove_children_tags(parent_tag, child_tags):
    children = parent_tag.findChildren(child_tags, recursive=True)
    for child in children:
        child.decompose()


# removes the static table of contents so we can replace it with a linked one
def remove_table_of_contents(soup):
    # search for toc
    tbl_of_contents_string = re.compile(r'Table of Contents')
    toc = soup.find(text=tbl_of_contents_string)

    # if a table of contents exists, remove it.
    if toc:
        toc = toc.parent
        toc_tag_type = toc.name

        # deletes next tag until it finds a new tag type
        for next_tag in list(toc.find_next_siblings()):
            if next_tag.name != toc_tag_type:
                return
            next_tag.decompose()


# creates a table of contents with links to each head tag
def make_new_table_of_contents(soup, tag):
    # loop through all header tags and put them in a list
    h_strings = []
    for h in soup.findAll(tag):
        for s in list(h.strings):
            h_strings.insert(0, s)

    # find the toc tag
    tbl_of_contents_string = re.compile(r'Table of Contents')
    toc = soup.find(text=tbl_of_contents_string)

    # if there is a table of contents, add new one below that
    if toc:
        toc = toc.parent

        # loop through and create a new tag for each header
        for s in h_strings:
            br = soup.new_tag('br')
            toc.insert_after(br)
            new_tag = soup.new_tag('a', href="#" + s)
            new_tag.string = s
            toc.insert_after(new_tag)
            
    # no table of contents so build a whole new one
    else:
        # find top tag and add below that
        top = soup.find('a', id="top")
        toc = soup.new_tag('h3')
        toc.string = 'Table of Contents'
        top.insert_after(toc)

        for s in h_strings:
            br = soup.new_tag('br')
            toc.insert_after(br)
            new_tag = soup.new_tag('a', href="#" + s)
            new_tag.string = s
            toc.insert_after(new_tag)


# converts all ftp links & url text to drive links
def convert_ftp_to_drive(soup):
    # replace href with drive link
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('ftp://podaac.jpl.nasa.gov/'):
            a['href'] = a['href'].replace('ftp://podaac.jpl.nasa.gov/', 'https://podaac-tools.jpl.nasa.gov/drive/files/')
        
    # replace <a> tag url string on page with drive link
    for a_tags in soup.find_all('a'):
        for s in list(a_tags.strings):
            if s.startswith('ftp://podaac.jpl.nasa.gov/'):
                new_link = s.replace('ftp://podaac.jpl.nasa.gov/', 'https://podaac-tools.jpl.nasa.gov/drive/files/')
                s.replace_with(new_link)


# adds an id to all tags using the string inside each tag
def add_id_to_tags(soup, tag):
    for tags in soup.findAll(tag):
        for s in list(tags.strings):
            tags['id'] = s


# adds bootstrap styling to document
def add_bootstrap(soup):
    # add responsive container class to all images
    for img in soup.find_all('img'):
        img['class'] = 'img-fluid'
        img['alt'] = 'image'

    # add responsive table class to all tables
    for tbl in soup.find_all('table'):
        tbl.wrap(soup.new_tag('div', **{'class': 'table-responsive'}))
        tbl['class'] = 'table table-bordered'


# add podaac specific header, footer, css styling etc
def add_podaac(soup):
    # adds alt tag and podaac specific img wrapper that needs to line up with PODAAC CSS
    for img in soup.find_all('img'):
        img['class'] = 'podaac-img-fluid'
        img['alt'] = 'image'

    # add responsive table class to all tables - needs to line up with PODAAC CSS
    for tbl in soup.find_all('table'):
        tbl.wrap(soup.new_tag('div', **{'class': 'podaac-table-responsive'}))
        tbl['class'] = 'podaac-table podaac-table-bordered'


# loops through all header tag strings and replaces them with structured words
def process_header(soup, tag):
    for h in soup.findAll(tag):
        # remove all <a> tags in headers
        remove_children_tags(h, 'a')

        # set header string variable for nlp analysis
        for s in list(h.strings):
            hs = nlp.prepare_string_for_nlp(s)

            # send word for nlp analysis
            replacement_string = nlp.get_replacement_word(hs)

            # if nlp returns a valid replacement word replace header section
            if replacement_string:
                s.replace_with(replacement_string)
    

# uses bs4 to parse html doc, returns html string
# driver function to process html file and run NLP
def parse(html, file_name, make_toc, ftp, run_nlp, css_type):

    ######################
    # Make Doc Look Good #
    # CSS, header/footer #
    ######################

    if css_type == 'podaac':
        # add podaac specific css, styling, header and footer

        #####################
        #    ** TO DO **    #
        # add podaac header and footer php hooks or otherwise
        # don't add anything that will mess up the soup obj creation
        # then later in the program can remove the head stuff and add php web hooks or however we want to add PODAAC stuff
        #####################
        
        # this needs to be set so that when it creates a new table of contents it has something to look for 
        # if no table of contents exists in the original DOCX document
        # the new table of contents function looks for the id='top' tag and creates it after that
        html = '<!DOCTYPE html><html><head><title>PODAAC HTML</title> \
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> \
            </head><body><div class="container" id="container"><a id="top" name="top"></a>' + html + '<br><br><a href="#top">Back to Top</a></div></body></html>'
        # setup soup
        soup = BeautifulSoup(html, 'html.parser') 
        add_podaac(soup)
    else:
        # add head, meta data, and container
        html = '<!DOCTYPE html><html><head><title>Converted HTML</title> \
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> \
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" \
            integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"> \
            </head><body><div class="container" id="container"><a id="top" name="top"></a>' + html + '<br><br><a href="#top">Back to Top</a></div></body></html>'
        # setup soup
        soup = BeautifulSoup(html, 'html.parser') 
        add_bootstrap(soup)

    # add title using file_name without file type extension
    t = os.path.splitext(file_name)[0]
    if soup.title:
        soup.title.string = t

    # convert all non-browser supported images to pngs
    soup = image_converter.parse(soup)

    ################################################
    # Natual Language Processing & Content Changes #
    ################################################

    # figures out which type of <h> tag is used for header sections
    header_type = get_type_of_header_tags_used(soup)
    
    # add id tags to each header 
    if header_type == 'both':
        if run_nlp:
            process_header(soup, 'h1')
            process_header(soup, 'h2')

        add_id_to_tags(soup, 'h1')
        add_id_to_tags(soup, 'h2')
    else:
        if run_nlp:
            process_header(soup, header_type)

        add_id_to_tags(soup, header_type)
    
    # make a new table of contents
    if make_toc:
        # removes any existing table of contents
        remove_table_of_contents(soup) 

        # makes a new table of contents out of the correct section headers
        if header_type == 'both':
            make_new_table_of_contents(soup, 'h1')
            make_new_table_of_contents(soup, 'h2')
        # if there are no section headers then dont make a new toc
        elif header_type == 'none':
            pass
        else:
            make_new_table_of_contents(soup, header_type)

    # parses ftp links and converts to corresponding drive links
    if ftp:
        convert_ftp_to_drive(soup)


    # ########################################################### #      
    # here is where we would add podaac specific stuff again      
    # for example, convert the soup obj to a string               
    # then add a php web hook to the front and back of the string 
    # then just return that string
    # ########################################################### #
    if css_type == 'podaac':
        html = str(soup)
        html = "<?php include('header.php');?><body>" + html + "</body><?php include('footer.php');?>"
        return html

    # return html as a string
    return str(soup)



################################
### not using this right now ###
################################


# only adds bootstrap to the html doc - used for save after making custom wysiwyg edits
def only_bootstrap(html):
    # adds header and footer
    html = '<!DOCTYPE html><html><head><title>Converted HTML</title><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"></head><body><div class="container" id="container"><a name="top"></a>' + html + '<br><br><a href="#top">Back to Top</a></div></body></html>'
    soup = BeautifulSoup(html, 'html.parser')  # setup soup object

    # add fluid container class to all images
    for img in soup.find_all('img'):
        img['class'] = 'img-fluid'

    # need to fix tables... not working!
    # add table class to all tables, make tables responsive
    for tbl in soup.find_all('table'):
        tbl.wrap(soup.new_tag('div', **{'class': 'table-responsive'}))
        tbl['class'] = 'table table-bordered'

    # return html as a string
    return str(soup)