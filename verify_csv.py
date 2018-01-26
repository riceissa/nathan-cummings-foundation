#!/usr/bin/env python3

import pandas

import util

def main():
    df = pandas.read_csv("data.csv", names=util.fieldnames)
    print(df.groupby('year')["prev_year_eoy_grants_payable",
                             "same_year_awards",
                             "same_year_payments",
                             "same_year_eoy_grants_payable"].sum())
    print(df.groupby(by=['year', 'program'])["same_year_awards",
                                             "same_year_payments",
                                             "same_year_eoy_grants_payable"]
            .sum())


if __name__ == "__main__":
    main()
