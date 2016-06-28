from lxml import html
import requests
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Copy a user\'s Github commit activity')
    parser.add_argument('user')
    parser.add_argument('repo_dir')
    args = parser.parse_args()

    page = requests.get('http://github.com/' + args.user)
    tree = html.fromstring(page.content)

    days = tree.xpath('//*[@id="contributions-calendar"]/div[1]/svg/g/g/rect')
    contribs = []
    for day in days:
        contribs.append(DayContribs(day))

    print(contribs)

class DayContribs:
    def __init__(self, element):
        self.count = int(element.get('data-count'))
        self.date = datetime.strptime(element.get('data-date'), '%Y-%m-%d')

if __name__ == '__main__':
    main()
