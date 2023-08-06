# -*- coding: utf8 -*-
# Copyright (c) 2019 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

# pylint: disable=protected-access

"""
Provides the [[Proxy]] type which can imitate a Python object that is resolved
on-demand.
"""

from six import PY2, iteritems
import copy

__author__ = 'Niklas Rosenstein <rosensteinniklas@gmail.com>'
__version__ = '0.0.2'


class Proxy(object):
  """
  Wraps an object returned by a callable. Every time the proxy is accessed,
  the callable is invoked and the access is redirected to the proxied object.

  .. note::

    For some use cases, using a proxy can lead to problems when
    `isinstance()` or checks are used. For example if you pass a proxy to
    a function that accepts an iterable, the instancecheck with
    [[collections.abc.Iterable]] will always return `True` as the [[Proxy]]
    class implements the `__iter__()` method. If you are stuck with this
    problem, use the [[make_proxy_class()]] function to create a new class
    excluding the `__iter__()` method.
  """

  __slots__ = ("__local", "__dict__", "__name__", "__wrapped__")
  __is_proxy__ = True

  def __init__(self, local=None, name=None, lazy=False, deref=False):
    object.__setattr__(self, "_Proxy__local", local)
    object.__setattr__(self, "_Proxy__lazy", lazy)
    object.__setattr__(self, "_Proxy__cache", None)
    object.__setattr__(self, "__name__", name)
    object.__setattr__(self, "_Proxy__deref", deref)
    if callable(local) and not hasattr(local, "__release_local__"):
      # "local" is a callable that is not an instance of Local or
      # LocalManager: mark it as a wrapped function.
      object.__setattr__(self, "__wrapped__", local)

  def _get_current_object(self):
    if self.__lazy:
      if self.__cache is None:
        object.__setattr__(self, "_Proxy__cache", self.__local())
      return self.__cache
    elif self.__local is None:
      raise RuntimeError('unbound proxy')
    else:
      return self.__local()

  @property
  def __dict__(self):
    try:
      return self._get_current_object().__dict__
    except RuntimeError:
      raise AttributeError("__dict__")

  def __repr__(self):
    try:
      obj = self._get_current_object()
    except RuntimeError:
      return "<%s unbound>" % type(self).__name__
    return repr(obj)

  def __bool__(self):
    try:
      return bool(self._get_current_object())
    except RuntimeError:
      return False

  if PY2:
    __nonzero__ = __bool__
    del __bool__

  def __unicode__(self):
    try:
      return unicode(self._get_current_object())  # noqa
    except RuntimeError:
      return repr(self)

  def __dir__(self):
    try:
      return dir(self._get_current_object())
    except RuntimeError:
      return []

  def __getattr__(self, name):
    if name == "__members__":
      return dir(self._get_current_object())
    return getattr(self._get_current_object(), name)

  def __setitem__(self, key, value):
    self._get_current_object()[key] = value

  def __delitem__(self, key):
    del self._get_current_object()[key]

  if PY2:
    __getslice__ = lambda x, i, j: x._get_current_object()[i:j]

    def __setslice__(self, i, j, seq):
      self._get_current_object()[i:j] = seq

    def __delslice__(self, i, j):
      del self._get_current_object()[i:j]

  def __call__(self, *a, **kw):
    if self.__deref:
      return self._get_current_object()
    else:
      return self._get_current_object()(*a, **kw)

  __setattr__ = lambda x, n, v: setattr(x._get_current_object(), n, v)
  __delattr__ = lambda x, n: delattr(x._get_current_object(), n)
  __str__ = lambda x: str(x._get_current_object())
  __lt__ = lambda x, o: x._get_current_object() < o
  __le__ = lambda x, o: x._get_current_object() <= o
  __eq__ = lambda x, o: x._get_current_object() == o
  __ne__ = lambda x, o: x._get_current_object() != o
  __gt__ = lambda x, o: x._get_current_object() > o
  __ge__ = lambda x, o: x._get_current_object() >= o
  __cmp__ = lambda x, o: cmp(x._get_current_object(), o)  # noqa
  __hash__ = lambda x: hash(x._get_current_object())
  __len__ = lambda x: len(x._get_current_object())
  __getitem__ = lambda x, i: x._get_current_object()[i]
  __iter__ = lambda x: iter(x._get_current_object())
  __contains__ = lambda x, i: i in x._get_current_object()
  __add__ = lambda x, o: x._get_current_object() + o
  __sub__ = lambda x, o: x._get_current_object() - o
  __mul__ = lambda x, o: x._get_current_object() * o
  __floordiv__ = lambda x, o: x._get_current_object() // o
  __mod__ = lambda x, o: x._get_current_object() % o
  __divmod__ = lambda x, o: x._get_current_object().__divmod__(o)
  __pow__ = lambda x, o: x._get_current_object() ** o
  __lshift__ = lambda x, o: x._get_current_object() << o
  __rshift__ = lambda x, o: x._get_current_object() >> o
  __and__ = lambda x, o: x._get_current_object() & o
  __xor__ = lambda x, o: x._get_current_object() ^ o
  __or__ = lambda x, o: x._get_current_object() | o
  __div__ = lambda x, o: x._get_current_object().__div__(o)
  __truediv__ = lambda x, o: x._get_current_object().__truediv__(o)
  __neg__ = lambda x: -(x._get_current_object())
  __pos__ = lambda x: +(x._get_current_object())
  __abs__ = lambda x: abs(x._get_current_object())
  __invert__ = lambda x: ~(x._get_current_object())
  __complex__ = lambda x: complex(x._get_current_object())
  __int__ = lambda x: int(x._get_current_object())
  __long__ = lambda x: long(x._get_current_object())  # noqa
  __float__ = lambda x: float(x._get_current_object())
  __oct__ = lambda x: oct(x._get_current_object())
  __hex__ = lambda x: hex(x._get_current_object())
  __index__ = lambda x: x._get_current_object().__index__()
  __coerce__ = lambda x, o: x._get_current_object().__coerce__(x, o)
  __enter__ = lambda x: x._get_current_object().__enter__()
  __exit__ = lambda x, *a, **kw: x._get_current_object().__exit__(*a, **kw)
  __radd__ = lambda x, o: o + x._get_current_object()
  __rsub__ = lambda x, o: o - x._get_current_object()
  __rmul__ = lambda x, o: o * x._get_current_object()
  __rdiv__ = lambda x, o: o / x._get_current_object()
  if PY2:
    __rtruediv__ = lambda x, o: x._get_current_object().__rtruediv__(o)
  else:
    __rtruediv__ = __rdiv__
  __rfloordiv__ = lambda x, o: o // x._get_current_object()
  __rmod__ = lambda x, o: o % x._get_current_object()
  __rdivmod__ = lambda x, o: x._get_current_object().__rdivmod__(o)
  __copy__ = lambda x: copy.copy(x._get_current_object())
  __deepcopy__ = lambda x, memo: copy.deepcopy(x._get_current_object(), memo)
  __class__ = property(lambda x: type(x._get_current_object()))


