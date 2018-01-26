#!/usr/bin/env python3

import re
import sys
import csv


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

SOURCE = {
        "data/2002-grants.txt": "http://www.nathancummings.org/sites/default/files/2002_audited_financials.pdf",
        "data/2003-grants.txt": "http://www.nathancummings.org/sites/default/files/2003_audited_financials.pdf",
        "data/2004-grants.txt": "http://www.nathancummings.org/sites/default/files/afs.pdf",
        "data/2005-grants.txt": "http://www.nathancummings.org/sites/default/files/17afs.pdf",
        "data/2006-grants.txt": "http://www.nathancummings.org/sites/default/files/2006_audited_financials.pdf",
        "data/2007-grants.txt": "http://www.nathancummings.org/sites/default/files/2007_audited_financials.pdf",
        "data/2008-grants.txt": "http://www.nathancummings.org/sites/default/files/2008_audited_financials.pdf",
        "data/2009-grants.txt": "http://www.nathancummings.org/sites/default/files/financials123109.pdf",
        "data/2010-grants.txt": "http://www.nathancummings.org/sites/default/files/2010_audited_financials_.pdf",
        "data/2011-grants.txt": "http://www.nathancummings.org/sites/default/files/2011_ncf_audit_final.pdf",
        "data/2012-grants.txt": "http://www.nathancummings.org/sites/default/files/financial_statements_final1.pdf",
        "data/2013-grants.txt": "http://www.nathancummings.org/sites/default/files/2013_audited_financials.pdf",
        "data/2014-grants.txt": "http://www.nathancummings.org/sites/default/files/2014.pdf",
        "data/2015-grants.txt": "http://www.nathancummings.org/sites/default/files/2015.pdf",
        "data/2016-grants.txt": "http://www.nathancummings.org/sites/default/files/fin_stmts_ye_dec._31_20162015.pdf",
        }


def main():
    fieldnames = ["grantee", "grantee_location", "url", "program",
                  "sub_area", "purpose", "year", "notes",
                  "prev_year_eoy_grants_payable", "same_year_awards",
                  "same_year_payments", "same_year_eoy_grants_payable"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)

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
                grant = {
                        "url": SOURCE[fp],
                        "year": int(fp[len("data/"):len("data/YYYY")]),
                        "grantee": grantee,
                        "prev_year_eoy_grants_payable":
                            amount(prev_year_eoy_grants_payable),
                        "same_year_awards":
                            amount(same_year_awards),
                        "same_year_payments":
                            amount(same_year_payments),
                        "same_year_eoy_grants_payable":
                            amount(same_year_eoy_grants_payable),
                        }
                line_num += 1
                writer.writerow(grant)


def is_amount(x):
    if x == "-":
        return True
    m1 = re.match(r"^((\d{1,3},)?\d{1,3},)?\d{1,3}$", x)
    m2 = re.match(r"^\(((\d{1,3},)?\d{1,3},)?\d{1,3}\)$", x)
    if m1 or m2:
        return True
    return False


def amount(x):
    if x == "-":
        return 0
    num = int(x.replace("(", "").replace(")", "").replace(",", ""))
    if "(" in x:
        assert ")" in x, x
        num = -num
    return num


if __name__ == "__main__":
    main()
