#! /usr/bin/env python
"""
Build the object library and the SpotifyAPI class.
"""
import argparse
from argparse import Namespace
import os

import build_object_library
import build_spotify_api_class


def get_args() -> Namespace:
    """Get the optional directory specified through the command line."""
    parser = argparse.ArgumentParser(
        description='Build .py files from yaml files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d',
                        '--directory',
                        type=str,
                        help='Target directory to place the built .py files.',
                        default='./src/spotifywrapper/')
    return parser.parse_args()


# def create_directory_structure(directory: str) -> None:
#     """Create the directory structure in the given directory location."""
#     object_library_path = os.path.join(directory, 'object_library')
#
#     if not os.path.isdir(directory):
#         os.mkdir(directory)
#     if not os.path.isdir(object_library_path):
#         os.mkdir(object_library_path)


if __name__ == '__main__':
    args = get_args()
    # create_directory_structure(args.directory)
    build_object_library.build(args.directory)
    build_spotify_api_class.build(args.directory)
