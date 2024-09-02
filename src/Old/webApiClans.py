from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def fetch_page_data(page_num):
    url = f"https://warthunder.com/en/community/claninfo/AVANGARD"
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'leaderboards')))
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    print(soup)
    input()
    table = soup.find('table', {'class': 'leaderboards'})
    squadrons = []

    if table:
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            if len(columns) >= 8:
                place = int(columns[0].text.strip())
                name = columns[1].text.strip()
                duel_ratio = columns[2].text.strip()
                members = columns[3].text.strip()
                air_targets = columns[4].text.strip()
                ground_targets = columns[5].text.strip()
                deaths = columns[6].text.strip()
                flight_time = columns[7].text.strip()

                squadrons.append({
                    'place': place,
                    'name': name,
                    'duel_ratio': duel_ratio,
                    'members': members,
                    'air_targets': air_targets,
                    'ground_targets': ground_targets,
                    'deaths': deaths,
                    'flight_time': flight_time
                })

    return squadrons

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

all_squadrons = []
for page_num in range(1, 11):
    squadrons = fetch_page_data(page_num)
    all_squadrons.extend(squadrons)
    time.sleep(2)

driver.quit()

sorted_squadrons = sorted(all_squadrons, key=lambda x: x['place'])

# with open("squadrons.log", "w", encoding="utf-8") as file:
for squadron in sorted_squadrons:
    print(f"Place: {squadron['place']}, Name: {squadron['name']}, Duel Ratio: {squadron['duel_ratio']}, "
               f"Members: {squadron['members']}, Air Targets: {squadron['air_targets']}, Ground Targets: {squadron['ground_targets']}, "
               f"Deaths: {squadron['deaths']}, Flight Time: {squadron['flight_time']}\n")