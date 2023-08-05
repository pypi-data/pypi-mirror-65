import ipaddress
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


@pytest.mark.parametrize('pkg', [
    'ipa-client',
])
def test_pkg(host, pkg):
    package = host.package(pkg)

    assert package.is_installed


@pytest.mark.parametrize('svc', [
    'dbus',
    'sssd',
])
def test_svc(host, svc):
    service = host.service(svc)

    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize('file, content', [
    ("/etc/ipa/default.conf", "ipa.example.test"),
    ("/etc/hosts", "test-0.example.test"),
    ("/etc/resolv.conf", "172.18.0.22"),
    ("/etc/novajoin/krb5.keytab", "test-0.example.test"),
])
def test_files(host, file, content):
    file = host.file(file)

    assert file.exists
    assert file.contains(content)


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
    assert 'Member services: nova/test-0.example.test@EXAMPLE.TEST' in result


@pytest.mark.parametrize('name', [
    'test-0.example.test',
    'test-0.ctlplane.example.test',
    'test-0.external.example.test',
    'test-0.internalapi.example.test',
    'test-0.storage.example.test',
    'test-0.storagemgmt.example.test',
])
def test_hosts(host, name):
    result = host.check_output('ipa host-find {}'.format(name))
    assert '1 host matched' in result


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
    result = host.check_output(
        'ipa service-show {}/test-0.{}.example.test@EXAMPLE.TEST'.format(
            service, subhost))
    assert 'Principal name: {}/test-0.{}.example.test@EXAMPLE.TEST'.format(
        service, subhost) in result
    assert 'Principal alias: {}/test-0.{}.example.test@EXAMPLE.TEST'.format(
        service, subhost) in result
    'Roles: Nova Host Manager' in result
    assert 'Managed by: test-0.{}.example.test, test-0.example.test'.format(
        subhost) in result


@pytest.mark.parametrize('ip, name', [
    ('2001:0db8:85a3:0000:0000:8a2e:0370:7333', 'foo'),
    ('2001:0db8:85a3:0000:0000:8a2e:0370:7333', 'bar'),
    ('192.168.24.111', 'bar'),
    ('192.168.24.1', 'undercloud.ctlplane'),
    ('192.168.24.115', 'overcloud.ctlplane'),
    ('10.0.0.135', 'overcloud'),
    ('172.17.0.15', 'overcloud.internalapi'),
    ('172.18.0.231', 'overcloud.storage'),
    ('172.19.0.164', 'overcloud.storagemgmt'),
    ('172.17.0.46', 'overcloud-controller-0'),
    ('10.0.0.116', 'overcloud-controller-0.external'),
    ('172.17.0.46', 'overcloud-controller-0.internalapi'),
    ('172.18.0.185', 'overcloud-controller-0.storage'),
    ('172.19.0.107', 'overcloud-controller-0.storagemgmt'),
    ('172.16.0.72', 'overcloud-controller-0.tenant'),
    ('192.168.24.122', 'overcloud-controller-0.ctlplane'),
    ('172.17.0.110', 'overcloud-novacompute-0'),
    ('172.17.0.110', 'overcloud-novacompute-0.internalapi'),
    ('172.18.0.243', 'overcloud-novacompute-0.storage'),
    ('172.16.0.195', 'overcloud-novacompute-0.tenant'),
    ('192.168.24.128', 'overcloud-novacompute-0.ctlplane')])
def test_dns(host, ip, name):
    result = host.check_output(
        'ipa dnsrecord-find ooo.test --name={}'.format(
            name))
    assert 'record: {}'.format(ip) in result


@pytest.mark.parametrize('ip, name', [
    ('2001:0db8:85a3:0000:0000:8a2e:0370:7334', 'foo'),
    ('2001:0db8:85a3:0000:0000:8a2e:0370:7333', 'bar'),
    ('192.168.24.111', 'bar'),
    ('192.168.24.1', 'undercloud.ctlplane'),
    ('192.168.24.115', 'overcloud.ctlplane'),
    ('10.0.0.135', 'overcloud'),
    ('172.17.0.15', 'overcloud.internalapi'),
    ('172.18.0.231', 'overcloud.storage'),
    ('172.19.0.164', 'overcloud.storagemgmt'),
    ('172.17.0.46', 'overcloud-controller-0'),
    ('10.0.0.116', 'overcloud-controller-0.external'),
    ('172.17.0.46', 'overcloud-controller-0.internalapi'),
    ('172.18.0.185', 'overcloud-controller-0.storage'),
    ('172.19.0.107', 'overcloud-controller-0.storagemgmt'),
    ('172.16.0.72', 'overcloud-controller-0.tenant'),
    ('192.168.24.122', 'overcloud-controller-0.ctlplane'),
    ('172.17.0.110', 'overcloud-novacompute-0'),
    ('172.17.0.110', 'overcloud-novacompute-0.internalapi'),
    ('172.18.0.243', 'overcloud-novacompute-0.storage'),
    ('172.16.0.195', 'overcloud-novacompute-0.tenant'),
    ('192.168.24.128', 'overcloud-novacompute-0.ctlplane')])
def test_reverse_dns(host, ip, name):
    reverse = ipaddress.ip_address(ip).reverse_pointer
    record, zone = reverse.split('.', 1)
    result = host.check_output(
        'ipa dnsrecord-find {} --name={}'.format(
            zone, record))
    assert 'record: {}'.format(name) in result
