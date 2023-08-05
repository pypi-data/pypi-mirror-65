import socket

import mock
import paramiko
from django.core.exceptions import ValidationError
from django.test import TestCase

from openwisp_users.models import Group, Organization

from .. import settings as app_settings
from ..models import Credentials
from .base import CreateConnectionsMixin


class TestModels(CreateConnectionsMixin, TestCase):
    _connect_path = 'paramiko.SSHClient.connect'

    def test_connection_str(self):
        c = Credentials(name='Dev Key', connector=app_settings.CONNECTORS[0][0])
        self.assertIn(c.name, str(c))
        self.assertIn(c.get_connector_display(), str(c))

    def test_device_connection_get_params(self):
        dc = self._create_device_connection()
        self.assertEqual(dc.get_params(), dc.credentials.params)
        dc.params = {'port': 2400}
        self.assertEqual(dc.get_params()['port'], 2400)
        self.assertEqual(dc.get_params()['username'], 'root')

    def test_device_connection_auto_update_strategy(self):
        dc = self._create_device_connection()
        self.assertEqual(dc.update_strategy, app_settings.UPDATE_STRATEGIES[0][0])

    def test_device_connection_auto_update_strategy_key_error(self):
        orig_strategy = app_settings.UPDATE_STRATEGIES
        orig_mapping = app_settings.CONFIG_UPDATE_MAPPING
        app_settings.UPDATE_STRATEGIES = (('meddle', 'meddle'),)
        app_settings.CONFIG_UPDATE_MAPPING = {'wrong': 'wrong'}
        try:
            self._create_device_connection()
        except ValidationError:
            failed = False
        else:
            failed = True
        # restore
        app_settings.UPDATE_STRATEGIES = orig_strategy
        app_settings.CONFIG_UPDATE_MAPPING = orig_mapping
        if failed:
            self.fail('ValidationError not raised')

    def test_device_connection_auto_update_strategy_missing_config(self):
        device = self._create_device(organization=self._create_org())
        self.assertFalse(hasattr(device, 'config'))
        try:
            self._create_device_connection(device=device)
        except ValidationError as e:
            self.assertIn('inferred from', str(e))
        else:
            self.fail('ValidationError not raised')

    def test_device_connection_connector_instance(self):
        dc = self._create_device_connection()
        self.assertIsInstance(dc.connector_instance, dc.connector_class)

    def test_device_connection_ssh_key_param(self):
        ckey = self._create_credentials_with_key()
        dc = self._create_device_connection(credentials=ckey)
        self.assertIn('pkey', dc.connector_instance.params)
        self.assertIsInstance(dc.connector_instance.params['pkey'],
                              paramiko.rsakey.RSAKey)
        self.assertNotIn('key', dc.connector_instance.params)

    @mock.patch(_connect_path)
    def test_ssh_connect(self, mocked_connect):
        ckey = self._create_credentials_with_key(port=self.ssh_server.port)
        dc = self._create_device_connection(credentials=ckey)
        dc.connect()
        mocked_connect.assert_called_once()
        self.assertTrue(dc.is_working)
        self.assertIsNotNone(dc.last_attempt)
        self.assertEqual(dc.failure_reason, '')
        dc.disconnect()

    def test_ssh_connect_failure(self):
        ckey = self._create_credentials_with_key(username='wrong',
                                                 port=self.ssh_server.port)
        dc = self._create_device_connection(credentials=ckey)
        dc.device.last_ip = None
        dc.device.save()
        with mock.patch(self._connect_path) as mocked_connect:
            mocked_connect.side_effect = Exception('Authentication failed.')
            dc.connect()
            mocked_connect.assert_called_once()
        self.assertEqual(dc.is_working, False)
        self.assertIsNotNone(dc.last_attempt)
        self.assertEqual(dc.failure_reason, 'Authentication failed.')

    def test_credentials_schema(self):
        # unrecognized parameter
        try:
            self._create_credentials(params={
                'username': 'root',
                'password': 'password',
                'unrecognized': True
            })
        except ValidationError as e:
            self.assertIn('params', e.message_dict)
        else:
            self.fail('ValidationError not raised')
        # missing password or key
        try:
            self._create_credentials(params={
                'username': 'root',
                'port': 22
            })
        except ValidationError as e:
            self.assertIn('params', e.message_dict)
        else:
            self.fail('ValidationError not raised')

    def test_device_connection_schema(self):
        # unrecognized parameter
        try:
            self._create_device_connection(params={
                'username': 'root',
                'password': 'password',
                'unrecognized': True
            })
        except ValidationError as e:
            self.assertIn('params', e.message_dict)
        else:
            self.fail('ValidationError not raised')

    def _prepare_address_list_test(self, last_ip=None,
                                   management_ip=None):
        update_strategy = app_settings.UPDATE_STRATEGIES[0][0]
        device = self._create_device(organization=self._create_org(),
                                     last_ip=last_ip,
                                     management_ip=management_ip)
        dc = self._create_device_connection(device=device,
                                            update_strategy=update_strategy)
        return dc

    def test_address_list(self):
        dc = self._prepare_address_list_test()
        self.assertEqual(dc.get_addresses(), [])

    def test_address_list_with_device_ip(self):
        dc = self._prepare_address_list_test(
            management_ip='10.0.0.2',
            last_ip='84.32.46.153',
        )
        self.assertEqual(dc.get_addresses(), [
            '10.0.0.2',
            '84.32.46.153'
        ])

    def test_device_connection_credential_org_validation(self):
        dc = self._create_device_connection()
        shared = self._create_credentials(name='cred-shared',
                                          organization=None)
        dc.credentials = shared
        dc.full_clean()
        # ensure credentials of other orgs aren't accepted
        org2 = self._create_org(name='org2')
        cred2 = self._create_credentials(name='cred2',
                                         organization=org2)
        try:
            dc.credentials = cred2
            dc.full_clean()
        except ValidationError as e:
            self.assertIn('credentials', e.message_dict)
        else:
            self.fail('ValidationError not raised')

    def test_auto_add_to_new_device(self):
        c = self._create_credentials(auto_add=True,
                                     organization=None)
        self._create_credentials(name='cred2',
                                 auto_add=False,
                                 organization=None)
        d = self._create_device(organization=Organization.objects.first())
        self._create_config(device=d)
        d.refresh_from_db()
        self.assertEqual(d.deviceconnection_set.count(), 1)
        self.assertEqual(d.deviceconnection_set.first().credentials, c)

    def test_auto_add_to_existing_device_on_creation(self):
        d = self._create_device(organization=Organization.objects.first())
        self._create_config(device=d)
        self.assertEqual(d.deviceconnection_set.count(), 0)
        c = self._create_credentials(auto_add=True,
                                     organization=None)
        org2 = Organization.objects.create(name='org2', slug='org2')
        self._create_credentials(name='cred2',
                                 auto_add=True,
                                 organization=org2)
        d.refresh_from_db()
        self.assertEqual(d.deviceconnection_set.count(), 1)
        self.assertEqual(d.deviceconnection_set.first().credentials, c)
        self._create_credentials(name='cred3',
                                 auto_add=False,
                                 organization=None)
        d.refresh_from_db()
        self.assertEqual(d.deviceconnection_set.count(), 1)
        self.assertEqual(d.deviceconnection_set.first().credentials, c)

    def test_auto_add_to_existing_device_on_edit(self):
        d = self._create_device(organization=Organization.objects.first())
        self._create_config(device=d)
        self.assertEqual(d.deviceconnection_set.count(), 0)
        c = self._create_credentials(auto_add=False,
                                     organization=None)
        org2 = Organization.objects.create(name='org2', slug='org2')
        self._create_credentials(name='cred2',
                                 auto_add=True,
                                 organization=org2)
        d.refresh_from_db()
        self.assertEqual(d.deviceconnection_set.count(), 0)
        c.auto_add = True
        c.full_clean()
        c.save()
        d.refresh_from_db()
        self.assertEqual(d.deviceconnection_set.count(), 1)
        self.assertEqual(d.deviceconnection_set.first().credentials, c)
        # ensure further edits are idempotent
        c.name = 'changed'
        c.full_clean()
        c.save()
        d.refresh_from_db()
        self.assertEqual(d.deviceconnection_set.count(), 1)
        self.assertEqual(d.deviceconnection_set.first().credentials, c)

    _exec_command_path = 'paramiko.SSHClient.exec_command'

    def _exec_command_return_value(self, stdin='', stdout='mocked',
                                   stderr='', exit_code=0):
        stdin_ = mock.Mock()
        stdout_ = mock.Mock()
        stderr_ = mock.Mock()
        stdin_.read().decode('utf8').strip.return_value = stdin
        stdout_.read().decode('utf8').strip.return_value = stdout
        stdout_.channel.recv_exit_status.return_value = exit_code
        stderr_.read().decode('utf8').strip.return_value = stderr
        return (stdin_, stdout_, stderr_)

    @mock.patch(_connect_path)
    def test_device_config_update(self, mocked_connect):
        org1 = self._create_org(name='org1')
        cred = self._create_credentials_with_key(organization=org1, port=self.ssh_server.port)
        device = self._create_device(organization=org1)
        update_strategy = app_settings.UPDATE_STRATEGIES[0][0]
        c = self._create_config(device=device)
        self._create_device_connection(device=device,
                                       credentials=cred,
                                       update_strategy=update_strategy)
        c.config = {
            'interfaces': [
                {
                    'name': 'eth10',
                    'type': 'ethernet',
                    'addresses': [
                        {
                            'family': 'ipv4',
                            'proto': 'dhcp'
                        }
                    ]
                }
            ]
        }
        c.full_clean()

        with mock.patch(self._exec_command_path) as mocked:
            mocked.return_value = self._exec_command_return_value()
            c.save()
            mocked.assert_called_once()
        c.refresh_from_db()
        self.assertEqual(c.status, 'applied')

    @mock.patch(_connect_path)
    def test_ssh_exec_exit_code(self, *args):
        ckey = self._create_credentials_with_key(port=self.ssh_server.port)
        dc = self._create_device_connection(credentials=ckey)
        dc.connector_instance.connect()
        with mock.patch(self._exec_command_path) as mocked:
            mocked.return_value = self._exec_command_return_value(exit_code=1)
            with self.assertRaises(Exception):
                dc.connector_instance.exec_command('trigger_command_not_found')
            dc.connector_instance.disconnect()
            mocked.assert_called_once()

    @mock.patch(_connect_path)
    def test_ssh_exec_timeout(self, *args):
        ckey = self._create_credentials_with_key(port=self.ssh_server.port)
        dc = self._create_device_connection(credentials=ckey)
        dc.connector_instance.connect()
        with mock.patch(self._exec_command_path) as mocked:
            mocked.side_effect = socket.timeout()
            with self.assertRaises(socket.timeout):
                dc.connector_instance.exec_command('trigger_timeout')
            dc.connector_instance.disconnect()
            mocked.assert_called_once()

    @mock.patch(_connect_path)
    def test_ssh_exec_exception(self, *args):
        ckey = self._create_credentials_with_key(port=self.ssh_server.port)
        dc = self._create_device_connection(credentials=ckey)
        dc.connector_instance.connect()
        with mock.patch(self._exec_command_path) as mocked:
            mocked.side_effect = RuntimeError('test')
            with self.assertRaises(RuntimeError):
                dc.connector_instance.exec_command('trigger_exception')
            dc.connector_instance.disconnect()
            mocked.assert_called_once()

    def test_connect_no_addresses(self):
        ckey = self._create_credentials_with_key(port=self.ssh_server.port)
        dc = self._create_device_connection(credentials=ckey)
        dc.device.last_ip = None
        dc.device.management_ip = None
        dc.save()
        with self.assertRaises(ValueError):
            dc.connector_instance.connect()

    def test_operator_group_permissions(self):
        group = Group.objects.get(name='Operator')
        permissions = group.permissions.filter(content_type__app_label='connection')
        self.assertEqual(permissions.count(), 3)

    def test_administrator_group_permissions(self):
        group = Group.objects.get(name='Administrator')
        permissions = group.permissions.filter(content_type__app_label='connection')
        self.assertEqual(permissions.count(), 6)
