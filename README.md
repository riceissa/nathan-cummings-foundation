This is for https://github.com/vipulnaik/donations

Specific issue: https://github.com/vipulnaik/donations/issues/23

i'm uploading the annual financial statements to google docs (to force OCR) and then copy-pasting each page to a text file, which should make it machine-processable for us

it's strange how google OCRs some pdfs (shows up as the "cached" option) while for others it doesn't (but if you upload to google drive it OCRs anyway)

This is what I mean by google drive: https://www.reddit.com/r/LifeProTips/comments/3umt3e/lpt_google_docs_has_a_very_accurate_free_ocr/

so sometimes the OCR thinks the grantee column is in a column text (like in a two-column paper layout), which means the grantee names are grouped together, and then the amounts are grouped together

whereas I want each line to be grantee, then amount

but if i fix each group on its own and make sure they have the same number of lines, I can actually merge them automatically using visual blocks and virtualedit in vim

# Summary

- 1991–1994: Table format, where each program has a separate page, and each
  page has several tables (for sub-areas of the program). To process, use
  `proc_table.py` or the tab-separated text files. (I haven't decided which is
  better yet.)
- 1995–1996: Paragraph format, where each program has a separate page, and each page
  has `<br>`-separated lines containing grant information. The grantee is in
  bold, the amounts usually show up at the end of the line, etc., so there is
  some regularity. To process, use `proc_list.py`.
- 1997: There is an annual report but no grants list.
- 1998–2000: The foundation [produced no report](https://web.archive.org/web/20100612122340/http://www.nathancummings.org:80/annual/index.html)
  for these years, so nothing to process.
- 2001: https://web.archive.org/web/20050508123155/http://www.nathancummings.net:80/annual/ncf_2001_grantlist.pdf
- 2002–2013: PDF format. Use OCR'd output.
- 2014–2015: ???
- 2016–2017: See http://www.nathancummings.org/what-we-fund/grants
