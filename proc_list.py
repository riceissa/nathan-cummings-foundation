#!/usr/bin/env python3

from bs4 import BeautifulSoup
import bs4
import re
import sys
import csv
import pdb


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
    fieldnames = ["grantee", "grantee_location", "url", "program",
                  "sub_area", "purpose", "year", "notes",
                  "prev_year_eoy_grants_payable", "same_year_awards",
                  "same_year_payments", "same_year_eoy_grants_payable"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)

    for fp in FILE_PATHS:
        with open(fp, "r") as f:
            soup = BeautifulSoup(f, "lxml")
            year = int(fp[len("data/"):len("data/YYYY")])
            if fp in br_style:
                for grant in split_on_br(soup):
                    purpose, grantee, location_amount = grant
                    if grant == (['\n'], None, []):
                        pass
                    elif not grantee:
                        print(fp, grant, file=sys.stderr)
                    else:
                        la_str = " ".join(map(cleaned, location_amount))
                        d = {"program": program_name(fp),
                             "year": year,
                             "url": SOURCE[fp],
                             "purpose": " ".join(map(cleaned, purpose)),
                             "notes": find_extra(la_str),
                             "grantee_location": find_location(la_str),
                             "same_year_awards": first_dollar(la_str),
                             "grantee": cleaned(grantee.text)}
                        writer.writerow(d)
            else:
                for grant in soup.find_all("p"):
                    pass


def split_on_br(soup):
    grants = []
    for br in soup.find_all("br"):
        curr = br.next_sibling
        first = []
        bold = None
        last = []
        while curr is not None and curr.name != "br":
            if curr.name != "b" and bold is None:
                first += [curr]
            elif curr.name == "b" and bold is None:
                bold = curr
            else:
                last += [curr]
            curr = curr.next_sibling
        grants.append((first, bold, last))
    return grants


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


def cleaned(s):
    if s is None:
        return ""
    if isinstance(s, bs4.element.Tag):
        return cleaned(s.text)
    try:
        result = re.sub(r"\s+", " ", s).strip()
    except:
        print(type(s), s, file=sys.stderr)
        raise TypeError
    return result


def bad_money(l):
    for s in l:
        if "$" in s and not s.strip().startswith("$"):
            return s
    return ""


if __name__ == "__main__":
    main()
