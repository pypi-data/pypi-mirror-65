""" Generation of samples for all activities in an LCI database

Built on the Brightway2 framework.
Stores each result (supply array, inventory vector, sampled matrices)
for each activity and each iteration is stored as an individual file.
These must then be assembled to be useful.
"""
import os
from pathlib import Path
#BRIGHTWAY2_DIR = Path('/home/plesage/projects/def-ciraig1/plesage/bw_dir')
#os.environ['BRIGHTWAY2_DIR'] = str(BRIGHTWAY2_DIR)
from brightway2 import *
import numpy as np
import click
import pickle
import json
import pyprind
import sys
import time
import multiprocessing as mp


def get_useful_info(result_dir, database_name, project_name, balance_water, balance_land_use):
    """Collect and save job-level data"""

    # Make directories
    result_dir = Path(result_dir)
    result_dir.mkdir(exist_ok=True, parents=True)
    common_dir = result_dir / 'common_files'
    common_dir.mkdir(exist_ok=True)

    # Generate sacrificial LCA whose attributes will be saved
    db = Database(database_name)
    collector_functional_unit = {act:act['production amount'] for act in db}
    activities = [act.key[1] for act in db]
    sacrificial_lca = LCA(collector_functional_unit)
    sacrificial_lca.lci()

    # Save various attributes for eventual reuse in interpretation
    file = os.path.join(common_dir, 'ordered_activity_codes.json')
    with open(file, "w") as f:
        json.dump(activities, f, indent=4)

    fp = os.path.join(common_dir, 'product_dict.pickle')
    with open(fp, "wb") as f:
        pickle.dump(sacrificial_lca.product_dict, f)

    fp = os.path.join(common_dir, 'bio_dict.pickle')
    with open(fp, "wb") as f:
        pickle.dump(sacrificial_lca.biosphere_dict, f)

    fp = os.path.join(common_dir, 'activity_dict.pickle')
    with open(fp, "wb") as f:
        pickle.dump(sacrificial_lca.activity_dict, f)

    fp = os.path.join(common_dir, 'tech_params.pickle')
    with open(fp, "wb") as f:
        pickle.dump(sacrificial_lca.tech_params, f)

    fp = os.path.join(common_dir, 'bio_params.pickle')
    with open(fp, "wb") as f:
        pickle.dump(sacrificial_lca.bio_params, f)

    fp = os.path.join(common_dir, 'IO_Mapping.pickle')
    with open(fp, "wb") as f:
        pickle.dump({v: k for k, v in mapping.items()}, f)

    fp = os.path.join(common_dir, 'tech_row_indices')
    np.save(fp, sacrificial_lca.technosphere_matrix.tocoo().row)

    fp = os.path.join(common_dir, 'tech_col_indices')
    np.save(fp, sacrificial_lca.technosphere_matrix.tocoo().col)

    fp = os.path.join(common_dir, 'bio_row_indices')
    np.save(fp, sacrificial_lca.biosphere_matrix.tocoo().row)

    fp = os.path.join(common_dir, 'bio_col_indices')
    np.save(fp, sacrificial_lca.biosphere_matrix.tocoo().col)

    if balance_water:
        get_water_balancing_data(result_dir, database_name, project_name, sacrificial_lca)
    if balance_land_use:
        get_land_use_balancing_data(result_dir, database_name, project_name, sacrificial_lca)

