import csv
from typing import Generator


def read(file: str, batchsize: int = 100) -> Generator:
    with open(file, "r") as f:
        reader = csv.DictReader(f)

        if batchsize is not None:
            batch = []
            for index, line in enumerate(reader):
                if index % batchsize == 0 and index > 0:
                    yield batch
                    del batch[:]
                batch.append(dict(line))
            yield batch
        else:
            for row in reader:
                yield row
