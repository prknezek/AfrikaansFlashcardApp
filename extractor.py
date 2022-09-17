import requests
from bs4 import BeautifulSoup
import pandas as pd

# Goal: Scrub list of Afrikaans words off website to use in Flashcard App
# Step 1: Gathering Data

url = 'https://1000mostcommonwords.com/1000-most-common-afrikaans-words/?_ga=2.35533153.1772808508.1658941687-1576810964.1658941687&_gl=1%2A13lk6zh%2A_ga%2AMTU3NjgxMDk2NC4xNjU4OTQxNjg3%2A_ga_8KVRFXKPM6%2AMTY1ODk0MTY4Ny4xLjEuMTY1ODk0MTY5NC4w'
res = requests.get(url)
html_page = res.content

soup = BeautifulSoup(html_page, 'html.parser')
text = soup.find_all(text=True)


output = ''

# whitelist only words from webpage
whitelist = [
    'td'
]

# adding text to output as a string
for t in text:
    if t.parent.name in whitelist:
        output += '{} '.format(t)

print(output)

# Step 2: writing data to txt file saved in directory

# opening text_file in directory
text_file = open("D:/Python Projects/Afrikaans Flashcard App/word_list.txt", 'w')
# writing output to text_file
text_file.write(output)
text_file.close()
