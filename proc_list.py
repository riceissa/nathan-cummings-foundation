#!/usr/bin/env python3

from bs4 import BeautifulSoup
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


def main():
    fieldnames = ["grantee", "grantee_location", "url", "program",
                  "sub_area", "purpose", "year",
                  "prev_year_eoy_grants_payable", "same_year_awards",
                  "same_year_payments", "same_year_eoy_grants_payable"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)

    for fp in FILE_PATHS:
        with open(fp, "r") as f:
            soup = BeautifulSoup(f, "lxml")
            year = int(fp[len("data/"):len("data/YYYY")])
            # if year == 1995:
                # for grant in soup.find_all("p"):
            if year == 1996:
                pdb.set_trace()
                for grant in soup.prettify().split("<br/>"):
                    d = {}
                    d["program"] = program_name(fp)
                    d["year"] = year
                    gsoup = BeautifulSoup(grant, "lxml")
                    grantee = gsoup.find("b")
                    if grantee:
                        location_amount = grantee.next_sibling
                        grantee = cleaned(grantee.text)
                        d["grantee"] = grantee
                        lst = list(filter(lambda x: x not in ["", "."],
                                          cleaned(location_amount).split(",")))
                        if lst and bad_money(lst):
                            print(lst)
                        writer.writerow(d)


def split_on_br(tag):
    grants = []
    for br in tag.find_all("br"):
        curr = br
        while curr is not None and curr.name != "br":
            pass


    while curr is not None:
        if curr.name == "br":
            is_head = True
            continue
        else:
            if is_head:
                is_head = False
                grants.append()
            else:
                pass
    return grants


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
