#!/usr/bin/env python3

import pdb

import re
import csv
import sys
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


SOURCE = {
    "data/1991-arts.html": "https://web.archive.org/web/20050508003333/http://nathancummings.org:80/annual91/000196.html",
    "data/1991-community.html": "https://web.archive.org/web/20081201112446/http://www.nathancummings.org/annual91/000206.html",
    "data/1991-environment.html": "https://web.archive.org/web/20081201112446/http://www.nathancummings.org/annual91/000198.html",
    "data/1991-health.html": "https://web.archive.org/web/20081201112446/http://www.nathancummings.org/annual91/000200.html",
    "data/1991-interprogram.html": "https://web.archive.org/web/20081201112446/http://www.nathancummings.org/annual91/000204.html",
    "data/1991-jewishlife.html": "https://web.archive.org/web/20081201112446/http://www.nathancummings.org/annual91/000202.html",
    "data/1992-arts.html": "https://web.archive.org/web/20081118174121/http://www.nathancummings.org/annual92/000179.html",
    "data/1992-community.html": "https://web.archive.org/web/20081118174121/http://www.nathancummings.org/annual92/000186.html",
    "data/1992-environment.html": "https://web.archive.org/web/20081118174121/http://www.nathancummings.org/annual92/000178.html",
    "data/1992-health.html": "https://web.archive.org/web/20081118174121/http://www.nathancummings.org/annual92/000181.html",
    "data/1992-interprogram.html": "https://web.archive.org/web/20081118174121/http://www.nathancummings.org/annual92/000185.html",
    "data/1992-jewishlife.html": "https://web.archive.org/web/20081118174121/http://www.nathancummings.org/annual92/000183.html",
    "data/1992-presidential.html": "https://web.archive.org/web/20081118174121/http://www.nathancummings.org/annual92/000187.html",
    "data/1992-prior.html": "https://web.archive.org/web/20081118174121/http://www.nathancummings.org/annual92/000189.html",
    "data/1992-researchdevelopmentevaluation.html": "https://web.archive.org/web/20081118174121/http://www.nathancummings.org/annual92/000188.html",
    "data/1993-arts.html": "https://web.archive.org/web/20081201105713/http://www.nathancummings.net/annual93/000159.html",
    "data/1993-community.html": "https://web.archive.org/web/20081201105713/http://www.nathancummings.net/annual93/000169.html",
    "data/1993-environment.html": "https://web.archive.org/web/20081201105713/http://www.nathancummings.net/annual93/000161.html",
    "data/1993-health.html": "https://web.archive.org/web/20081201105713/http://www.nathancummings.net/annual93/000163.html",
    "data/1993-interprogram.html": "https://web.archive.org/web/20081201105713/http://www.nathancummings.net/annual93/000167.html",
    "data/1993-jewishlife.html": "https://web.archive.org/web/20081201105713/http://www.nathancummings.net/annual93/000165.html",
    "data/1993-presidential.html": "https://web.archive.org/web/20081201105713/http://www.nathancummings.net/annual93/000170.html",
    "data/1993-researchdevelopmentevaluation.html": "https://web.archive.org/web/20081201105713/http://www.nathancummings.net/annual93/000171.html",
    "data/1994-arts.html": "https://web.archive.org/web/20081201100814/http://www.nathancummings.org/annual94/000142.html",
    "data/1994-community.html": "https://web.archive.org/web/20081201100814/http://www.nathancummings.org/annual94/000150.html",
    "data/1994-environment.html": "https://web.archive.org/web/20081201100814/http://www.nathancummings.org/annual94/000144.html",
    "data/1994-health.html": "https://web.archive.org/web/20081201100814/http://www.nathancummings.org/annual94/000146.html",
    "data/1994-interprogram.html": "https://web.archive.org/web/20081201100814/http://www.nathancummings.org/annual94/000149.html",
    "data/1994-jewishlife.html": "https://web.archive.org/web/20081201100814/http://www.nathancummings.org/annual94/000148.html",
    "data/1994-presidential.html": "https://web.archive.org/web/20081201100814/http://www.nathancummings.org/annual94/000151.html",
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
            for table in soup.find_all("table"):
                trs = table.find_all("tr")
                try:
                    num_col = len(trs[1].find_all("td"))
                except IndexError:
                    # This is a table with just one row, so skip it
                    continue
                if year in [1991, 1992] and num_col != 5:
                    # These two years have five columns
                    continue
                if year in [1993, 1994] and num_col != 4:
                    # These two years have four columns
                    continue
                label = sub_area(table)
                for tr in trs:
                    d = {}
                    d["url"] = SOURCE[fp]
                    d["program"] = program_name(fp)
                    d["year"] = year
                    d["sub_area"] = label

                    cols = tr.find_all("td")
                    # pdb.set_trace()
                    try:
                        d["grantee_location"] = cleaned(cols[0].i.extract().text)
                    except:
                        pass
                    d["grantee"] = cleaned(cols[0].text)
                    d["purpose"] = cleaned(cols[1].text)
                    if year in [1991, 1992]:
                        d["same_year_awards"] = (cleaned(cols[2].text)
                                                 .replace(",", "")
                                                 .replace(",", ""))
                        d["same_year_payments"] = (cleaned(cols[3].text)
                                                   .replace(",", "")
                                                   .replace(",", ""))
                        d["same_year_eoy_grants_payable"] = (cleaned(cols[4].text)
                                                             .replace(",", "")
                                                             .replace(",", ""))
                    if year in [1993, 1994]:
                        d["same_year_awards"] = (cleaned(cols[2].text)
                                                 .replace(",", "")
                                                 .replace("$", ""))
                        d["same_year_payments"] = (cleaned(cols[3].text)
                                                   .replace(",", "")
                                                   .replace("$", ""))
                    writer.writerow(d)


def sub_area(table):
    """Find the sub-area of the grant. These are given right above the table in
    bold."""
    tag = table.previous_sibling
    while tag is not None and tag.find("b") in [None, -1]:
        tag = tag.previous_sibling
    if tag:
        return cleaned(tag.find("b").text)
    return ""


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


if __name__ == "__main__":
    main()
