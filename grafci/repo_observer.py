import argparse
import json
import os
import subprocess
import sys

from grafci import pytest_helpers


def update_repository(repository: str) -> None:
    """Update the watched repository and check for new commit_id."""
    try:
        return subprocess.check_output(['./update_repo.sh', repository])
    except subprocess.CalledProcessError as process_error:
        raise SystemError(
            'Could not update and check repository. ',
            'Reason {process_error}'.format(process_error=process_error),
        )


def run_tests(commit_id, repo_folder: str):
    subprocess.check_output(
        ['./test_runner_script.sh', repo_folder, commit_id],
    )
    test_results = pytest_helpers.run_pytest_tests(repo_folder)
    filename = 'test_results/test_result_{commit}.json'.format(
        commit=commit_id,
    )
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as results_file:
        json.dump(test_results, results_file)


def dispatch_commit_for_test(repo_folder: str):
    with open('.commit_id', 'r') as commit_file:
        commit = commit_file.readline().strip()
        run_tests(commit, repo_folder)


def parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'repo',
        metavar='REPO',
        type=str,
        help='path to the repository this will observe',
    )
    return parser.parse_args(args)


def _poll(repo):
    update_repository(repo)
    if os.path.isfile('.commit_id'):
        dispatch_commit_for_test(repo)


def poll(args: argparse.Namespace) -> None:  # pragma: no cover
    """Pool repository for new commit."""
    while True:  # noqa: WPS457
        _poll(args.repo)


def main():  # pragma: no cover
    args = parse_args(sys.argv[1:])
    poll(args)


if __name__ == '__main__':  # pragma: no cover
    main()
