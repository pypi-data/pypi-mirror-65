#!/usr/bin/env python3
#**************************************************************************
# Copyright (C) 2019 Thomas Touhey <thomas@touhey.fr>
# This file is part of the thobject project, which is MIT-licensed.
#**************************************************************************
""" Definition of the thobject database, based on temporary data and
	databases. Also integrates features useful for managing a cache. """

from tinydb import TinyDB as _TinyDB
from tinydb.storages import MemoryStorage as _MemoryStorage
from warnings import warn as _warn
#from ._base import Object as _Object

__all__ = ["Cache"]


class Cache:
	""" The caching database definition. """

	def __init__(self):
		# Let's define our database but keep in in-memory.
		# TODO: add an option to keep it persistent?

		self._db = _TinyDB(storage = _MemoryStorage)

	def add(self, obj):
#		if not isinstance(obj, _Object):
#			raise Exception("thobject cache can only store objects based "
#				"on thobject.Object.")
		# TODO

		pass # TODO

# End of file.
