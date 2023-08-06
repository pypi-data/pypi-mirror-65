# pyaaisc
Python AAindex database scrape

AAindex website: https://www.genome.jp/aaindex/

### Instalation

```
pip install pyaaisc
```

### Usage

```python
from pyaaisc import Aaindex

aai = Aaindex()
for result in aai.search('charge'):
    print(result)

record = aai.get('KLEP840101')
print(record.accession_number, record.title)

```
```
## output
>>> ('CHAM830107', 'A parameter of charge transfer capability (Charton-Charton, 1983)')
>>> ('CHAM830108', 'A parameter of charge transfer donor capability (Charton-Charton, 1983)')
>>> ('FAUJ880111', 'Positive charge (Fauchere et al., 1988)')
>>> ('FAUJ880112', 'Negative charge (Fauchere et al., 1988)')
>>> ('KLEP840101', 'Net charge (Klein et al., 1984)')

>>> KLEP840101 Prediction of protein function from sequence properties: Discriminant analysis of a data base
```
