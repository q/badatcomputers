import os
import errno

from dulwich.repo import Repo
from dulwich.objects import Blob, Tree, TreeEntry, Commit
from dulwich.client import get_transport_and_path

from django.conf import settings
import uuid

from fnmatch import fnmatch

import logging
log = logging.getLogger('gungnir.git.utils')

def iter_find_files(path, glob_pattern):
    """Generator that yields files in a directory matching a given glob.
        Will be used for finding settings and requirements files in a repo"""

    for dirpath, dirnames, filenames in os.walk(path):

        for filename in filenames:
            if fnmatch(filename, glob_pattern):
                yield os.path.join(dirpath, filename)



def pull_repo(git_url, ref=None, repo_path=None):
    """Given a url to a repo save it to disk"""

    client, path = get_transport_and_path(git_url)

    if repo_path is None:
        repo_path = os.path.join(settings.REPO_ROOT, uuid.uuid4())

    if not os.path.exists(repo_path):
        repo = Repo.init(repo_path, mkdir=True)

    else:
        repo = Repo.init(repo_path)

    refs = client.fetch(path, repo)

    for ref in refs.items():
        repo.refs.add_if_new(*ref)


    return repo

def get_tree_from_commit(repo, commit_sha):
    """Given a SHA string reference to a commit, return the Tree object representing it"""

    commit = repo.get_object(commit_sha)

    if type(commit) is not Commit:
        raise AttributeError('Not a valid commit')

    tree_sha =  commit.tree
    tree = repo.get_object(tree_sha)
    return tree


def write_tree_to_disk(repo, tree, base_path):
    """Walk the git object tree for a given commit and write everything out to disk"""

    for tree_entry in tree.iteritems():
        # object might look like a bad name here, but its what they're referred to as internally in git.
        repo_object = repo.get_object(tree_entry.sha)

        repo_object_path = os.path.join(base_path, tree_entry.path)

        if type(repo_object) == Blob:
            log.warning('Creating {0}...'.format(repo_object_path))
            f = open(repo_object_path, 'w+')
            f.write(repo_object.data)
            f.close()

            os.chmod(repo_object_path, tree_entry.mode)

        elif type(repo_object) == Tree:
            try:
                log.warning('Creating directory {0}...'.format(repo_object_path))
                os.mkdir(repo_object_path)

                # We'll just accept that our default directory umask makes sense
            except OSError as e:
                if e.errno == errno.EEXIST:
                    continue
                else:
                    raise
            write_tree_to_disk(repo, repo_object, repo_object_path)