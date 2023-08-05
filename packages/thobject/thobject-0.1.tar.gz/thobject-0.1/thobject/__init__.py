#!/usr/bin/env python3
#**************************************************************************
# Copyright (C) 2019 Thomas Touhey <thomas@touhey.fr>
# This file is part of the thobject project, which is MIT-licensed.
#**************************************************************************
""" thobject allows you to define useful objects in Python. """

from .version import version
from ._base import Object, Property
from ._cache import Cache
from ._props import (DateProperty, BoolProperty, EnumProperty,
	ArrayProperty, ObjectProperty, ValueProperty, TextProperty)

__all__ = ["version",
	"Object", "Property", "Cache",

	"DateProperty", "BoolProperty", "EnumProperty", "ArrayProperty",
	"ObjectProperty", "ValueProperty", "TextProperty"]

# End of file.
