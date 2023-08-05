# -*- coding: UTF-8 -*-

class EDNEncoder(object):
    def __init__(self, sort_keys=False, sort_sets=False):
        self.sort_keys = sort_keys
        self.sort_sets = sort_sets

    def encode(self, obj):
        if is_collection(obj):
            return '[{}]'.format(" ".join(self._encode_seq(obj)))
        else:
            return str(obj)

    def _encode_seq(self, objs):
            return [self.encode(o) for o in objs]
