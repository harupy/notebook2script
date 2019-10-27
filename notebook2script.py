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
    parser.add_argument('-d', '--dir', required=True, help='Directory containing notebooks')
    parser.add_argument('-o', '--out', default='scripts',
                        help='Directory where python scirpts will be stored (default: scripts)')
    return parser.parse_args()


def extract_code(notebook):
    # filter code cells
    ret = ''
    divider = '\n\n#%%\n'
    for cell in notebook['cells']:
        # skip markdown cells
        if cell['cell_type'] == 'markdown':
            continue

        code = ''.join(cell['source']).strip()

        # skip empty cells
        if code == '':
            continue

        ret += code + divider

    return ret[:-5]  # trim divider after the last cell


def main():
    # parse command line arguments
    args = get_args()
    in_dir = args.dir
    out_dir = args.out

    for root, dirs, files in os.walk(in_dir):
        # skip empty directory and checkpoints
        if len(files) == 0 or root.endswith('.ipynb_checkpoints'):
            continue

        # make directory to store script
        save_dir = os.path.join(out_dir, *root.split(os.sep)[1:])

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for fname in files:
            # process only notebooks otherwise skip
            if not fname.endswith('.ipynb'):
                continue

            # extract code from notebook
            print('processing:', fname)
            nb_path = os.path.join(root, fname)
            notebook = read_json(nb_path)
            code = extract_code(notebook)

            # save extracted code as script
            save_path = os.path.join(save_dir, fname)
            save_path = replace_extension(save_path, '.py')
            with open(save_path, 'w') as f:
                f.write(code)


if __name__ == '__main__':
    main()
