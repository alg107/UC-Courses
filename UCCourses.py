from bs4 import BeautifulSoup
import requests
import datetime
import random
from termcolor import colored

## TODO:
##   - Sift through or at least label labs tutorials etc.

# Constants

descr_id = "ctl00_ContentPlaceHolder1_CourseOccurrenceDescriptionLabel"
code_id = "ctl00_ContentPlaceHolder1_CourseCodeLabel"
title_id = "ctl00_ContentPlaceHolder1_CourseOccurrenceTitleLabel"
cred_id = "ctl00_ContentPlaceHolder1_PointsAndEftsLabel"
sem_id = "ctl00_ContentPlaceHolder1_SemesterLabel"

# Setup

class Course:
    def __init__(self, title, code, description, sess_list, credits, sem):
        self.title = title
        self.code = code
        self.description = description
        self.sess_list = sess_list
        self.credits = credits
        self.sem = sem

    def __str__(self):
        return self.code + " - " + self.title

class Session:
    def __init__(self, day, start, end, loc, type_):
        self.day = day
        self.start = start
        self.end = end
        self.loc = loc
        self.type_ = type_

    def __str__(self):
        return self.day + ": " + str(self.start) + "-" + str(self.end)



url_skel = "https://www.canterbury.ac.nz/courseinfo/GetCourseDetails.aspx?course="

#print(soup.prettify())


def text_from_id(soup, ID):
    return soup.find(id=ID).string

def process_time(time):
    time = time.split(" - ")
    starth, startm = time[0].split(":")
    endh, endm = time[1].split(":")
    start = datetime.time(int(starth), int(startm))
    end = datetime.time(int(endh), int(endm))
    return (start, end)

def extract_sessions(block):
    sess_list = []
    for sess in block:
        type_ = None 
        day = sess.select('td[data-title="Day"]')[0].text
        time = sess.select('td[data-title="Time"]')[0].text
        start, end = process_time(time)
        loc = sess.select('td[data-title="Location"]')[0].text
        sess_c = Session(day, start, end, loc, type_)
        sess_list.append(sess_c)
    return sess_list
        

def parse_html(soup):
    description = text_from_id(soup,descr_id)
    code = text_from_id(soup, code_id)
    title = text_from_id(soup, title_id)

    sessblock = soup.find(id="RepeatTable")
    sesslabels = [a.contents for a in sessblock.find_all("strong")]
    sessions = sessblock.find_all("tr", class_="datarow")
    sess_list = extract_sessions(sessions)

    credits =  soup.find(id=cred_id).contents[0].split(" ")[0]
    credits = int(credits)

    sem = text_from_id(soup, sem_id)

    c = Course(title, code, description, sess_list, credits, sem)
    return c

def process_course(course):
    url = url_skel + course
    res = requests.get(url)
    html_doc = res.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    return parse_html(soup)

def process_course_list(lst):
    course_list = []
    for course in lst:
       try:
           c = process_course(course)
           course_list.append(c)
       except:
           pass
    return course_list

def timesort(t):
    return t[1].start.hour

def gen_timetable(c_list):
    timetable = {
        "Monday":[],
        "Tuesday":[],
        "Wednesday":[],
        "Thursday":[],
        "Friday":[],
        }
    for c in c_list:
        for sess in c.sess_list:
            timetable[sess.day].append((c, sess))
    
    for i in timetable:
        timetable[i] = sorted(timetable[i], key=timesort)
    return timetable

colours = [
        "grey",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
        ]
def timetable_rep(timetable, leg):
    cols = colours
    codecols = {}
    codes = set()
    for day in timetable:
        for i in timetable[day]:
            codes.add(i[0].code)
    for code in codes:
        #random.seed(code)
        col = random.choice(cols)
        codecols[code] = col
        cols.remove(col)

    on = "###"
    off = "---"

    modif = str(datetime.datetime.now())

    print("   Mon Tue Wed Thu Fri")
    for hour in range(8,19):
        spacer = ""
        if hour < 10:
            spacer = "  "
        else:
            spacer = " "
        print(hour, end=spacer)
        for i in timetable:
            filler = off
            for a in timetable[i]:
                if a[1].start.hour == hour:
                    #random.seed(a[0].code+modif)
                    #colour = random.choice(colours)
                    filler = colored(on, codecols[a[0].code])
            print(filler, end=" ")
        print('\n', end="")

    if leg:
        print("\nLegend:\n")
        for code in codes:
            print(code, end=" - ")
            print(colored(on, codecols[code]))
