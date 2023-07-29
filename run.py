import json
import os
import uuid
from threading import Thread

from flask import Flask, Response, request, send_file
from waitress import serve

from utils import is_valid_uuid, process_txt, process_png, process_pdf, split_rows, get_modal_markers_count, \
    get_haplotypes_count, replace_rows

app = Flask(__name__)


@app.route('/request_txt', methods=['POST'])
def request_txt():
    request_id = str(uuid.uuid4())
    print(f'Received RQ request_txt: {request_id}')
    splitted_rows = split_rows(request.data)
    modal_markers_count = get_modal_markers_count(splitted_rows)
    replaced_rows = replace_rows(splitted_rows, modal_markers_count)
    Thread(target=process_txt,
           args=(request_id, replaced_rows)).start()
    return Response(json.dumps(dict(requestId=request_id)),
                    mimetype='application/json')


@app.route('/request_png', methods=['POST'])
def request_png():
    request_id = str(uuid.uuid4())
    print(f'Received RQ request_png: {request_id}')
    splitted_rows = split_rows(request.data)
    modal_markers_count = get_modal_markers_count(splitted_rows)
    haplotypes_count = get_haplotypes_count(splitted_rows)
    replaced_rows = replace_rows(splitted_rows, modal_markers_count)
    Thread(target=process_png,
           args=(request_id, replaced_rows, request.headers, modal_markers_count, haplotypes_count)).start()
    return Response(json.dumps(dict(requestId=request_id)),
                    mimetype='application/json')


@app.route('/request_pdf', methods=['POST'])
def request_pdf():
    request_id = str(uuid.uuid4())
    print(f'Received RQ request_pdf: {request_id}')
    splitted_rows = split_rows(request.data)
    modal_markers_count = get_modal_markers_count(splitted_rows)
    haplotypes_count = get_haplotypes_count(splitted_rows)
    replaced_rows = replace_rows(splitted_rows, modal_markers_count)
    Thread(target=process_pdf,
           args=(request_id, replaced_rows, request.headers, modal_markers_count, haplotypes_count)).start()
    return Response(json.dumps(dict(requestId=request_id)),
                    mimetype='application/json')


@app.route('/response', methods=['GET'])
def response():
    args = request.args.to_dict()
    request_id = args.get("requestId")
    print(f'Received RQ response: {request_id}')
    if not is_valid_uuid(request_id):
        return Response(json.dumps(dict(status="Wrong requestId!")),
                        mimetype='application/json')
    file_path = f'{os.getcwd()}\\murka\\nw\\viz\\{request_id}\\result.zip'
    if not os.path.exists(file_path):
        return Response(json.dumps(dict(status="File not ready!")),
                        mimetype='application/json')
    return send_file(file_path, mimetype='application/zip')


if __name__ == '__main__':
    serve(app,
          host="0.0.0.0",
          port=8080)
