from app import app

# dependencies
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

# converter files
from converter import handle_input, parse_html

app.secret_key = os.urandom(24)  # for cors to work

UPLOAD_FOLDER = './converter'
ALLOWED_EXTENSIONS = set(['docx'])

app.config['MAX_CONTENT_LENGTH'] = 32 * \
    1024 * 1024  # limit file uploads to 32 mb
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# checks file type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# handles main post request from react frontend
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        # handles doing only bootstrap
        only_bootstrap = request.values['onlybootstrap']
        if only_bootstrap == 'true':
            only_bootstrap_html_output = request.values['htmloutput']
            file = False
        else:
            file = request.files['file']
            only_bootstrap_html_output = False

        # handles whether to make new table of contents
        make_toc = request.values['toc']
        make_toc = True if make_toc == 'true' else False

        # convert ftp links to drive links
        ftp = request.values['ftp']
        ftp = True if ftp == 'true' else False

        # handles whether or not to do NLP
        do_nlp = request.values['donlp']
        do_nlp = True if do_nlp == 'true' else False

        css_type = request.values['csstype']

        # send file to be converted
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except OSError as err:
                print(err)

            # convert file and run all parsing operations
            # gets back and string of html
            html = handle_input.check_file_type_and_process(
                filename, make_toc, ftp, do_nlp, css_type)
            return jsonify(html)
        # sends html back through to add bootstrap after its been in the frontend WYSIWYG editor
        elif only_bootstrap_html_output:
            only_bootstrap_html_output = parse_html.only_bootstrap(
            only_bootstrap_html_output)
            return jsonify(only_bootstrap_html_output)
        # just in case a file gets through the frontend file type checks
        else:
            print('wrong file type')
            return jsonify('error')
    except:
        return jsonify('error')


if __name__ == '__main__':
    app.run()

CORS(app, expose_headers='Authorization')
