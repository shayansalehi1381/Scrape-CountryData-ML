from sklearn import tree
import requests
import mysql.connector
from bs4 import BeautifulSoup
import numpy as np

sql = mysql.connector.connect(user = 'root',password = 'sh13441346@',
                              host = 'localhost',database = 'countries')
cursor = sql.cursor()

url = 'https://www.scrapethissite.com/pages/simple/'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text,'html.parser')
    countries = soup.find_all('div',class_='col-md-4 country')
    for country in countries:
        country_name = country.find('h3',class_="country-name").get_text(strip=True)
        capital = country.find('span',class_="country-capital").get_text(strip=True)
        population = int(country.find('span', class_="country-population").get_text(strip=True))
        area = float(country.find('span', class_="country-area").get_text(strip=True))
        cursor.execute('INSERT INTO info (Country_Name,Capital,Population,Area) VALUES (%s,%s,%s,%s)'
                       ,(country_name,capital,population,area))
    sql.commit()
else:
    print(f"Error: {response.status_code}")

population_List = []
area_List = []
cursor.execute('SELECT Population,Area FROM info;')
for row in cursor.fetchall():
    population, area = row
    population_List.append(population)
    area_List.append(area)


X = np.array(population_List).reshape(-1, 1)
y = np.array(area_List)

cls = tree.DecisionTreeRegressor()
cls.fit(X, y)

new_data = np.array([[90000000]])
predicted_area = cls.predict(new_data)

print(f"Predicted Area: {predicted_area[0]} km²")


cursor.close()
sql.close()
print("Done!")