import multiprocessing
import os
import time

start = time.time()

class SharedValue(object):
    """A multi-process shared value with automatic lock"""
    def __init__(self, value=0, type="i"):
        """
        :param type: see full list of possible in standard module: ctypes.*
        """
        self._val = multiprocessing.Value(type, value)
        # self.name = "TEST"
        # self._debug(f"init with {value}")
        self.name = ""

    def with_name(self, name):
        self.name = name
        return self

    @property
    def lock(self):
        return self._val.get_lock()

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __cmp__(self, other):
        other = self._get(other)
        if not isinstance(other, type(self._val)):
            raise TypeError(other, type(self._val), type(other))
        with self.lock:
            if self._val.value == other:
                return 0
            elif self._val.value > other:
                return 1
            return -1

    def __iadd__(self, other):
        self.__add__(other)
        return self

    def __imod__(self, other):
        self.__mod__(other)
        return self

    def __isub__(self, other):
        self.__sub__(other)
        return self

    # TODO may be bug?
    def __add__(self, other):
        with self.lock:
            other = self._get(other)
            self._debug(f"add {other}, before")
            if not isinstance(other, int):
                raise NotImplementedError()
            self._val.value += other
            self._debug(f"add {other}, after")
            return self._val.value

    def __mod__(self, other):
        with self.lock:
            other = self._get(other)
            if not isinstance(other, int):
                raise NotImplementedError()
            return self._val.value % other

    def __sub__(self, other):
        self.__add__(-other)

    @property
    def value(self):
        with self.lock:
            self._debug("getter")
            return self._val.value

    @value.setter
    def value(self, _value):
        with self.lock:
            self._debug("setter before")
            _value = self._get(_value)
            if not isinstance(_value, type(self._val)):
                raise TypeError(_value, type(self._val), type(_value))
            self._val.value = _value
            self._debug("setter after")

    def _debug(self, operation):
        if self.name:
            global start
            print(f"DEBUG {time.time()-start:.3f} [{os.getpid()}] {self.name} > {operation} : {self._val.value}")

    def _get(self, v):
        if self._type(v):
            return v.value
        return v

    def _type(self, v):
        return isinstance(v, SharedValue)

    # def __repr__(self):
    #     return "<SharedCounter %v>" % self._val.value

    def __format__(self, format_spec):
        return self._val.value.__format__(format_spec)

    def __str__(self):
        return str(self.value)