#!/usr/bin/env python3

import re

import util


def main():
    grants = []
    with open("data/2001-grants.txt", "r") as f:
        grant = ""
        for line in f:
            grant += line
            if not line.strip():
                grants.append(grant.strip())
                grant = ""
    for g in map(parsed_grant, grants):
        print(g)


def parsed_grant(grant):
    m = re.match(r"([^()]+)\(([^)]+)\)", grant)
    m2 = re.search(r"\$((\d{1,3},)?\d{1,3},)?\d{1,3}$", grant)
    grantee = ""
    location = ""
    duration = ""
    amount = 0
    if m:
        grantee = util.cleaned(m.group(1))
        location = util.cleaned(m.group(2))
        (duration,) = parsed_middle_part(grant[len(m.group(0)):grant.find(". . .")].strip())
    if m2:
        amount = int(m2.group(0).strip().replace("$", "").replace(",", ""))
    return (grantee, location, amount, notes)


def parsed_middle_part(middle_part):
    m = re.search(r"[ ]\d+[ ](year|years|month|months)$", middle_part)
    if m:
        duration = m.group(0).strip()
        return duration


if __name__ == "__main__":
    main()
