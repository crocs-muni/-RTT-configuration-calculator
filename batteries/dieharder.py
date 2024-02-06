# SPDX-License-Identifier: MIT
from typing import Optional
from utilities import concatenate_test_ids, WARN_VARIABLE

DEFAULT_PSAMPLES = 100

WARN_OMIT = "WARNING - This test was marked as bad by Dierharder."

TEST_NAMES = {
    0: "Dieharder Diehard Birthdays Test",
    1: "Dieharder Diehard OPERM5 Test",
    2: "Dieharder Diehard 32x32 Binary Rank Test",
    3: "Dieharder Diehard 6x8 Binary Rank Test",
    4: "Dieharder Diehard Bitstream Test",
    5: "Dieharder Diehard OPSO",
    6: "Dieharder Diehard OQSO Test",
    7: "Dieharder Diehard DNA Test",
    8: "Dieharder Diehard Count the 1s (stream) Test",
    9: "Dieharder Diehard Count the 1s Test (byte)",
    10: "Dieharder Diehard Parking Lot Test",
    11: "Dieharder Diehard Minimum Distance (2d Circle) Test",
    12: "Dieharder Diehard 3d Sphere (Minimum Distance) Test",
    13: "Dieharder Diehard Squeeze Test",
    14: "Dieharder Diehard Sums Test",
    15: "Dieharder Diehard Runs Test",
    16: "Dieharder Diehard Craps Test",
    17: "Dieharder Marsaglia and Tsang GCD Test",
    100: "Dieharder STS Monobit Test",
    101: "Dieharder STS Runs Test",
    102: "Dieharder STS Serial Test (Generalized)",
    200: "Dieharder RGB Bit Distribution Test",
    201: "Dieharder RGB Generalized Minimum Distance Test",
    202: "Dieharder RGB Permutations Test",
    203: "Dieharder RGB Lagged Sum Test",
    204: "Dieharder RGB Kolmogorov-Smirnov Test",
    205: "Dieharder Byte Distribution",
    206: "Dieharder DAB DCT",
    207: "Dieharder DAB Fill Tree Test",
    208: "Dieharder DAB Fill Tree Test 2",
    209: "Dieharder DAB Monobit 2 Test",
}

BYTES_PER_PSAMPLE = {0: 153624,
                     1: 4000020,
                     2: 5120000,
                     3: 2400000,
                     4: 1048584,
                     5: 8388608,
                     6: 5592416,
                     7: 2621484,
                     8: 256004,
                     9: 5120000,
                     10: 96000,
                     11: 64000,
                     12: 48000,
                     13: 9225522,
                     14: 796,
                     15: 400000,
                     16: 5402336,
                     17: 80000000,
                     100: 400000,
                     101: 400000,
                     102: 400000,
                     204: 40000,
                     205: 614400000,
                     206: 51200000,
                     207: 452016414,
                     208: 116881518,
                     209: 260000000}

NTUPLES = {200: (1, 12), 201: (2, 5), 202: (2, 5), 203: (0, 32)}

TEST_IDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 100,
            101, 102, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209]

VARIABLE_SIZE_TESTS = {13, 16, 207, 208}


def get_bytes_per_psample(args, test_id: int, ntup: Optional[int]) -> int:
    """Returns number of bytes used by one repetition of first-level
       test (psample). The test is identified by tuple (test_id, ntup),
       ntup must be None for tests where it is not applicable.

       :param args: parsed command line arguments
       :param test_id: int identifying the tests
       :param ntup: int identifying the test variant, None if the test has no variants.
       :return: int representing number of bytes needed for one repetition (psample) of chosen test.
    """
    # tests with variants
    if test_id == 200 and 1 <= ntup <= 12:
        return ntup * 800000 + 4
    elif test_id == 201 and 2 <= ntup <= 5:
        return ntup * 40000
    elif test_id == 202 and 2 <= ntup <= 5:
        return ntup * 400000
    elif test_id == 203 and 0 <= ntup <= 32:
        return (ntup + 1) * 4000000
    # tests with variable size
    elif test_id in VARIABLE_SIZE_TESTS:
        return int(BYTES_PER_PSAMPLE[test_id] * (1 + args.dieharder_buffer))
    # rest of tests (with no variants and constant sizes)
    elif test_id in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 17,
                     100, 101, 102, 204, 205, 206, 209} and ntup is None:
        return BYTES_PER_PSAMPLE[test_id]
    raise ValueError("Invalid test ID or combination of test ID and ntup")


def calculate_psamples(args, test_id: int, ntup: Optional[int], file_size: int) -> int:
    """Returns number of repetitions (psamples) of the given first-level
       test. The test is identified by tuple (test_id, ntup),
       ntup must be None for tests where it is not applicable.

       :param args: parsed command line arguments
       :param test_id: int identifying the tests
       :param ntup: int identifying the test variant, None if the test has no variants
       :param file_size: size of the tested file in bytes
       :return: Number of possible repetitions of first-level tests (psample) for given test and file_size.
    """
    if test_id == 0:
        psamples = (file_size - 24) // get_bytes_per_psample(args, test_id, ntup)
    else:
        psamples = file_size // get_bytes_per_psample(args, test_id, ntup)
    return psamples + (1 if args.increased else 0)


