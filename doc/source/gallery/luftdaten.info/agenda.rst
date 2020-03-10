########################
Luftdatenpumpe v0 Agenda
########################

.. contents::
   :local:
   :depth: 1

----


************
Introduction
************
- http://luftdaten.info/
- http://deutschland.maps.luftdaten.info/


*****
Goals
*****
- https://grafana.com/plugins/grafana-worldmap-panel


***********
Walkthrough
***********

Import CSV data
===============
::

    cd ~/dev/foss/contrib/luftdaten.info/archive.luftdaten.info/2017-02-25

    cat 2017-02-25_sds011_sensor_777.csv | http POST http://luftdaten.getkotori.org/api/luftdaten/testdrive/earth/42/data Content-Type:text/csv --timeout 500

    HTTP/1.1 200 OK
    Channel-Id: /mqttkit-1/testdrive/earth/42
    Content-Type: application/json
    Date: Tue, 28 Mar 2017 22:56:52 GMT
    Server: TwistedWeb/17.1.0
    Transfer-Encoding: chunked

    [
        {
            "message": "Received header fields ['sensor_id', 'sensor_type', 'location', 'lat', 'lon', 'time', 'P1', 'durP1', 'ratioP1', 'P2', 'durP2', 'ratioP2']",
            "type": "info"
        },
        {
            "message": "Received #22 readings",
            "type": "info"
        }
    ]

We added `commit 49256945 <https://github.com/daq-tools/kotori/commit/49256945>`_
to make Kotori conveniently grok the CSV format used by http://archive.luftdaten.info/::

    # Convenience hack to support import from http://archive.luftdaten.info/
    elif first_line.startswith('sensor_id'):
        header_line = first_line
        data_lines.pop(0)


Grafana Worldmap Plugin
=======================

Setup
-----
https://grafana.com/plugins/grafana-worldmap-panel/installation


References
----------
- https://github.com/grafana/worldmap-panel/issues/9#issuecomment-224861471
- https://github.com/grafana/worldmap-panel/pull/20
- https://github.com/grafana/worldmap-panel/issues/30
- https://stackoverflow.com/questions/38213098/grafana-worldmap-panel-with-influxdb
- https://stackoverflow.com/questions/39154884/grafana-worldmap-panel-with-influxdb-doesnt-show-points



Vendor configuration
====================

https://github.com/daq-tools/kotori/blob/0.22.1/etc/examples/vendors/luftdaten.ini

Add vendor configuration to Kotori::

    # Activate
    root@elbanco:/etc/kotori/apps-enabled# ln -s ../apps-available/luftdaten.ini .

    # Bounce daemon
    systemctl restart kotori


*****
Ready
*****

Phase 1
=======
Import CSV data (see above).
[29.03.17 02:18:04] Andreas Motl: ready: https://luftdaten.getkotori.org/

Phase 2
=======
Feed data from live data API from luftdaten.info to MQTT using
`luftdatenpumpe.py <https://github.com/daq-tools/kotori/blob/0.22.1/kotori/vendor/luftdaten/luftdatenpumpe.py>`_.

[29.03.17 16:44:09] Richard Pobering: ping. ich habe das dashboard jetzt inhaltlich nochmal ein bisschen angepasst:

    - https://luftdaten.getkotori.org/grafana/dashboard/db/luftdaten-testdrive-automatic

Phase 3
=======
November 2018 - February 2019

- https://weather.hiveeyes.org/grafana/dashboards/f/NFeP70fik/luft-ldi
- https://community.hiveeyes.org/t/erneuerung-der-luftdatenpumpe/1199
- https://community.hiveeyes.org/t/ldi-data-plane-v2/1412
