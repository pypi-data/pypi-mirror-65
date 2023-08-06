import os
from pathlib import Path
#BRIGHTWAY2_DIR = Path('/home/plesage/projects/def-ciraig1/plesage/bw_dir') #beluga
BRIGHTWAY2_DIR = Path('/home/plesage/project/plesage/bw_dir') #cedar
os.environ['BRIGHTWAY2_DIR'] = str(BRIGHTWAY2_DIR)
from brightway2 import *
import numpy as np
import os
import click
import time
import multiprocessing as mp
import pickle
from pathlib import Path
from math import ceil
import json

import presamples

def calculate_lci_arrays(activity_list, result_dir, worker_id, project_name, database_name,
                         presample_id):

    projects.set_current(project_name)
    result_dir = Path(result_dir)
    common_files_dir = result_dir / "common_files"
    g_master_dir = result_dir / "lci"
    g_samples_dir = g_master_dir / "chunk_{}".format(presample_id)
    g_samples_dir_temp = g_samples_dir / "temp"
    g_samples_dir_temp.mkdir(exist_ok=True)

    with open(common_files_dir/"bio_dict.pickle", 'rb') as f:
        ref_bio_dict = pickle.load(f)
    presamples_directory = result_dir / "presamples" / "chunk_{}".format(presample_id)
    pp = presamples.PresamplesPackage(presamples_directory)
    total_iterations = pp.ncols
    print("total_iterations", total_iterations)

    g_dimensions = len(ref_bio_dict)

    for act_i, act_code in enumerate(activity_list):
        print("Worker {} working on {} of {}".format(worker_id, act_i+1, len(activity_list)))
        t0 = time.time()
        lci = np.memmap(
            filename=str(g_samples_dir_temp / "{}.npy".format(act_code)),
            dtype="float32",
            mode='w+',
            shape=(g_dimensions, total_iterations)
        )
        act_key = (database_name, act_code)

        mc  =MonteCarloLCA({act_key: get_activity(act_key)['production amount']}, presamples=[pp.path])
        for i in range(total_iterations):
            try:
                next(mc)
                this_g = np.squeeze(np.array(mc.inventory.sum(axis=1)))
                assert this_g.size==g_dimensions
                lci[:, i] = this_g
            except Exception as err:
                print("***********************\nWorker {}, activity {} problem with iteration {}:{}".format(worker_id, act_key, i, err))
                lci[:, i] = np.full(g_dimensions, np.nan).ravel()
        lci_as_arr = np.array(lci)
        assert lci_as_arr.shape==(g_dimensions, total_iterations), "Dimention not ok: {}".format(lci_as_arr.shape)
        del lci
        Path(g_samples_dir_temp/"{}.npy".format(act_code)).unlink()
        np.save(str(g_samples_dir / "{}.npy".format(act_code)), lci_as_arr)
        lci_as_arr = None # Free up memory
        print("Time for worker {} to calculate LCI for activity {}: {} minutes".format(worker_id, act_code, (time.time() - t0)/60))

def techno_dicts_equal(ref_techno_dict, new_techno_dict):
    """ Returns True if two product or activity dicts are functionally equivalent

    Difference in database name are ignored.
    """
    ref_techno_dict_for_comparison = {k[1]:v for k, v in ref_techno_dict.items()}
    new_techno_dict_for_comparison = {k[1]: v for k, v in new_techno_dict.items()}
    return ref_techno_dict_for_comparison == new_techno_dict_for_comparison

def get_techno_dicts_translator(ref_techno_dict, new_techno_dict):
    """ Return dict where k, v are resp. indices in reference and new techno matrix

    Applicable to both products (rows in A matrix) and
    activities (columns in A and B matrices)
    The names of the databases do not need to be the same, but the codes
    should be common
    """
    ref_bd_name = list(ref_techno_dict.keys())[0][0]
    new_bd_name = list(new_techno_dict.keys())[0][0]
    return {ref_techno_dict[(ref_bd_name, k[1])]: new_techno_dict[(new_bd_name, k[1])] for k in
            new_techno_dict.keys()}

@click.command()
@click.option('--project_name', default='default', help='Brightway2 project name', type=str)
@click.option('--database_name', help='Database name', type=str)
@click.option('--result_dir', help='Base directory path for precalculated samples', type=str)
@click.option('--parallel_jobs', help='Number of CPUs allocated to this work', type=int)
@click.option('--presamples_id', help='Integer representing the presample package', type=int, default=None)
@click.option('--slice_id', help='Slice ID for job arrays, useful when dispatching calculations on computer clusters', type=int, default=None)
@click.option('--number_of_slices', help='Total number of slices for job arrays, useful when dispatching calculations on computer clusters', type=int, default=None)
def dispatch_lci_calculators(project_name, database_name, result_dir, cpus,
                             presamples_id, slice_id=None, number_of_slices=None):
    """ Dispatches LCI array calculations to distinct processes (multiprocessing)

    If number_of_slices/slice_id are not None, then only a subset of database activities are processed.
    """
    # Ensure base data exist and are valid
    assert project_name in projects, "Project {} not in projects".format(project_name)
    projects.set_current(project_name)
    assert database_name in databases, "Database {} not in databases".format(database_name)

    # Base directory with samples and common files subdirectories
    result_dir = Path(result_dir)

    # Check existence of directory with common files
    common_files_dir = result_dir / "common_files"
    assert common_files_dir.is_dir(), "no common files at {}".format(common_files_dir)

    # Check existence of presamples directory
    presamples_directory = result_dir / "presamples" / "chunk_{}".format(presamples_id)
    assert presamples_directory.is_dir(), "no presamples directory at {}".format(presamples_directory)

    # Create directory for LCI arrays
    g_master_dir = result_dir / "lci"
    g_master_dir.mkdir(exist_ok=True)
    g_samples_dir = g_master_dir / "chunk_{}".format(presamples_id)
    g_samples_dir.mkdir(exist_ok=True)

    chunks = lambda l, n: [l[i:i + n] for i in range(0, len(l), n)]

    # Identify subset of activities to treat
    with open(common_files_dir/"ordered_activity_codes.json", 'r') as f:
        all_activities = json.load(f)
    if slice_id is None or number_of_slices is None:
        activities = all_activities
    else:
        activities = chunks(all_activities, ceil(len(all_activities)/(number_of_slices)))[slice_id]

    activities_to_treat = []
    for act in activities:
        lci_filename = "{}.npy".format(act)
        # Check if this result has already been generated
        if lci_filename in os.listdir(g_samples_dir):
            # And make sure all columns were filled in with results
            if not any(np.load(str(g_samples_dir / lci_filename), mmap_mode='r').sum(axis=0) == 0):
                # If all done, then go on to the next activity
                continue
        else:
            activities_to_treat.append(act)
    print("Total of {} lci arrays to generate".format(len(activities_to_treat)))


    activity_sublists = chunks(activities_to_treat, ceil(len(activities_to_treat)/cpus))
    workers = []
    for i, s in enumerate(activity_sublists):
        j = mp.Process(target=calculate_lci_arrays,
                       args=(s, result_dir, i, project_name, database_name, presamples_id)
                       )
        workers.append(j)
    for w in workers:
        w.start()
    for w in workers:
        w.join()

if __name__=='__main__':
    __spec__ = None
    dispatch_lci_calculators()