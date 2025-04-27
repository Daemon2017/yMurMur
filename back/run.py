import json
import os
import uuid

from flask import Flask, Response, request, send_file
from flask_cors import CORS
from waitress import serve

from processors import process_txt, process_png, process_pdf, process_dot
from utils import get_from_ych, get_markers_count, get_haplotype_names, is_same_size, get_from_raw

INPUT_FORMAT = 'InputFormat'

APPLICATION_ZIP_MIMETYPE = 'application/zip'
APPLICATION_JSON_MIMETYPE = 'application/json'

HAPLOTYPES_COUNT_ERROR = 'In the set, in addition to the modal, there must be more than 1 haplotype!'
HAPLOTYPES_SIZE_ERROR = 'All haplotypes must be the same length as the modal haplotype!'
FILE_NOT_READY_ERROR = 'File not ready!'

app = Flask(__name__)
cors = CORS(app)


@app.route('/request_txt', methods=['POST'])
def request_txt():
    request_id = str(uuid.uuid4())
    print(f'Received RQ request_txt: {request_id}')
    rows = []
    if request.headers[INPUT_FORMAT] == "raw":
        rows = get_from_raw(request.data)
    else:
        rows = get_from_ych(request.data)
    markers_count = get_markers_count(rows)
    if not is_same_size(rows, markers_count):
        return haplotypes_size_error()
    haplotype_names = get_haplotype_names(rows)
    if len(haplotype_names) <= 1:
        return haplotypes_count_error()
    process_txt(request_id, rows, request.headers, markers_count)
    file_path = f'{os.getcwd()}/murka/nw/viz/{request_id}/result.zip'
    if not os.path.exists(file_path):
        return file_not_ready_error()
    return send_file(file_path, mimetype=APPLICATION_ZIP_MIMETYPE)


@app.route('/request_dot', methods=['POST'])
def request_dot():
    request_id = str(uuid.uuid4())
    print(f'Received RQ request_dot: {request_id}')
    rows = []
    if request.headers[INPUT_FORMAT] == "raw":
        rows = get_from_raw(request.data)
    else:
        rows = get_from_ych(request.data)
    markers_count = get_markers_count(rows)
    if not is_same_size(rows, markers_count):
        return haplotypes_size_error()
    haplotype_names = get_haplotype_names(rows)
    if len(haplotype_names) <= 1:
        return haplotypes_count_error()
    process_dot(request_id, rows, request.headers, markers_count, haplotype_names)
    file_path = f'{os.getcwd()}/murka/nw/viz/{request_id}/result.zip'
    if not os.path.exists(file_path):
        return file_not_ready_error()
    return send_file(file_path, mimetype=APPLICATION_ZIP_MIMETYPE)


@app.route('/request_png', methods=['POST'])
def request_png():
    request_id = str(uuid.uuid4())
    print(f'Received RQ request_png: {request_id}')
    rows = []
    if request.headers[INPUT_FORMAT] == "raw":
        rows = get_from_raw(request.data)
    else:
        rows = get_from_ych(request.data)
    markers_count = get_markers_count(rows)
    if not is_same_size(rows, markers_count):
        return haplotypes_size_error()
    haplotype_names = get_haplotype_names(rows)
    if len(haplotype_names) <= 1:
        return haplotypes_count_error()
    process_png(request_id, rows, request.headers, markers_count, haplotype_names)
    file_path = f'{os.getcwd()}/murka/nw/viz/{request_id}/result.zip'
    if not os.path.exists(file_path):
        return file_not_ready_error()
    return send_file(file_path, mimetype=APPLICATION_ZIP_MIMETYPE)


@app.route('/request_pdf', methods=['POST'])
def request_pdf():
    request_id = str(uuid.uuid4())
    print(f'Received RQ request_pdf: {request_id}')
    rows = []
    if request.headers[INPUT_FORMAT] == "raw":
        rows = get_from_raw(request.data)
    else:
        rows = get_from_ych(request.data)
    markers_count = get_markers_count(rows)
    if not is_same_size(rows, markers_count):
        return haplotypes_size_error()
    haplotype_names = get_haplotype_names(rows)
    if len(haplotype_names) <= 1:
        return haplotypes_count_error()
    process_pdf(request_id, rows, request.headers, markers_count, haplotype_names)
    file_path = f'{os.getcwd()}/murka/nw/viz/{request_id}/result.zip'
    if not os.path.exists(file_path):
        return file_not_ready_error()
    return send_file(file_path, mimetype=APPLICATION_ZIP_MIMETYPE)


def haplotypes_size_error():
    error = HAPLOTYPES_SIZE_ERROR
    print(error)
    return Response(json.dumps(dict(error=error)), mimetype=APPLICATION_JSON_MIMETYPE)


def haplotypes_count_error():
    error = HAPLOTYPES_COUNT_ERROR
    print(error)
    return Response(json.dumps(dict(error=error)), mimetype=APPLICATION_JSON_MIMETYPE)


def file_not_ready_error():
    error = FILE_NOT_READY_ERROR
    print(error)
    return Response(json.dumps(dict(error=error)), mimetype=APPLICATION_JSON_MIMETYPE)


if __name__ == '__main__':
    print('yMurMur ready!')
    serve(app,
          host='0.0.0.0',
          port=8080)
