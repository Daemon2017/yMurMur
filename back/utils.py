import os
import random
import re
import shutil
import string
import subprocess
from itertools import repeat
from multiprocessing import Process, Pool, cpu_count

import pydot

murka_additional_args = '-T "MJ" ' \
                        '-S "VB|RSW|RSR|EM|THR2" ' \
                        '-V "VP|VL|VR" ' \
                        '-I 1 ' \
                        '-F 20.0 ' \
                        '-H "N" ' \
                        '-P "1;1.4;2.25;5000;1;1.4;2.25;5000;0;0.75;500;50;33;" ' \
                        '-C "0;50;0;" ' \
                        '-M "0; 0; 0; 0; RESCHECK|FASTUNION|MORETREES; 1; 0; 0; SEP1|NTT|NT1|NT2|NTD|LEUC|PS|SL|NV|LE|PT|PTE|DA|NTDX|EXTV|EXTVDA|EXTVDAP|ASCPRN|EXPV|EXTEEDA; 0; LBDA|UBRSPH|KEEPBND|BNDREPEATS3|BNDPERC2|EXTTEST2|EXTTESTP2|PRUNE3|REDREP3|PROCMSG1|NWPERFMON|REDPMLEV2|COMPLTRAVERSAL|KEEPTREE|OOO1|DEFERPW3; " ' \
                        '-J 0 ' \
                        '-X 0 ' \
                        '-Y 0 ' \
                        '-U 0 ' \
                        '-W 0 ' \
                        '-Z 0 ' \
                        '-s "BCACHE|DCACHE|THASH" ' \
                        '-j "CONSTSPLITS|EQSPLITS|PSHELLING|POSTPROC|CONTRACTNT2|ROOTING|ALLOWTERMROOT|MIDPOINTROOT|MSNCACHE|NWGRCACHE|FASTMJ|WPHEUR|MPSTAT|NWAGE" ' \
                        '-e 0 ' \
                        '-x 0 ' \
                        '-b 100 ' \
                        '-f "NOFU|NS3|STAPPR|FH" ' \
                        '-m 0.6 ' \
                        '-n 100 ' \
                        '-l 10 ' \
                        '-t "RDF" ' \
                        '-d 0.8 ' \
                        '-o "SEQTABLE|TAXATABLE|CHARTABLE|CHARCHNGTABLE|NW|NWEXT|STAT|STP|MPCOMPTABLE|MPRFTDMATRIX|MPPARTTABLE|MPTOPOTABLE|CHARSTTABLE|DMATRIX" ' \
                        '-c "inn_" ' \
                        '-p "nw" ' \
                        '-q "stat" ' \
                        '-u "nwlinktbl#" ' \
                        '-O "seq.rdf" ' \
                        '-w "distmx" ' \
                        '-D "charsttbl" ' \
                        '-z "taxatbl#" ' \
                        '-a "chartbl#" ' \
                        '-k "charchngtbl#" ' \
                        '-A "CONVERT" ' \
                        '-Q "wtdistmx" ' \
                        '-K "rftdistmx" ' \
                        '-R "tcmptbl" ' \
                        '-B "parttbl" ' \
                        '-L "topotbl" '


def get_from_raw(data):
    rows = data \
        .decode('utf-8') \
        .replace('-', ',') \
        .replace('\t,', ',') \
        .replace('\t', ',') \
        .replace(', ', ',') \
        .replace(' ', ',') \
        .splitlines()
    new_rows = [
        ','.join(['STR' + str(i) for i in range(len(rows[0].split(',')[1:]))]),
        '',
        ''
    ]
    for row in rows:
        splitted_row = row.split(',')
        new_rows.append(splitted_row[0])
        new_rows.append(','.join(splitted_row[1:]))
        new_rows.append(1)
    return new_rows


def get_from_ych(data):
    rows = data \
        .decode('utf-8') \
        .replace(', ', ',') \
        .splitlines()
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


def create_ych(body_rows, request_id, seq_path):
    print(f'Creating YCH-file for RQ {request_id}...')
    with open(f'{seq_path}/request.ych',
              'w',
              encoding='utf-8') as text_file:
        for row in body_rows:
            text_file.write(f'{row}\n')
    print(f'YCH-file for RQ {request_id} created.')


def create_rdf(request_id, seq_path):
    print(f'Creating RDF-file for RQ {request_id}...')
    prepare_args = ''
    if os.name == 'nt':
        prepare_args = '{0}/murka/prepare.exe '.format(os.getcwd())
    else:
        prepare_args = '{0}/murka/prepare/prepare '.format(os.getcwd())
    prepare_args += '-T "YCH2RDF" ' \
                    '-S "VB" ' \
                    '-V "VP" ' \
                    '-I "1" ' \
                    '-F "20.0" ' \
                    '-i "{1}/request.ych" ' \
                    '-o "{1}/request.rdf" ' \
                    '-s "{0}/murka/data/metric/ymx" ' \
                    '-p "INEQ|MX" ' \
                    '-d 2 ' \
                    '-n 2'.format(os.getcwd(), seq_path)
    subprocess.run(prepare_args,
                   shell=True,
                   check=False,
                   cwd=f'{os.getcwd()}/murka')
    ych_path = f'{seq_path}/request.ych'
    if os.path.exists(ych_path):
        os.remove(ych_path)
    print(f'RDF-file for RQ {request_id} created.')


