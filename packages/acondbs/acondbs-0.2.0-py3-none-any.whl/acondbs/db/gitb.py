"""Git operations
"""
from pathlib import Path
import git
import warnings

##__________________________________________________________________||
def commit(path, message=None):
    """commit all changes in a git repository to git

    If the path is not a git repository, unless it is empty, it will
    be initialized as a new repository.

    Parameters
    ----------
    path : str
        The path to a git repository
    message : str, optional
        Commit message.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If `path` is not a directory

    """

    path = Path(path)
    if not path.is_dir():
        raise ValueError("path is not a directory: {}".format(path))

    if is_git_repo(path):
        repo = git.Repo(path)
    else:
        if not list(path.iterdir()):
            warnings.warn('the directory is empty. nothing to commit: {}'.format(path))
            return
        repo = git.Repo.init(path)

    if not repo.is_dirty(untracked_files=True):
        warnings.warn('the repo is clean. nothing to commit: {}'.format(path))
        return

    repo.git.add(A=True)

    if not message:
        message = 'commit all'
    repo.index.commit(message)

##__________________________________________________________________||
def is_git_repo(path):
    """test if a folder is a git repository

    copied from https://stackoverflow.com/a/39956572/7309855

    """
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False

##__________________________________________________________________||
