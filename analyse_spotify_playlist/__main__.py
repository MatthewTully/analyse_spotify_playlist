"""Entry point for the application."""

import argparse
import sys

from analyse_spotify_playlist.analyse_spotify_playlist import main
from analyse_spotify_playlist.file_output import FileOutput
from analyse_spotify_playlist.logger import Log

logger = Log()
file_handler = FileOutput()


if "__main__" in __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        type=str,
        help="Playlist Id/s to analyse. If more than one, split by comma",
    )
    parser.add_argument(
        "-v", "--verbose", help="Print analysis to the terminal", action="store_true"
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Analytical depth.\n0 - Basic Summary (default),\n1 - shows in depth section,\n2 - shows raw audio feature information with highest, lowest, and average value.",
    )
    parser.add_argument("-o", "--output", help="Path to the output")

    args = parser.parse_args()

    verbose = False
    if args.verbose:
        verbose = args.verbose
    logger.set_logger(verbose)
    input_ids = args.input.split(",")

    if len(input_ids) == 0:
        logger.print("No ids provided for analysis")
        sys.exit(1)

    depth = args.depth
    output_path = args.output

    if isinstance(output_path, str):
        file_handler.set_output_path(output_path)
        if not FileOutput.path is None:
            file_handler.set_write_to_file_flag(True)
            print(f"File output enabled. Outputting to {file_handler.path.absolute()}")
        else:
            print("Provided Path does not exist, No file output.")
            if verbose is False:
                print(
                    "No valid output enabled: Invalid output path and verbose flag not set. Please set a valid path, or use the verbose flag to print to console.\nExiting..."
                )
                sys.exit(1)
    elif output_path is None and verbose is False:
        print(
            "No valid output enabled: Please set -verbose flag, or an -output location."
        )
        sys.exit(1)

    main(input_ids, depth)
