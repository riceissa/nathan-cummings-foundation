#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import sys


def main():
    soup = BeautifulSoup(open(sys.argv[1], "r"), "lxml")
    for grant in soup.prettify().split("<br/>"):
        gsoup = BeautifulSoup(grant, "lxml")
        grantee = gsoup.find("b")
        if grantee:
            location_amount = grantee.next_sibling
            grantee = cleaned(grantee.text)
            lst = list(filter(lambda x: x not in ["", "."],
                              cleaned(location_amount).split(",")))
            if lst and bad_money(lst):
                print(lst)


def cleaned(s):
    if s is None:
        return ""
    return re.sub(r"\s+", " ", s).strip()


def bad_money(l):
    for s in l:
        if "$" in s and not s.strip().startswith("$"):
            return s
    return ""


if __name__ == "__main__":
    main()