def proxy_set_value(proxy, value):
  """ Permanently overrides the internal value of a #Proxy. """

  object.__setattr__(proxy, '_Proxy__lazy', True)
  object.__setattr__(proxy, '_Proxy__cache', value)


def proxy_deref(proxy):
  if not isinstance(proxy, Proxy):
    raise RuntimeError('expected Proxy object, got {}'.format(
      type(proxy).__name__))
  return proxy._get_current_object()


def proxy_decorator(proxy_cls=None, name=None, lazy=False, deref=False):
  """
  Decorator for converting function declarations into [[Proxy]] objects.
  """

  if proxy_cls is None:
    proxy_cls = Proxy

  def decorator(func):
    return proxy_cls(func, name or func.__name__, lazy, deref)

  return decorator


def make_proxy_class(name, base=None, include=None, exclude=None):
  """
  Produces a new class that is the same as [[Proxy]] but does not inherit
  from it. Members can be specifically included and excluded with the
  *include*/*exclude* arguments.

  If *base* is not specified, it defaults to the [[Proxy]] class.
  """

  if base is None:
    base = Proxy

  members = {}
  for cls in reversed(base.__mro__):
    members.update(cls.__dict__)

  filtered_members = {}
  for key, value in iteritems(members):
    take = False
    if include is not None and key in include:
      take = True
    elif include is None and (key.startswith('__') and key.endswith('__') or key == '_get_current_object'):
      take = True
    if exclude is not None and key in exclude:
      take = False
    if key in ['__name__', '__wrapped__', '__weakref__', '__module__', '__doc__'] \
        and (not include or key not in include):
      take = False
    if take:
      filtered_members[key] = value

  return type(name, (object,), filtered_members)
