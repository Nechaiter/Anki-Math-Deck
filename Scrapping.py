from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Firefox instance
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)
# driver.minimize_window()
import json
import os

class Course:
    def __init__(self, courseName, link, units):
        self.courseName = courseName
        self.link = link
        self.units = units

    def to_dict(self):
        return {'courseName': self.courseName, 'link': self.link, 'units': self.units}

class Unit:
    def __init__(self, unitName, link, exercises):
        self.unitName = unitName
        self.link = link
        self.exercises = exercises

    def to_dict(self):
        return {'unitName': self.unitName, 'link': self.link, 'exercises': self.exercises}

class Exercise:
    def __init__(self, exerciseName, link):
        self.exerciseName = exerciseName
        self.link = link

    def to_dict(self):
        return {'exerciseName': self.exerciseName, 'link': self.link}
    
    
url="https://www.khanacademy.org/math"
driver.get(url)
time.sleep(1)

# Accepts cookies popup
driver.find_element(By.CSS_SELECTOR,"[id='onetrust-accept-btn-handler']").click()

# findElement('data-testid','identifier-field').send_keys(usermail)
# findElement('data-testid','password-field').send_keys(password)
# findElement('data-testid','log-in-submit-button').click()
# time.sleep(3)

import Courses_list
courses = [None] * len(Courses_list.Other)

# Find courses names and links
courses_html_elements=driver.find_elements(By.CSS_SELECTOR,"._t2uf76")

def specialCharacterParser(name):
    return name.replace(':', '').replace('/', '').replace('\\', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('𝘶', 'u').replace('®︎','').replace('®','')

## Extract the course name and link to iterate through their units
for course_element in courses_html_elements:
    course_title_element = course_element.find_element(By.TAG_NAME, value='a')
    try:
        course_name = specialCharacterParser(course_title_element.text)
        value_index = Courses_list.Other.index(course_name)
    except ValueError:
        value_index = -1

    if value_index != -1:
        courses[value_index] = Course(course_name, course_title_element.get_attribute('href'), []).to_dict()

print(courses)

def obtain_units(timeout=1):
    selectors = [
        "[data-testid='mastery-practice-content-item']",
        "._168icmv"
    ]
    selectors_count = 0
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._duavrzj")))
    exercise_html_element = []
    for selector in selectors:
        try:
            # exercise_html_element = exercise_html_element + driver.find_elements(By.CSS_SELECTOR, selector)
            if selector == "[data-testid='mastery-practice-content-item']":
                # ._xu2jcg
                mastery_elements = WebDriverWait(driver, timeout).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
                for mastery_element in mastery_elements:
                    found = mastery_element.find_elements(By.CSS_SELECTOR, "._xu2jcg")
                    exercise_html_element += found
            else:
                exercise_html_element = exercise_html_element + WebDriverWait(driver, timeout).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
        except:
            print(selector, "not found")
            selectors_count += 1
        if selectors_count == len(selectors):
            print("\033[91mWARNING\033[0m")
            print("\033[91mNo exercises of any type were found. Please check if there are new ones using unspecified selectors.\033[0m")
    return exercise_html_element


## Extract the units and append them to their specific course
for course in courses:
    url = course["link"]
    driver.get(url)
    time.sleep(3)

    # Wait for unit cards to appear
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._c53vsu1")))

    # Unit title elements
    units_html_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='unit-header']")
    units = []

    # Save the unit name and their corresponding link to iterate through them
    for unit_title_element in units_html_elements:
        units.append(Unit(unit_title_element.text, unit_title_element.get_attribute('href'), []).to_dict())

    # Save the exercises and again, iterate through them
    for unit in units:
        url = unit["link"]
        driver.get(url)
        time.sleep(3)
        print(unit["unitName"])
        # Save all the HTML exercises found in a list
        exercises_html_elements = obtain_units()

        # Save all the exercise classes in a list
        exercises = []
        for exercise_element in exercises_html_elements:
            exercise_element_data = exercise_element.find_element(By.CSS_SELECTOR, '._dwmetq')
            link = exercise_element_data.get_attribute('href')
            exercise_name = exercise_element_data.find_element(By.TAG_NAME, value='span').text
            exercises.append(Exercise(exercise_name, link).to_dict())

        unit["exercises"] = exercises

    course["units"] = units

data = {'courses': courses}

filename="main_courses.json"
path=os.path.join(os.getcwd()+"/json_files",filename)
with open(path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)



