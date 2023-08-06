from bs4 import BeautifulSoup
import requests


class Aaindex:

    search_url = 'https://www.genome.jp/dbget-bin/www_bfind_sub?'
    record_url = 'https://www.genome.jp/dbget-bin/www_bget?'

    def __init__(self, source='web'):
        pass

    def search(self, keyword, dbkey='aaindex', max_hits=0):
        loc = 'locale=en'
        serv = 'serv=gn'
        keywords = 'keywords=' + '+'.join(keyword.split())
        page = 'page=1'
        max_hits = f'max_hit={max_hits}'
        dbkey = f'dbkey={dbkey}'
        params = '&'.join([loc, serv, keywords, page, max_hits, dbkey])
        url = ''.join([self.search_url, params])
        r = requests.get(url)
        if r.status_code == 200:
            return self._parse_search_response(r)

    def _parse_search_response(self, response):
        soup = BeautifulSoup(response.text, features='html.parser')
        divs = (x for x in soup.find_all('div'))
        results = []
        for div in divs:
            if div.a:
                name = div.a.get_text()
                next_div = next(divs)
                text = next_div.get_text()
                results.append((name, text.strip()))
        return results

    def get(self, record_id, dbkey='aaindex'):
        params = ':'.join([dbkey, record_id])
        url = ''.join([self.record_url, params])
        r = requests.get(url)
        if r.status_code == 200:
            new_record = Record(record_id).from_response(r.text)
            return new_record


class Record:

    response_data = ''

    def __init__(self, record_id):
        self.record_id = record_id

    def from_response(self, response):
        soup = BeautifulSoup(response, features='html.parser')
        self.response_data = soup.find_all('pre').pop().get_text().strip()
        if len(self.response_data.split('\n')) <= 1:
            raise FileNotFoundError(f'{self.record_id}: No such data was found.')
        return self

    @property
    def accession_number(self):
        return self._rip_data('H')

    @property
    def data_description(self):
        return self._rip_data('D')

    @property
    def pmid(self):
        return self._rip_data('R')

    @property
    def author(self):
        return self._rip_data('A')

    @property
    def title(self):
        return self._rip_data('T')

    @property
    def journal_reference(self):
        return self._rip_data('J')

    @property
    def similar_entities(self):
        acn = (x for x in self._rip_data('C').split())
        data = [(x, float(next(acn))) for x in acn]
        return data

    @property
    def index_data(self):
        idx_data = self._rip_data('I').split()
        data = {}
        for i in range(10):
            a1 = idx_data[i].split('/')[0]
            a2 = idx_data[i].split('/')[1]
            v1 = float(idx_data[i+10])
            v2 = float(idx_data[i+20])
            data[a1] = v1
            data[a2] = v2
        return data

    def _rip_data(self, flag):
        data = []
        line_generator = (x for x in self.response_data.split('\n'))
        for line in line_generator:
            if line.startswith(flag):
                data.extend(line.split()[1:])
                while True:
                    next_line = next(line_generator)
                    if next_line.startswith(' '):
                        data.extend(next_line.split())
                    else:
                        break
        return ' '.join(data)
