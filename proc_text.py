#!/usr/bin/env python3

import re
import sys


FILE_PATHS = [
        "data/2002-grants.txt",
        "data/2003-grants.txt",
        "data/2004-grants.txt",
        "data/2005-grants.txt",
        "data/2006-grants.txt",
        "data/2007-grants.txt",
        "data/2008-grants.txt",
        "data/2009-grants.txt",
        "data/2010-grants.txt",
        "data/2011-grants.txt",
        "data/2012-grants.txt",
        "data/2013-grants.txt",
        "data/2014-grants.txt",
        "data/2015-grants.txt",
        "data/2016-grants.txt",
        ]


def main():
    for fp in FILE_PATHS:
        with open(fp, "r") as f:
            line_num = 1
            for line in f:
                (grantee, prev_year_eoy_grants_payable,
                 same_year_awards, same_year_payments,
                 same_year_eoy_grants_payable) = line.strip().rsplit(" ", 4)
                assert is_amount(prev_year_eoy_grants_payable), (fp, line_num)
                assert is_amount(same_year_awards), (fp, line_num)
                assert is_amount(same_year_payments), (fp, line_num)
                assert is_amount(same_year_eoy_grants_payable), (fp, line_num)
                line_num += 1


def is_amount(x):
    if x == "-":
        return True
    m1 = re.match(r"^((\d{1,3},)?\d{1,3},)?\d{1,3}$", x)
    m2 = re.match(r"^\(((\d{1,3},)?\d{1,3},)?\d{1,3}\)$", x)
    if m1 or m2:
        # num = int(x.replace("(", "").replace(")", "").replace(",", ""))
        return True
    return False


if __name__ == "__main__":
    main()
