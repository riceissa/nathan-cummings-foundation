#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup


FILE_PATHS = [
    "data/1991-arts.html",
    "data/1991-community.html",
    "data/1991-environment.html",
    "data/1991-health.html",
    "data/1991-interprogram.html",
    "data/1991-jewishlife.html",
    "data/1992-arts.html",
    "data/1992-community.html",
    "data/1992-environment.html",
    "data/1992-health.html",
    "data/1992-interprogram.html",
    "data/1992-jewishlife.html",
    "data/1992-presidential.html",
    "data/1992-prior.html",
    "data/1992-researchdevelopmentevaluation.html",
    "data/1993-arts.html",
    "data/1993-community.html",
    "data/1993-environment.html",
    "data/1993-health.html",
    "data/1993-interprogram.html",
    "data/1993-jewishlife.html",
    "data/1993-presidential.html",
    "data/1993-researchdevelopmentevaluation.html",
    "data/1994-arts.html",
    "data/1994-community.html",
    "data/1994-environment.html",
    "data/1994-health.html",
    "data/1994-interprogram.html",
    "data/1994-jewishlife.html",
    "data/1994-presidential.html",
]


def main():
    for fp in FILE_PATHS:
        with open(fp, "r") as f:
            soup = BeautifulSoup(f, "lxml")
            for table in soup.find_all("table"):
                trs = table.find_all("tr")
                try:
                    num_col = len(trs[1].find_all("td"))
                except IndexError:
                    # This is a table with just one row, so skip it
                    continue
                if num_col != 5:
                    continue
                label = sub_area(table)
                print(label)
                for tr in trs:
                    cols = tr.find_all("td")
                    try:
                        location = cleaned(cols[0].find("i").text)
                    except:
                        location = ""
                    print(label, location,
                          list(map(lambda x: cleaned(x.text), cols)))


def sub_area(table):
    """Find the sub-area of the grant. These are given right above the table in
    bold."""
    tag = table.previous_sibling
    while tag is not None and tag.find("b") in [None, -1]:
        tag = tag.previous_sibling
    if tag:
        return cleaned(tag.find("b").text)
    return ""


def cleaned(s):
    if s is None:
        return ""
    try:
        result = re.sub(r"\s+", " ", s).strip()
    except:
        print(type(s), s)
        raise TypeError
    return result


if __name__ == "__main__":
    main()
