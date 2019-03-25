from flask import Flask, request, send_file
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/",methods=['GET', 'POST'])
def send_files():
    if request.method == 'POST':
        file = request.files['file']
        return send_file(BytesIO(file.stream.read()),attachment_filename='data.qif',as_attachment=True)
    return '''
    <!doctype html>
    <title>Upload file</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=False)
