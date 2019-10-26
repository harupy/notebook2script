import os
import json
import argparse


def read_json(fp):
    with open(fp, 'r') as f:
        return json.load(f)


def replace_extension(fp, ext):
    ext = ext if ext.startswith('.') else '.' + ext
    root = os.path.splitext(fp)[0]
    return root + ext


def get_args():
    parser = argparse.ArgumentParser(description='Extract code from Jupyter notebooks')
    parser.add_argument('-d', '--dir', required=True, help='Directory where notebooks are stored')
    parser.add_argument('-o', '--out', default='scripts',
                        help='Directory where python scirpts will be saved (default: scripts)')
    return parser.parse_args()


def extract_code(notebook):
    code = ''
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            code += ''.join(cell['source']) + '\n' * 2
    return code


def main():
    # parse command line arguments
    args = get_args()
    in_dir = args.dir
    out_dir = args.out

    # make output directory if it doesn't exist
    if not os.path.exists(in_dir):
        os.makedirs(out_dir)

    for fname in os.listdir(in_dir):
        # process only notebooks
        if fname.endswith('.ipynb'):
            print('processing:', fname)
            nb_path = os.path.join(in_dir, fname)
            notebook = read_json(nb_path)
            code = extract_code(notebook)

            # save extracted code as a python script
            save_path = os.path.join(out_dir, fname)
            save_path = replace_extension(save_path, '.py')
            with open(save_path, 'w') as f:
                f.write(code)


if __name__ == '__main__':
    main()
