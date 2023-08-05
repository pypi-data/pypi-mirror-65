import json
import logging

logger = logging.getLogger('mirzaki.json_walker')


class JsonWalkerReturnException(Exception):
    pass


class JsonWalker(object):

    def __bool__(self):
        return self.__inner_cool_data__ is not None

    def __eq__(self, other):
        return self.__inner_cool_data__ == other

    def __gt__(self, other):
        return self.__inner_cool_data__ > other

    def __ge__(self, other):
        return self.__inner_cool_data__ >= other

    def __lt__(self, other):
        return self.__inner_cool_data__ < other

    def __le__(self, other):
        return self.__inner_cool_data__ <= other

    def __str__(self):
        return str(self.__inner_cool_data__)

    def __int__(self):
        return int(self.__inner_cool_data__)

    @property
    def _(self):
        """ Returns a properties value """
        return self.__inner_cool_data__

    def __(self, default=None):
        return default if self.__inner_cool_data__ is None else self.__inner_cool_data__

    def __init__(self, data) -> None:
        if isinstance(data, set):
            raise TypeError("Can't parse Set")
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                pass
        if isinstance(data, JsonWalker):
            data = data._
        self.__inner_cool_data__ = data

    def __getattribute__(self, name: str):
        try:
            return super().__getattribute__(name)
        except:
            try:
                return JsonWalker(self.__inner_cool_data__[name])
            except (KeyError, TypeError):
                return JsonWalker(None)

    def __getitem__(self, item):
        try:
            return JsonWalker(self.__inner_cool_data__[item])
        except (KeyError, TypeError):
            return JsonWalker(None)

    def __iter__(self):
        if self.__inner_cool_data__ is not None:
            if isinstance(self.__inner_cool_data__, list):
                for i in self.__inner_cool_data__:
                    yield JsonWalker(i)
            elif isinstance(self.__inner_cool_data__, dict):
                for key, value in self.__inner_cool_data__.items():
                    yield key, JsonWalker(value)
            else:
                return iter([])
        else:
            return iter([])

    def __len__(self):
        if self.__inner_cool_data__ is None:
            return 0
        return len(self.__inner_cool_data__)
