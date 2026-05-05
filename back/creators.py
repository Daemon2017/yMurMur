import os
import subprocess

import utils

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
        .format(os.getcwd(), request_id, seq_path,
                utils.get_rho(markers_count, years_per_generation, avg_mutation_rate))
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
                  '-G "GraphViz; 1; ROOTPREFERRED|TXNAMES|ROOTONLY|TREEONLY|NOPOOL|AGE; 1.8; 1.1; 0.1; 2.0; 75.0; ; ; ; viz/{1}/output/nw#.dot; ; viz/tpl/nwtpl.txt; ; " ' \
                  '-i "{2}/request.rdf" ' \
                  '-N {3} ' \
        .format(os.getcwd(), request_id, seq_path,
                utils.get_rho(markers_count, years_per_generation, avg_mutation_rate))
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
