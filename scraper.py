from bs4 import BeautifulSoup
import requests
import time

subjects_url = "https://www.canterbury.ac.nz/courseinfo/AdvancedSearch.aspx"
sub_url = "https://www.canterbury.ac.nz/courseinfo/GetCourses.aspx?course="
res = requests.get(subjects_url)
soup = BeautifulSoup(res.text, features="html.parser")
codes_id = "ctl00_ContentPlaceHolder1_CourseCodeDropDownList"
names = soup.find(id=codes_id).find_all("option")
names = [a.text for a in names[1:]]

def get_codes(name):
    time.sleep(1) 
    res = requests.get(sub_url+name)
    soup = BeautifulSoup(res.text, features="html.parser")
    table = soup.find(id="GetCourses")
    try:
        print("Scraped", name)
        return [i.text for i in table.select("td.tableTitle > strong > span")]
    except:
        print("Nothing found for ", name)
        return None

def save_codes():
    with open("codes.db", "w+") as f:
        for i in names:
            codes = get_codes(i)
            if codes==None:
                continue
            for g in codes:
                f.write(g+"\n")