def dieharder(args, file_size: int):
    """Creates and returns battery configuration for Dieharder battery.
       The configuration is returned as dictionary.

       :param args:parsed command line arguments
       :param file_size: size of the tested file in bytes
       :return: battery configuration in dictionary form
    """
    test_ids = []
    omitted_ids = []
    result = {"defaults": {
        "psamples": DEFAULT_PSAMPLES,
        "test-ids": []},
        "test-specific-settings": [],
        "omitted-tests": []}

    for test_id in TEST_IDS:
        # tests with variants
        if test_id in {200, 201, 202, 203}:
            entry = dieharder_test_with_variants(args, test_id, file_size)
        # tests with no variants
        else:
            entry = dieharder_no_variant_test(args, test_id, file_size)

        # The test is omitted
        if entry is None:
            omitted_ids.append(test_id)
        # The test has same settings as defaults (expected to happen almost never)
        elif entry == {}:
            test_ids.append(test_id)
        else:
            test_ids.append(test_id)
            result["test-specific-settings"].append(entry)

    result["defaults"]["test-ids"] = concatenate_test_ids(test_ids)
    result["omitted-tests"] = concatenate_test_ids(omitted_ids)
    return result


def dieharder_no_variant_test(args, test_id: int, file_size: int):
    """ Creates entry for test-specific-settings for a test with no variants.
    
    :param args: parsed command line arguments
    :param test_id: id of chosen test
    :param file_size: size of the tested file in bytes
    :return: None if the test will not be executed, empty dictionary if the
            test has settings equal to defaults, dictionary with the entry otherwise.
    """
    psamples = calculate_psamples(args, test_id, None, file_size)
    # Test marked as bad by Dieharder, omitted by default
    if test_id in {5, 6, 7, 14}:
        psamples = 0

    if psamples == 0:
        return None
    # Tests that require no test-specific settings entry.
    if psamples == DEFAULT_PSAMPLES and test_id not in VARIABLE_SIZE_TESTS:
        return {}
    test = {
        "test-id": test_id,
        "psamples": psamples
    }
    if test_id in VARIABLE_SIZE_TESTS:
        test["comment"] = WARN_VARIABLE
    return test


def dieharder_test_with_variants(args, test_id: int, file_size: int):
    """ Creates entry for test-specific-settings for a test with variants.

        :param args: parsed command line arguments
        :param test_id: id of chosen test
        :param file_size: size of the tested file in bytes
        :return: None if the test will not be executed, dictionary with the entry otherwise.
        """
    test = {
        "test-id": test_id,
        "variants": [],
        "omitted-variants": []
    }
    ntup_min, ntup_max = NTUPLES[test_id]
    for ntup in range(ntup_min, ntup_max + 1):
        variant = dieharder_variant(args, test_id, ntup, file_size)
        if variant is None:
            test["omitted-variants"].append("-n {}".format(ntup))
        else:
            test["variants"].append(variant)

    if len(test["variants"]) == 0:
        return None
    return test


def dieharder_variant(args, test_id: int, ntup: int, file_size: int):
    """
    Creates the one variant setting for test entry inside test-specific-settings.

    :param args: parsed command line arguments
    :param test_id: int identifying the test
    :param ntup: int identifying the test variant
    :param file_size: size of the tested file in bytes
    :return: None if the variant will not be executed, dictionary with the variant entry otherwise.
    """
    psamples = calculate_psamples(args, test_id, ntup, file_size)
    if psamples == 0:
        return None
    variant = {"arguments": "-n {}".format(ntup),
               "psamples": psamples}
    # TODO: check if this is necessary
    if test_id == 201:
        variant["arguments"] += " -t 10000"
    return variant


def dieharder_defaults(args):
    """
    Creates the defaults (information for user) for Dieharder battery.

    :param args: parsed command line arguments
    :return: Dictionary with the defaults
    """
    defaults = {"test-ids": concatenate_test_ids(TEST_IDS),
                "test-specific-defaults": []}
    for test_id in TEST_IDS:
        test = {"test-id": test_id,
                "test-name": TEST_NAMES[test_id],
                "psamples": DEFAULT_PSAMPLES}

        # Tests with variants
        if test_id in {200, 201, 202, 203}:
            ntup_min, ntup_max = NTUPLES[test_id]
            test["ntup-range"] = "{} - {}".format(ntup_min, ntup_max)
            test["variants"] = []
            for ntup in range(ntup_min, ntup_max + 1):
                test["variants"].append({
                    "ntup": ntup,
                    "bytes-per-psample": get_bytes_per_psample(args, test_id, ntup)
                })
        # Tests with no variants
        else:
            test["bytes-per-psample"] = get_bytes_per_psample(args, test_id, None)

        if test_id in {201, 204}:
            test["psamples"] = 1000
        elif test_id in {205, 206, 207, 208, 209}:
            test["psamples"] = 1

        if test_id in {13, 16, 207, 208}:
            test["comment"] = WARN_VARIABLE
        elif test_id in {5, 6, 7, 14}:
            test["comment"] = WARN_OMIT

        defaults["test-specific-defaults"].append(test)
    return defaults
