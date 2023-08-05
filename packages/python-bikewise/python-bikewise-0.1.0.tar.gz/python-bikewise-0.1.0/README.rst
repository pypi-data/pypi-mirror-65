python-bikewise
================

A simple `BikeWise <https://www.bikewise.org/>`__ API wrapper.

License: `MIT <https://en.wikipedia.org/wiki/MIT_License>`__.

Installation
------------

::

    pip install python-bikewise

API Examples
------------
Make an instance of the ``BikeWise`` class. For example:

.. code:: python

    from bikewise import BikeWise
    bike = BikeWise()


You can access incident or location information:

- Access the ``incidents`` endpoint if you’d like more detailed information about bike incidents.
- Access the ``locations`` endpoint if you'd like to map incident locations. This endpoint behaves exactly like incidents, but returns a valid geojson.
- Access the ``locations.markers`` endpoint (behaves like root ``locations`` endpoint) to return simplestyled markers (mapbox styled markers).

A table of acceptable parameters for methods in ``BikeWise()``. Note, some parameters are restricted to certain methods - please look at the examples below.

+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ﻿Parameter           | Data Type | Description                                          | Notes                                                                                                                                                                                                             |
+======================+===========+======================================================+===================================================================================================================================================================================================================+
| ``page``             | integer   | Page of results to fetch.                            |                                                                                                                                                                                                                   |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``per_page``         | integer   | Number of results to return per page. Defaults to 25 |                                                                                                                                                                                                                   |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``occurred_before``  | integer   | End of period                                        | Accepts UTC unix timestamps.                                                                                                                                                                                      |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``occurred_after``   | integer   | Start of period                                      | Accepts UTC unix timestamps.                                                                                                                                                                                      |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``incident_type``    | string    | Only incidents of specific type                      |                                                                                                                                                                                                                   |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``proximity``        | string    | Center of location for proximity search              | Accepts an ip address, an address, zipcode, city, or latitude,longitude - i.e. ``70.210.133.87``, ``210 NW 11th Ave, Portland, OR``, ``60647``, ``Chicago, IL``, and ``45.521728,-122.67326`` are all acceptable. |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``proximity_square`` | integer   | Size of the proximity search                         | Sets the length of the sides of the square to find matches inside of. The square is centered on the location specified by ``proximity``.                                                                          |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``query``            | string    | Full text search of incidents                        |                                                                                                                                                                                                                   |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``id``               | integer   | Incident ID                                          |                                                                                                                                                                                                                   |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``limit``            | integer   | Max number of results to return. Defaults to 100     |                                                                                                                                                                                                                   |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``all``              | boolean   | Give ‘em all to me. Will ignore limit                | If you pass the ``all`` parameter it returns all matches (which can be big, > 4mb), otherwise it returns the 100 most recent.                                                                                     |
+----------------------+-----------+------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


Incidents:

.. code:: python

    # incidents method parameters
    """
    bike.incidents(page=0, per_page=25)
    bike.incidents.id(id)
    bike.incidents.features(page=0, per_page=25, occurred_before=0, occurred_after=0,
                            incident_type="", proximity="", proximity_area=0, query="")
    """

    # example
    >>> bike.incidents.features(per_page=1, occurred_after=1440444800, incident_type='theft')
    >>> {'incidents': [{'address': 'Portland, OR, 97227',
                        'description': 'Taken from basement',
                        'id': 115242,
                        'location_description': None,
                        'location_type': None,
                        'media': {'image_url': None, 'image_url_thumb': None},
                        'occurred_at': 1585854000,
                        'source': {'api_url': 'https://bikeindex.org/api/v1/bikes/705265',
                                   'html_url': 'https://bikeindex.org/bikes/705265',
                                   'name': 'BikeIndex.org'},
                        'title': 'Stolen 2018 On-One Dirty Disco(black)',
                        'type': 'Theft',
                        'type_properties': None,
                        'updated_at': 1585862797,
                        'url': 'https://bikewise.org/api/v1/incidents/115242'}]}


Locations & Markers:

.. code:: python

    # locations method parameters
    """
    bike.locations(limit=100, all=False)
    bike.locations.features(occurred_before=0, occurred_after=0, incident_type="", proximity="",
                            proximity_area=0, query="", limit=100, all=False)
    bike.locations.markers(occurred_before=0, occurred_after=0, incident_type="", proximity="",
                           proximity_area=0, query="", limit=100, all=False)
    """

    # example
    >>> bike.locations.features(occurred_after=1440444800, incident_type='theft', limit=1)
    >>> {'features': [{'geometry': {'coordinates': [-122.6766628, 45.5461375],
                                    'type': 'Point'},
                       'properties': {'description': 'Taken from basement <a '
                                                     'href="https://bikeindex.org/bikes/705265" '
                                                     'target="_blank">View details</a>',
                                      'id': 115242,
                                      'marker-color': '#BD1622',
                                      'marker-size': 'small',
                                      'occurred_at': '2020-04-02 14:00:00 -0500',
                                      'title': 'Stolen 2018 On-One Dirty Disco '
                                               '(04-02-2020)'},
                       'type': 'Feature'}],
         'type': 'FeatureCollection'}


Support
-------
If you find any bug or you want to propose a new feature, please use the `issues tracker <https://github.com/irahorecka/python-bikewise/issues>`__. I'll be happy to help!
