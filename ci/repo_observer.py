import argparse
import os
import socket
import subprocess
import sys

from ci import helpers


def update_repository(repository: str) -> None:
    """Update the watched repository and check for new commit_id."""
    try:
        return subprocess.check_output(['./update_repo.sh', repository])
    except subprocess.CalledProcessError as process_error:
        raise SystemError(
            'Could not update and check repository. ', \
            'Reason {process_error}'.format(process_error=process_error),
        )


def dispatch_commit_for_test(dispatcher_host: str, dispatcher_port: int):
    with open('.commit_id', 'r') as commit_file:
        commit = commit_file.readline()
        response = helpers.communicate(
            dispatcher_host,
            dispatcher_port,
            'dispatch:{commit}'.format(commit=commit),
        )
    if response != 'OK':
        raise ConnectionError(
            'Could not dispatch the test {response}'.format(response=response),
        )


def parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dispatcher-server',
        help='dispatcher host:port, by default it uses localhost:8888',
        default='localhost:8888',
        action='store',
    )
    parser.add_argument(
        'repo',
        metavar='REPO',
        type=str,
        help='path to the repository this will observe',
    )
    return parser.parse_args(args)


def verify_dispatcher_status(dispatcher_host: str, dispatcher_port: int):
    try:
        return helpers.communicate(
            dispatcher_host,
            dispatcher_port,
            'status',
        )
    except socket.error as socket_error:
        raise ConnectionError(
            'Could not communicate with dispatcher server ' /
            '{error}'.format(error=socket_error),
        )


def poll(args: argparse.Namespace) -> None:
    """Pool repository for new commit."""
    dispatcher_host, dispatcher_port = args.dispatcher_server.split(':')
    while True:
        update_repository(args.repo)
        if os.path.isfile('.commit_id'):
            response = verify_dispatcher_status(
                dispatcher_host,
                int(dispatcher_port),
            )
            if response == 'OK':
                dispatch_commit_for_test(dispatcher_host, int(dispatcher_port))
            else:
                raise ConnectionError(
                    'Could not communicate with dispatcher server {e}',
                )


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    poll(args)
