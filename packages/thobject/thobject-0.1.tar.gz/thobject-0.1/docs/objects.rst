Objects with thobject
=====================

Objects with thobject are like any object in Python, with properties and
values, except the syntax is different and some pre-established properties
are already set and enough for most projects.

For defining a simple thobject object, you can do the following:

.. code-block:: python

	from thobject import Object

	class SampleObject(Object):
		""" A simple object in our example codebase. It has no
			properties for the moment; some will come later! """

		pass

Adding value properties
-----------------------

Value properties are simple properties with a class. For example, you could
have an integer as a property representing the number of items in a box:

.. code-block:: python

	from thobject import Object, ValueProperty

	class Box(Object):
		""" A box containing items. """

		item_count = ValueProperty(cls = int)
		price = ValueProperty(cls = float)

Adding boolean properties
-------------------------

For boolean values, it is prefereable to use the following property:

.. code-block:: python

	from thobject import Object, BoolProperty

	class LightSwitch(Object):
		""" A light switch with a state. """

		state = BoolProperty(default = True)

Adding date properties
----------------------

For dates, it is recommended to use the corresponding property, which also
includes the timezone (by default, UTC will be put into the datetime). Here
is an example:

.. code-block:: python

	from thobject import Object, DateProperty
	from pytz import timezone

	class Event(Object):
		""" Some event with example date properties. """

		some_utc_date = DateProperty()
		some_french_date = DateProperty(timezone = timezone('Europe/Paris'))

Adding enumeration properties
-----------------------------

For enumerations where the class is inherited from the standard ``Enum`` class,
you can use the following property:

.. code-block:: python

	from enum import Enum
	from thobject import Object, EnumProperty

	class BiologicalSex(Enum):
		""" Biological sex. """

		OTHER = 0
		MALE = 1
		FEMALE = 2

	class Individual(Object):
		""" Some individual. """

		biological_sex = EnumProperty(enum = biological_sex,
			default = BiologicalSex.OTHER)

Adding array properties
-----------------------

.. todo::

	Document the ``ArrayProperty`` class.

Adding object properties
------------------------

.. todo::

	Document the ``ObjectProperty`` class.

Adding text properties
----------------------

.. todo::

	Document the ``TextProperty`` class.
