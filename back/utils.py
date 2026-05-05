import os
import random
import re
import shutil
import string
from datetime import datetime
from itertools import repeat
from multiprocessing import Process, Pool, cpu_count

import pydot


def get_from_raw(data):
    rows = data \
        .decode('utf-8') \
        .splitlines()
    rows = list(filter(None, rows))
    for i in range(len(rows)):
        rows[i] = rows[i] \
            .rstrip('\t -') \
            .replace('\t', ',') \
            .replace('    ', ',') \
            .replace('   ', ',') \
            .replace('  ', ',') \
            .replace(' ', ',') \
            .replace('-', ',')
    new_rows = [
        ','.join(['STR' + str(i) for i in range(len(rows[0].split(',')[1:]))]),
        '',
        ''
    ]
    haplotype_names = []
    for row in rows:
        splitted_row = row.split(',')
        haplotype_name = splitted_row[0]
        if haplotype_name not in haplotype_names:
            new_rows.append(haplotype_name)
            markers_row = []
            for marker in splitted_row[1:]:
                markers_row.append(str(round(float(marker))))
            new_rows.append(','.join(markers_row))
            new_rows.append(1)
            haplotype_names.append(haplotype_name)
    return new_rows


def get_from_ych(data):
    rows = data \
        .decode('utf-8') \
        .splitlines()
    for i in range(len(rows)):
        rows[i] = rows[i] \
            .replace(', ', ',')
    del rows[3:6]
    markers_columns = rows[0].split(',')
    for i, row in enumerate(rows):
        if i > 0:
            columns = row.split(',')
            if len(columns) > 1:
                values = []
                for j, column in enumerate(columns):
                    column_values = column.split('-')
                    if markers_columns[j] in ['D385', 'D459', 'YCAII', 'CDY', 'D395S', 'D413']:
                        values.extend([column_values[0], column_values[-1]])
                    elif markers_columns[j] in ['D464']:
                        values.extend([column_values[0], column_values[1], column_values[-2], column_values[-1]])
                    else:
                        values.extend([column_values[-1]])
                rows[i] = ','.join(values)
    rows[0] = ','.join(['STR' + str(i) for i in range(get_markers_count(rows))])
    return rows


def get_markers_count(rows):
    return len(rows[4].split(','))


def get_haplotype_names(rows):
    haplotype_names = []
    for i in range(3, len(rows), 3):
        haplotype_names.append(rows[i])
    return haplotype_names


def is_same_size(rows, markers_count):
    for i in range(4, len(rows), 3):
        splitted_row = rows[i].split(',')
        if len(splitted_row) != markers_count:
            return False
    return True


def get_rho(markers_count, years_per_generation, avg_mutation_rate):
    return float(years_per_generation) / float(avg_mutation_rate) / markers_count


def create_folder(request_id, path):
    print(f'Creating folder {path} for RQ {request_id}...')
    os.makedirs(path,
                exist_ok=True)
    print(f'Folder {path} for RQ {request_id} created.')


def remove_extra_dot(viz_path):
    output_path = f'{viz_path}/output'
    pattern = re.compile('nw_mp_\\d*.dot')
    for dot_filename in os.listdir(output_path):
        if not pattern.match(dot_filename):
            os.remove(f'{output_path}/{dot_filename}')


def modify_dot(request_id, viz_path, haplotype_names, average_age):
    print(f'Modifying DOT-file for RQ {request_id}...')
    output_path = f'{viz_path}/output'
    files_list = os.listdir(output_path)
    if os.name == 'nt':
        with Pool(processes=cpu_count()) as pool:
            pool.starmap(process_dot_modification,
                         zip(files_list, repeat(average_age), repeat(haplotype_names), repeat(output_path)))
    else:
        tasks = [Process(target=process_dot_modification,
                         args=(dot_filename, average_age, haplotype_names, output_path,))
                 for dot_filename in files_list]
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
    print(f'DOT-file for RQ {request_id} modified.')


