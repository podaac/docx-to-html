import os
import mammoth


# converts docx to html and returns html
# uses mammoth pip library for the conversion
def convert_to_html(file_name):
    with open('converter/' + file_name, 'rb') as f:
        document = mammoth.convert_to_html(f)
        html = document.value

    # delete docx file
    if os.path.exists('converter/' + file_name):
        os.remove('converter/' + file_name)
    else:
        print('err deleting docx')

    return html