def generate_samples(project_name,
                     database_name,
                     result_dir,
                     worker_id,
                     iterations,
                     balance_water,
                     balance_land_use,
                     task_id
                     ):
    """Generate database-wide correlated Monte Carlo samples

    This function is a worker function. It is called from
    the `generate_samples` function, that dispatches the Monte Carlo
    work to a specified number of workers.
    """
    t0 = time.time()
    # Open the project containing the target database
    projects.set_current(project_name)
    db = Database(database_name)

    # Set directories
    result_dir = Path(result_dir)
    common_dir = result_dir / "common_files"
    assert common_dir.is_dir(), "No common files found"
    needed_files = [
        'ordered_activity_codes.json',
        'product_dict.pickle',
        'bio_dict.pickle',
        'activity_dict.pickle',
        'tech_params.pickle',
        'bio_params.pickle',
        'IO_Mapping.pickle',
        'tech_row_indices.npy',
        'tech_col_indices.npy',
        'bio_row_indices.npy',
        'bio_col_indices.npy'
    ]
    if balance_water:
        needed_files.append('water_info')
    if balance_land_use:
        needed_files.append('land_use_info')
    available = os.listdir(common_dir)
    missing = []
    for f in needed_files:
        if f not in available:
            missing.append(f)
    if missing:
        raise ValueError("Missing common files: {}".format(missing))

    samples_dir = result_dir / "matrix_samples_raw" / "{}".format(task_id)

    # Create an LCA object that spans all demands
    collector_functional_unit = {act: act['production amount'] for act in db}
    mc = MonteCarloLCA(demand=collector_functional_unit)
    mc.load_data()

    A_matrix_samples = np.memmap(
        filename=str(samples_dir/"A_{}.npy".format(worker_id)),
        dtype="float64",
        mode='w+',
        shape=(mc.technosphere_matrix.tocoo().data.size, iterations)
    )
    B_matrix_samples = np.memmap(
        filename=str(samples_dir/"B_{}.npy".format(worker_id)),
        dtype="float64",
        mode='w+',
        shape=(mc.biosphere_matrix.tocoo().data.size, iterations)
    )

    for i in pyprind.prog_bar(range(iterations), stream=sys.stderr):
        # Sample new values for technosphere and biosphere matrices
        next(mc)
        if balance_water:
            mc = balance_water_exchanges(mc, common_dir)
        if balance_land_use:
            mc = balance_land_use_exchanges(mc, common_dir)
        A_matrix_samples[:, i] = mc.technosphere_matrix.tocoo().data
        A_matrix_samples.flush()
        B_matrix_samples[:, i] = mc.biosphere_matrix.tocoo().data
        B_matrix_samples.flush()
    print(
        "finished {} iterations".format(
            iterations
        )
    )
    A_samples_as_arr = np.array(A_matrix_samples)
    B_samples_as_arr = np.array(B_matrix_samples)
    del A_matrix_samples
    del B_matrix_samples
    np.save(str(samples_dir/"A_{}.npy".format(worker_id)), np.array(A_samples_as_arr))
    np.save(str(samples_dir /"B_{}.npy".format(worker_id)), np.array(B_samples_as_arr))

    print("Took {} for {} iterations".format(time.time()-t0, iterations))

@click.command()
@click.option('--project_name', default='default', help='Brightway2 project name', type=str)
@click.option('--database_name', help='Database name', type=str)
@click.option('--result_dir', help='Base directory path for precalculated samples', type=str)
@click.option('--parallel_jobs', help='Number of CPUs allocated to this work', type=int)
@click.option('--iterations', help='Number of iterations in total', type=int)
@click.option('--balance_water', help='Balance water exchanges', default=False, type=bool)
@click.option('--balance_land_use', help='Balance land use exchanges', default=False, type=bool)
@click.option('--_generate_common_files', default=False, type=bool)
@click.option('--task_id', default=0, type=int)
def dispatch_sampler(project_name, database_name, result_dir, cpus, iterations, balance_water,
                     balance_land_use, generate_common_files, task_id):
    # Identify all activities for which samples are required
    #print(os.environ['BRIGHTWAY2_DIR'])
    t0 = time.time()
    if project_name not in projects:
        raise ValueError("Missing project")
    projects.set_current(project_name)
    if database_name not in databases:
        raise ValueError("Missing database")

    result_dir = Path(result_dir)
    common_files_dir = result_dir / "common_files"
    assert common_files_dir.is_dir(), "no common files at {}".format(common_files_dir)
    matrix_samples_dir = result_dir / "matrix_samples_raw" / "{}".format(task_id)
    matrix_samples_dir.mkdir(exist_ok=False, parents=True)

    if generate_common_files:
        print("Generating common files, this may take some time.")
        get_useful_info(result_dir, database_name, project_name, balance_water, balance_land_use)

    # Calculate number of iterations per worker.
    it_per_worker = [iterations//cpus for _ in range(cpus)]
    for _ in range(iterations-cpus*(iterations//cpus)):
        it_per_worker[_]+=1

    # Dispatch actual sampling work to workers
    workers = []
    for worker_id in range(cpus):
        child = mp.Process(target=generate_samples,
                           args=(
                               project_name,
                               database_name,
                               result_dir,
                               worker_id,
                               it_per_worker[worker_id],
                               balance_water,
                               balance_land_use,
                               task_id
                           )
                           )
        workers.append(child)
    print("Time to get workers going: {} seconds".format(time.time() - t0))
    for w in workers:
        w.start()
    for w in workers:
        w.join()


if __name__ == '__main__':
    __spec__ = None
    dispatch_sampler()