def process_dot_modification(dot_filename, average_age, haplotype_names, output_path):
    dot_filename_path = f'{output_path}/{dot_filename}'
    graphs = pydot.graph_from_dot_file(dot_filename_path)
    graph = graphs[0]
    graph.del_node('"\\n"')
    for node in graph.get_nodes():
        attributes = node.get_attributes()
        if ('shape' in attributes) and (attributes['shape'] == 'plaintext'):
            label = attributes['label']
            regex = re.compile('\"(\d*.\d*)\\\\n\+-(\d*.\d*)y\"')
            result = regex.match(label)
            new_expectation = round(float(average_age)) + round(float(result.group(1)))
            new_dispersion = round(float(result.group(2)))
            new_label = regex.sub(f'"{str(new_expectation)}\\\\n+-{str(new_dispersion)}y"', label)
            node.set('label', new_label)
    for edge in graph.get_edges():
        source = edge.get_source().replace('"', '')
        if source in haplotype_names:
            new_node = ''.join(random.choices(string.ascii_letters, k=12))
            graph.add_node(pydot.Node(name=f'"{new_node}"', label='', style='bold'))
            replace_edge_source_and_destination(graph, source, new_node)
            graph.add_edge(pydot.Edge(src=f'"{new_node}"', dst=f'"{source}"', arrowhead='none'))
    subgraph = pydot.Subgraph(rank='same')
    for node in graph.get_nodes():
        if node.get_name().replace('"', '') in haplotype_names:
            subgraph.add_node(node)
    graph.add_subgraph(subgraph)
    graph.write(path=dot_filename_path, format='raw')


def replace_edge_source_and_destination(graph, old, new):
    for edge in graph.get_edges():
        attributes = edge.get_attributes()
        source = edge.get_source().replace('"', '')
        destination = edge.get_destination().replace('"', '')
        if source == old:
            graph.del_edge(src_or_list=f'"{old}"', dst=f'"{destination}"')
            graph.add_edge(pydot.Edge(src=f'"{new}"', dst=f'"{destination}"', **attributes))
        if destination == old:
            graph.del_edge(src_or_list=f'"{source}"', dst=f'"{old}"')
            graph.add_edge(pydot.Edge(src=f'"{source}"', dst=f'"{new}"', **attributes))


def create_graph(request_id, viz_path, tree_direction, markers_count, haplotypes_count, output_extension,
                 output_format, years_per_generation, avg_mutation_rate):
    print(f'Creating graph files for RQ {request_id}...')
    output_path = f'{viz_path}/output'
    files_list = os.listdir(output_path)
    if os.name == 'nt':
        with Pool(processes=cpu_count()) as pool:
            pool.starmap(process_graph_creation,
                         zip(files_list, repeat(haplotypes_count), repeat(markers_count), repeat(output_path),
                             repeat(tree_direction), repeat(output_extension), repeat(output_format),
                             repeat(years_per_generation), repeat(avg_mutation_rate)))
    else:
        tasks = [Process(target=process_graph_creation,
                         args=(dot_filename, haplotypes_count, markers_count, output_path,
                               tree_direction, output_extension, output_format,
                               years_per_generation, avg_mutation_rate))
                 for dot_filename in files_list]
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
    print(f'Graph files for RQ {request_id} created.')


def process_graph_creation(dot_filename, haplotypes_count, markers_count, output_path, tree_direction, output_extension,
                           output_format, years_per_generation, avg_mutation_rate):
    output_filename = dot_filename.replace('.dot', output_extension)
    dot_filename_path = f'{output_path}/{dot_filename}'
    graphs = pydot.graph_from_dot_file(dot_filename_path)
    graph = graphs[0]
    graph.del_node('"\\n"')
    graph.set_graph_defaults(rankdir=tree_direction,
                             label=f'{datetime.now().date()}: {markers_count} STRs, {haplotypes_count} haplotypes, {years_per_generation} yr/gen, {avg_mutation_rate} amr')
    filename_path = f'{output_path}/{output_filename}'
    graph.write(path=filename_path, format=output_format)
    os.remove(dot_filename_path)


def create_zip(request_id, viz_path):
    print(f'Creating ZIP-file for RQ {request_id}...')
    output_path = f'{viz_path}/output'
    shutil.make_archive(f'{viz_path}/result',
                        'zip',
                        output_path)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    print(f'ZIP-file for RQ {request_id} created.')
