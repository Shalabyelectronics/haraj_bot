import os
import shutil
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager

Download_path = r"C:\Users\dalla\.wdm\drivers\chromedriver\win32"
CHROME_DRIVER = os.environ.get("CHROMEDRIVER")
HARAJ_USER_NAME = os.environ.get("HARAJ_USER_NAME")
HARAJ_PASSWORD = os.environ.get("HARAJ_PASSWORD")
HARAJ_WEBSITE = r"https://haraj.com.sa/"


def check_web_driver():
    try:
        Service(executable_path=CHROME_DRIVER)
    except Exception as r:
        print(r)
        CHROM_VERSION = ChromeDriverManager().driver.get_version()
        Service(executable_path=ChromeDriverManager().install())
        shutil.move(os.path.join(Download_path, CHROM_VERSION, "chromedriver.exe"), r"C:\WebDriver\bin")

    return webdriver.Chrome()


def haraj_login(any_driver):
    any_driver.implicitly_wait(5)
    any_driver.find_element(By.XPATH, '//*[@data-icon="sign-in-alt"]').click()
    WebDriverWait(any_driver, 10).until(ec.visibility_of_element_located((By.NAME, "user")))
    time.sleep(1)
    user_name = any_driver.find_element(By.NAME, "user")
    user_name.send_keys(HARAJ_USER_NAME)
    time.sleep(1)
    password = any_driver.find_element(By.NAME, "pass")
    password.send_keys(HARAJ_PASSWORD)
    time.sleep(2)
    submit = any_driver.find_element(By.XPATH, '//*[text()="دخــــول"]')
    submit.click()


def car_search_setting(any_driver):
    time.sleep(1)
    WebDriverWait(any_driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@alt="car"]')))
    select_cars_section = any_driver.find_element(By.XPATH, '//*[@alt="car"]')
    select_cars_section.click()
    time.sleep(1)
    cars_brands = any_driver.find_elements(By.XPATH, '/html/body/div/div/div[3]/div[2]/div[2]/div[1]/div[1]/ul/li')
    all_cars_brands = {}
    for i, car in enumerate(cars_brands, start=1):
        print(i, car.text)
        all_cars_brands.update({i: car})
    chose_car_brand = int(input("أختر العلامة التجارية للسيارة : "))
    chosen_brand = all_cars_brands[chose_car_brand]
    chosen_brand.click()
    cars_models = any_driver.find_elements(By.XPATH, '/html/body/div/div/div[3]/div[2]/div[2]/div[1]/div[2]/ul/li')
    all_cars_models = {}
    for i, model in enumerate(cars_models, start=1):
        print(i, model.text)
        all_cars_models.update({i: model})
    chose_car_model = int(input("أختر الموديل من هذه العلامة التجارية : "))
    chosen_model = all_cars_models[chose_car_model]
    chosen_model.click()
    time.sleep(1)
    click_on_city = any_driver.find_element(By.XPATH, '//*[text()="كل المناطق"]')
    click_on_city.click()
    locations_available = any_driver.find_elements(By.XPATH,
                                                   '/html/body/div/div/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/ul/li')
    locations_available.pop(0)
    all_locations_available = {}
    for i, location in enumerate(locations_available, start=1):
        print(i, location.text)
        all_locations_available.update({i: location})
    chosen_location = int(input(" أختر منطقة البحث : "))
    user_chosen_location = all_locations_available[chosen_location]
    time.sleep(1)
    user_chosen_location.click()


def save_search_results(any_driver):
    time.sleep(1)
    all_results = any_driver.find_elements(By.XPATH, '//*[@class="postlist"]/div')
    results_data = {}
    if len(all_results) > 1:
        all_results.pop(0)
        test = 0
        for index, _ in enumerate(all_results, start=2):
            any_driver.find_element(By.XPATH, f'//*[@class="postlist"]/div[{index}]/div/div/a').click()
            time.sleep(1.5)
            result_page = any_driver.current_url
            r = requests.get(result_page)
            if r.status_code == 200:
                page_date = r.text
                soup = BeautifulSoup(page_date, "html.parser")
                result_title = soup.find(name="h1")
                result_post_time = soup.find(id="post_time")
                phone_number = any_driver.find_element(By.CLASS_NAME, 'contact')
                result_key = index - 1
                result_data = {result_key: {}}
                result_data[result_key].update({"result_title": result_title.string,
                                                 "result_post_time": result_post_time.string,
                                                 "phone_number": phone_number.text,
                                                 "result_page": result_page})
                results_data.update(result_data)
                time.sleep(1.5)
                any_driver.back()
                time.sleep(1.5)
                if test > 2:
                    break
                test += 1
    return results_data


def data_entry_results(any_driver, results_data):
    time.sleep(1)
    any_driver.execute_script("window.open('https://forms.gle/DAwNoFno27J7ey1v9','new window')")
    any_driver.switch_to.window(any_driver.window_handles[1])
    time.sleep(3)
    for key in list(results_data.keys()):
        data_title_input = any_driver.find_element(By.XPATH,
                                                   '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        data_post_time_input = any_driver.find_element(By.XPATH,
                                                       '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        data_phone_number_input = any_driver.find_element(By.XPATH,
                                                          '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        data_link_input = any_driver.find_element(By.XPATH,
                                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
        result_title = results_data[key]["result_title"]
        result_post_time = results_data[key]["result_post_time"]
        phone_number = results_data[key]["phone_number"]
        result_page = results_data[key]["result_page"]
        time.sleep(2)
        data_title_input.send_keys(result_title)
        time.sleep(0.5)
        data_post_time_input.send_keys(result_post_time)
        time.sleep(0.5)
        data_phone_number_input.send_keys(phone_number)
        time.sleep(0.5)
        data_link_input.send_keys(result_page + Keys.TAB + Keys.ENTER)
        time.sleep(0.5)
        any_driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()


if __name__ == '__main__':
    driver = check_web_driver()
    driver.get(HARAJ_WEBSITE)
    haraj_login(driver)
    car_search_setting(driver)
    data = save_search_results(driver)
    data_entry_results(driver, data)
    time.sleep(5)
