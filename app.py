from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

IMAGE_FOLDER = os.path.join('static', 'images')

@app.route('/')
def index():
    images = os.listdir(IMAGE_FOLDER)
    return render_template('index.html', images=images)

@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
