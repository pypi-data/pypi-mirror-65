# Copyright 2020 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import copy

from tripleo_ipa.ansible_plugins.filter import service_metadata
from tripleo_ipa.tests import base as tests_base

# Short-hand prefixes
MS = 'managed_service_'
CS = 'compact_service_'


class TestParseServiceMetadata(tests_base.TestCase):

    def setUp(self):
        super(TestParseServiceMetadata, self).setUp()

    def test_parse_service_metadata(self):

        domain = 'example.test'
        host_fqdn = 'test-0.' + domain
        md = {
            CS + 'HTTP': [
                'ctlplane', 'storage', 'storagemgmt', 'internalapi', 'external'
            ],
            CS + 'haproxy': ['ctlplane', 'storage', 'storagemgmt', 'internalapi'],
            CS + 'libvirt-vnc': ['internalapi'],
            CS + 'mysql': ['internalapi'],
            CS + 'neutron_ovn': ['internalapi'],
            CS + 'novnc-proxy': ['internalapi'],
            CS + 'ovn_controller': ['internalapi'],
            CS + 'ovn_dbs': ['internalapi'],
            CS + 'rabbitmq': ['internalapi'],
            CS + 'redis': ['internalapi'],
            MS + 'haproxyctlplane': 'haproxy/test-0.ctlplane.' + domain,
            MS + 'haproxyexternal': 'haproxy/test-0.' + domain,
            MS + 'haproxyinternal_api': 'haproxy/test-0.internalapi.' + domain,
            MS + 'haproxystorage': 'haproxy/test-0.storage.' + domain,
            MS + 'haproxystorage_mgmt': 'haproxy/test-0.storagemgmt.' + domain,
            MS + 'mysqlinternal_api': 'mysql/test-0.internalapi.' + domain,
            MS + 'ovn_dbsinternal_api': 'ovn_dbs/test-0.internalapi.' + domain,
            MS + 'redisinternal_api': 'redis/test-0.internalapi.' + domain
        }

        expected_services = [
            ('test-0.ctlplane.example.test', 'HTTP'),
            ('test-0.storage.example.test', 'HTTP'),
            ('test-0.storagemgmt.example.test', 'HTTP'),
            ('test-0.internalapi.example.test', 'HTTP'),
            ('test-0.external.example.test', 'HTTP'),
            ('test-0.ctlplane.example.test', 'haproxy'),
            ('test-0.example.test', 'haproxy'),
            ('test-0.internalapi.example.test', 'haproxy'),
            ('test-0.storage.example.test', 'haproxy'),
            ('test-0.storagemgmt.example.test', 'haproxy'),
            ('test-0.internalapi.example.test', 'libvirt-vnc'),
            ('test-0.internalapi.example.test', 'mysql'),
            ('test-0.internalapi.example.test', 'neutron_ovn'),
            ('test-0.internalapi.example.test', 'novnc-proxy'),
            ('test-0.internalapi.example.test', 'ovn_controller'),
            ('test-0.internalapi.example.test', 'ovn_dbs'),
            ('test-0.internalapi.example.test', 'rabbitmq'),
            ('test-0.internalapi.example.test', 'redis')
        ]

        services = service_metadata.parse_service_metadata(md, host_fqdn)
        self.assertEqual(len(services), len(expected_services))
        for service in services:
            self.assertIn(service, expected_services)

    def test_parse_service_metadata_with_long_domain_name(self):

        domain = 'cloud.example.test'
        host_fqdn = 'test-0.' + domain
        md = {
            CS + 'HTTP': [
                'ctlplane', 'storage', 'storagemgmt', 'internalapi', 'external'
            ],
            CS + 'haproxy': ['ctlplane', 'storage', 'storagemgmt', 'internalapi'],
            CS + 'libvirt-vnc': ['internalapi'],
            CS + 'mysql': ['internalapi'],
            CS + 'neutron_ovn': ['internalapi'],
            CS + 'novnc-proxy': ['internalapi'],
            CS + 'ovn_controller': ['internalapi'],
            CS + 'ovn_dbs': ['internalapi'],
            CS + 'rabbitmq': ['internalapi'],
            CS + 'redis': ['internalapi'],
            MS + 'haproxyctlplane': 'haproxy/test-0.ctlplane.' + domain,
            MS + 'haproxyexternal': 'haproxy/test-0.' + domain,
            MS + 'haproxyinternal_api': 'haproxy/test-0.internalapi.' + domain,
            MS + 'haproxystorage': 'haproxy/test-0.storage.' + domain,
            MS + 'haproxystorage_mgmt': 'haproxy/test-0.storagemgmt.' + domain,
            MS + 'mysqlinternal_api': 'mysql/test-0.internalapi.' + domain,
            MS + 'ovn_dbsinternal_api': 'ovn_dbs/test-0.internalapi.' + domain,
            MS + 'redisinternal_api': 'redis/test-0.internalapi.' + domain
        }

        expected_services = [
            ('test-0.ctlplane.cloud.example.test', 'HTTP'),
            ('test-0.storage.cloud.example.test', 'HTTP'),
            ('test-0.storagemgmt.cloud.example.test', 'HTTP'),
            ('test-0.internalapi.cloud.example.test', 'HTTP'),
            ('test-0.external.cloud.example.test', 'HTTP'),
            ('test-0.ctlplane.cloud.example.test', 'haproxy'),
            ('test-0.cloud.example.test', 'haproxy'),
            ('test-0.internalapi.cloud.example.test', 'haproxy'),
            ('test-0.storage.cloud.example.test', 'haproxy'),
            ('test-0.storagemgmt.cloud.example.test', 'haproxy'),
            ('test-0.internalapi.cloud.example.test', 'libvirt-vnc'),
            ('test-0.internalapi.cloud.example.test', 'mysql'),
            ('test-0.internalapi.cloud.example.test', 'neutron_ovn'),
            ('test-0.internalapi.cloud.example.test', 'novnc-proxy'),
            ('test-0.internalapi.cloud.example.test', 'ovn_controller'),
            ('test-0.internalapi.cloud.example.test', 'ovn_dbs'),
            ('test-0.internalapi.cloud.example.test', 'rabbitmq'),
            ('test-0.internalapi.cloud.example.test', 'redis')
        ]

        services = service_metadata.parse_service_metadata(md, host_fqdn)
        self.assertEqual(len(services), len(expected_services))
        for service in services:
            self.assertIn(service, expected_services)
