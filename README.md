This is for https://github.com/vipulnaik/donations

Specific issue: https://github.com/vipulnaik/donations/issues/23

i'm uploading the annual financial statements to google docs (to force OCR) and then copy-pasting each page to a text file, which should make it machine-processable for us

it's strange how google OCRs some pdfs (shows up as the "cached" option) while for others it doesn't (but if you upload to google drive it OCRs anyway)

This is what I mean by google drive: https://www.reddit.com/r/LifeProTips/comments/3umt3e/lpt_google_docs_has_a_very_accurate_free_ocr/

so sometimes the OCR thinks the grantee column is in a column text (like in a two-column paper layout), which means the grantee names are grouped together, and then the amounts are grouped together

whereas I want each line to be grantee, then amount

but if i fix each group on its own and make sure they have the same number of lines, I can actually merge them automatically using visual blocks and virtualedit in vim

# Summary

|Year|Format|Source|Script to produce CSV|
|----|------|------|---------------------|
|1991–1994|Table format, where each program has a separate page, and each page has several tables (for sub-areas of the program).|See the annual reports linked from [here](https://web.archive.org/web/20100612122340/http://www.nathancummings.org:80/annual/index.html)|`proc_table.py` or the tab-separated text files (I haven't decided which is better yet)|
|1995–1996|Paragraph format, where each program has a separate page, and each page has `<br>`-separated lines containing grant information *or* grants in separate `<p>` tags. The grantee is in bold, the amounts usually show up at the end of the line, etc., so there is some regularity.|See the annual reports linked from [here](https://web.archive.org/web/20100612122340/http://www.nathancummings.org:80/annual/index.html)|`proc_list.py`|
|1997|There is an annual report but no grants list.|See the [annual report](https://web.archive.org/web/20081118170945/http://www.nathancummings.org/annual97/000056.html)|None|
|1998–2000|The foundation [produced no report](https://web.archive.org/web/20100612122340/http://www.nathancummings.org:80/annual/index.html) for these years, so nothing to process.|None|None|
|2001|Strange PDF|[Source](https://web.archive.org/web/20050508123155/http://www.nathancummings.net:80/annual/ncf_2001_grantlist.pdf)||
|2002–2016|PDF format. We use an OCR version (produced by Google Docs or Google search cache) and process that instead.|[2002–2013](http://www.nathancummings.org/news-and-reports/annual-reports/List); [2014–2016](http://www.nathancummings.org/about-the-foundation/Financial-Statments)|`proc_text.py`|
|2017|Strange PDF. Might be best to wait until the financial report comes out.|[Source](http://www.nathancummings.org/what-we-fund/grants)||
