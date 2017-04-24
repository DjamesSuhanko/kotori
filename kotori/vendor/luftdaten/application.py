# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@getkotori.org>
import json
from pkg_resources import resource_filename
from jinja2 import Template
from twisted.logger import Logger
from grafana_api_client import GrafanaPreconditionFailedError
from kotori.daq.graphing.grafana import GrafanaManager, GrafanaApi

log = Logger()

class LuftdatenGrafanaManager(GrafanaManager):

    def __init__(self, *args, **kwargs):
        GrafanaManager.__init__(self, *args, **kwargs)
        self.tpl_dashboard_map      = self.get_template('grafana-map.json')
        self.tpl_dashboard_location = self.get_template('grafana-location.json')

    def get_template(self, filename):
        return Template(file(resource_filename('kotori.vendor.luftdaten', filename)).read().decode('utf-8'))

    def provision(self, storage_location, message, topology):

        topology = topology or {}
        dashboard_name = self.strategy.topology_to_label(topology)

        # TODO: Improve locking to prevent race conditions.

        if self._skip_creation(storage_location.database, storage_location.measurement):
            return

        log.info('Provisioning Grafana for database "{}" and series "{}". dashboard={}'.format(
            storage_location.database,
            storage_location.measurement,
            dashboard_name))

        self.create_datasource(storage_location)


        data_dashboard = {
            'database': storage_location.database,
            'measurement': storage_location.measurement,
            'measurement_events': storage_location.measurement_events,
        }
        dashboard_json_map = self.tpl_dashboard_map.render(data_dashboard, title='{name} map automatic'.format(name=dashboard_name))
        dashboard_json_location = self.tpl_dashboard_location.render(data_dashboard, title='{name} location automatic'.format(name=dashboard_name))

        for dashboard_json in [dashboard_json_map, dashboard_json_location]:

            try:
                log.info('Creating/updating dashboard "{}"'.format(dashboard_name))
                response = self.grafana_api.grafana_client.dashboards.db.create(dashboard=json.loads(dashboard_json), overwrite=True)
                log.info(u'Grafana response: {response}', response=json.dumps(response))

            except GrafanaPreconditionFailedError as ex:
                if 'name-exists' in ex.message or 'A dashboard with the same name already exists' in ex.message:
                    log.warn(ex.message)
                else:
                    raise

        # Remember dashboard/panel creation for this kind of data inflow
        self._signal_creation(storage_location.database, storage_location.measurement)
