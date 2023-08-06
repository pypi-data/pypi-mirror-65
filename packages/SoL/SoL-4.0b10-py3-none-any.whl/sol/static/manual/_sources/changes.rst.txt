.. -*- coding: utf-8 -*-

Changes
-------

4.0b10 (2020-04-14)
~~~~~~~~~~~~~~~~~~~

* Fix deployment issues


4.0b9 (2020-04-14)
~~~~~~~~~~~~~~~~~~

* Fix deployment issues


4.0b8 (2020-04-14)
~~~~~~~~~~~~~~~~~~

* New optional "social site" URL on tournaments

* Store all boards misses, not just the totals


4.0b7 (2020-04-09)
~~~~~~~~~~~~~~~~~~

* Show both the scores and the errors in the training tournament's Lit view


4.0b6 (2020-04-08)
~~~~~~~~~~~~~~~~~~

* Fix bug that allowed the self-insertion to only one of the competitors...


4.0b5 (2020-04-08)
~~~~~~~~~~~~~~~~~~
:note: one month of captivity...

* Other minor tweaks to "Corona Carrom" management


4.0b4 (2020-04-07)
~~~~~~~~~~~~~~~~~~

* Minor tweaks to "Corona Carrom" management


4.0b3 (2020-04-05)
~~~~~~~~~~~~~~~~~~

* Restore "email" and "language" on players, removed in 4.0a5

* Add support for "Corona Carrom", “El Carrom en los tiempos del Covid-19”


4.0b2 (2020-02-15)
~~~~~~~~~~~~~~~~~~

* Highlight winners in the results printout, as suggested by Carlito

* New "donations" section in the user's manuals (still draft!)


4.0b1 (2020-02-10)
~~~~~~~~~~~~~~~~~~

* New introductory chapter in the user manual, thanks to Elisa for the preliminary text

* New "world" fake country and icon, for international federations

* Add an entry in the main menu to change account's UI language

* Take into account the selected round when printing tourney's matches, for consistency with
  the results printout

* Use darkblue instead of red to highlight winners, as red may suggest an error condition


4.0a10 (2020-02-06)
~~~~~~~~~~~~~~~~~~~

* Add a rating on the clubs, used as default when creating new associated championships

* Clearer identification of ratings, showing their level and associated club, if any


4.0a9 (2020-02-05)
~~~~~~~~~~~~~~~~~~

* Show the user's email in the "owner" lookup, to avoid name clashes

* Fix serialization of the new hosting club tourney's attribute

* New button to start the countdown after 60 seconds

* Fix the actions deactivation logic based on the owner id for new records


4.0a8 (2020-02-01)
~~~~~~~~~~~~~~~~~~

* Add a rating on the championships, used as default when creating new associated tournaments


4.0a7 (2020-01-31)
~~~~~~~~~~~~~~~~~~

* Revise the obfuscation algorithm of player names, using an hash of the original one instead
  of simple truncation, to avoid conflicts; also, from now on it gets applied also to the
  exported streams

* Highlight the not-yet-scored matches in the tourney management window

* Allow emblems and portraits up to 512Kb in size


4.0a6 (2020-01-29)
~~~~~~~~~~~~~~~~~~

* Nicer rendering of the main Lit page

* Simpler way to open the Lit page of a tourney from its management window

* Allow to save partial results, to be on the safe side when there are lots of boards

* Show the "hosting club" on all printouts, if present


4.0a5 (2020-01-25)
~~~~~~~~~~~~~~~~~~

* Remove "email", "language" and "phone" from players data

* Remove player's rate from participants printout

* Omit the player's club in the ranking printout for international tourneys

* Add the player's nationality in matches and results printouts

* Add an "hosting club" to tournaments


4.0a4 (2020-01-18)
~~~~~~~~~~~~~~~~~~

* New association between clubs and users: now a user may add a
  championship/tourney/rating/player only to clubs he either owns or is associated with

* Add a link to send an email to the instance' admin on the login panel


4.0a3 (2020-01-13)
~~~~~~~~~~~~~~~~~~

* Use a three-state flag for the player's *agreed privacy*: when not explicitly expressed, SoL
  assumes they are publicly discernible if they participated to tournaments after January 1,
  2020

* Player's first and last names must be longer that one single character


4.0a2 (2020-01-11)
~~~~~~~~~~~~~~~~~~

* Fix issue with UI language negotiation

* Use the better maintained `Fomantic-UI`__ fork of `Semantic-UI`__ in the “Lit” interface

__ https://fomantic-ui.com/
__ https://semantic-ui.com/

* New tournaments *delay compatriots pairing* option

* Technicalities:

  * Official repository is now https://gitlab.com/metapensiero/SoL

  * NixOS__ recipes (thanks to azazel@metapensiero.it)

__ https://nixos.org/


4.0a1 (2018-08-06)
~~~~~~~~~~~~~~~~~~

.. warning:: Backward **incompatible** version

   This release uses a different algorithm to crypt the user's password: for this reason
   previous account credentials cannot be restored and shall require manual intervention.

   It's **not** possible to *upgrade* an existing SoL3 database to the latest version.

   However, SoL4 is able to import a backup of a SoL3 database made by ``soladmin backup``.

* Different layout for matches and results printouts, using two columns for the competitors to
  improve readability (suggested by Daniele)

* New tournaments *retirements policy*

* New "women" and "under xx" tourney's ranking printouts

* New “self sign up” procedure

* New “forgot password” procedure

* New "agreed privacy" on players

* Somewhat prettier “Lit” interface, using `Semantic-UI tables`__

* Technicalities:

  * Development moved to GitLab__

  * Officially supported on Python 3.6 and 3.7, not anymore on <=3.5

  * Shiny new pytest-based tests suite

  * Uses `python-rapidjson`__ instead `nssjson`__, as I officially declared the latter as
    *abandoned*

  * Uses `PyNaCl`__ instead of `cryptacular`__, as the former is much better maintained

  * "Users" are now a separated entity from "players": now the login "username" is a mandatory
    email and the password must be longer than **five** characters (was three before)


__ https://semantic-ui.com/collections/table.html
__ https://gitlab.com/metapensiero/SoL
__ https://pypi.org/project/python-rapidjson/
__ https://pypi.org/project/nssjson/
__ https://pypi.org/project/PyNaCl/
__ https://pypi.org/project/cryptacular/
