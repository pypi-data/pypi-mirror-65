from collections import UserDict


class Args(UserDict):
    def __getitem__(self, key):
        value = super().__getitem__(key)
        if callable(value):
            value = value()
        return value
