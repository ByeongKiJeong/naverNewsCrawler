origin https://github.com/jangsoopark/naverNewsCrawler
mdf by byeongkijeong(jbk958@gmail.com)

How to Use

prerequisite BeautifulSoap4 -> pip install bs4

in console
python navernews.py <start date> <end date> <mode>

ex) python navernews.py 20150101 20151231 0

mode : 0(in data folder, date first), 1(in each folder, section first), 2(in each folder, date first)

output : formatted json with 5 factors(title, date, time, contents, journal)

