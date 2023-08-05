thobject: create cache-like objects for everyday use
====================================================

thobject tries to make it easy at creating your own objects for simple
cache database-like objects. It became a project on its own from the
`SGDFi <https://sgdfi.touhey.pro/>`_ code base.

Examples
--------

Defining an object.

.. code-block:: python

	from datetime import datetime
	from thobject import (Object, DateProperty, ValueProperty,
		TextProperty)
	from pytz import timezone

	# Define some objects.

	paristz = timezone('Europe/Paris')

	class Event(Object):
		""" An event in our example codebase. It has an URL to identify,
			a name, and start and end dates in the Paris timezone. """

		id = ValueProperty(unique = True, cls = int)
		participants = ValueProperty(cls = int)
		name = TextProperty(lines = 1, not_empty = True)
		start = DateProperty(timezone = paristz)
		end = DateProperty(timezone = paristz)

Creating such an object.

.. code-block:: python

	# First method: all in the constructor.

	event0 = Event(id = 5, name = "hello, world",
		start = datetime(2019, 12, 14, 14, 0),
		end = datetime(2019, 12, 14, 15, 0))

	# Second method: use property set.

	event1 = Event()
	event1.id = 6
	event1.participants = 120
	event1.name = "hello, world"
	event1.start = datetime(2020, 12, 14, 1, 0)
	event1.end = datetime(2020, 12, 15, 1, 0)

Using the cache.

.. code-block:: python

	from thobject import Cache

	cache = Cache()

	# Add the two initial events.

	cache.add(event0)
	cache.add(event1)

	# We want to update event1's participant count.

	cache.add(Event(id = 6, name = "hello, people"), based_on = 'id')
