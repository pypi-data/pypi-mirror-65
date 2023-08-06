.. -*- coding: utf-8 -*-
.. :Project:   SoL -- Introduction
.. :Created:   gio 9 ott 2008 11:40:17 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2008, 2009, 2010, 2013, 2014, 2015, 2016, 2018, 2019, 2020 Lele Gaifax
..

=====================
 Scarry On Lin{e|ux}
=====================

-------------------------------------------------------------
Powerful and complete solution to manage Carrom championships
-------------------------------------------------------------

:version: 4
:author: Lele Gaifax <lele@metapensiero.it>
:license: GPLv3
:status: |pipeline| |coverage|

.. |pipeline| image:: https://gitlab.com/metapensiero/SoL/badges/master/pipeline.svg
   :target: https://gitlab.com/metapensiero/SoL/pipelines/
   :alt: CI build status

.. |coverage| image:: https://gitlab.com/metapensiero/SoL/badges/master/coverage.svg
   :target: https://gitlab.com/metapensiero/SoL/pipelines/
   :alt: Overall test coverage

This project contains some tools that make it easier the organization of a championship of
Carrom_ tournaments using a variant of the `Swiss system`__, or even *everyone against
everyone* events.

__ https://en.wikipedia.org/wiki/Swiss-system_tournament

The main component is a Pyramid_ application serving two distinct user interfaces:

1. A very light, HTML only, read only view of the whole database, where you can actually browse
   thru the clubs, championships, tourneys, players and ratings. You can see it in action on
   the public SoL instance at https://sol4.metapensiero.it/lit/.

2. A complete ExtJS_ based desktop-like application, that exposes all the functionalities
   described below__ in an easy to manage interface.

.. attention:: SoL **requires** Python 3, it does **not** work with Python 2

__ Goals_

.. _Carrom: https://en.wikipedia.org/wiki/Carrom
.. _Pyramid: https://trypyramid.com/
.. _ExtJS: https://www.sencha.com/products/extjs/

.. contents:: :depth: 2


Goals
=====

These are the key points:

1. Multilingual application

   Scarry spoke only Italian, because the i18n mechanism in Delphi (and in general under
   Windows) sucks. Most of the code was written and commented in Italian too, and that made it
   very difficult to get foreign contributions.

2. Multiuser

   There is a *super user* (named “admin” by default) that can do everything, in particular
   create other *normal users*, who can then log in and manage her own tournaments, but can't
   change information owned by other users.

   SoL 4 also implements an optional *self registration* procedure.

3. Real database

   Scarry used Paradox tables, but we are in the third millennium, now: SoL uses a real, even
   if simple and light, SQL database under its skin.

4. Easy to use

   The application is usually driven by computer-illiterated guys, so little to no surprises.

5. Easy to deploy

   Gods know how many hours went in building f*cking installers with BDE goodies!

6. Bring back the fun

   Programming in Python is just that, since the beginning!


High level description
----------------------

The application implements the following features:

* basic tables editing, like adding a new player, opening a new championship, manually tweaking
  the scores, and so on;

* handle a single tourney

  a. compose a list of `competitors`: usually this is just a single player, but there are two
     people in doubles, or more (teams)

  b. set up the first round, made up of `matches`, each pairing two distinct `competitors`: if
     the tournament is associated with a `rating` this considers the Glicko2__ rate of each
     player, otherwise uses a random pairing; either way, the tournament secretary is able to
     manually change the combinations

  c. print the game sheets, where the player will write the scores

  d. possibly show a countdown, to alert the end of the game

  e. insert the score of each match

  f. compute the new ranking

  g. print the current ranking

  h. possibly offer a way to withdraw some competitors, or to add a new competitor

  i. compute the next round

  j. repeat steps c. thru i. usually up to seven rounds

  k. possibly offer a way to go back, delete last round, correct a score and repeat

  l. if required, play up to three final rounds between the first two competitors

  m. recompute the ranking, assigning prizes

  n. update the `rating` the tournament is associated to

* handle a championship of tourneys

  * each tourney is associated to one championship

  * print the championship ranking

* data exchange, to import/export whole tourneys in a portable way

__ https://en.wikipedia.org/wiki/Glicko_rating_system


Installation and Setup
======================

