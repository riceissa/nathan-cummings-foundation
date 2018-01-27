#!/usr/bin/env python3

from bs4 import BeautifulSoup
import bs4
import re
import sys
import csv
import pdb

import util

FILE_PATHS = [
        "data/1995-arts.html",
        "data/1995-community.html",
        "data/1995-environment.html",
        "data/1995-health.html",
        "data/1995-interprogram.html",
        "data/1995-jewishlife.html",
        "data/1995-presidential.html",
        "data/1996-arts.html",
        "data/1996-community.html",
        "data/1996-environment.html",
        "data/1996-health.html",
        "data/1996-interprogram.html",
        "data/1996-jewishlife.html",
        "data/1996-presidential.html",
        ]

SOURCE = {
        "data/1995-arts.html": "https://web.archive.org/web/20070824030901/http://nathancummings.org/annual95/000126.html",
        "data/1995-community.html": "https://web.archive.org/web/20081201094333/http://www.nathancummings.org/annual95/000135.html",
        "data/1995-environment.html": "https://web.archive.org/web/20081201094333/http://www.nathancummings.org/annual95/000128.html",
        "data/1995-health.html": "https://web.archive.org/web/20081201094333/http://www.nathancummings.org/annual95/000130.html",
        "data/1995-interprogram.html": "https://web.archive.org/web/20081201094333/http://www.nathancummings.org/annual95/000134.html",
        "data/1995-jewishlife.html": "https://web.archive.org/web/20081201094333/http://www.nathancummings.org/annual95/000132.html",
        "data/1995-presidential.html": "https://web.archive.org/web/20081201094333/http://www.nathancummings.org/annual95/000136.html",
        "data/1996-arts.html": "https://web.archive.org/web/20081201110132/http://www.nathancummings.org/annual96/000108.html",
        "data/1996-community.html": "https://web.archive.org/web/20081201110132/http://www.nathancummings.org/annual96/000117.html",
        "data/1996-environment.html": "https://web.archive.org/web/20081201110132/http://www.nathancummings.org/annual96/000110.html",
        "data/1996-health.html": "https://web.archive.org/web/20081201110132/http://www.nathancummings.org/annual96/000112.html",
        "data/1996-interprogram.html": "https://web.archive.org/web/20081201110132/http://www.nathancummings.org/annual96/000116.html",
        "data/1996-jewishlife.html": "https://web.archive.org/web/20081201110132/http://www.nathancummings.org/annual96/000114.html",
        "data/1996-presidential.html": "https://web.archive.org/web/20081201110132/http://www.nathancummings.org/annual96/000118.html",
        }


# These are the files that use a <br>-delimited list. The other ones use
# separate paragraphs (<p> tags).
br_style = {
        "data/1996-arts.html",
        "data/1996-environment.html",
        "data/1996-health.html",
        "data/1996-interprogram.html",
        "data/1996-jewishlife.html",
        }


def main():
    writer = csv.DictWriter(sys.stdout, fieldnames=util.fieldnames)

    for fp in FILE_PATHS:
        with open(fp, "r") as f:
            soup = BeautifulSoup(f, "lxml")
            if fp in br_style:
                for br in soup.find_all("br"):
                    write_grant(partitioned_line(br.next_sibling),
                                find_sub_area(br), fp, writer)
            else:
                for para in soup.find_all("p"):
                    write_grant(partitioned_line(list(para.children)[0]),
                                find_sub_area(para), fp, writer)


def find_sub_area(elem):
    curr = elem
    while curr is not None and curr.name != "h2":
        curr = curr.previous_sibling
    return util.cleaned(curr)

def partitioned_line(elem):
    first = []
    bold = None
    last = []
    curr = elem
    while curr is not None and curr.name != "br":
        if curr.name != "b" and bold is None:
            first += [curr]
        elif curr.name == "b" and bold is None:
            bold = curr
        else:
            last += [curr]
        curr = curr.next_sibling
    return (first, bold, last)


def write_grant(grant, sub_area, file_path, writer):
    purpose, grantee, location_amount = grant
    year = int(file_path[len("data/"):len("data/YYYY")])
    if grant == (['\n'], None, []):
        pass
    elif not grantee:
        print(file_path, grant, file=sys.stderr)
    else:
        la_str = " ".join(map(util.cleaned, location_amount))
        d = {"program": program_name(file_path),
             "sub_area": sub_area,
             "year": year,
             "url": SOURCE[file_path],
             "purpose": " ".join(map(util.cleaned, purpose)),
             "notes": find_extra(la_str),
             "grantee_location": find_location(la_str),
             "same_year_awards": first_dollar(la_str),
             "grantee": util.cleaned(grantee.text)}
        # writer.writerow(d)


def first_dollar(string):
    """Find and return the first dollar amount in string."""
    m = re.match(r"[^$]*\$([0-9,]+)", string)
    if m:
        return int(m.group(1).replace(",", ""))
    return ""


def find_location(string):
    """Find and return the location in string."""
    dollar = string.find("$")
    if dollar > 0:
        loc = string[:dollar].strip()
        if loc.endswith(","):
            loc = loc[:-1]
        if loc.startswith(","):
            loc = loc[1:].strip()
        return loc
    return ""


def find_extra(string):
    """Find extra information about the grant, appearing after the first dollar
    amount."""
    result = ""
    dollar = string.find("$")
    if dollar > 0:
        space = string.find(" ", dollar)
        if space > 0:
            result = string[space:].strip()
            if result.startswith("(") and result.endswith(")"):
                result = result[1:-1]
    return result


def program_name(filepath):
    program_part = filepath.split("-")[1].split(".")[0]
    rename = {
            "arts": "Arts",
            "community": "Community",
            "environment": "Environment",
            "health": "Health",
            "interprogram": "Interprogram",
            "jewishlife": "Jewish life",
            "presidential": "Presidential grant",
            "prior": "Prior grant",
            "researchdevelopmentevaluation": "Research, Development & Evaluation Grant",
            }
    return rename[program_part]


if __name__ == "__main__":
    main()
