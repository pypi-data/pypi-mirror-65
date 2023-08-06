class ImmutableDict(dict):
    """A dict that can be updated only through the `update` or
    `setdefault` methods.
    """
    def __setitem__(self, key, value):
        raise NotImplementedError(
            'This dict cannot be altered through direct assignation')

    def __hash__(self):
        items = self.items()
        res = hash(items[0])
        for item in items[1:]:
            res ^= hash(item)
        return res
