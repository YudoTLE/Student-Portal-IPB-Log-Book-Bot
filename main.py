import pandas as pd
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configuration
with open('config.json', 'r') as f:
    config = json.load(f)

EXCEL_FILE = config['EXCEL_FILE']
SHEET_NAME = config['SHEET_NAME']
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']


# Load excel file
df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

N = len(df)
M = len(df.columns)


# Load data
SCHEMA    = ['date' , 'time_start', 'time_end', 'activity', 'lecturer', 'mentoring', 'location', 'description', 'proof']

all_data = [{} for _ in range(N)]

fields = [None] * M
for i in range(M):
    for schema in SCHEMA:
        if f'#{ schema }' in str(df.columns[i]):
            fields[i] = schema

            break

for i in range(N):
    for j in range(M):
        if not fields[j]:
            continue
        if not df.iloc[i, j]:
            continue

        all_data[i][fields[j]] = str(df.iloc[i, j])


# Input data to Student Portal using selenium
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)

def get_element(by, value, timeout=10):
    wait = WebDriverWait(driver, timeout=timeout)
    wait.until(EC.presence_of_element_located((by, value)))

    return driver.find_element(by, value)

def get_elements(by, value, timeout=10):
    wait = WebDriverWait(driver, timeout=timeout)
    wait.until(EC.presence_of_all_elements_located((by, value)))

    return driver.find_elements(by, value)

driver.get('https://studentportal.ipb.ac.id')

get_element(By.ID, 'Username').send_keys(USERNAME)
get_element(By.ID, 'Password').send_keys(PASSWORD)
get_element(By.CLASS_NAME, 'btn').click()

driver.get('https://studentportal.ipb.ac.id/Kegiatan/AktivitasKampusMerdeka/index')

input('Press enter if you have moved to your designated activity!')

for data in all_data:
    time.sleep(2)

    get_element(By.XPATH, "//a[contains(@class, 'btn') and starts-with(@onclick, 'OpenModal')]").click()

    time.sleep(1)
    
    if 'date' in data:
        get_element(By.ID, 'Waktu').send_keys(data['date'])
        get_element(By.ID, 'isi_modal').click()

    if 'time_end' in data:
        print(data['time_end'])
        get_element(By.ID, 'Tsw').click()
        get_element(By.ID, 'Tsw').send_keys(Keys.CONTROL, 'a')
        get_element(By.ID, 'Tsw').send_keys(Keys.BACKSPACE)
        get_element(By.ID, 'Tsw').send_keys(data['time_end'])
        get_element(By.ID, 'Tsw').send_keys(Keys.ENTER)

    if 'time_start' in data:
        get_element(By.ID, 'Tmw').click()
        get_element(By.ID, 'Tmw').clear()
        get_element(By.ID, 'Tmw').send_keys(data['time_start'])
        get_element(By.ID, 'Tmw').send_keys(Keys.ENTER)

    if 'activity' in data:
        get_element(By.ID, 'select2-JenisLogbookKegiatanKampusMerdekaId-container').click()
        if data['activity'] == 'Bimbingan':
            get_element(By.XPATH, "//li[starts-with(@id, 'select2-JenisLogbookKegiatanKampusMerdekaId-result-') and contains(@id, '-1')]").click()
        if data['activity'] == 'Ujian':
            get_element(By.XPATH, "//li[starts-with(@id, 'select2-JenisLogbookKegiatanKampusMerdekaId-result-') and contains(@id, '-2')]").click()
        if data['activity'] == 'Kegiatan':
            get_element(By.XPATH, "//li[starts-with(@id, 'select2-JenisLogbookKegiatanKampusMerdekaId-result-') and contains(@id, '-3')]").click()

    if 'lecturer' in data:
        print(data['lecturer'])
        get_element(
            By.XPATH,
            "//div[@class='form-check']//input[@type='checkbox']"
            # f"//div[@class='form-check']//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{ data['lecturer'] }')]"
        ).click()

    if 'mentoring' in data:
        if data['mentoring'] == 'Hybrid':
            get_element(By.XPATH, "//input[@name='IsLuring' and @checked='checked']").click()
        if data['mentoring'] == 'Offline':  
            get_element(By.XPATH, "//input[@name='IsLuring' and @value='true']").click()
        if data['mentoring'] == 'Online':
            get_element(By.XPATH, "//input[@name='IsLuring' and @value='false']").click()

    if 'location' in data:
        get_element(By.ID, 'Lokasi').send_keys(data['location'])

    if 'description' in data:
        get_element(By.ID, 'Keterangan').send_keys(data['description'])

    get_element(By.XPATH, "//input[@type='submit' and @value='Simpan']").click()

input()

driver.quit()
