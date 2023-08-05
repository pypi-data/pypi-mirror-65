# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2020 Kevin Walchko
# see LICENSE for full details
##############################################
import pickle
import attr


@attr.s(slots=True)
class PickleJar(object):
    """
    My silly little data collector ... this probably isn't super useful. Data
    is stored in a dictionary:

    {
        topic: [d1,d2,d3 ...],
        topic: [d1,d2,d3 ...],
        topic: [d1,d2,d3 ...],
        ...
    }
    """
    fd = attr.ib(default=None)
    buffer = attr.ib(default=attr.Factory(dict))
    counter = attr.ib(default=0)
    buffer_size = attr.ib(default=500)

    def __del__(self):
        self.close()

    def init(self, fname, buffer_size=500):
        """
        Initialize the picklejar for saving data to a file.

        fname: file name
        buffer_size: how many times push gets called before the current
            buffer gets flushed to the file
        """
        self.fd = open(fname, 'wb')
        self.buffer = {}
        self.buffer_size = buffer_size
        self.counter = 0

    def push(self, topic, data):
        """
        This save data in a key, value dictionary.

        topic: string that is the key
        data: any python object that is the value
        """
        if not self.fd: raise Exception("PickleJar.init() not set")
        if topic not in self.buffer:
            self.buffer[topic] = []
        self.buffer[topic].append(data)
        self.counter += 1
        if self.counter > self.buffer_size:
            self.write()
            self.counter = 0

    def add(self, b):
        for k in b.keys():
            if k in self.buffer:
                self.buffer[k] += b[k]
            else:
                self.buffer[k] = b[k]

    def read(self, fname):
        f = open(fname, 'rb')
        self.buffer = {}
        while True:
            try:
                d = pickle.load(f)
                print(">>", len(d), d)
                self.add(d)
            except EOFError:
                break
        f.close()

    def write(self):
        if not self.fd:
            raise Exception("PickleJar.init() not set")
        ret = self.fd.write(pickle.dumps(self.buffer))
        # print("w", ret, self.buffer)
        self.buffer = {}

    def close(self):
        if self.fd:
            if len(self.buffer) > 0:
                self.write()
            self.fd.close()
            self.fd = None
