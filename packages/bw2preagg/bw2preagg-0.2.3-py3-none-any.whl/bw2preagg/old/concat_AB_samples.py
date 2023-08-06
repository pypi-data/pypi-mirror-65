from pathlib import Path
import json
import shutil
import click
import numpy as np

@click.command()
@click.option('--result_dir', help='Base directory path for precalculated samples', type=str)
def concat_samples(result_dir):
    """Delete directories with corrupt AB samples"""

    result_dir = Path(result_dir)
    common_files_dir = result_dir / "common_files"
    assert common_files_dir.is_dir(), "no common files at {}".format(common_files_dir)
    good_dir_fp = common_files_dir/"good_dirs.json"
    samples_dir = result_dir / "AB_samples"
    samples_dir.mkdir(exist_ok=True)
    if not good_dir_fp.is_file():
        raise ValueError("Must first identify good files first using check_AB.py")
    with open(common_files_dir/"good_dirs.json", 'r') as f:
        good_dirs_dict = json.load(f)

    total_iterations = sum(list(good_dirs_dict.values()))
    position = 0
    for i, (dirpath, iterations) in enumerate(good_dirs_dict.items()):
        print("Adding {} samples from {}".format(iterations, dirpath))
        dirpath=Path(dirpath)
        A = np.load(dirpath / "A_0.npy")
        B = np.load(dirpath / "B_0.npy")
        if i==0:
            A_rows = A.shape[0]
            B_rows = B.shape[0]
            A_matrix_samples = np.memmap(
                filename=str(samples_dir / "A_total.npy"),
                dtype="float64",
                mode='w+',
                shape=(A_rows, total_iterations)
            )

            B_matrix_samples = np.memmap(
                filename=str(samples_dir / "B_total.npy"),
                dtype="float64",
                mode='w+',
                shape=(B_rows, total_iterations)
            )

        A_matrix_samples[:, position:position + iterations] = A
        B_matrix_samples[:, position:position + iterations] = B
        A_matrix_samples.flush()
        B_matrix_samples.flush()
        position += iterations

if __name__ == '__main__':
    __spec__ = None
    concat_samples()