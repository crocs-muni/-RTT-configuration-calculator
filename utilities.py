# SPDX-License-Identifier: MIT
from typing import List, Optional
from re import compile

KILO = 1024
MEGA = KILO ** 2
GIGA = KILO ** 3
TERA = KILO ** 4

WARN_VARIABLE = "WARNING - This test uses variable amount of data."


def parse_size(size: str) -> Optional[int]:
    """Converses size from string to integer. Size must be all numeric,
       only the last character may denote unit (kilo, mega, giga or tera)."""
    if size.isnumeric():
        return int(size)

    # check is size matches format '123M'
    regex = compile("^[0-9]+[kKmMgGtT]$")
    if regex.fullmatch(size) is None:
        return None

    unit = size[-1]
    if unit in "kK":
        power = KILO
    elif unit in "mM":
        power = MEGA
    elif unit in "gG":
        power = GIGA
    else:
        power = TERA
    return int(size[:-1]) * power


def concatenate_test_ids(test_ids: List[int]) -> List[str]:
    """Shortens the list of test IDs (integers) into more compact
    format. For example [1, 2, 3, 5, 6] -> ["1-3", "5-6"]."""
    concat = []
    if len(test_ids) == 0:
        return []
    first = test_ids[0]
    last = test_ids[0]
    for test_id in test_ids[1:]:
        if test_id != last + 1:
            if first == last:
                concat.append("{}".format(last))
            else:
                concat.append("{}-{}".format(first, last))
            first = test_id
        last = test_id

    if first == last:
        concat.append("{}".format(first))
    else:
        concat.append("{}-{}".format(first, last))
    return concat
