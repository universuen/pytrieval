"""
This file is used to convert csv file to database file.
"""

import csv
from datetime import datetime
import sys

from tqdm import tqdm

from pytrieval.config import path
from pytrieval.database.handler import Handler
from pytrieval.database.models import News
from pytrieval import config

config.logger.level = 'INFO'
handler = Handler(config.database.url)

print('started')

"""
from: https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
"""
maxsize = sys.maxsize
while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxsize)
        break
    except OverflowError:
        maxsize = int(maxsize / 10)

with open(path.data / 'articles.csv', 'r', newline='', encoding='utf8') as f:
    csv_reader = csv.reader(f)
    for idx, item in tqdm(enumerate(csv_reader)):
        if idx == 0:
            continue
        handler.insert(
            News(
                title=item[2],
                publication=item[3],
                author=item[4],
                date=datetime.strptime(item[5], '%Y-%m-%d'),
                url=item[8],
                content=item[9]
            )
        )

print('finished')
