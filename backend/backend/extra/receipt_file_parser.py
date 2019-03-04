import time
import pyexcel

from django.conf import settings
from django.core.files import File

from backend.backend.models import receipt_row


class Parser:

    @classmethod
    def parse(self, file):

        # this is a proper analysis file parse and update database
        parser = ReceiptFileParser(file.path)

        for r in parser.records:
            print(r)


class ReceiptFileParser:

    def __init__(self, path):
        self._records = pyexcel.get_records(file_name=path)

    @property
    def records(self):
        for row in self._records:
            yield row


class ContentRow:
    def __init__(self, row):
        self.row = row

    @property
    def gen(self):
        return self.row['Gene']

    @property
    def allel_frekvens(self):
        res = self.row['gnomAD']
        return res if res != '.' else "N/A"

    @property
    def eksom(self):
        return self.row['Exon']

    @property
    def intron(self):
        return self.row['Intron']

    @property
    def variant(self):
        return self.row['Nucl_Change']

    @property
    def aminosyre(self):
        return self.row['AA_Change']
