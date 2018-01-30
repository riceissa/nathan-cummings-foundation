#!/usr/bin/env python3

import csv

import util


def main():
    with open("all_data.csv", "r") as f:
        reader = csv.DictReader(f, fieldnames=util.fieldnames)

        first = True
        print("""insert into donations (donor, donee, amount, donation_date,
        donation_date_precision, donation_date_basis, cause_area, url,
        donor_cause_area_url, notes, affected_countries, affected_states,
        affected_cities, affected_regions) values""")

        for row in reader:
            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Nathan Cummings Foundation"),  # donor
                mysql_quote(row['grantee']),  # donee
                row['same_year_awards'],  # amount
                mysql_quote(row['year'] + "-01-01"),  # donation_date
                mysql_quote("year"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(row['program'] + ("/" + row['sub_area'] if row['sub_area'] else "")),  # cause_area
                mysql_quote(row['url']),  # url
                mysql_quote(""),  # donor_cause_area_url
                mysql_quote("; ".join(filter(bool,
                                             [row['purpose'],
                                              row['notes'],
                                              row['duration']]))),  # notes
                mysql_quote(""),  # affected_countries
                mysql_quote(""),  # affected_states
                mysql_quote(""),  # affected_cities
                mysql_quote(""),  # affected_regions
            ]) + ")")
            first = False
        print(";")


def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


if __name__ == "__main__":
    main()
