import hashlib
import re

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def voyager_date():
    url = "https://science.nasa.gov/mission/voyager/voyager-1/"
    src = requests.get(url).text
    soup = BeautifulSoup(src, "lxml")
    table = soup.find("table")
    for tr in table.find_all("tr"):
        tds = tr.find_all("td")
        key = tds[0].get_text()
        val = tds[1].get_text()
        if "Launch Date and Time" in key:
            raw_date = val
            break
    raw_date = raw_date.replace("Sept", "Sep")
    dt = datetime.strptime(raw_date, "%b. %d, %Y / %H:%M:%S UT")
    date = dt.strftime("%Y%m%d")
    return date

def rfc1149_date():
    url = "https://datatracker.ietf.org/doc/html/rfc1149"
    src = requests.get(url).text
    soup = BeautifulSoup(src, "lxml")

    pre = soup.find("pre").text
    maybe_dates = re.findall(r"\b\d{1,2}\s+[a-zA-Z]+\s+\d{4}\b", pre)
    for maybe_date in maybe_dates:
        try:
            dt = datetime.strptime(maybe_date, "%d %B %Y")
            date = dt.strftime("%Y%m%d")
            break
        except:
            continue

    return date if date else None

def brain_codepoint():
    url = "https://unicode-org.github.io/emoji/emoji/charts-17.0/emoji-list.html"
    src = requests.get(url).text
    soup = BeautifulSoup(src, "lxml")
    brain = soup.find("img", {"alt": "🧠"})
    tr = brain.find_parent("tr")
    code = tr.find("td", class_="code").get_text()
    return code.replace("U+", "")

def btc_genesis_date():
    url = "https://raw.githubusercontent.com/https://raw.githubusercontent.com/bitcoin/bitcoin/master/src/kernel/chainparams.cpp"
    src = requests.get(url).text

    match = re.search(r'CBlock\(.*nTime=(\d+),', src)
    dt = datetime.fromtimestamp(int(match.group(1)))
    return dt.strftime("%Y%m%d")

def kr2_isbn10():
    url = "https://www.cs.princeton.edu/~bwk/cbook.html"
    src = requests.get(url).text
    soup = BeautifulSoup(src, "lxml")
    brs = soup.find_all("br")
    for br in brs:
        maybe_isbn = br.next_sibling
        if "ISBN" in maybe_isbn:
            isbns = re.findall(r"\b\d-\d{2}-\d{6}-\d\b", maybe_isbn)
            return isbns[0].replace("-", "")



voyager_date = voyager_date()
print(voyager_date)
rfc1149_date = rfc1149_date()
print(rfc1149_date)
brain_codepoint = brain_codepoint()
print(brain_codepoint)
btc_genesis_date = btc_genesis_date()
print(btc_genesis_date)
kr2_isbn10 = kr2_isbn10()
print(kr2_isbn10)

flag = f"FLAG{{{voyager_date}-{rfc1149_date}-{brain_codepoint}-{btc_genesis_date}-{kr2_isbn10}}}"

print(hashlib.sha256(flag.encode("utf-8")).hexdigest())