#Copyright © 2020 Noel Kaczmarek
import json


FILE_HEADER_SIZE = 64


class Shard:
    def __init__(self, file):
        self.file = file

    def create(self, index, offset, data):
        self.index = index
        self.size = len(data)
        self.offset = offset
        self.data = data
        self.header = self.generateHeader()

    def read(self, **kwargs):
        with open(self.file, 'rb') as f:
            if kwargs.get('header', True):
                f.seek(FILE_HEADER_SIZE, 0)
            content = f.read()
        return content

    def write(self, **kwargs):
        with open(self.file, 'wb') as f:
            if kwargs.get('write_header', True):
                f.write(self.header)
                f.seek(FILE_HEADER_SIZE, 0)
            f.write(self.data)
    
    def readHeader(self):
        with open(self.file, 'rb') as f:
            self.header = f.read(FILE_HEADER_SIZE)

        header = self.header.decode().split('}')[0] + '}'
        header = json.loads(header)
        self.index = header['index']
        self.size = header['size']
        self.offset = header['offset']

    def generateHeader(self):
        return json.dumps({'index': self.index, 'size': self.size, 'offset': self.offset}).encode('utf-8')