#!/usr/bin/env python
# -*- coding: utf-8 -*-

class KVStorageMixin(object):
    def __getitem__(self, key):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()

