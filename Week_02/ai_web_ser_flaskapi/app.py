from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_restful import Api, Resource
import os

app = Flask(__name__)
api = Api(app)

class AnimalImage(Resource):
    def get(self, animal):
        valid_animals = ['cat', 'dog', 'elephant']
        if animal in valid_animals:
            return {'image_url': f'/static/images/{animal}.jpg'}
        return {'error': 'Invalid animal'}, 400

class FileInfo(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'error': 'No selected file'}, 400
        
        file_info = {
            'name': file.filename,
            'size': len(file.read()),
            'type': file.content_type
        }

        return file_info

api.add_resource(AnimalImage, '/api/animal/<string:animal>')
api.add_resource(FileInfo, '/api/file-info')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
