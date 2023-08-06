#!/usr/bin/env python3

import operator


class DLLElement:
    def __init__(self, val=None, prv=None, nxt=None, lst=None):
        if isinstance(val, DLLElement):
            val = val.value
        self.prev = prv
        self.next = nxt
        self.value = val
        self.list = lst
        if prv is not None:
            prv.next = self
        if nxt is not None:
            nxt.prev = self


class DLL:
    def __init__(self, iterable=None):
        self.first = None
        self.last = None
        self.size = 0
        if iterable is not None:
            self.extend(iterable)

    def __iter__(self, start=None):
        current = self.first
        if start is not None:
            current = start
        while current is not None:
            yield current
            current = current.next

    def __reversed__(self, start=None):
        current = self.last
        if start is not None:
            current = start
        while current is not None:
            yield current
            current = current.prev

    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.to_list())

    def _find_matching_element(self, item, attrgetter, value, ignore_attrgetter=None, ignore_value=None, forward=True):
        current = item
        direction = operator.attrgetter("next")
        if not forward:
            direction = operator.attrgetter("prev")
        while direction(current) is not None:
            current = direction(current)
            if ignore_attrgetter is not None:
                if ignore_attrgetter(current) == ignore_value:
                    continue
            if attrgetter(current) == value:
                return current
        return None

    def append(self, item):
        element = DLLElement(item, self.last, None, self)
        if self.first is None:
            self.first = element
        self.last = element
        self.size += 1

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def insert_left(self, item, ref_element):
        element = DLLElement(item, ref_element.prev, ref_element, self)
        ref_element.prev = element
        if self.first is ref_element:
            self.first = element
        self.size += 1

    def next_matching(self, item, attrgetter, value, ignore_attrgetter=None, ignore_value=None):
        self._find_matching_element(item, attrgetter, value, ignore_attrgetter, ignore_value, forward=True)

    def previous_matching(self, item, attrgetter, value, ignore_attrgetter=None, ignore_value=None):
        self._find_matching_element(item, attrgetter, value, ignore_attrgetter, ignore_value, forward=False)

    def remove(self, element):
        if self.first is element:
            self.first = element.next
        if self.last is element:
            self.last = element.prev
        if element.prev is not None:
            element.prev.next = element.next
        if element.next is not None:
            element.next.prev = element.prev
        self.size -= 1

    def to_list(self):
        return [e.value for e in self]
