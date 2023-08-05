**********************************
MR german books plugin for unidown
**********************************
|maintained| |programming language| |license|

|travis| |requirements| |codacy|

|pypi|

----

Download all available german ebooks from the MobileRead `wiki <https://wiki.mobileread.com/wiki/Free_eBooks-de/de>`__ and the `publication thread <https://www.mobileread.com//forums/showthread.php?t=31130>`__

Lädt alle verfügbaren deutschen eBooks von der MobileRead `Wikiliste <https://wiki.mobileread.com/wiki/Free_eBooks-de/de>`__ und dem `Veröffentlichungsthread <https://www.mobileread.com//forums/showthread.php?t=31130>`__ herunter.

----

Information - *English*
=======================

This is a plugin for `unidown <https://github.com/IceflowRE/unidown>`__, in short unidown manages the already downloaded ebooks and prevents that they will be downloaded again.

Installation
------------

Install `Python <https://www.python.org/downloads/>`__ 3.8 or greater.

Open a terminal and install with:

.. code-block:: shell

    pip install unidown-mr-de

This installs the main program `unidown <https://github.com/IceflowRE/unidown>`__ and this ``mr_de`` plugin.

Usage
-----

Open a terminal and:

.. code-block:: shell

    unidown -p mr_de

Options
-------

There are some options you can choose from:

delay
    Delay (seconds) between the downloads (default: 2s).
include
    Include formats into download, to include unrecognized file types use ``unrecognized`` as part of the options list.
    If no options are given include refers to include all.
exclude
    Include formats into download, to include unrecognized file types use ``unrecognized`` as part of the options list.
    If no options are given exclude refers to exclude nothing.

If both include and exclude are given, it first includes all given formats and then excludes all given excludes.

Example:

.. code-block:: shell

    unidown -p mr_de -o delay=4 -o include=epub,mobi,lrf,imp,pdf,lit,azw,azw3,rar,lrx

.. code-block:: shell

    unidown -p mr_de delay=4 exclude=png,jpg,jpeg,unrecognized

Downloaded files
----------------

By default the program creates a downloads folder in the executing directory. So the ebooks are in ``./downloads/mr_de``.

Notes
-----

You should respect that MobileRead.com is a privately owned, operated and funded community and should not set that delay value to a low value.

Information - *Deutsch*
=======================

Dies ist ein Plugin für das Programm `unidown <https://github.com/IceflowRE/unidown>`__, unidown übernimmt die Verwaltung damit bereits heruntergeladene eBooks nicht nochmal heruntergeladen werden.

Installieren
------------

Installiere `Python <https://www.python.org/downloads/>`__ 3.8 oder höher.

Öffne ein Terminal und installiere es mit:

.. code-block:: shell

    pip install unidown-mr-de

Dies Installiert das Programm `unidown <https://github.com/IceflowRE/unidown>`__ und dieses Plugin.

Benutzung
---------

Öffne ein Terminal und:

.. code-block:: shell

    unidown -p mr_de

Optionen
--------

Es können verschiedene Optionen hinzugefügt werden.

delay
    Verzögerung (Sekunden) zwischen den Downloads (Standard: 2s).
include
    Liste von Formaten zum Downloaden, um Dateitypen zu downloaden die nicht erkannt werden können, muss ``unrecognized`` zur Liste hinzugefügt werden.
    Falls keine Option angegeben wurde, werden alle Typen inkludiert.
exclude
    Liste von Formaten die Ausgeschlossen werden, um Dateitypen auszuschließen die nicht erkannt werden können, muss ``unrecognized`` zur Liste hinzugefügt werden.
    Falls keine Option angegeben wurde, wird kein Typ ausgeschlossen.

Falls beide Optionen angegeben werden, wird erst der include Filter und dann der exclude Filter angewandt.

.. code-block:: shell

    unidown -p mr_de -o delay=4 -o include=epub,mobi,lrf,imp,pdf,lit,azw,azw3,rar,lrx

.. code-block:: shell

    unidown -p mr_de delay=4 exclude=png,jpg,jpeg,unrecognized

Heruntergeladene Dateien
------------------------

Standardmäßig erstellt das Programm in dem Ordner, von dem es ausgeführt wurde, einen Downloadordner. Somit befinden sich die heruntergeladenen eBooks in `./downloads/mr_de`.

Hinweis
-------

Es sollte beachtet werden, dass MobileRead.com privat gegründet und betrieben wird, daher sollte der delay Wert nicht zu gering gesetzt werden.

----

Web
===

https://github.com/IceflowRE/unidown-mr_de

Credits
=======

- Developer
    - `Iceflower S <https://github.com/IceflowRE>`__
        - iceflower@gmx.de

Third Party
-----------

unidown
    - `Iceflower S <https://github.com/IceflowRE>`__
    - https://github.com/IceflowRE/unidown/
    - `GPLv3 <https://github.com/IceflowRE/unidown/blob/master/LICENSE.md>`__
urllib3
    - `Andrey Petrov and contributors <https://github.com/shazow/urllib3/blob/master/CONTRIBUTORS.txt>`_
    - https://github.com/shazow/urllib3
    - `MIT <https://github.com/shazow/urllib3/blob/master/LICENSE.txt>`__

License
-------

.. image:: http://www.gnu.org/graphics/gplv3-127x51.png
   :alt: GPLv3
   :align: center

Copyright (C) 2015-2018 Iceflower S

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

.. Badges.

.. |maintained| image:: https://img.shields.io/badge/maintained-yes-brightgreen.svg

.. |programming language| image:: https://img.shields.io/badge/language-Python_3.7-orange.svg
   :target: https://www.python.org/

.. |license| image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |travis| image:: https://img.shields.io/travis/com/IceflowRE/unidown-mr_de/master.svg?label=Travis%20CI
   :target: https://travis-ci.com/IceflowRE/unidown-mr_de
   
.. |appveyor| image:: https://img.shields.io/appveyor/ci/IceflowRE/unidown-mr-de/master.svg?label=AppVeyor%20CI
    :target: https://ci.appveyor.com/project/IceflowRE/unidown-mr-de/branch/master

.. |requirements| image:: https://requires.io/github/IceflowRE/unidown-mr_de/requirements.svg?branch=master
   :target: https://requires.io/github/IceflowRE/unidown-mr_de/requirements/?branch=master

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/8b542926cd9e445c97545f2245aac712
   :target: https://www.codacy.com/app/IceflowRE/unidown-mr_de

.. |pypi| image:: https://img.shields.io/pypi/v/unidown-mr-de.svg
   :target: https://pypi.org/project/unidown-mr-de/
