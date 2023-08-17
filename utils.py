import os
import shutil
import subprocess
import uuid

import pydot

markers_names = '393,390,D19,391,385a,385b,426,388,439,3891,392,3892,458,459a,459b,455,454,447,437,448,449,464a,464b,' \
                '464c,464d,460,GATA,YCAa,YCAb,456,607,576,570,CDYa,CDYb,442,438,531,578,395a,395b,590,537,641,472,' \
                '406,511,425,413a,413b,557,594,436,490,534,450,444,481,520,446,617,568,487,572,640,492,565,710,485,' \
                '632,495,540,714,716,717,505,556,549,589,522,494,533,636,575,638,462,452,445,YGATAA10,463,441,' \
                'YGGAAT1B07,525,712,593,650,532,715,504,513,561,552,726,635,587,643,497,510,434,461,435'
mutation_rate = '10,6,7,9,6,4,99,14,5,7,21,4,3,19,13,51,30,4,18,10,2,6,5,5,5,6,7,13,9,4,6,2,2,2,2,5,19,23,58,27,19,' \
                '83,10,29,99,7,9,11,5,6,4,21,71,45,3,50,4,3,6,4,13,17,10,11,30,28,18,20,20,20,20,20,20,20,20,20,20,' \
                '20,15,15,15,15,15,15,15,15,15,15,15,10,10,10,10,10,10,10,10,10,10,10,5,5,5,5,5,5,5,5,5,5,5'
murka_additional_args = '-T "MJ" ' \
                        '-S "VB|RSW|EM|THR2" ' \
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
                        '-j "CONSTSPLITS|EQSPLITS|PSHELLING|POSTPROC|CONTRACTNT2|ROOTING|ALLOWTERMROOT|MIDPOINTROOT|MSNCACHE|NWGRCACHE|FASTMJ|WPHEUR|MPSTAT|CONSTREE|NWAGE" ' \
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
                        '-N 3.465 ' \
                        '-Q "wtdistmx" ' \
                        '-K "rftdistmx" ' \
                        '-R "tcmptbl" ' \
                        '-B "parttbl" ' \
                        '-L "topotbl" '


def get_rows(data):
    return data \
        .decode('utf-8') \
        .replace(", ", ",") \
        .replace("-", ",") \
        .splitlines()


def get_modal_markers_count(prepared_rows):
    return len(prepared_rows[4].split(','))


def get_haplotypes_count(prepared_rows):
    haplotypes_count = 0
    for row in prepared_rows[6:]:
        if len(row.split(',')) > 1:
            haplotypes_count += 1
    return haplotypes_count


def is_same_size(prepared_rows, modal_markers_count):
    for row in prepared_rows[6:]:
        splitted_row = row.split(',')
        if len(splitted_row) > 1:
            if len(splitted_row) != modal_markers_count:
                return False
    return True


def get_prepared_rows(rows, modal_markers_count):
    rows[0] = ','.join(markers_names.split(',')[:modal_markers_count])
    rows[1] = ','.join(mutation_rate.split(',')[:modal_markers_count])
    del rows[3:6]
    return rows


def create_folders(request_id, seq_path, viz_path):
    os.makedirs(seq_path,
                exist_ok=True)
    os.makedirs(f'{viz_path}/output',
                exist_ok=True)
    print(f'Folders for RQ {request_id} created.')


def create_ych(body_rows, request_id, seq_path):
    with open(f'{seq_path}/request.ych',
              'w',
              encoding='utf-8') as text_file:
        for row in body_rows:
            text_file.write(f"{row}\n")
    print(f'YCH-file for RQ {request_id} created.')


def create_rdf(request_id, seq_path):
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
    ych_path = f"{seq_path}/request.ych"
    if os.path.exists(ych_path):
        os.remove(ych_path)
    print(f'RDF-file for RQ {request_id} created.')


def create_txt(request_id, seq_path):
    murka_args = ''
    if os.name == 'nt':
        murka_args = '{0}/murka/murka.exe '.format(os.getcwd())
    else:
        murka_args = '{0}/murka/murka/murka '.format(os.getcwd())
    murka_args += murka_additional_args
    murka_args += '-r "{0}/murka/data/metric/states_str0050ineq_2_2" ' \
                  '-G "TRDF; 4; ROOTPREFERRED|DIST|CHNAMES|CHCHNG|TXFR|ROOTONLY|TREEONLY|NOPOOL|NOSEQ|MPPART; 4; 3; 0.0; 0.0; ; ; ; ; viz/{1}/output/nw#.txt; ; ; ; " ' \
                  '-i "{2}/request.rdf" ' \
        .format(os.getcwd(), request_id, seq_path)
    subprocess.run(murka_args,
                   shell=True,
                   check=False,
                   cwd=f'{os.getcwd()}/murka')
    rdf_path = f"{seq_path}/request.rdf"
    if os.path.exists(rdf_path):
        os.remove(rdf_path)
    if os.path.exists(seq_path):
        os.rmdir(seq_path)
    print(f'TXT-file for RQ {request_id} created.')


