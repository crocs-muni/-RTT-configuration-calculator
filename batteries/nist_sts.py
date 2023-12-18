# SPDX-License-Identifier: MIT
TEST_NAMES = {
    1: "NIST Statistical Testing Suite Frequency (monobits) test",
    2: "NIST Statistical Testing Suite Test For Frequency Within A Block",
    3: "NIST Statistical Testing Suite Cumulative Sum (Cusum) Test",
    4: "NIST Statistical Testing Suite Runs Test",
    5: "NIST Statistical Testing Suite Test for the Longest Run of Ones in a Block",
    6: "NIST Statistical Testing Suite Random Binary Matrix Rank Test",
    7: "NIST Statistical Testing Suite Discrete Fourier Transform (Spectral) Test",
    8: "NIST Statistical Testing Suite Non-overlapping (Aperiodic) Template Matching Test",
    9: "NIST Statistical Testing Suite Overlapping (Periodic) Template Matching Test",
    10: "NIST Statistical Testing Suite Maurer's Universal Statistical Test",
    11: "NIST Statistical Testing Suite Approximate Entropy Test",
    12: "NIST Statistical Testing Suite Random Excursions Test",
    13: "NIST Statistical Testing Suite Random Excursions Variant Test",
    14: "NIST Statistical Testing Suite Serial Test",
    15: "NIST Statistical Testing Suite Linear Complexity Test",
}

WARN_SIZE = "WARNING - Used NIST Stream Size it too big for the data size."


def nist_sts_test(args, file_size: int):
    """
    Creates configuration for NIST STS battery.

    :param args: Parsed program arguments.
    :param file_size: Size of file the configuration is created for (in bytes).
    :return: The configuration for NIST STS battery, in dictionary form.
    """
    # No test set for execution, user must choose bigger stream size.
    if file_size < args.nist_stream_size:
        return {
            "defaults": {
                "test-ids": []
            },
            "omitted-test": ["1-15"],
            "comment": WARN_SIZE
        }
    return {
        "defaults": {
            "test-ids": ["1-15"],
            "stream-size": str(args.nist_stream_size),
            # file_size is in bytes, stream_size in bits
            "stream-count": str((file_size * 8) // args.nist_stream_size)
        },
        "test-specific-settings": []
    }


def nist_sts_defaults(args):
    """
        Creates defaults (information for the user) for NIST STS battery.

        :param args: Parsed program arguments.
        :return: The defaults for NIST STS battery, in dictionary form.
        """
    defaults = {"test-ids": ["1-15"],
                "test-specific-defaults": []}
    for test_id in range(1, 16):
        defaults["test-specific-defaults"].append(
            {"test-id": test_id,
             "test-name": TEST_NAMES[test_id],
             "bytes-per-stream": str(args.nist_stream_size // 8)}
        )
    return defaults
