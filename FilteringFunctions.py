
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import hashlib 


def get_exercise_content(driver):
    try:
        time.sleep(3)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'exercise-chrome-content-for-mobile-zoom'))
        )
        title = driver.find_element(By.CSS_SELECTOR, '[data-testid="content-library-content-title"]').text
        options = driver.find_elements(By.CSS_SELECTOR, 'li.perseus-radio-option')
        
        if options:
            option_texts = []
            for opt in options:

                try:
                    letter_elem = opt.find_element(By.CSS_SELECTOR, 'button ._177sg8x span')
                    letter = letter_elem.text.strip()
                except Exception:
                    letter = ""
                try:
                    mathjax_elem = opt.find_element(By.CSS_SELECTOR, 'button .mathjax-wrapper mjx-assistive-mml')
                    mathjax = mathjax_elem.get_attribute("innerHTML").strip()
                except Exception:
                    mathjax = ""
                try:
                    paragraph_elem = opt.find_element(By.CSS_SELECTOR, 'button .perseus-renderer .paragraph')
                    paragraph_text = paragraph_elem.text.strip()
                    if mathjax:
                        paragraph_text = paragraph_text.replace(mathjax, "").strip()
                except Exception:
                    paragraph_text = ""

                option_texts.append("|" + mathjax + "|" + paragraph_text)
            option_texts.sort()
            unique_content = title + '||' + '||'.join(option_texts)
        else:
            problem_text = ""
            mathjax_contents = []
            try:
                problem_elem = driver.find_element(By.CSS_SELECTOR, '.perseus-renderer')
                problem_text = problem_elem.text.strip()
                mathjax_elems = problem_elem.find_elements(By.CSS_SELECTOR, 'mjx-assistive-mml')
                for mjx in mathjax_elems:
                    mathjax_contents.append(mjx.get_attribute("innerHTML").strip())
            except Exception:
                pass
            unique_content = title + '||' + problem_text + '||' + '||'.join(mathjax_contents)
    except Exception:
        unique_content = ""
    return unique_content





def filter_duplicates(courses):
    seen_names = set()
    seen_hashes = set()
    name_to_exercise = {}

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    
    for course in courses:
        for unit in course.get("units", []):
            filtered_exercises = []

            for exercise in unit.get("exercises", []):
                name = exercise.get("exerciseName", "")
                if name not in seen_names:
                    seen_names.add(name)
                    filtered_exercises.append(exercise)
                    name_to_exercise[name] = exercise
                else:
                    # If the name has been seen before
                    driver.get(exercise["link"])
                    content = get_exercise_content(driver)
                    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                    print(name_to_exercise[name])
                    if "hash" not in name_to_exercise[name]:
                        driver.get(name_to_exercise[name]["link"])
                        original_content = get_exercise_content(driver)
                        original_hash = hashlib.md5(original_content.encode('utf-8')).hexdigest()
                        name_to_exercise[name]["hash"] = original_hash
                        seen_hashes.add(original_hash)

                    if content_hash != name_to_exercise[name]["hash"] and content_hash not in seen_hashes:
                        seen_hashes.add(content_hash)
                        filtered_exercises.append(exercise)

                    print(name_to_exercise[name])

            unit["exercises"] = filtered_exercises
    driver.quit()
    return courses




def filter_duplicates_both(main_courses, side_courses):
    seen_names = set()
    seen_hashes = set()
    name_to_exercise = {}

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)

    for course in main_courses + side_courses:
        for unit in course.get("units", []):
            filtered_exercises = []

            for exercise in unit.get("exercises", []):
                name = exercise.get("exerciseName", "")
                if name not in seen_names:
                    seen_names.add(name)
                    filtered_exercises.append(exercise)
                    name_to_exercise[name] = exercise
                else:
                    # If the name has been seen before
                    driver.get(exercise["link"])
                    content = get_exercise_content(driver)
                    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                    print(name_to_exercise[name])
                    if "hash" not in name_to_exercise[name]:
                        driver.get(name_to_exercise[name]["link"])
                        original_content = get_exercise_content(driver)
                        original_hash = hashlib.md5(original_content.encode('utf-8')).hexdigest()
                        name_to_exercise[name]["hash"] = original_hash
                        seen_hashes.add(original_hash)

                    if content_hash != name_to_exercise[name]["hash"] and content_hash not in seen_hashes:
                        
                        seen_hashes.add(content_hash)
                        filtered_exercises.append(exercise)        

                    print(name_to_exercise[name])

            unit["exercises"] = filtered_exercises
    driver.quit()
    return main_courses, side_courses