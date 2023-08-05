import os

import pytest
import testinfra
import testinfra.utils.ansible_runner

inventory = os.environ['MOLECULE_INVENTORY_FILE']
testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    inventory).get_hosts('all')


def setup_module(module):
    for host in testinfra_hosts:
        testinfra.get_host('ansible://' + host,
                           ansible_inventory=inventory
        ).check_output('echo password123 | kinit admin')


def teardown_module(module):
    for host in testinfra_hosts:
        testinfra.get_host('ansible://' + host,
                           ansible_inventory=inventory
        ).check_output('kdestroy')


@pytest.mark.parametrize('perm', [
    {'name': 'Modify host password', 'right': "write",
     'type': "host", 'attrs': "userpassword"},
    {'name': 'Write host certificate', 'right': "write",
     'type': "host", 'attrs': "usercertificate"},
    {'name': 'Modify host userclass', 'right': "write",
     'type': "host", 'attrs': "userclass"},
    {'name': 'Modify service managedBy attribute', 'right': "write",
     'type': "service", 'attrs': "managedby"},
])
def test_permissions(host, perm):
    result = host.check_output('ipa permission-find "{name}"'.format(**perm))
    assert '1 permission matched' in result
    assert 'Granted rights: {right}'.format(**perm) in result
    assert 'Type: {type}'.format(**perm) in result
    assert 'Effective attributes: {attrs}'.format(**perm) in result


@pytest.mark.parametrize('pri', [
    'Nova Host Management',
])
def test_privilages(host, pri):
    result = host.check_output('ipa privilege-find "{}"'.format(pri))
    assert '1 privilege matched' in result
    assert 'Privilege name: {}'.format(pri) in result
    assert 'Description: {}'.format(pri) in result


def test_privilege_permissions(host):
    pri = 'Nova Host Management'
    perms = [
    'System: add hosts',
    'System: remove hosts',
    'Modify host password',
    'Modify host userclass',
    'System: Modify hosts',
    'Modify service managedBy attribute',
    'System: Add krbPrincipalName to a Host',
    'System: Add Services',
    'System: Remove Services',
    'Revoke certificate',
    'System: manage host keytab',
    'System: Manage host certificates',
    'System: modify services',
    'System: manage service keytab',
    'System: read dns entries',
    'System: remove dns entries',
    'System: add dns entries',
    'System: update dns entries',
    'Retrieve Certificates from the CA',
    ]
    result = host.check_output('ipa privilege-show "{}"'.format(pri))
    assert 'Privilege name: {}'.format(pri) in result
    for perm in perms:
        assert perm.lower() in result.lower()


def test_role(host):
    role = 'Nova Host Manager'
    pri = 'Nova Host Management'
    result = host.check_output('ipa role-show "{}"'.format(role))
    assert 'Role name: {}'.format(role) in result
    assert 'Description: {}'.format(role) in result
    assert 'Privileges: {}'.format(pri) in result
    assert 'nova/test-0.example.test@EXAMPLE.TEST' not in result


@pytest.mark.parametrize('name', [
    'test-0.example.test',
    'test-0.ctlplane.example.test',
    'test-0.external.example.test',
    'test-0.internalapi.example.test',
    'test-0.storage.example.test',
    'test-0.storagemgmt.example.test',
])
def test_hosts(host, name):
    host.run_expect([1], 'ipa host-find {}'.format(name))


@pytest.mark.parametrize('service, subhost', [
    ('HTTP', 'ctlplane'),
    ('HTTP', 'external'),
    ('HTTP', 'internalapi'),
    ('HTTP', 'storage'),
    ('HTTP', 'storagemgmt'),
    ('haproxy', 'ctlplane'),
    ('haproxy', 'internalapi'),
    ('haproxy', 'storage'),
    ('haproxy', 'storagemgmt'),
    ('libvirt-vnc', 'internalapi'),
    ('mysql', 'internalapi'),
    ('neutron_ovn', 'internalapi'),
    ('novnc-proxy', 'internalapi'),
    ('ovn_controller', 'internalapi'),
    ('ovn_dbs', 'internalapi'),
    ('rabbitmq', 'internalapi'),
    ('redis', 'internalapi'),
])
def test_services(host, service, subhost):
    host.run_expect(
        [2],
        'ipa service-show {}/test-0.{}.example.test@EXAMPLE.TEST'.format(
            service, subhost))
