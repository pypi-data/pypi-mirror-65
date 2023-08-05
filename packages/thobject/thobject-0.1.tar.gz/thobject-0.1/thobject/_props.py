#!/usr/bin/env python3
#**************************************************************************
# Copyright (C) 2019 Thomas Touhey <thomas@touhey.fr>
# This file is part of the thobject project, which is MIT-licensed.
#**************************************************************************
""" Definition of some default property types. """

import re as _re

from copy import deepcopy as _deepcopy
from enum import Enum
from datetime import (datetime as _datetime, date as _date,
	timezone as _timezone)
from pytz import utc as _utc

from ._base import Property as _Property

__all__ = ["DateProperty", "BoolProperty", "EnumProperty",
	"ArrayProperty", "ObjectProperty", "ValueProperty", "TextProperty"]

class _Array:
	""" An array of certain objects, for the base class. """

	def __init__(self, types = ()):
		self.__list  = []
		self.__types = types

	def __repr__(self):
		return repr(self.__list)

	def __iter__(self):
		return iter(self.__list)

	def __len__(self):
		return len(self.__list)

	def __getitem__(self, x):
		return self.__list[x]

	def add(self, elt):
		""" Add an element into the array. """

		if self.__types and not any(isinstance(elt, t) \
			for t in self.__types):
			raise TypeError("element to add is of unknown type "
				f"{type(elt)}")
		if any(elt is e or elt == e for e in self.__list):
			raise ValueError("element already inserted")
		self.__list.append(elt)

	def empty(self):
		""" Empty the array. """

		self.__list = []

_datere = _re.compile('(?P<dom>[0-9]+)\/(?P<mon>[0-9]+)\/(?P<yr>[0-9]+)')

class DateProperty(_Property):
	""" A date property. """

	def init(self, *_, timezone = None):
		self.__date = None

		if isinstance(timezone, _timezone):
			self.__tz = _timezone
		else:
			self.__tz = _utc

	def defaultdoc(self, element, name):
		return f"The {name.replace('_', ' ')} timestamp for the {element}."

	def get(self):
		return self.__date

	def set(self, value):
		if value is None:
			self.__date = value
			return

		if   isinstance(value, _datetime):
			pass # use the value as is.
		elif isinstance(value, _date):
			value = _datetime.fromordinal(value.toordinal())
		elif type(value) == str:
			m = _datere.match(value)
			if   m is None:
				raise TypeError("uncorrectly formatted date string: " \
					f"{repr(value)}")
			else: # if m.group('yr'):
				year = int(m.group('yr'))
				mon  = int(m.group('mon'))
				dom  = int(m.group('dom'))
				value = _datetime(year, mon, dom)
		else:
			raise TypeError("Could not determinate a valid datetime.")

		if value.tzinfo is None:
			value = value.replace(tzinfo = self.__tz)
		self.__date = value

	def delete(self):
		self.__date = value

class BoolProperty(_Property):
	""" A boolean property. """

	def init(self, *_, default = False):
		self.__default = bool(default)
		self.__value = self.__default

	def defaultdoc(self, element, name):
		return f"If the {element} has {name.replace('_', ' ')}."

	def get(self):
		return self.__value

	def set(self, value):
		if value is None:
			self.__value = self.__default
		else:
			self.__value = bool(value)

	def delete(self):
		self.__value = self.__default

class EnumProperty(_Property):
	""" An enumeration property. """

	def init(self, *_, enum = Enum, default = None):
		if default is not None:
			try:
				default = enum(default)
			except ValueError:
				msg = "Default should be None or a valid enum value."
				raise ValueError(msg) from None

		self.__enum = enum
		self.__default = default
		self.__value = default

	def defaultdoc(self, element, name):
		return f"The {name.replace('_', ' ')} constant for " \
			f"the {element.lower()}."

	def get(self):
		return self.__value

	def set(self, value):
		if value is None:
			self.__value = self.__default
		else:
			self.__value = self.__enum(value)

	def delete(self):
		self.__value = self.__default

class ArrayProperty(_Property):
	""" An array made of different objets.
		`types` are the accepted types (an empty array representing that
		all types are accepted). """

	def init(self, *_, types = ()):
		self.__array = _Array(types)

	def defaultdoc(self, element, name):
		return f"The {name.replace('_', ' ')} array for the " \
			f"{element.lower()}."

	def get(self):
		return self.__array

	def set(self, value):
		if value is None:
			self.__array.empty()
			return

		raise ValueError("non settable")

	def delete(self):
		self.__array.empty()

class ObjectProperty(_Property):
	""" An object property among specified types. """

	def init(self, *_, types = (), default = None):
		self.__default = default
		self.__types = types
		self.__value = self.__default

	def get(self):
		return self.__value

	def set(self, value):
		if value is None:
			self.__value = self.__default
			return

		if not any(isinstance(value, cls) for cls in self.__types):
			raise ValueError("Shall be an instance of one of: " \
				f"{repr(self.__types)}")

		self.__value = value

	def delete(self):
		self.__value = self.__default

class ValueProperty(_Property):
	""" A value property.
		Basically uses a class to store its value. """

	def init(self, *_, cls, default = None):
		self.__cls = cls
		self.__data = default

	def get(self):
		return self.__data

	def set(self, value):
		if value is None:
			self.__data = _deepcopy(default)
			return

		self.__data = self.__cls(value)

	def delete(self):
		self.__data = _deepcopy(default)

class TextProperty(_Property):
	""" A text property.
		`lines` represents the maximum number of allowed lines.
		`maxchars` represents the maximum number of characters.
		`not_empty`: if True, empty strings are considered as None. """

	def init(self, lines = 0, maxchars = 0, not_empty = False):
		self.__value = None
		self.__lines = lines
		self.__maxchars = maxchars
		self.__nempty = bool(not_empty)

	def get(self):
		return self.__value

	def set(self, value):
		if value is None or (self.__nempty and value == ''):
			self.__value = None
			return

		value = str(value)

		# Manage the lines.

		value = value.splitlines()
		lines = self.__lines
		if lines < 0:
			lines = len(value)

		tab  = ['\n'.join(value[:lines])] if lines != 0 else []
		tab += value[lines:]
		value = ' '.join(tab)
		del tab

		# Manage the maximum number of characters.

		maxchars = self.__maxchars
		if maxchars > 0 and len(value) > maxchars:
			msg = f"{name}: max text length exceeded (> {maxchars})"
			raise ValueError(msg)

		self.__value = value

	def delete(self):
		self.__value = None

# End of file.
