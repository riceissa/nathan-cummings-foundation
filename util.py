#!/usr/bin/env python3

import re
import bs4
import sys

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


fieldnames = ["year", "program", "sub_area", "grantee", "grantee_location",
              "url", "duration", "support_type", "purpose", "notes",
              "prev_year_eoy_grants_payable", "same_year_awards",
              "same_year_payments", "same_year_eoy_grants_payable"]
