#######
SWTools
#######


.. image:: https://img.shields.io/pypi/v/swtools.svg
        :target: https://pypi.python.org/pypi/swtools

.. image:: https://readthedocs.org/projects/swtools/badge/?version=latest
        :target: https://swtools.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



Shortwave CLI tools for SWLing and DXing!
=========================================


SWLookup
--------
**SWLookup** is a command line tool to lookup shortwave frequency data.
Easily lookup a frequency by following the prompts. Local time is optional
but recommended for more accurate results.


SWLing
------
**SWLing** is the command line companion tool to **SWLookup**. It features a
simple menu with pre-built reports to analyze shortwave listening data to
highlight top stations, transmitters, and frequencies. The reports are built
using the data saved to a CSV file with while using the **SWLookup** application.


SWUpdate
--------
**SWUpdate** is a command line companion tool to **SWLookup**. It allows the
update of the shortwave frequency table. Simple run and pick an update file.



* Free software: MIT license
* Documentation: https://swtools.readthedocs.io.



Features
--------
* Lookup schedules for a frequency with optional local time.
* Save shortwave listening session information to a CSV file.
* View shortwave listening history for the current frequency.
* View shortwave listening highlights with SWLing reports.
* Update the shortwave frequency table.


Task List and OFI's
-------------------
* Move ``colorize`` from reports.py to functions.py.
* Remove ``first_digit`` from reports.py.
* Import ``first_digit`` and ``colorize`` from functions.py instead of static methods in reports.py.
* Refactor report paramaters implementation in reports.py to use the ``Prompter`` class.
* Add column for trasnmitter power in history lookup.
* Publish documentation to ``Read The Docs``.


Planned Features
----------------
* Add a new report that lists everything on-air in the xx band for current time and weekday.
* Add a new report to search for a station or program.
* Add dBu quality measurements table and translate to S meter values for diplay.


Data Disclaimer
---------------
At first this tool used the EiBi frequency data. However, since 2019-12-06 it was changed to use
the Aoki BI Newsletter data as the main frequency lookup table. The main reason for the change
was that the data is much simpler to work with. Despite the cons, I felt the data is more
maintainable and easier to update as required. The plan is to eventually merge the two lists.

**Aoki Pros**

* The data is updated more often with program schedule changes
* It simplifies the SQL by eliminating the need for joins to use different code tables
* The station column usually contains the name AND the program simplifying listening discovery
* The days of operation column uses a more consitent data format
* The transmitter location and it's geocoordinates are in separate columns

**Aoki Cons**

* There are less frequencies listed (ex: time signal stations are not included)
* There is no target area information for transmitters
* There is no state/country information for the transmitter location

Please note that this data is *free* and comes with absolutely no guarantees.


Credits
-------

Shortwave schedules are from Aoki's excellent (and free!) `Bi Newsletter`_.

.. _`Bi Newsletter`: http://www1.s2.starcat.ne.jp/ndxc/


Additional information from the excellent (and free!) `EiBi Shortwave Schedules`_.

.. _`EiBi Shortwave Schedules`: http://eibispace.de/


ASCII art logos created with the free `Text to ASCII Art Generator (TAAG)`_ tool using the slant FIGlet font.

.. _`Text to ASCII Art Generator (TAAG)`: http://patorjk.com/software/taag/


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

