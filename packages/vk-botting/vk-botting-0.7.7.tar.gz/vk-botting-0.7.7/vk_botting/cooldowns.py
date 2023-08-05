"""
The MIT License (MIT)

Copyright (c) 2019-2020 MrDandycorn

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import time
from enum import Enum


class BucketType(Enum):
    default = 0
    user = 1
    conversation = 2
    member = 3


class Cooldown:

    def __init__(self, rate, per, type):
        self.rate = int(rate)
        self.per = float(per)
        self.type = type
        self._window = 0.0
        self._tokens = self.rate
        self._last = 0.0

        if not isinstance(self.type, BucketType):
            raise TypeError('Cooldown type must be a BucketType')

    def get_tokens(self, current=None):
        if not current:
            current = time.time()
        tokens = self._tokens
        if current > self._window + self.per:
            tokens = self.rate
        return tokens

    def update_rate_limit(self, current=None):
        current = current or time.time()
        self._last = current
        self._tokens = self.get_tokens(current)
        if self._tokens == self.rate:
            self._window = current
        if self._tokens == 0:
            return self.per - (current - self._window)
        self._tokens -= 1
        if self._tokens == 0:
            self._window = current

    def reset(self):
        self._tokens = self.rate
        self._last = 0.0

    def copy(self):
        return Cooldown(self.rate, self.per, self.type)

    def __repr__(self):
        return '<Cooldown rate: {0.rate} per: {0.per} window: {0._window} tokens: {0._tokens}>'.format(self)


class CooldownMapping:
    def __init__(self, original):
        self._cache = {}
        self._cooldown = original

    def copy(self):
        ret = CooldownMapping(self._cooldown)
        ret._cache = self._cache.copy()
        return ret

    @property
    def valid(self):
        return self._cooldown is not None

    @classmethod
    def from_cooldown(cls, rate, per, type):
        return cls(Cooldown(rate, per, type))

    def _bucket_key(self, msg):
        bucket_type = self._cooldown.type
        if bucket_type is BucketType.user:
            return msg.from_id
        elif bucket_type is BucketType.conversation:
            return msg.peer_id
        elif bucket_type is BucketType.member:
            return msg.peer_id, msg.from_id

    def _verify_cache_integrity(self, current=None):
        current = current or time.time()
        dead_keys = [k for k, v in self._cache.items() if current > v._last + v.per]
        for k in dead_keys:
            del self._cache[k]

    def get_bucket(self, message, current=None):
        if self._cooldown.type is BucketType.default:
            return self._cooldown

        self._verify_cache_integrity(current)
        key = self._bucket_key(message)
        if key not in self._cache:
            bucket = self._cooldown.copy()
            self._cache[key] = bucket
        else:
            bucket = self._cache[key]

        return bucket

    def update_rate_limit(self, message, current=None):
        bucket = self.get_bucket(message, current)
        return bucket.update_rate_limit(current)
