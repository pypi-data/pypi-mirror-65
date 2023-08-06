import csv
import sys

import fiona

from itertools import chain, islice
from typing import Dict, Iterable, Any

from geomet import wkt

csv.field_size_limit(sys.maxsize)


def grouper(n, iterable):
    """https://stackoverflow.com/a/8991553/4453925"""
    it = iter(iterable)
    while True:
       chunk = tuple(islice(it, n))
       if not chunk:
           return
       yield chunk


class wkt_dialect(csv.unix_dialect):
    delimiter = '|'
    quoting = csv.QUOTE_MINIMAL


def create_line(feature: Dict[str, Any]) -> Iterable:
    return chain(
        [feature['id']],
        (str(value) for value in feature['properties'].values()),
        [wkt.dumps(feature['geometry'])]
    )


def list_fields(src: fiona.Collection) -> list:
    return list(chain(
        ['id'],
        (key.lower() for key in src.schema['properties'].keys()),
        ['wkt'])
    )


def convert_to_wkt(input_file: str, output_file: str):

    with fiona.open(input_file) as src, \
            open(output_file, 'w') as output_fobj:
        writer = csv.writer(output_fobj, dialect=wkt_dialect)
        writer.writerow(list_fields(src))

        for group in grouper(1000, src):
            writer.writerows((create_line(row) for row in group if row['geometry'] is not None))
