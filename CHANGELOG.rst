====================
Length Release Notes
====================

.. contents:: Topics

v0.8.1
======

Minor Changes
-------------

- Add the scaling factor feature, which enables to scale the units to adjust
  the ruler to the object to measure when this object is zoomed,
  for example[`#34`_]

.. _#34: https://github.com/herve4m/length/issues/34

Bugfixes
--------

- Fix the alpha channel being ignore when opacity is set to zero [`#33`_].

.. _#33: https://github.com/herve4m/length/issues/33

v0.7.0
======

Minor Changes
-------------

- Add the relative percentage unit, which enables percentage to be relative to
  the dimensions of the ruler itself [`#27`_]

.. _#27: https://github.com/herve4m/length/issues/27

Bugfixes
--------

- Fix the alpha channel of the custom background color getting ignored [`#28`_].

.. _#28: https://github.com/herve4m/length/issues/28


v0.6.0
======

Minor Changes
-------------

- Use version 48 of the GNOME runtime.


v0.5.0
======

Minor Changes
-------------

- Italian and Dutch translations.


v0.4.0
======

Minor Changes
-------------

- Add a control in the main menu to change the orientation of the ruler.
- Add help (yelp) content.
- Add diagonal rulers when the ruler window is extended.


v0.3.1
======

Bugfixes
--------

- In some environments, the system does not provide a monitor description, which resulted in Length ignoring the monitor. With this fix, Length uses the monitor manufacturer and model when the description is not available.


v0.3.0
======

Minor Changes
-------------

- Add picas and points as units for the ruler.
- Enable calibration of each monitor in a multiple display environment.


v0.2.2
======

Bugfixes
--------

- Fix wrong monitor detection.


v0.2.1
======

Bugfixes
--------

- Fix quality issues per the quality guidelines.
- Fix issue for when GdkMonitor is None.


v0.2.0
======

Bugfixes
--------

- Fix quality issues per the quality guidelines.

Translations
------------

- Italian translation


v0.1.1
======

Bugfixes
--------

- The menu button was barely visible in dark mode. Now the button has a background color that makes it visible.


v0.1.0
======

Release Summary
---------------

Initial release of Length.
