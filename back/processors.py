import os

from back.utils import create_folder, create_ych, create_rdf, create_txt, create_dot, create_png, create_pdf, create_zip


def process_txt(request_id, prepared_rows, headers, modal_markers_count):
    seq_path = f'{os.getcwd()}/murka/data/seq/{request_id}'
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folder(request_id, seq_path)
    create_folder(request_id, f'{viz_path}/output')
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_txt(request_id, seq_path, modal_markers_count, headers['ypg'], headers['amr'])
    create_zip(request_id, viz_path)


def process_dot(request_id, prepared_rows, headers, modal_markers_count):
    seq_path = f'{os.getcwd()}/murka/data/seq/{request_id}'
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folder(request_id, seq_path)
    create_folder(request_id, f'{viz_path}/output')
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_dot(request_id, seq_path, modal_markers_count, headers['ypg'], headers['amr'])
    create_zip(request_id, viz_path)


def process_png(request_id, prepared_rows, headers, modal_markers_count, haplotypes_count):
    seq_path = f'{os.getcwd()}/murka/data/seq/{request_id}'
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folder(request_id, seq_path)
    create_folder(request_id, f'{viz_path}/output')
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_dot(request_id, seq_path, modal_markers_count, headers['ypg'], headers['amr'])
    create_png(request_id, viz_path, headers['rankdir'], modal_markers_count, haplotypes_count)
    create_zip(request_id, viz_path)


def process_pdf(request_id, prepared_rows, headers, modal_markers_count, haplotypes_count):
    seq_path = f'{os.getcwd()}/murka/data/seq/{request_id}'
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folder(request_id, seq_path)
    create_folder(request_id, f'{viz_path}/output')
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_dot(request_id, seq_path, modal_markers_count, headers['ypg'], headers['amr'])
    create_pdf(request_id, viz_path, headers['rankdir'], modal_markers_count, haplotypes_count)
    create_zip(request_id, viz_path)
