from app.db import insert_exploit, insert_service, remove_service, disable_exploit, remove_exploit, fetch_exploits_by_service, fetch_exploit_by_id
from flask import Blueprint, request, jsonify
import os
import sqlite3
import threading

api = Blueprint("api", __name__)


@api.route('/exploits/add', methods=['POST'])
def add_exploit():
    if 'exploitFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    if 'service' not in request.form:
        return jsonify({'error': 'No service selected'}), 400

    file = request.files['exploitFile']
    service = request.form.get('service')

    if file and file.filename.endswith('.py'):
        filename = os.path.basename(file.filename)

        upload_path = os.path.join('/exploits', filename)
        file.save(upload_path)

        local = threading.local()

        if not hasattr(local, "conn"):
            local.conn = sqlite3.connect('/database/database.db')

        insert_exploit(filename, service, True)

        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format. Only .py files are allowed'}), 400


@api.route('/services/add', methods=['POST'])
def add_service():
    service_name = request.json.get('serviceName')
    port = int(request.json.get('portNumber'))

    if port < 0 or port > 65535:
        return jsonify({'message': 'Port is outside of allowed range'}), 400

    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect('/database/database.db')

    insert_service(service_name, port)
    return jsonify({'message': 'Service successfully added'}), 200


@api.route('/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect('/database/database.db')

    exploits = fetch_exploits_by_service(service_id)
    if len(exploits) > 0:
        return jsonify({'message': 'Service cannot be deleted as exploits are currently linked to it'}), 400

    remove_service(service_id)
    return jsonify({'message': 'Service successfully deleted'}), 200


@api.route('/exploits/<exploit_id>', methods=['DELETE'])
def delete_exploit(exploit_id):
    disable = request.args.get('disable')
    if not disable:
        return jsonify({'message': 'Disable parameter not defined'}), 400

    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect('/database/database.db')

    if disable == 'true':
        disable_exploit(exploit_id)
        return jsonify({'message': 'Exploit successfully disabled'}), 200
    elif disable == 'false':
        name = fetch_exploit_by_id(exploit_id)[0][1]
        print(f"Deleting: {name}")
        remove_exploit(exploit_id)
        filepath = f"/exploits/{name}"
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'message': 'Exploit successfully deleted'}), 200

    return jsonify({'message': 'Disable parameter not set to allowed value'}), 400
