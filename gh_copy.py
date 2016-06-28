from lxml import html
import requests
import argparse
from datetime import datetime, timedelta
from git import Repo, Actor
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Copy a user\'s Github commit activity')
    parser.add_argument('user')
    parser.add_argument('repo_dir')
    parser.add_argument('name')
    parser.add_argument('email')
    args = parser.parse_args()

    page = requests.get('http://github.com/' + args.user)
    tree = html.fromstring(page.content)

    days = tree.xpath('//*[@id="contributions-calendar"]/div[1]/svg/g/g/rect')
    contribs = []
    for day in days:
        contribs.append(DayContribs(day))

    repo = Repo(args.repo_dir)
    assert not repo.bare

    dummy_file = Path(args.repo_dir, 'dummy_file')
    index = repo.index

    author = Actor(args.name, args.email)

    for contrib in contribs:
        for i in range(contrib.count):
            dummy_file.touch()
            index.add([dummy_file.as_posix()])
            commit = index.commit('dummy commit', author=author, committer=author, author_date=contrib.date.isoformat())
            assert commit.type == 'commit'

class DayContribs:
    def __init__(self, element):
        self.count = int(element.get('data-count'))
        self.date = datetime.strptime(element.get('data-date'), '%Y-%m-%d') + timedelta(hours=12)

if __name__ == '__main__':
    main()