The very first requirement to install an instance of SoL on your own machine is getting Python
3.6 or better\ [#]_. This step obviously depends on the operating system you are using: on most
GNU/Linux distributions it is already available\ [#]_, for example on Debian and derivatives
like Ubuntu the following command will do the task::

  $ apt-get install python3

If instead you are using M$-Windows, you should select the right installer from the downloads__
page on https://www.python.org/.

Another recommended, although optional, add-on is the `DejaVu fonts`__ set, to support a rather
wide range of `glyphs`__ when producing the PDFs printouts. As usual, on GNU/Linux it's a
matter of executing the following command

::

  $ apt-get install fonts-dejavu

or equivalent for your distribution, while on M$-Windows you need to download__ them and
extract the archive in the right location which usually is ``C:\Windows\Fonts``.

__ https://www.python.org/downloads/windows/
__ https://dejavu-fonts.github.io/
__ https://en.wikipedia.org/wiki/Glyph
__ https://sourceforge.net/projects/dejavu/files/dejavu/2.37/dejavu-fonts-ttf-2.37.zip


The good old way
----------------

1. Install ``SoL`` using ``pip``::

    pip install SoL

   that will download the latest version of SoL from PyPI__ and all its dependencies as well

   __ https://pypi.org/project/SoL/

2. Install ExtJS_ 4.2.1::

    python3 -m metapensiero.extjs.desktop

3. Create a standard config file::

    soladmin create-config config.ini

   and edit it as appropriate; you can also directly specify the name and the password of the
   *super user* (by default the name is ``admin`` and the password will be asked
   interactively)::

    soladmin create-config --admin differentone --password str4nge

4. Setup the database::

    soladmin initialize-db config.ini

5. Load official data::

    soladmin restore config.ini

6. Run the application server::

    pserve config.ini

7. Enjoy!
   ::

    firefox http://localhost:6996/

   or, for poor Window$ users or just because using Python makes you
   happier::

    python -m webbrowser http://localhost:6996/


Pre-built Docker image
----------------------

.. note:: This is a work-in-progress facility: better documentation and helper tools are on the
          way! It targets brave souls willing to face a *bleeding edge* experience.

          Current state is based on the work contributed by `Amar Sanakal`__, thank you!

Another option, if you have a 64bit computer, is to run the pre-built Docker_ image.

__ https://bitbucket.org/amar-sanakal/solista
.. _Docker: https://www.docker.com/

Requirements
~~~~~~~~~~~~

First of all, you must enable the *hardware virtualization* in the ``BIOS`` of your computer.

Then you can proceed to install the ``Docker Engine`` for your particular operating system
(that is, `GNU/Linux`__, `Windows`__ or `Mac OS X`__).

After you have tested the install in the ``Docker Quickstart terminal`` (for example as
depicted here__), run the following command in the same window::

  docker run -d -p 80:6996 --name sol amarsanakal/solista

This will start the software and is now accessible on port 80. You can access it as
``http://<ip-address>``.

The ``<ip-address>`` is the ip address of the docker machine running on your PC. This would
have been displayed to you when you launched the Docker Quickstart terminal. You can check it
anytime by running::

  docker-machine ls

the ip address is shown under the URL column. Use that without the port number shown there. See
https://docs.docker.com/machine/get-started/ for more details.

__ https://docs.docker.com/linux/
__ https://docs.docker.com/windows/
__ https://docs.docker.com/mac/
__ https://docs.docker.com/windows/step_three/

Developer's playground
~~~~~~~~~~~~~~~~~~~~~~

If you are a developer and want to play with Docker_, you can checkout SoL sources and

* build an image with ``make docker-build``
* change the admin credentials with ``make docker-change-admin``
* start SoL within a Docker container with ``make docker-start``, then visit
  ``http://localhost:6996/`` as usual

See ``Makefile.docker`` for other related targets.

Roadmap
~~~~~~~

1. Provide some *Unix shell scripts* and *Windows batch files* to make the end users happier
2. Complete this section
3. Figure out how to build a new image on hub.docker.com whenever a new SoL release happens


Development
===========

Since version 4 the development has been moved to GitLab__: the previous repository on
Bitbucket__ is now just a mirror, automatically kept in sync when new commits land on the
primary one.

The complete sources can be downloaded with the following command::

    git clone https://gitlab.com/metapensiero/SoL.git

I recommend using a *virtual environment* to keep you isolated from the system packages::

    python3 -m venv env
    source env/bin/activate

After that, you can setup a development environment by executing the command::

    pip install -r requirements/development.txt

You must then install the required ExtJS 4 sources executing::

    python -m metapensiero.extjs.desktop --src

If you are a developer, you are encouraged to create your own `fork` of the software and
possibly open a `pull request`: I will happily merge your changes!

You can run the tests suite with either

::

    make test

or with a more specific

::

    pytest tests/models

__ https://gitlab.com/metapensiero/SoL
__ https://bitbucket.org/lele/sol


I18N / L10N
-----------

Currently SoL is translated in English\ [#]_, French and Italian. If you know other languages
and want to contribute, the easiest way to create a new translation is to create an account on
the Weblate__ site and follow its `translators guide`__.

.. image:: https://hosted.weblate.org/widgets/sol/-/287x66-white.png
   :target: https://hosted.weblate.org/engage/sol/
   :alt: Translation status
   :align: center

Otherwise if like me you prefer using more traditional tools\ [#]_ you can extract a copy of
the sources and operate directly on the local catalogs under the directory ``src/sol/locale``.

To extract translatable messages use the following command::

    make update-catalogs

To check your work you must compile them with::

    make compile-catalogs

__ https://hosted.weblate.org/projects/sol/
__ https://docs.weblate.org/


Feedback and support
--------------------

If you run in troubles, or want to suggest something, or simply a desire of saying *“Thank
you”* raises up, feel free to contact me via email as ``lele at metapensiero dot it``.

Consider also joining the `dedicated mailing list`__ where you can get in contact with other
users of the application. There is also an `issues tracker`__ where you can open a new tickets
about bugs or enhancements.

__ https://groups.google.com/d/forum/sol-users
__ https://gitlab.com/metapensiero/SoL/issues

-----

.. [#] As of this writing I'm using version 3.7.0 and I'd recommend using that, but SoL used to
       work great with any version higher than 3.4.

.. [#] In fact it may even be already installed!

.. [#] The are actually two distinct catalogs, to take into account US and UK variants.

.. [#] GNU Emacs comes to mind of course, but there are zillions of them: start looking at the
       `gettext page <https://en.wikipedia.org/wiki/Gettext>`_ on Wikipedia.
