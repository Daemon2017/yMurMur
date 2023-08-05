import json
import os
import uuid
from threading import Thread

from flask import Flask, Response, request, send_file
from waitress import serve

from utils import is_valid_uuid, process_txt, process_png, process_pdf, get_rows, get_modal_markers_count, \
    get_haplotypes_count, get_prepared_rows, is_same_size

app = Flask(__name__)


@app.route('/request_txt', methods=['POST'])
def request_txt():
    request_id = str(uuid.uuid4())
    print(f'Received RQ request_txt: {request_id}')
    rows = get_rows(request.data)
    modal_markers_count = get_modal_markers_count(rows)
    if modal_markers_count <= 111:
        haplotypes_count = get_haplotypes_count(rows)
        if haplotypes_count > 1:
            if is_same_size(rows, modal_markers_count):
                prepared_rows = get_prepared_rows(rows, modal_markers_count)
                Thread(target=process_txt,
                       args=(request_id, prepared_rows)).start()
                return Response(json.dumps(dict(requestId=request_id)),
                                mimetype='application/json')
            else:
                return Response(json.dumps(dict(error="All haplotypes must be the same length "
                                                      "as the modal haplotype!")),
                                mimetype='application/json')
        else:
            return Response(json.dumps(dict(error="In the set, in addition to the modal, "
                                                  "there must be more than 1 haplotype!")),
                            mimetype='application/json')
    else:
        return Response(json.dumps(dict(error="A modal haplotype cannot have more than 111 markers!")),
                        mimetype='application/json')


@app.route('/request_png', methods=['POST'])
def request_png():
    request_id = str(uuid.uuid4())
    print(f'Received RQ request_png: {request_id}')
    rows = get_rows(request.data)
    modal_markers_count = get_modal_markers_count(rows)
    if modal_markers_count <= 111:
        haplotypes_count = get_haplotypes_count(rows)
        if haplotypes_count > 1:
            if is_same_size(rows, modal_markers_count):
                prepared_rows = get_prepared_rows(rows, modal_markers_count)
                Thread(target=process_png,
                       args=(request_id, prepared_rows, request.headers, modal_markers_count, haplotypes_count)).start()
                return Response(json.dumps(dict(requestId=request_id)),
                                mimetype='application/json')
            else:
                return Response(json.dumps(dict(error="All haplotypes must be the same length "
                                                      "as the modal haplotype!")),
                                mimetype='application/json')
        else:
            return Response(json.dumps(dict(error="In the set, in addition to the modal, "
                                                  "there must be more than 1 haplotype!")),
                            mimetype='application/json')
    else:
        return Response(json.dumps(dict(error="A modal haplotype cannot have more than 111 markers!")),
                        mimetype='application/json')


@app.route('/request_pdf', methods=['POST'])
def request_pdf():
    request_id = str(uuid.uuid4())
    print(f'Received RQ request_pdf: {request_id}')
    rows = get_rows(request.data)
    modal_markers_count = get_modal_markers_count(rows)
    if modal_markers_count <= 111:
        haplotypes_count = get_haplotypes_count(rows)
        if haplotypes_count > 1:
            if is_same_size(rows, modal_markers_count):
                prepared_rows = get_prepared_rows(rows, modal_markers_count)
                Thread(target=process_pdf,
                       args=(request_id, prepared_rows, request.headers, modal_markers_count, haplotypes_count)).start()
                return Response(json.dumps(dict(requestId=request_id)),
                                mimetype='application/json')
            else:
                return Response(json.dumps(dict(error="All haplotypes must be the same length "
                                                      "as the modal haplotype!")),
                                mimetype='application/json')
        else:
            return Response(json.dumps(dict(error="In the set, in addition to the modal, "
                                                  "there must be more than 1 haplotype!")),
                            mimetype='application/json')
    else:
        return Response(json.dumps(dict(error="A modal haplotype cannot have more than 111 markers!")),
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
    print('yMurMur!')
    serve(app,
          host="0.0.0.0",
          port=8080)
