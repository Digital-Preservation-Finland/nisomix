MIX Library
===========

This repository contains general Python functions for MIX 2.0 XML handling.

Installation
------------

Installation and usage requires Python 3.6 or newer.
The software is tested with Python 3.6 on Centos 7.x release.

Create a virtual environment::
    
    python3 -m venv venv

Run the following to activate the virtual environment::

    source venv/bin/activate

Install the required software with commands::

    pip install --upgrade pip==20.2.4 setuptools
    pip install -r requirements_github.txt
    pip install .

To deactivate the virtual environment, run ``deactivate``.
To reactivate it, run the ``source`` command above.

Usage
-----

Import the library with::

    import nisomix
  
All the functions can now be used with calling nisomix.<function>.

For example, the image_characteristics() function in image_information_base.py
can be used with::

    img = nisomix.image_characteristics(width=200, height=400, ...)

This creats a MIX <BasicImageCharacteristics> element with <imageWidth> and 
<imageHeight> to img as lxml.etree.

Most container elements are created using own functions. Subelements as
lxml.etree data types are added to the parent as a list using the
child_elements function argument where applicable.

Elements with textual content are added as arguments for their parent function.
They accept strings or integers when applicable (see the MIX schema for
element content types). Repeating elements can be given as a list containing
the element values as list items. Rational type elements can likewise be given
as a list, with the list items containing the numerator and the denominator
values.

Several elements accepted only a restricted set of values. These values are
documented in the MIX schema.

The two functions image_data and gps_data that return the MIX <ImageData> and
<GPSData> elements respectively accept a contents dictionary as argument. The
dictionary keys are matched to corresponding elements. The empty dictionaries
can be imported using the IMAGE_DATA_CONTENTS and GPS_DATA_CONTENTS global
variables and then populated with data that is passed to the functions. Import
the dictionaries like this::

    contents = nisomix.IMAGE_DATA_CONTENTS

Please, see the MIX documentation for more information:
https://www.loc.gov/standards/mix/

Copyright
---------
Copyright (C) 2018 CSC - IT Center for Science Ltd.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>.
