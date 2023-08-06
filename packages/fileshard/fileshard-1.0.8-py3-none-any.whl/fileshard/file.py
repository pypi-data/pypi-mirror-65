#Copyright © 2020 Noel Kaczmarek
from fileshard.shard import Shard

import math
import os

SHARDS_PER_FILE = 4
SHARD_SIZE = 100


class File:
    def __init__(self, file, **kwargs):
        self._file = file
        self._data = b''
        self._shards = []
        self.header = kwargs.get('header', True)
        self._output_dir = kwargs.get('output_dir', '.')
        self.split_by_size = kwargs.get('split_by_size', True)

    def read(self, bytes=None, offset=0):
        with open(self.file, 'rb') as f:
            f.seek(offset, 0)
            if bytes:
                content = f.read(bytes)
            else:
                content = f.read()
            f.close()

        return content

    def write(self, file=None):
        if not file:
            file = self.file

        with open(file, 'wb') as f:
            f.write(self.data)
            f.close()

    def split(self, **kwargs):
        try:
            self._size = os.stat(self._file).st_size
        except:
            self._size = len(self.data)
        
        if self.split_by_size:
            shards = math.ceil(self.size / SHARD_SIZE)
            shard_size = SHARD_SIZE
        else:
            shards = SHARDS_PER_FILE
            shard_size = round(self.size / SHARDS_PER_FILE)

        for i in range(shards):
            if kwargs.get('from_bytes', False):
                data = bytes(self.data)[shard_size * i:shard_size * i + shard_size]
            else:
                data = self.read(shard_size, shard_size * i)
            
            shard = Shard(os.path.join(self.output_dir, '%s_%d' % (self.file, i)))
            shard.create(i, shard_size * i, data)
            self.shards.append(shard)

        if kwargs.get('write', True):
            for shard in self.shards:
                shard.write(write_header=self.header)

    def weld(self):
        for shard in self.shards:
            self._data += shard.read(header=False)

        return self.data

    def sortShards(self, shards):
        sorted = []
        counter = 0

        for i in range(len(shards)):
            for shard in shards:
                if shard.index == counter:
                    sorted.append(shard)
            counter += 1
        return sorted

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file):
        self._file = file

    @property
    def size(self):
        return self._size

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def output_dir(self):
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir):
        self._output_dir = output_dir

    @property
    def shards(self):
        return self._shards

    @shards.setter
    def shards(self, shards):
        if self.header:
            for shard in shards:
                shard.readHeader()

        self._shards = self.sortShards(shards)