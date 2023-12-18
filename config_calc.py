# SPDX-License-Identifier: MIT
from batteries import nist_sts, dieharder, testu01
import json
import utilities
from sys import argv, stderr, exit
from os import stat
import argparse

# Constants used to differentiate TestU01 batteries.
SMALL_CRUSH = 4
CRUSH = 5


def create_json(arguments, json_file, file_size: int):
    configuration = {
        "options": argv,
        "data-size": file_size,
        "randomness-testing-toolkit": {
            "dieharder-settings": dieharder.dieharder(arguments, file_size),
            "dieharder-defaults": dieharder.dieharder_defaults(arguments),

            "nist-sts-settings": nist_sts.nist_sts_test(arguments, file_size),
            "nist-sts-defaults": nist_sts.nist_sts_defaults(arguments),

            "tu01-rabbit-settings": testu01.rabbit(arguments, file_size),
            "tu01-rabbit-defaults": testu01.rabbit_defaults(arguments),

            "tu01-smallcrush-settings": testu01.crush(arguments, SMALL_CRUSH, file_size),
            "tu01-smallcrush-defaults": testu01.crush_defaults(arguments, SMALL_CRUSH),

            "tu01-crush-settings": testu01.crush(arguments, CRUSH, file_size),
            "tu01-crush-defaults": testu01.crush_defaults(arguments, CRUSH),

            "tu01-alphabit-settings": testu01.alphabit(arguments, file_size),
            "tu01-alphabit-defaults": testu01.alphabit_defaults(arguments),

            "tu01-blockalphabit-settings": testu01.block_alphabit(arguments, file_size),
            "tu01-blockalphabit-defaults": testu01.block_alphabit_defaults(arguments),
        }
    }
    print(json.dumps(configuration, indent=4), file=json_file)


def main(arguments) -> None:
    if arguments.data_file is not None:
        data_size = stat(arguments.data_file).st_size
    else:
        parsed = utilities.parse_size(arguments.size)
        if parsed is None:
            print("File size string is not in valid format.", file=stderr)
            exit(-1)
        data_size = parsed

    if data_size == 0 and arguments.data_file is not None:
        print("The data size is 0, please insert a positive number", file=stderr)
        exit(-1)
    elif data_size == 0 and arguments.data_file is None:
        print("The tested file is empy, please choose nonempty file", file=stderr)
        exit(-1)

    with open(arguments.config_file, "w") as config_file:
        create_json(arguments, config_file, data_size)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="RTT Configuration calculator.",
        description="Calculates battery configuration files for RTT and rtt-py."
    )

    # Input size arguments - only one of them may be used
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f","--data-file",
                       type=str,
                       help="Path to file with data to be tested."
                       )

    group.add_argument("-s","--size",
                       type=str,
                       help="Size of data that will be tested. Either integer, or integer followed by a unit \
                            (K, M, G, T are accepted as powers of two)."
                       )


    # Remaining arguments
    parser.add_argument("-c","--config-file",
                        type=str,
                        default="config.json",
                        help="Path to file the configuration will be written to. Defaults value is 'config.json'."
                        )


    parser.add_argument("-i","--increased",
                        action="store_true",
                        default=False,
                        help="All tests will be set with number of repetitions of the first-level test one higher \
                              than it should be. Main purpose is for testing."
                        )



    parser.add_argument("--dieharder-buffer",
                        type=float,
                        default=0.001,
                        help="Sets buffer size to Dieharder tests with variable size. Default value is 0.1%%. Using \
                              lower value may lead to file rewinds."
                        )



    parser.add_argument("--nist-stream-size",
                        type=int,
                        default=1000000,
                        help="Sets stream size argument for NIST battery. Default value is 1,000,000. Lower values\
                              will break recommendations for some tests."
                        )


    parser.add_argument("--tu01-buffer",
                        type=float,
                        default=0.01,
                        help="Sets buffer size to test with variable size from all TestU01 batteries. Default value\
                              is 1%%. Using lower value may lead to file rewinds."
                        )


    parser.add_argument("--tu01-bit-nb",
                        type=int,
                        default=52428800,
                        help="Sets bit_nb argument to TestU01's Rabbit, Alphabit and BlockAlphabit batteries. Defaults\
                              value is 52,428,800. Lower values will not be applicable for some tests."
                        )



    return parser.parse_args()


if __name__ == "__main__":
    prog_args = parse_arguments()
    main(prog_args)
