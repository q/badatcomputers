from celery.task import task
from django.conf import settings
import hashlib
import os


from git import Repo as GitRepo
from gungnir.projects.models import Repo
from gungnir.projects.utils import clone_repo



def repo_app_hash(repo_url, app_name):
    return hashlib.sha1(app_name + repo_url).hexdigest()


@task
def fetch_repo_for_existing_entry(repo_id):

    repo = Repo.objects.get(pk=repo_id)

    if repo.repo_exists() and not os.path.exists():
        repo_path = repo.path_on_disk

    else:
        repo_path, branches = pre_fetch_repo(repo.url, repo.application.name)

    print 'REPO PATH IS: {0}'.format(repo_path)
    git_repo = GitRepo(repo_path)

    current_head = git_repo.head
    desired_head = getattr(git_repo.branches, repo.branch)

    if current_head.commit != desired_head.commit:
        desired_head.checkout()

    repo.path_on_disk = repo_path
    repo.save(async_task=False)

    return repo_id, repo_path


@task
def pre_fetch_repo(repo_url, app_name):
    # TODO: Add locking so that this can only be run once per repo_url/app_name pairs

    repo_path_hash = repo_app_hash(repo_url, app_name)

    repo_path = os.path.join(settings.REPO_ROOT,  repo_path_hash)

    if os.path.exists(repo_path):
        return repo_path, []

    repo = clone_repo(repo_url, local_path=repo_path)

    branches = list()
    for branch in repo.heads:
        branches.append(branch.name)

    return repo_path, branches