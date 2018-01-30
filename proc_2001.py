#!/usr/bin/env python3

import re
import csv
import sys

import util


def main():
    writer = csv.DictWriter(sys.stdout, fieldnames=util.fieldnames)

    grants = []
    with open("data/2001-grants.txt", "r") as f:
        grant = ""
        for line in f:
            grant += line
            if not line.strip():
                grants.append(grant.strip())
                grant = ""
    for g in map(parsed_grant, grants):
        writer.writerow(g)


def parsed_grant(grant):
    m = re.match(r"([^()]+)\(([^)]+)\)", grant)
    m2 = re.search(r"\$((\d{1,3},)?\d{1,3},)?\d{1,3}$", grant)
    grantee = ""
    location = ""
    duration = ""
    amount = 0
    if m:
        grantee = title_cased(util.cleaned(m.group(1)))
        location = title_cased(util.cleaned(m.group(2)))
        (duration, support_type,
         purpose) = parsed_middle_part(
                        grant[len(m.group(0)):grant.find(". . .")].strip())
    if m2:
        amount = int(m2.group(0).strip().replace("$", "").replace(",", ""))
    return {"year": 2001,
            "grantee": grantee,
            "grantee_location": location,
            "same_year_awards": amount,
            "duration": duration,
            "support_type": support_type,
            "purpose": purpose}


def parsed_middle_part(middle_part):
    duration = ""
    support_type = ""
    purpose = ""

    m_year = re.search(r"\d+[ ](?:year|years|month|months)$", middle_part)
    if m_year:
        duration = util.cleaned(m_year.group(0))
        middle_part = middle_part[:m_year.start(0)]
    m = re.search(r"""(?:(.+)\n)?
                      ((?:To|For|Multi).+)""",
                  middle_part, flags=re.DOTALL|re.VERBOSE|re.MULTILINE)

    if m:
        support_type = util.cleaned(m.group(1))
        purpose = util.cleaned(m.group(2))
    return (duration, support_type, purpose)


def title_cased(s):
    words = []
    blacklist = {"P.E.F.": "",
                 "KCRW": "",
                 "‘AINA": "‘Aina",
                 "CLAL-THE": "CLAL - The",
                 "CEC": "",
                 "MPS": "",
                 "HUC-SKIRBALL": "HUC-Skirball",
                 "SNITOW/KAUFMAN": "Snitow-Kaufman Productions",
                 "US": "",
                 "USA": "",
                 "USACTION": "USAction",
                 "FHS/UNITED": "FHS/United"}
    for word in s.split():
        if word in blacklist:
            if blacklist[word]:
                words.append(blacklist[word])
            else:
                words.append(word)
        elif word.lower() in ["in", "the", "at", "for", "of", "on", "a", "and"]:
            words.append(word.lower())
        else:
            words.append(word[0] + word[1:].lower())
    result = " ".join(words)
    if re.search(r", [A-Z][a-z]$", result):
        # Fix for state codes like "New York, Ny"
        result = result[:-1] + result[-1].upper()
    if result:
        return result[0].upper() + result[1:]
    else:
        return result


if __name__ == "__main__":
    main()
