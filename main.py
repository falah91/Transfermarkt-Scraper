import requests
# pip install beautifulsoup4
from bs4 import BeautifulSoup
import csv

heads = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

pages = list(range(1, 5))
footballer_list = []
price_list = []

for page in pages:
    url = "https://www.transfermarkt.de/1-bundesliga/marktwerte/wettbewerb/L1/ajax/ywi/page/" + str(page)
    response = requests.get(url, headers=heads)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="yw1")

    footballers = table.find_all(lambda tag: tag.name == "td" and tag.get("class") == ["hauptlink"])
    for player in footballers:
        player_name = player.text.replace("\n", "")
        footballer_list.append(player_name)

    prices = table.find_all("td", {"class": "rechts hauptlink"})
    for p in prices:
        price = p.text.split()[0].replace(",", ".")
        price_list.append(price)


data = zip(footballer_list, price_list)
print(list(data))
csv_file = "Bundesliga.csv"

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Player name', 'Market value'])
    data = zip(footballer_list, price_list)
    writer.writerows(data)
