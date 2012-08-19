import os
from uuid import uuid4
from fnmatch import fnmatch
from git import Repo

from django.conf import settings


def iter_find_files(path, glob_pattern):
    """Generator that yields files in a directory matching a given glob.
        Will be used for finding settings and requirements files in a repo"""

    for dirpath, dirnames, filenames in os.walk(path):

        for filename in filenames:
            if fnmatch(filename, glob_pattern):
                yield os.path.join(dirpath, filename)

def clone_repo(repo_url, local_path=None):

    if local_path is None:
        repo_root = getattr(settings, 'REPO_ROOT', '/tmp')
        local_path = os.path.join(repo_root, uuid4())

    repo =  Repo.clone_from(repo_url, local_path)
    return repo

def get_branches_from_repo(repo_path):
    repo = Repo(repo_path)

def switch_repo_branch(repo_path, new_branch_name, current_branch_name):
    repo = Repo(repo_path)

    repo.branches.master.checkout()

    new_branch = getattr(repo.branches, branch_name )
    new_branch.checkout()

    return Repo(repo_path)