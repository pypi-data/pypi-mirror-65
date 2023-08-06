import click
import os
import numpy as np
from pathlib import Path
import json
import pickle
BRIGHTWAY2_DIR = Path('/home/plesage/projects/def-ciraig1/plesage/bw_dir') # beluga
os.environ['BRIGHTWAY2_DIR'] = str(BRIGHTWAY2_DIR)
from brightway2 import *
import presamples


@click.command()
@click.option('--project_name', default='default', help='Brightway2 project name', type=str)
@click.option('--result_dir', help='Base directory path for precalculated samples', type=str)
@click.option('--chunk_size', help='Number of cols in presamples', type=int)
def create_AB_presample_resources(result_dir, project_name, chunk_size):
    print("In create_AB_presample_resources with following args:")
    print(result_dir, project_name, chunk_size)

    """Generate presample resource to be used in Monte Carlo"""
    print(projects)
    print(os.environ['BRIGHTWAY2_DIR'])
    assert project_name in projects, "Project {} not in projects".format(project_name)
    projects.set_current(project_name)
    result_dir = Path(result_dir)
    assert result_dir.is_dir()
    common_files_dir = result_dir / "common_files"
    assert common_files_dir.is_dir(), "no common files at {}".format(common_files_dir)
    matrix_samples_dir = result_dir / "AB_samples"
    assert matrix_samples_dir.is_dir(), "no matrix presamples at {}".format(matrix_samples_dir)
    presamples_dir = result_dir/"presamples"
    presamples_dir.mkdir(exist_ok=True)

    good_dir_fp = common_files_dir/"good_dirs.json"
    if not good_dir_fp.is_file():
        raise ValueError("Must first identify good files first using check_AB.py")
    with open(common_files_dir/"good_dirs.json", 'r') as f:
        good_dirs_dict = json.load(f)
    total_iterations = sum(list(good_dirs_dict.values()))

    tech_row_indices = np.load(common_files_dir/"tech_row_indices.npy")
    tech_col_indices = np.load(common_files_dir/"tech_col_indices.npy")
    bio_row_indices = np.load(common_files_dir/"bio_row_indices.npy")
    bio_col_indices = np.load(common_files_dir/"bio_col_indices.npy")

    with open(common_files_dir/"bio_dict.pickle", 'rb') as f:
        bio_dict = pickle.load(f)
    with open(common_files_dir/"activity_dict.pickle", 'rb')as f:
        activity_dict = pickle.load(f)
    with open(common_files_dir/"product_dict.pickle", 'rb')as f:
        product_dict = pickle.load(f)
    rev_product_dict = {v: k for k, v in product_dict.items()}
    rev_activity_dict = {v: k for k, v in activity_dict.items()}
    rev_bio_dict = {v: k for k, v in bio_dict.items()}
    print("loaded easy data")

    off_diag =\
        np.squeeze(
            np.argwhere(
                np.array(
                    [x!=y for x, y in zip(tech_row_indices, tech_col_indices)]
                )
            )
        )
    print("got off diags")
    A_samples = np.memmap(
        filename=str(matrix_samples_dir / 'A_total.npy'),
        dtype='float64',
        mode='r')
    print("mmap worked")
    A_samples = A_samples.reshape(-1, total_iterations)
    print("reshape worked")
    A_samples = np.array(A_samples)
    print("convert to array worked: we're in business")

    A_samples[off_diag] = A_samples[off_diag]*-1
    B_samples = np.memmap(
        filename=str(matrix_samples_dir / 'B_total.npy'),
        dtype='float64',
        mode='r')
    print("mmap worked - B")
    B_samples = B_samples.reshape(-1, total_iterations)
    print("reshape worked - B")
    B_samples = np.array(B_samples)
    print("convert to array worked: we're in business - B")

    print("loaded matrices")
    prod_or_techno = [
        'technosphere' if tech_col_indices[i] != tech_row_indices[i]
        else 'production'
        for i in range(tech_col_indices.size)
    ]
    print("prod or techno done")

    A_indices = [
        (
            rev_product_dict[i],
            rev_activity_dict[j],
            prod_or_techno[i]
        ) for i, j in zip(
            list(tech_row_indices), list(tech_col_indices)
        )
    ]
    print("A indices done")
    B_indices = [(rev_bio_dict[i], rev_activity_dict[j], 'biosphere') for i, j in
                 zip(list(bio_row_indices), list(bio_col_indices))]
    print("B indices done")
    assert len(A_indices)==A_samples.shape[0]
    assert len(B_indices) == B_samples.shape[0]

    print("getting chunks")
    chunks = lambda l, n: [l[i:i + n] for i in range(0, len(l), n)]

    print("ready to generate presamples")
    for i, chunk in enumerate(chunks(np.arange(total_iterations), chunk_size)):
        print("Creating presamples package chunck_{} with {} cols".format(i, chunk.size))
        presamples.create_presamples_package(
            matrix_data=[
                (A_samples[:, chunk], A_indices, 'technosphere'),
                (B_samples[:, chunk], B_indices, 'biosphere')
            ],
            name="chunk_{}".format(i),
            seed="sequential",
            id_="chunk_{}".format(i),
            dirpath=presamples_dir
        )

if __name__=='__main__':
    __spec__ = None
    create_AB_presample_resources()
