from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
import json
from sys import platform


class Week:
    def __init__(self, week_number):
        self.week_number = int(week_number)
        self.groups = []

    def add_group(self,name, day, start_time, end_time):
        self.groups.append(Group(name, day, start_time, end_time))

    def __repr__(self):
        return f"Week {self.week_number}"


class Group:
    def __init__(self, name, day, start_time, end_time):
        self.name = name
        self.day = day
        self.start_time = float(start_time)
        self.end_time = float(end_time)
        self.lecture = name == "Forelesning"

    def __repr__(self):
        return self.name


def extract_data():
    subject_code = input("What subject would you like to fetch: ").upper()
    url = f"https://tp.uio.no/uib/timeplan/timeplan.php?id={subject_code}&type=course&sem=20v&lang=en"
    options = Options()
    options.add_argument("-headless")
    if platform == "win32":
        driver = webdriver.Firefox(executable_path="dep/geckodriver.exe", options=options)
    elif platform == "linux" or platform == "linux2":
        driver = webdriver.Firefox(executable_path="dep/geckodriver", options=options)
    else:
        assert False, f"Expected platform win32, linux or linux2 not {platform}"
    driver.get(url)
    time.sleep(2)
    results = driver.find_elements_by_class_name("cal_table")
    assert len(results) > 0, f"Found no tables. maybe the subject code is wrong. Subject code given {subject_code}"
    plan = []
    for result in results:
        text = result.text.split('\n')
        assert text[0].split()[0] == "Calendar", f"Language seems to be wrong expected calendar not {text[0].split()[0]}"
        week = Week(text[0].split()[2])
        plan.append(week)
        for string in text:
            if any(day in string for day in ["mon", "tue", "wed", "thu", "fri"]):
                string = string.split()
                if string[-1] == "Forelesning":
                    week.add_group(string[-1], string[0], string[2].replace(":", "."),string[4].replace(":", "."))
                else:
                    week.add_group(string[-2] + " " + string[-1], string[0], string[2].replace(":", "."), string[4].replace(":", "."))
    driver.quit()
    return plan


def write_to_file():
    pass
    # TODO write data to file


def clean_data():
    pass
    # TODO clean data and check for consistency between the weeks


data = extract_data()
print("hello")
