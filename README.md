This is for https://github.com/vipulnaik/donations

Specific issue: https://github.com/vipulnaik/donations/issues/23

i'm uploading the annual financial statements to google docs (to force OCR) and then copy-pasting each page to a text file, which should make it machine-processable for us

it's strange how google OCRs some pdfs (shows up as the "cached" option) while for others it doesn't (but if you upload to google drive it OCRs anyway)

This is what I mean by google drive: https://www.reddit.com/r/LifeProTips/comments/3umt3e/lpt_google_docs_has_a_very_accurate_free_ocr/

so sometimes the OCR thinks the grantee column is in a column text (like in a two-column paper layout), which means the grantee names are grouped together, and then the amounts are grouped together

whereas I want each line to be grantee, then amount

but if i fix each group on its own and make sure they have the same number of lines, I can actually merge them automatically using visual blocks and virtualedit in vim
