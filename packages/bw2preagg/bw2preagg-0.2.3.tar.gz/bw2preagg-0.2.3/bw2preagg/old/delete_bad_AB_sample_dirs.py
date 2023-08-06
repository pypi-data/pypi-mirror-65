from pathlib import Path
import json
import shutil
import click

@click.command()
@click.option('--result_dir', help='Base directory path for precalculated samples', type=str)
def delete_bad_dirs(result_dir):
    """Delete directories with corrupt AB samples"""

    result_dir = Path(result_dir)
    common_files_dir = result_dir / "common_files"
    assert common_files_dir.is_dir(), "no common files at {}".format(common_files_dir)
    bad_dir_fp = common_files_dir/"bad_dirs.json"
    if not bad_dir_fp.is_file():
        raise ValueError("Must first identify bad files first using check_AB.py")
    with open(common_files_dir/"bad_dirs.json", 'r') as f:
        bad_dirs_dict = json.load(f)
    for fp, reason in bad_dirs_dict.items():
        print("Delete {}".format(fp))
        print("Reasons:")
        for s in reason:
            print("\t{}".format(s))
        shutil.rmtree(Path(fp))

if __name__ == '__main__':
    __spec__ = None
    delete_bad_dirs()