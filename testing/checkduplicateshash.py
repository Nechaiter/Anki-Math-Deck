import hashlib
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import FilteringFunctions

input_file = "others/MBND_duplicates.txt"

## Extract all links from the file
links = []
i = 0
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith("https://"):
            i += 1
            if current_title:
                links.append((current_title, line))
        else:
            current_title = line

from collections import defaultdict

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)
hash_dict = defaultdict(list)
j=0
for name, link in links:
    j=j+1
    driver.get(link)
    content = FilteringFunctions.get_exercise_content(driver)
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    hash_dict[name].append(content_hash)
    print(j," of ", i)
driver.quit()

for name in hash_dict:
    print(name)
    for h in hash_dict[name]:
        print(h)