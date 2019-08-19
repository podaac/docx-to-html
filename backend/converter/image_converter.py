from PIL import Image
import os
import base64
import time


# search for all emfs and convert to png
def convert_emfs_to_pngs(soup):
    # set a counter to name the emf and increment counter to create new
    # file names so it doesn't mess up any async calls from frontend
    tmp = 'tmp'
    while os.path.exists(tmp+'.emf'):
        tmp += '1'

    tmp_emf = tmp+'.emf'
    tmp_png = tmp+'.png'

    for img in soup.find_all('img'):
        prefix = 'data:image/x-emf;base64,'
        if img['src'].startswith(prefix):
            s = img['src']
            s = s[len(prefix):]

            try:
                # decode string to binary and save it as an emf file
                img_data = base64.b64decode(str(s))
                with open(tmp_emf, 'wb') as f:
                    f.write(img_data)

                # use inkscape to convert emf to png    
                try:
                    cmd = 'inkscape -e ' + tmp_png + ' ' + tmp_emf
                    os.system(cmd)
                except:
                    print('inkscape conversion error')

                # encode binary png as a string
                with open(tmp_png, 'rb') as png:
                    png_string = base64.b64encode(png.read())

                # decode to utf-8 and write replacement png string to img src
                png_string = png_string.decode('utf-8')
                img['src'] = 'data:image/png;base64,' + png_string
            except:
                print('emf to png conversion failed')
            
            # delete tmp files
            if os.path.exists(tmp_emf):
                os.remove(tmp_emf)
            if os.path.exists(tmp_png):
                os.remove(tmp_png)  


# search for all wmf's and convert to png
def convert_wmfs_to_pngs(soup):
    # set a counter to name the wmf and increment counter to create new
    # file names so it doesn't mess up any async calls from frontend
    tmp = 'tmp'
    while os.path.exists(tmp+'.wmf'):
        tmp = tmp+'1'

    tmp_wmf = tmp+'.wmf'
    tmp_png = tmp+'.png'

    for img in soup.find_all('img'):
        prefix = 'data:image/x-wmf;base64,'
        if img['src'].startswith(prefix):
            s = img['src']
            s = s[len(prefix):] # gets string without prefix

            try:
                # decode string to binary and save it as a wmf file
                img_data = base64.b64decode(str(s))
                with open(tmp_wmf, 'wb') as f:
                    f.write(img_data)

                # use inkscape to convert wmf to png 
                try:
                    cmd = 'inkscape -e ' + tmp_png + ' ' + tmp_wmf
                    os.system(cmd)
                except:
                    print('inkscape conversion error')

                # encode binary png as a string
                with open(tmp_png, 'rb') as png:
                    png_string = base64.b64encode(png.read())

                # decode to utf-8 and write replacement png string to img src
                png_string = png_string.decode('utf-8')
                img['src'] = 'data:image/png;base64,' + png_string
            except:
                print('wmf to png image conversion failed')

            # delete tmp files
            if os.path.exists(tmp_wmf):
                os.remove(tmp_wmf)
            if os.path.exists(tmp_png):
                os.remove(tmp_png) 


# search for all tiffs and convert to jpgs
def convert_tiffs_to_pngs(soup):
    # set a counter to name the tiff and increment counter to create new
    # file names so it doesn't mess up any async calls from frontend
    tmp = 'tmp'
    while os.path.exists(tmp+'.tiff'):
        tmp = tmp+'1'

    for img in soup.find_all('img'):
        prefix = 'data:image/tiff;base64,'
        if img['src'].startswith(prefix):
            s = img['src']
            s = s[len(prefix):] # gets string without prefix

            try:
                # decode string to binary and save it as a tiff file
                img_data = base64.b64decode(str(s))
                with open(tmp+'.tiff', 'wb') as f:
                    f.write(img_data)

                # convert tiff to png using Pillow
                image = Image.open(tmp+'.tiff')
                image.save(tmp+'.png')

                # # encode binary png as a string
                with open(tmp+'.png', 'rb') as png:
                    png_string = base64.b64encode(png.read())

                # decode to utf-8 and write replacement png string to img src
                png_string = png_string.decode('utf-8')
                img['src'] = 'data:image/png;base64,' + png_string
            except:
                print('tiff to png image conversion failed')

            # delete tmp files
            if os.path.exists(tmp+'.tiff'):
                os.remove(tmp+'.tiff')
            if os.path.exists(tmp+'.png'):
                os.remove(tmp+'.png')            


# driver function to run the converters and return the soup object
def parse(soup):
    convert_tiffs_to_pngs(soup)
    convert_emfs_to_pngs(soup)
    convert_wmfs_to_pngs(soup)
    
    return soup
