import logging
import argparse

import drvn.installer.example_module
import drvn.installer._logging as drvn_logger


def main():
    args = _parse_arguments()

    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    drvn_logger.configure(log_level)

    logging.info(drvn.installer.example_module.example_public_function())


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.description = "Installers for various software with options on additionally installing custom configs."
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enables printing of debug statements",
    )
    arguments = parser.parse_args()
    return arguments
