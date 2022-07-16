from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
delay = 10

driver.get('https://components.ifsc-climbing.org/results/')
time.sleep(2)
years = Select(WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "years"))))
time.sleep(1)
for year in years.options:
    year.click()
    indexes = Select(WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "indexes"))))
    time.sleep(0.5)
    for index in indexes.options:
        index.click()
        events = Select(WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "events"))))
        time.sleep(0.5)
        for i in range(1, len(events.options)):
            events.select_by_index(i)
            event = events.first_selected_option
            event.click()
            categories = Select(WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "categories"))))
            time.sleep(0.3)
            for i in range(1, len(categories.options)):
                categories.select_by_index(i)
                cat = categories.first_selected_option
                time.sleep(0.3)
                try:
                    # if cat.text == "Select category":
                    #     continue
                    cat.click()
                except:
                    pass
                #WebDriverWait(driver, delay).until(EC.staleness_of(cat), message = "waiting")
                #WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'table_id')))
                try:
                    #time.sleep(0.3)
                    table = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "table_id")))
                    #time.sleep(0.1)
                except:
                    continue
                    #time.sleep(0.3)
                for row in table.find_elements(By.CSS_SELECTOR, "tr"):
                    try:
                    #if(row.find_element(By.CLASS_NAME, "odd") or row.find_element(By.CLASS_NAME, "even")):
                        if (row.find_element(By.CLASS_NAME, "nation").text == "SRB"):
                            for cell in row.find_elements(By.CSS_SELECTOR, "td"):
                                print(cell.text)
                            print('------------------------')   
                        #time.sleep(0.1)
                    #else:
                    #    continue
                    except:
                        pass
time.sleep(0)
driver.quit()