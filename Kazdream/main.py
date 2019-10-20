import requests
import csv
from bs4 import BeautifulSoup

BASE_URL = "https://www.zakon.kz/news"

def get_html(url):
    response = requests.get(url)
    return response.text

#Parsing site's content
def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('div', id='dle-content')
    
    projects  = []

    for articles in table.find_all('div', class_='cat_news_item')[1:]:

        projects.append({
            'title': articles.a.text,
            'dates': [dates.text for dates in articles.find_all('span')],
            'comments': [comments.text for comments in articles.find_all('span', class_='comm_num')]
        })
    
    return projects

#Saving the content into csv-file
def save(projects, path):
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Title', 'Date', 'Comments'))

        for project in projects:
            writer.writerow((project['title'], ', '.join(project['dates']), project['comments']))   
            

def main():
    projects = parse(get_html(BASE_URL))
    save(projects, 'zakon.csv') 
"""
Well, I tried so hard, but it saves all data as some unreadable 'kasha', 
even when in console it prints ok all today's news

"""

if __name__ == '__main__':
    main()