Checkmk Commander
=================

Efficient Curses interface for Checkmk Raw, <https://checkmk.com/>.

![Logo](https://gitlab.com/larsfp/checkmk-commander/-/raw/master/images/logo_256.png)

The goal is not to completely avoid the web interface, but to speed up common day-to-day tasks. Actions like acknowledge, downtime, reinventorize can be done in seconds, with keyboard only. Overview is clean and simple.

Beta quality. Can be used, but report bugs!

Project home: <https://gitlab.com/larsfp/checkmk-commander>

Screenshots
-----------

![Acknowledge and help v.8](https://gitlab.com/larsfp/checkmk-commander/-/raw/master/images/ack0.8.gif)

![Details v.6](https://gitlab.com/larsfp/checkmk-commander/-/raw/master/images/Screenshotv.6.png)

![Overview v.3](https://gitlab.com/larsfp/checkmk-commander/-/raw/master/images/Screenshotv.3.png)

Installation
------------

From PIP:

```bash
pip3 install checkmk-commander
```

Run command: chkcom

Hot-keys
--------

Press ? in app to get an overview.

Implementation details and limitations
--------------------------------------

Uses CheckMK's web API. You need an "machine" account with a secret. A normal user won't work.

High pri features
-----------------

* [x] list service problems from several checkmk instances
* [x] ack service problems
  * [x] Show popup to add comment
  * [x] Parse time from comment
  * [x] ack service problems on all sites, not just main host
* [x] ack host problems
* [x] downtime service problems
* [x] comment service problems
* [x] show down hosts

Medium pri features
----------------

* [ ] list (distributed monitoring) site statuses
* [x] Reinventorize a host
* [x] Make actions async
* [x] Add logging
* [ ] show service problem count

Low pri features
----------------

* [x] Ability to run remotely (without being on checkmk host)
* [ ] Reschedule check
* [ ] Add new host?
* [ ] Search in alert list
* [ ] Search in all host/services
* [ ] Sort alert list
* [ ] Act on more than one alert at a time?
* [ ] if running locally, fetch secret from var/check_mk/web/USER/automation.secret
* [ ] Show in overview that comments on a service exists
* [ ] List event notifications
* [ ] List hosts/services in downtime

TODO
----

* Improve readability, colors.
* Clean up code.
* Find down time for down-alerts.
* Fetch host comments for down hosts.
* Status bar at bottom should perhaps be switched for a scrolling textview with "Host- and Service events"
* Icon, desktop integration. <https://pypi.org/project/install-freedesktop/>
* I can only assume syslog is os dependent.
* Write unit tests

Development
-----------

Tests can be run with ```tox```.

Inspirations and help
---------------------

* Icon made by RallyPointComic <https://anus.no/>
* <https://github.com/aranair/rtscli/>
* <https://forum.checkmk.com/t/writing-to-nagios-cmd-in-distributed-monitoring/17616>
* <https://checkmk.com/cms_legacy_multisite_automation.html>
