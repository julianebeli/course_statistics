from config import username, password, url
import requests
from bs4 import BeautifulSoup as soup


class Reader:
    def __init__(self):
        self.session = self.authenticate()

    def authenticate(self):
        login_url = '{}/login/canvas'.format(url)
        session = requests.Session()
        login_page = session.get(login_url)
        login_page_soup = soup(login_page.text, 'lxml')
        i = [x['value']
             for x in login_page_soup.find_all(attrs=dict(name='authenticity_token'))]
        authenticity_token = i[0]

        payload = {'utf8': 1,
                   'authenticity_token': authenticity_token,
                   'redirect_to_ssl': 1,
                   'pseudonym_session[unique_id]': username,
                   'pseudonym_session[password]': password,
                   'pseudonym_session[remember_me]': 0
                   }

        print('authenticating  ...')
        p = session.post(login_url, data=payload)
        return session

    def get_stats(self, courseid):
        stats_url = '{}/courses/{}/statistics'
        print('getting data from {}'.format(stats_url.format(url, courseid)))
        stats_page = self.session.get(stats_url.format(url, courseid))
        stat_tables = soup(stats_page.text, 'lxml').find_all(id='stats')
        tables = stat_tables[0].find_all('table')
        stats = []
        for t in tables:
            stats.append(list(filter(lambda x: x != '\n', t.strings)))

        [totals, assignments, files] = stats
        totals = list(filter(lambda x: x.isnumeric(), stats[0]))
        assignments = list(filter(lambda x: x.isnumeric(), stats[1]))
        files = list(map(lambda x: x.split(" ")[0], [
                         stats[2][3], stats[2][4], stats[2][6], stats[2][7]]))

        return (totals + assignments + files)


if __name__ == "__main__":
    R = Reader()
    course = 25606
    print(R.get_stats(course))
