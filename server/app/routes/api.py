from app.db import insert_exploit
from flask import Blueprint, request, jsonify
import os
import threading
import sqlite3

api = Blueprint("api", __name__)


@api.route('/exploits/add', methods=['POST'])
def add_exploit():
    # Check if the request contains a file
    if 'exploitFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['exploitFile']

    # Check if the file is allowed (e.g., only .py files)
    if file and file.filename.endswith('.py'):
        filename = os.path.basename(file.filename)

        # Define the upload path
        upload_path = os.path.join('./exploits', filename)

        # Save the file to the defined path
        file.save(upload_path)

        local = threading.local()

        if not hasattr(local, "conn"):
            local.conn = sqlite3.connect('database.db')

        insert_exploit(filename, True)

        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format. Only .py files are allowed'}), 400