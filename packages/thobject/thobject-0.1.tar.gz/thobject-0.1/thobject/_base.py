#!/usr/bin/env python3
#**************************************************************************
# Copyright (C) 2019 Thomas Touhey <thomas@touhey.fr>
# This file is part of the thobject project, which is MIT-licensed.
#**************************************************************************
""" Definition of the base elements for the module, which include
	the object metaclass definition and the property definition. """

from inspect import getargspec as _getargspec
from warnings import warn as _warn

__all__ = ["Object", "ObjectType", "Property"]

class Property:
	""" A base property. """

	def __init__(self, *args, doc = None, **kwargs):
		self._doc = doc

		if len(args) > 0:
			_warn("Positional arguments are not used with "
				"thobject properties.")

		try:
			spec = _getargspec(self.init)
		except:
			pass

		self.init(**kwargs)

	def init(self, *_, **kwargs):
		""" Normal initialize method. """

		self.doc = "The default property."

	def doc(self, element, name):
		""" The documentation string method. """

		if self.__doc is not None:
			return self.__doc
		return self.defaultdoc(element, name)

	def defaultdoc(self, element, name):
		""" A default documentation string method. """

		return f"A default property for a {element.lower()}."

	def defaultdoc(self, element, name):
		""" """

	def get(self):
		""" Get the current property value. """

		return None

	def set(self, value):
		""" Set the current property value. """

		pass

	def delete(self):
		""" Delete the current property value. """

		pass


class ObjectType(type):
	""" The metaclass class for all thobject objects. """

	def __new__(cls, clsname, superclasses, attributedict):
		# Get the list of properties.

		def _defineprop(name, prop):
			property_list.append(name)
			attributedict[name] = property(lambda _: prop.get(),
				lambda _, x: prop.set(x), lambda _: prop.delete,
				prop.doc)

		property_list = []
		for key, value in list(attributedict.items()):
			if key in ('__qualname__', '__doc__'):
				continue

			del attributedict[key]
			if key[:1] == '_' or not isinstance(value, Property):
				continue

			_defineprop(key, value)

		# Add the initializing function.

		def __init__(self, *args, **kwargs):
			if len(args) > 0:
				raise Exception("no positional arguments are allowed")

			for name, value in kwargs.items():
				if not name in property_list:
					raise KeyError(f"no such property {repr(name)}")

				setattr(self, name, value)

		attributedict['__init__'] = __init__

		# Add the representing function.

		def __repr__(self):
			attrs = lambda: (f"{name} = {repr(val)}" for name, val
				in map(lambda x: (x, getattr(self, x)), property_list)
				if val is not None)

			return f"{self.__class__.__name__}({', '.join(attrs())})"

		attributedict['__repr__'] = __repr__

		# Finish up the work.

		return type.__new__(cls, clsname, superclasses, attributedict)

class Object(metaclass = ObjectType):
	""" Base thobject object. Doesn't actually do anything. """

	pass

# End of file.
