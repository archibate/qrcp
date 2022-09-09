from flask import Flask, request, redirect
import os

app = Flask('qrcp')

@app.route('/')
def index():
    return '''<html>
    <head>
        <title>QRCP</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
    </head>
    <body>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" multiple="multiple"/>
            <input type="submit" name="Submit"/>
        </form>
    </body>
</html>
'''

@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.isdir('files'):
        os.mkdir('files')
    files = request.files.getlist('file')
    for f in files:
        if f.filename:
            path = os.path.join('files', f.filename)
            f.save(path)
    return redirect('/')

if __name__ == '__main__':
    import socket
    import pyqrcode
    from PIL import Image
    from io import BytesIO

    ip = socket.gethostbyname(socket.gethostname())
    port = 7684
    url = f'http://{ip}:{port}/'
    print(url)

    qrc = pyqrcode.create(url)
    png = BytesIO()
    with png as f1:
        qrc.png(f1, 20)
        with Image.open(f1) as im:
            im.show()

    app.run('0.0.0.0', port)
