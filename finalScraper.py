from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# Service account json path
SERVICE_ACCOUNT_FILE = ''

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# ID of your spreadsheet
SPREADSHEET_ID = ''

try:
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
except HttpError as err:
    print(err)
rangeAll = '{0}!A1:Z'.format("test2")
body = {}
resultClear = service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=rangeAll,
                                                    body=body).execute()

driver = webdriver.Chrome()
delay = 20
counter = 0

driver.get('https://components.ifsc-climbing.org/results/')
time.sleep(2)

years = Select(WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "years"))))
for i in range(0, len(years.options)):
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "years")))
    try:
        years.select_by_index(i)
        time.sleep(0.3)
        indexes = Select(WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "indexes"))))
    except:
        continue
    if len(indexes.options) == 1:
        continue
    for y in range(1, len(indexes.options)):
        try:
            indexes.select_by_index(y)
            time.sleep(0.3)
            events = Select(WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "events"))))
        except:
            continue
        if len(events.options) == 1:
            continue
        for z in range(1, len(events.options)):
            try:
                events.select_by_index(z)
                time.sleep(0.3)
                categories = Select(WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "categories"))))
            except:
                continue
            if len(categories.options) == 1:
                continue
            for x in range(1, len(categories.options)):
                try:
                    categories.select_by_index(x)
                    time.sleep(0.3)
                except:
                    continue
                try:
                    table = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "table_id")))
                except:
                    print('table load fail!')
                    continue
                for row in table.find_elements(By.CSS_SELECTOR, "tr"):
                    try:
                        if (row.find_element(By.CLASS_NAME, "nation").text == "SRB"):
                            result =[]
                            cellRes = []
                            counter += 1
                            for cell in row.find_elements(By.CSS_SELECTOR, "td"):
                                cellRes.append(cell.text)
                            result.append(cellRes)
                            request = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                                            range=f"test2!A{counter}", 
                                                            valueInputOption="USER_ENTERED", 
                                                            body={"values":result}).execute()
                            print(result)   
                    except:
                        pass
time.sleep(2)
driver.quit()