def create_txt(request_id, seq_path, markers_count, years_per_generation, avg_mutation_rate):
    print(f'Creating TXT-file for RQ {request_id}...')
    murka_args = ''
    if os.name == 'nt':
        murka_args = '{0}/murka/murka.exe '.format(os.getcwd())
    else:
        murka_args = '{0}/murka/murka/murka '.format(os.getcwd())
    murka_args += murka_additional_args
    murka_args += '-r "{0}/murka/data/metric/states_str0050ineq_2_2" ' \
                  '-G "TRDF; 4; ROOTPREFERRED|TXNAMES|ROOTONLY|TREEONLY|NOPOOL|AGE|NOSEQ; 4; 3; 0.0; 0.0; ; ; ; ; viz/{1}/output/nw#.txt; ; ; ; " ' \
                  '-i "{2}/request.rdf" ' \
                  '-N {3} ' \
        .format(os.getcwd(), request_id, seq_path, get_rho(markers_count, years_per_generation, avg_mutation_rate))
    subprocess.run(murka_args,
                   shell=True,
                   check=False,
                   cwd=f'{os.getcwd()}/murka')
    rdf_path = f'{seq_path}/request.rdf'
    if os.path.exists(rdf_path):
        os.remove(rdf_path)
    if os.path.exists(seq_path):
        os.rmdir(seq_path)
    print(f'TXT-file for RQ {request_id} created.')


def create_dot(request_id, seq_path, markers_count, years_per_generation, avg_mutation_rate):
    print(f'Creating DOT-file for RQ {request_id}...')
    murka_args = ''
    if os.name == 'nt':
        murka_args = '{0}/murka/murka.exe '.format(os.getcwd())
    else:
        murka_args = '{0}/murka/murka/murka '.format(os.getcwd())
    murka_args += murka_additional_args
    murka_args += '-r "{0}/murka/data/metric/states_str0050ineq_2_2" ' \
                  '-G "GraphViz; 1; ROOTPREFERRED|TXNAMES|ROOTONLY|TREEONLY|NOPOOL|AGE; 1.8; 1.1; 0.1; 2.0; 86.0; ; ; ; viz/{1}/output/nw#.dot; ; viz/tpl/nwtpl.txt; ; " ' \
                  '-i "{2}/request.rdf" ' \
                  '-N {3} ' \
        .format(os.getcwd(), request_id, seq_path, get_rho(markers_count, years_per_generation, avg_mutation_rate))
    subprocess.run(murka_args,
                   shell=True,
                   check=False,
                   cwd=f'{os.getcwd()}/murka')
    rdf_path = f'{seq_path}/request.rdf'
    if os.path.exists(rdf_path):
        os.remove(rdf_path)
    if os.path.exists(seq_path):
        os.rmdir(seq_path)
    print(f'DOT-file for RQ {request_id} created.')


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
            new_value = float(average_age) + float(result.group(1))
            new_label = regex.sub(f'"{str(new_value)}\\\\n+-\\2y"', label)
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


def create_graph(request_id, viz_path, tree_direction, markers_count, haplotypes_count, output_extension, output_format):
    print(f'Creating graph files for RQ {request_id}...')
    output_path = f'{viz_path}/output'
    files_list = os.listdir(output_path)
    if os.name == 'nt':
        with Pool(processes=cpu_count()) as pool:
            pool.starmap(process_graph_creation,
                         zip(files_list, repeat(haplotypes_count), repeat(markers_count), repeat(output_path),
                             repeat(tree_direction), repeat(output_extension), repeat(output_format)))
    else:
        tasks = [Process(target=process_graph_creation,
                         args=(dot_filename, haplotypes_count, markers_count, output_path,
                               tree_direction, output_extension, output_format,))
                 for dot_filename in files_list]
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
    print(f'Graph files for RQ {request_id} created.')


def process_graph_creation(dot_filename, haplotypes_count, markers_count, output_path, tree_direction, output_extension,
                           output_format):
    output_filename = dot_filename.replace('.dot', output_extension)
    dot_filename_path = f'{output_path}/{dot_filename}'
    graphs = pydot.graph_from_dot_file(dot_filename_path)
    graph = graphs[0]
    graph.del_node('"\\n"')
    graph.set_graph_defaults(rankdir=tree_direction, label=f'Y{markers_count}, {haplotypes_count} haplotypes')
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
