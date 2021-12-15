#!python3

import git
from urllib.parse import urlparse
import os
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <path to file>')
    print('Note that this script requires the working directory to be in a git repository with a remote named `origin`')

file = sys.argv[1]

repo = git.Repo(os.getcwd())
origin = repo.remote('origin')
if not origin:
    print('** Failed to detect remote origin! **')
    sys.exit(1)

parts = urlparse(origin.url)
if not parts.scheme:
    parts = urlparse('ssh://' + origin.url)

git_root = Path(repo.git.rev_parse('--show-toplevel')).resolve()
file_path = Path(file).resolve().relative_to(git_root)

if parts.scheme == 'ssh':
    print(f'https://{parts.hostname}/' + '/'.join((parts.netloc.split(':', 1)
          [-1], parts.path.lstrip('/').removesuffix('.git'), 'blob', repo.active_branch.name, str(file_path))))
elif parts.scheme in {'http', 'https'}:
    print(f'https://{parts.hostname}/' + '/'.join((parts.path.strip(
        '/').removesuffix('.git'), 'blob', repo.active_branch.name, str(file_path))))
else:
    print(f'remote origin has unrecognized URL scheme: {parts.scheme!r}; currently supported are ssh and http(s)', file=sys.stderr)
    sys.exit(1)
