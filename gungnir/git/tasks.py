from celery.task import task

from django.conf import settings
import hashlib
import os


from projects.models import Repo
from git.utils import pull_repo, get_tree_from_commit, write_tree_to_disk

def push_repo_to_disk(repo_id, head_ref=None):
    """Given a repo id pull it to disk"""
    repo = Repo.objects.get(pk=repo_id)

    hashed_repo_url = hashlib.sha1(repo.url).hexdigest()
    repo_path = os.path.join(settings.REPO_ROOT, hashed_repo_url)

    repo = pull_repo(repo.url, repo_path=repo_path)


    # May want to replace this with a chosen list of commits
    if not head_ref:
        head_ref = repo.head()

    commit = repo.get_object(head_ref)
    tree = get_tree_from_commit(commit)

    files_path = os.path.join(repo_path, 'data')
    write_tree_to_disk(repo, tree, files_path )

    return repo_path