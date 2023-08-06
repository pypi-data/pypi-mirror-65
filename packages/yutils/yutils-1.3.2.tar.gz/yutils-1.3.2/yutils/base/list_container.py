#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38


class ListContainer(object):
    """
    An object that wraps a list, allowing you to use your object as a list and configure it as you wish.
    """
    def __init__(self, _list, _objects_type):
        """
        :param _list: the original list you wish to keep in the backbone of your object
        :type _list: list
        :param _objects_type: a plural name for your objects in your ListContainer! This is for printing your object.
                              For Example:
                              >>> class Students(ListContainer):
                              >>>     def __init__(self):
                              >>>         super().__init__([], 'students')
        :type _objects_type: str
        """
        self._list = _list
        self._objects_type = _objects_type

    def __contains__(self, item):
        return self._list.__contains__(item)

    def __delitem__(self, key):
        return self._list.__delitem__(key)

    def __eq__(self, other):
        return self._list.__eq__(other._list)

    def __ge__(self, other):
        return self._list.__ge__(other._list)

    def __getitem__(self, item):
        return self._list.__getitem__(item)

    def __getslice__(self, i, j):
        return self._list.__getslice__(i, j)

    def __gt__(self, other):
        return self._list.__gt__(other._list)

    def __iter__(self):
        return self._list.__iter__()

    def __le__(self, other):
        return self._list.__le__(other)

    def __len__(self):
        return self._list.__len__()

    def __lt__(self, other):
        return self._list.__lt__(other)

    def __ne__(self, other):
        return self._list.__ne__(other)

    def __setitem__(self, key, value):
        return self._list.__setitem__(key, value)

    def __setslice__(self, i, j, sequence):
        return self._list.__setslice__(i, j, sequence)

    def __bool__(self):
        return any(self._list)

    def __nonzero__(self):
        return self.__bool__()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '<{class_name} object with {length} {objects_type}'.format(
            class_name=self.__class__.__name__,
            length=len(self),
            objects_type=self._objects_type
        )

    def append(self, obj):
        return self._list.append(obj)

    def count(self, value):
        return self._list.count(value)

    def extend(self, iterable):
        return self._list.extend(iterable)

    def insert(self, index, obj):
        return self._list.insert(index, obj)

    def pop(self, index=-1):
        return self._list.pop(index)

    def remove(self, value):
        return self._list.remove(value)

    def reverse(self):
        return self._list.reverse()

    def sort(self, cmp=None, key=None, reverse=False):
        return self._list.sort(cmp=cmp, key=key, reverse=reverse)
