import os
from pathlib import Path
#BRIGHTWAY2_DIR = Path('/home/plesage/projects/def-ciraig1/plesage/bw_dir')
#os.environ['BRIGHTWAY2_DIR'] = str(BRIGHTWAY2_DIR)

import numpy as np
import click
from brightway2 import projects, Database, LCA, databases
import json

def check_AB(dirpath, lca):
    """Check that the sampled A and B matrices are not corrupt"""

    dirpath = Path(dirpath)

    A_ok = True
    B_ok = True
    reason = []

    if not (dirpath / 'A_0.npy').is_file():
        A_ok = False
        reason.append("A samples missing")
    else:
        A = np.load(dirpath / 'A_0.npy')
        if not np.all(np.isfinite(A)):
            A_ok = False
            reason.append('A sample contains corrupt entries')
        if not A.shape[0]==len(lca.technosphere_matrix.data):
            A_ok = False
            reason.append('A sample wrong size')
    if not (dirpath / 'B_0.npy').is_file():
        B_ok = False
        reason.append("B samples missing")
    else:
        B = np.load(dirpath / 'B_0.npy')
        if not np.all(np.isfinite(B)):
            B_ok = False
            reason.append('B sample contains corrupt entries')
        if not B.shape[0]==len(lca.biosphere_matrix.data):
            B_ok = False
            reason.append('B sample wrong size')
    if A_ok and B_ok and A.shape[1]!=B.shape[1]:
        A_ok=False
        B_ok=False
        reason.append('Inconsistent number of iterations')
    if A_ok and B_ok:
        return True, A.shape[1]
    else:
        return False, reason

@click.command()
@click.option('--project_name', default='default', help='Brightway2 project name', type=str)
@click.option('--database_name', help='Database name', type=str)
@click.option('--result_dir', help='Base directory path for precalculated samples', type=str)

def check_multiple_AB_samples_dir(project_name, database_name, result_dir):
    """ Check multiple dirs with AB samples"""
    if project_name not in projects:
        raise ValueError("Missing project")
    projects.set_current(project_name)
    if not database_name in databases:
        print(databases)
        raise ValueError("Missing database", database_name, "available: ", databases)

    result_dir = Path(result_dir)
    common_files_dir = result_dir / "common_files"
    assert common_files_dir.is_dir(), "no common files at {}".format(common_files_dir)
    matrix_samples_dir = result_dir / "matrix_samples_raw"
    assert matrix_samples_dir.is_dir(), "Directory with AB samples subdirectories not found at {}".format(
        str(matrix_samples_dir)
    )

    fu = {act:1 for act in Database(database_name)}
    lca = LCA(fu)
    lca.lci()

    good_dirs = {}
    bad_dirs = {}

    for dirpath in matrix_samples_dir.iterdir():
        if not dirpath.is_dir():
            bad_dirs[dirpath]="Not a directory"
            continue
        ok, detail = check_AB(dirpath, lca)
        if ok:
            good_dirs[str(dirpath)]=detail
        else:
            bad_dirs[str(dirpath)]=detail

    with open(common_files_dir/'good_dirs.json', 'w') as fp:
        json.dump(good_dirs, fp)
    with open(common_files_dir/'bad_dirs.json', 'w') as fp:
        json.dump(bad_dirs, fp)

    total_iterations_available = sum(list(good_dirs.values()))
    print("\n**********************************************")
    print("Total good iterations available: ", total_iterations_available)
    if len(bad_dirs) is not 0:
        print("Total bad directories: ", len(bad_dirs))
        print("\tSee bad_dirs.json for more detail")
        print("\tUse delete_bad_AB_samples_dir.py to delete bad directories")
    print("**********************************************")






if __name__ == '__main__':
    __spec__ = None
    check_multiple_AB_samples_dir()