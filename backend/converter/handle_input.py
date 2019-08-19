from converter import convertDOCX2HTML
from converter import parse_html


# checks file type to send to the correct converter and parser
def check_file_type_and_process(file_name, make_toc, ftp, do_nlp, css_type):
    if file_name.endswith('.pdf'):
        print("file is pdf - throw error ")
    # currently the only part doing anything
    elif file_name.endswith('.docx'):
        # converts docx to html string
        html = convertDOCX2HTML.convert_to_html(file_name)

        # parses html to add styling, toc, edit content, etc
        # returns string html
        return parse_html.parse(html, file_name, make_toc, ftp, do_nlp, css_type)
    elif file_name.endswith('.doc'):
        print("filetype not supported, please convert to a docx")
    else:
        print("not a pdf or docx, throw an error")