def create_dot(request_id, seq_path):
    murka_args = ''
    if os.name == 'nt':
        murka_args = '{0}/murka/murka.exe '.format(os.getcwd())
    else:
        murka_args = '{0}/murka/murka/murka '.format(os.getcwd())
    murka_args += murka_additional_args
    murka_args += '-r "{0}/murka/data/metric/states_str0050ineq_2_2" ' \
                  '-G "GraphViz; 1; ROOTPREFERRED|CHNAMES|CHCHNG|TXNAMES|TXFR|TXFRSZ|TXCD|ROOTONLY|TREEONLY|NOPOOL|AGE|MPPART; 1.8; 1.1; 0.1; 2.0; 86.0; ; ; ; viz/{1}/output/nw#.dot; ; viz/tpl/nwtpl.txt; ; " ' \
                  '-i "{2}/request.rdf" ' \
        .format(os.getcwd(), request_id, seq_path)
    subprocess.run(murka_args,
                   shell=True,
                   check=False,
                   cwd=f'{os.getcwd()}/murka')
    rdf_path = f"{seq_path}/request.rdf"
    if os.path.exists(rdf_path):
        os.remove(rdf_path)
    if os.path.exists(seq_path):
        os.rmdir(seq_path)
    print(f'DOT-file for RQ {request_id} created.')


def create_png(request_id, viz_path, rankdir, markers_count, haplotypes_count):
    output_path = f'{viz_path}/output'
    for dot_filename in os.listdir(output_path):
        png_filename = dot_filename.replace(".dot", ".png")
        dot_filename_path = f'{output_path}/{dot_filename}'
        graph = pydot.graph_from_dot_file(dot_filename_path)
        graph[0].set_graph_defaults(rankdir=rankdir)
        graph[0].set_graph_defaults(rankdir=rankdir, label=f'Y{markers_count}, {haplotypes_count} haplotypes')
        png_filename_path = f'{output_path}/{png_filename}'
        graph[0].write_png(png_filename_path)
        os.remove(dot_filename_path)
    print(f'PNG-file for RQ {request_id} created.')


def create_pdf(request_id, viz_path, rankdir, markers_count, haplotypes_count):
    output_path = f'{viz_path}/output'
    for dot_filename in os.listdir(output_path):
        pdf_filename = dot_filename.replace(".dot", ".pdf")
        dot_filename_path = f'{output_path}/{dot_filename}'
        graph = pydot.graph_from_dot_file(dot_filename_path)
        graph[0].set_graph_defaults(rankdir=rankdir, label=f'Y{markers_count}, {haplotypes_count} haplotypes')
        pdf_filename_path = f'{output_path}/{pdf_filename}'
        graph[0].write_pdf(pdf_filename_path)
        os.remove(dot_filename_path)
    print(f'PDF-file for RQ {request_id} created.')


def create_zip(request_id, viz_path):
    output_path = f'{viz_path}/output'
    shutil.make_archive(f'{viz_path}/result',
                        'zip',
                        output_path)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    print(f'ZIP-file for RQ {request_id} created.')


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def process_txt(request_id, prepared_rows):
    seq_path = f"{os.getcwd()}/murka/data/seq/{request_id}"
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folders(request_id, seq_path, viz_path)
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_txt(request_id, seq_path)
    create_zip(request_id, viz_path)


def process_png(request_id, prepared_rows, headers, modal_markers_count, haplotypes_count):
    seq_path = f"{os.getcwd()}/murka/data/seq/{request_id}"
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folders(request_id, seq_path, viz_path)
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_dot(request_id, seq_path)
    create_png(request_id, viz_path, headers['rankdir'], modal_markers_count, haplotypes_count)
    create_zip(request_id, viz_path)


def process_pdf(request_id, prepared_rows, headers, modal_markers_count, haplotypes_count):
    seq_path = f"{os.getcwd()}/murka/data/seq/{request_id}"
    viz_path = f'{os.getcwd()}/murka/nw/viz/{request_id}'
    create_folders(request_id, seq_path, viz_path)
    create_ych(prepared_rows, request_id, seq_path)
    create_rdf(request_id, seq_path)
    create_dot(request_id, seq_path)
    create_pdf(request_id, viz_path, headers['rankdir'], modal_markers_count, haplotypes_count)
    create_zip(request_id, viz_path)
