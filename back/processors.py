import os

from utils import create_folder, create_ych, create_rdf, create_txt, create_dot, create_graph, create_zip, \
    modify_dot, remove_extra_dot

TREE_DIRECTION = 'TreeDirection'
AVERAGE_MUTATION_RATE = 'AverageMutationRate'
AVERAGE_AGE = 'AverageAge'
YEARS_PER_GENERATION = 'YearsPerGeneration'
IMPROVE_APPEARANCE = 'ImproveAppearance'


def process_txt(request_id, prepared_rows, headers, modal_markers_count):
    seq_path = f'{os.getcwd()}/murka/data/seq/{request_id}'
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folder(request_id, seq_path)
    create_folder(request_id, f'{viz_path}/output')
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_txt(request_id, seq_path, modal_markers_count, headers[YEARS_PER_GENERATION], headers[AVERAGE_MUTATION_RATE])
    create_zip(request_id, viz_path)


def process_dot(request_id, prepared_rows, headers, modal_markers_count, haplotype_names):
    seq_path = f'{os.getcwd()}/murka/data/seq/{request_id}'
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folder(request_id, seq_path)
    create_folder(request_id, f'{viz_path}/output')
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_dot(request_id, seq_path, modal_markers_count, headers[YEARS_PER_GENERATION], headers[AVERAGE_MUTATION_RATE])
    remove_extra_dot(viz_path)
    if headers[IMPROVE_APPEARANCE] == "True":
        modify_dot(request_id, viz_path, haplotype_names, headers[AVERAGE_AGE])
    create_zip(request_id, viz_path)


def process_jpg(request_id, prepared_rows, headers, modal_markers_count, haplotype_names):
    seq_path = f'{os.getcwd()}/murka/data/seq/{request_id}'
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folder(request_id, seq_path)
    create_folder(request_id, f'{viz_path}/output')
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_dot(request_id, seq_path, modal_markers_count, headers[YEARS_PER_GENERATION], headers[AVERAGE_MUTATION_RATE])
    remove_extra_dot(viz_path)
    if headers[IMPROVE_APPEARANCE] == "True":
        modify_dot(request_id, viz_path, haplotype_names, headers[AVERAGE_AGE])
    create_graph(request_id, viz_path, headers[TREE_DIRECTION], modal_markers_count, len(haplotype_names),
                 '.jpg', 'jpg', headers[YEARS_PER_GENERATION], headers[AVERAGE_MUTATION_RATE])
    create_zip(request_id, viz_path)


def process_png(request_id, prepared_rows, headers, modal_markers_count, haplotype_names):
    seq_path = f'{os.getcwd()}/murka/data/seq/{request_id}'
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folder(request_id, seq_path)
    create_folder(request_id, f'{viz_path}/output')
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_dot(request_id, seq_path, modal_markers_count, headers[YEARS_PER_GENERATION], headers[AVERAGE_MUTATION_RATE])
    remove_extra_dot(viz_path)
    if headers[IMPROVE_APPEARANCE] == "True":
        modify_dot(request_id, viz_path, haplotype_names, headers[AVERAGE_AGE])
    create_graph(request_id, viz_path, headers[TREE_DIRECTION], modal_markers_count, len(haplotype_names),
                 '.png', 'png', headers[YEARS_PER_GENERATION], headers[AVERAGE_MUTATION_RATE])
    create_zip(request_id, viz_path)


def process_pdf(request_id, prepared_rows, headers, modal_markers_count, haplotype_names):
    seq_path = f'{os.getcwd()}/murka/data/seq/{request_id}'
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folder(request_id, seq_path)
    create_folder(request_id, f'{viz_path}/output')
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_dot(request_id, seq_path, modal_markers_count, headers[YEARS_PER_GENERATION], headers[AVERAGE_MUTATION_RATE])
    remove_extra_dot(viz_path)
    if headers[IMPROVE_APPEARANCE] == "True":
        modify_dot(request_id, viz_path, haplotype_names, headers[AVERAGE_AGE])
    create_graph(request_id, viz_path, headers[TREE_DIRECTION], modal_markers_count, len(haplotype_names),
                 '.pdf', 'pdf', headers[YEARS_PER_GENERATION], headers[AVERAGE_MUTATION_RATE])
    create_zip(request_id, viz_path)
