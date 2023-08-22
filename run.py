import json
import os
import uuid

from flask import Flask, Response, request, send_file
from flask_cors import CORS
from waitress import serve

from utils import process_txt, process_png, process_pdf, get_rows, get_modal_markers_count, \
    get_haplotypes_count, get_prepared_rows, is_same_size

app = Flask(__name__)
cors = CORS(app)


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
                process_txt(request_id, prepared_rows)
                file_path = f'{os.getcwd()}/murka/nw/viz/{request_id}/result.zip'
                if not os.path.exists(file_path):
                    error = "File not ready!"
                    print(error)
                    return Response(json.dumps(dict(error=error)), mimetype='application/json')
                return send_file(file_path, mimetype='application/zip')
            else:
                error = "All haplotypes must be the same length as the modal haplotype!"
                print(error)
                return Response(json.dumps(dict(error=error)), mimetype='application/json')
        else:
            error = "In the set, in addition to the modal, there must be more than 1 haplotype!"
            print(error)
            return Response(json.dumps(dict(error=error)), mimetype='application/json')
    else:
        error = "A modal haplotype cannot have more than 111 markers!"
        print(error)
        return Response(json.dumps(dict(error=error)), mimetype='application/json')


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
                process_png(request_id, prepared_rows, request.headers, modal_markers_count, haplotypes_count)
                file_path = f'{os.getcwd()}/murka/nw/viz/{request_id}/result.zip'
                if not os.path.exists(file_path):
                    error = "File not ready!"
                    print(error)
                    return Response(json.dumps(dict(error=error)), mimetype='application/json')
                return send_file(file_path, mimetype='application/zip')
            else:
                error = "All haplotypes must be the same length as the modal haplotype!"
                print(error)
                return Response(json.dumps(dict(error=error)), mimetype='application/json')
        else:
            error = "In the set, in addition to the modal, there must be more than 1 haplotype!"
            print(error)
            return Response(json.dumps(dict(error=error)), mimetype='application/json')
    else:
        error = "A modal haplotype cannot have more than 111 markers!"
        print(error)
        return Response(json.dumps(dict(error=error)), mimetype='application/json')


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
                process_pdf(request_id, prepared_rows, request.headers, modal_markers_count, haplotypes_count)
                file_path = f'{os.getcwd()}/murka/nw/viz/{request_id}/result.zip'
                if not os.path.exists(file_path):
                    error = "File not ready!"
                    print(error)
                    return Response(json.dumps(dict(error=error)), mimetype='application/json')
                return send_file(file_path, mimetype='application/zip')
            else:
                error = "All haplotypes must be the same length as the modal haplotype!"
                print(error)
                return Response(json.dumps(dict(error=error)), mimetype='application/json')
        else:
            error = "In the set, in addition to the modal, there must be more than 1 haplotype!"
            print(error)
            return Response(json.dumps(dict(error=error)), mimetype='application/json')
    else:
        error = "A modal haplotype cannot have more than 111 markers!"
        print(error)
        return Response(json.dumps(dict(error=error)), mimetype='application/json')


if __name__ == '__main__':
    print('yMurMur!')
    serve(app,
          host="0.0.0.0",
          port=os.environ['PORT'])
