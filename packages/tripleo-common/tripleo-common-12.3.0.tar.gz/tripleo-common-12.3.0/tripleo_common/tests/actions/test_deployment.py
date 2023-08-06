# Copyright 2016 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import json
import mock

from heatclient import exc as heat_exc
from mistral_lib import actions
from swiftclient import exceptions as swiftexceptions

from tripleo_common.actions import deployment
from tripleo_common.tests import base


class OrchestrationDeployActionTest(base.TestCase):

    def setUp(self,):
        super(OrchestrationDeployActionTest, self).setUp()
        self.server_id = 'server_id'
        self.config = 'config'
        self.name = 'name'
        self.input_values = []
        self.action = 'CREATE'
        self.signal_transport = 'TEMP_URL_SIGNAL'
        self.timeout = 300
        self.group = 'script'

    def test_extract_container_object_from_swift_url(self):
        swift_url = 'https://example.com' + \
            '/v1/a422b2-91f3-2f46-74b7-d7c9e8958f5d30/container/object' + \
            '?temp_url_sig=da39a3ee5e6b4&temp_url_expires=1323479485'

        action = deployment.OrchestrationDeployAction(self.server_id,
                                                      self.config, self.name,
                                                      self.timeout)
        self.assertEqual(('container', 'object'),
                         action._extract_container_object_from_swift_url(
                             swift_url))

    @mock.patch(
        'heatclient.common.deployment_utils.build_derived_config_params')
    def test_build_sc_params(self, build_derived_config_params_mock):
        build_derived_config_params_mock.return_value = 'built_params'
        action = deployment.OrchestrationDeployAction(self.server_id,
                                                      self.config, self.name)
        self.assertEqual('built_params', action._build_sc_params('swift_url'))
        build_derived_config_params_mock.assert_called_once()

    @mock.patch('tripleo_common.actions.base.TripleOAction.get_object_client')
    def test_wait_for_data(self, get_obj_client_mock):
        mock_ctx = mock.MagicMock()

        swift = mock.MagicMock()
        swift.get_object.return_value = ({}, 'body')
        get_obj_client_mock.return_value = swift

        action = deployment.OrchestrationDeployAction(self.server_id,
                                                      self.config, self.name)
        self.assertEqual('body', action._wait_for_data('container',
                                                       'object',
                                                       context=mock_ctx))
        get_obj_client_mock.assert_called_once()
        swift.get_object.assert_called_once_with('container', 'object')

    @mock.patch('tripleo_common.actions.base.TripleOAction.get_object_client')
    @mock.patch('time.sleep')
    def test_wait_for_data_timeout(self, sleep, get_obj_client_mock):
        mock_ctx = mock.MagicMock()
        swift = mock.MagicMock()
        swift.get_object.return_value = ({}, None)
        get_obj_client_mock.return_value = swift

        action = deployment.OrchestrationDeployAction(self.server_id,
                                                      self.config, self.name,
                                                      timeout=10)
        self.assertIsNone(action._wait_for_data('container',
                                                'object',
                                                context=mock_ctx))
        get_obj_client_mock.assert_called_once()
        swift.get_object.assert_called_with('container', 'object')
        # Trying every 3 seconds, so 4 times for a timeout of 10 seconds
        self.assertEqual(swift.get_object.call_count, 4)

    @mock.patch('tripleo_common.actions.base.TripleOAction.get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    @mock.patch('heatclient.common.deployment_utils.create_temp_url')
    @mock.patch('tripleo_common.actions.deployment.OrchestrationDeployAction.'
                '_extract_container_object_from_swift_url')
    @mock.patch('tripleo_common.actions.deployment.OrchestrationDeployAction.'
                '_build_sc_params')
    @mock.patch('tripleo_common.actions.deployment.OrchestrationDeployAction.'
                '_wait_for_data')
    def test_run(self, wait_for_data_mock, build_sc_params_mock,
                 extract_from_swift_url_mock, create_temp_url_mock,
                 get_heat_mock, get_obj_client_mock):
        extract_from_swift_url_mock.return_value = ('container', 'object')
        mock_ctx = mock.MagicMock()
        build_sc_params_mock.return_value = {'foo': 'bar'}
        config = mock.MagicMock()
        sd = mock.MagicMock()
        get_heat_mock().software_configs.create.return_value = config
        get_heat_mock().software_deployments.create.return_value = sd
        wait_for_data_mock.return_value = '{"deploy_status_code": 0}'

        action = deployment.OrchestrationDeployAction(self.server_id,
                                                      self.config, self.name)
        expected = actions.Result(
            data={"deploy_status_code": 0},
            error=None)
        self.assertEqual(expected, action.run(context=mock_ctx))
        create_temp_url_mock.assert_called_once()
        extract_from_swift_url_mock.assert_called_once()
        build_sc_params_mock.assert_called_once()
        get_obj_client_mock.assert_called_once()
        wait_for_data_mock.assert_called_once()

        sd.delete.assert_called_once()
        config.delete.assert_called_once()
        get_obj_client_mock.delete_object.called_once_with('container',
                                                           'object')
        get_obj_client_mock.delete_container.called_once_with('container')

    @mock.patch('tripleo_common.actions.base.TripleOAction.get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    @mock.patch('heatclient.common.deployment_utils.create_temp_url')
    @mock.patch('tripleo_common.actions.deployment.OrchestrationDeployAction.'
                '_extract_container_object_from_swift_url')
    @mock.patch('tripleo_common.actions.deployment.OrchestrationDeployAction.'
                '_build_sc_params')
    @mock.patch('tripleo_common.actions.deployment.OrchestrationDeployAction.'
                '_wait_for_data')
    def test_run_timeout(self, wait_for_data_mock, build_sc_params_mock,
                         extract_from_swift_url_mock, create_temp_url_mock,
                         get_heat_mock, get_obj_client_mock):
        extract_from_swift_url_mock.return_value = ('container', 'object')
        mock_ctx = mock.MagicMock()
        config = mock.MagicMock()
        sd = mock.MagicMock()
        get_heat_mock().software_configs.create.return_value = config
        get_heat_mock().software_deployments.create.return_value = sd
        wait_for_data_mock.return_value = None

        action = deployment.OrchestrationDeployAction(self.server_id,
                                                      self.config, self.name)
        expected = actions.Result(
            data={},
            error="Timeout for heat deployment 'name'")
        self.assertEqual(expected, action.run(mock_ctx))

        sd.delete.assert_called_once()
        config.delete.assert_called_once()
        get_obj_client_mock.delete_object.called_once_with('container',
                                                           'object')
        get_obj_client_mock.delete_container.called_once_with('container')

    @mock.patch('tripleo_common.actions.base.TripleOAction.get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    @mock.patch('heatclient.common.deployment_utils.create_temp_url')
    @mock.patch('tripleo_common.actions.deployment.OrchestrationDeployAction.'
                '_extract_container_object_from_swift_url')
    @mock.patch('tripleo_common.actions.deployment.OrchestrationDeployAction.'
                '_build_sc_params')
    @mock.patch('tripleo_common.actions.deployment.OrchestrationDeployAction.'
                '_wait_for_data')
    def test_run_failed(self, wait_for_data_mock, build_sc_params_mock,
                        extract_from_swift_url_mock, create_temp_url_mock,
                        get_heat_mock, get_obj_client_mock):
        extract_from_swift_url_mock.return_value = ('container', 'object')
        mock_ctx = mock.MagicMock()
        config = mock.MagicMock()
        sd = mock.MagicMock()
        get_heat_mock().software_configs.create.return_value = config
        get_heat_mock().software_deployments.create.return_value = sd
        wait_for_data_mock.return_value = '{"deploy_status_code": 1}'

        action = deployment.OrchestrationDeployAction(self.server_id,
                                                      self.config, self.name)
        expected = actions.Result(
            data={"deploy_status_code": 1},
            error="Heat deployment failed for 'name'")
        self.assertEqual(expected, action.run(mock_ctx))

        sd.delete.assert_called_once()
        config.delete.assert_called_once()
        get_obj_client_mock.delete_object.called_once_with('container',
                                                           'object')
        get_obj_client_mock.delete_container.called_once_with('container')


class OvercloudRcActionTestCase(base.TestCase):
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    def test_no_stack(self, mock_get_orchestration, mock_get_object):

        mock_ctx = mock.MagicMock()

        not_found = heat_exc.HTTPNotFound()
        mock_get_orchestration.return_value.stacks.get.side_effect = not_found

        action = deployment.OvercloudRcAction("overcast")
        result = action.run(mock_ctx)

        self.assertEqual(result.error, (
            "The Heat stack overcast could not be found. Make sure you have "
            "deployed before calling this action."
        ))

    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    def test_no_env(self, mock_get_orchestration, mock_get_object):

        mock_ctx = mock.MagicMock()

        mock_get_object.return_value.get_object.side_effect = (
            swiftexceptions.ClientException("overcast"))

        action = deployment.OvercloudRcAction("overcast")
        result = action.run(mock_ctx)
        self.assertEqual(result.error, "Error retrieving environment for plan "
                                       "overcast: overcast")

    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    def test_no_password(self, mock_get_orchestration, mock_get_object):
        mock_ctx = mock.MagicMock()

        mock_get_object.return_value.get_object.return_value = (
            {}, "version: 1.0")

        action = deployment.OvercloudRcAction("overcast")
        result = action.run(mock_ctx)

        self.assertEqual(
            result.error,
            "Unable to find the AdminPassword in the plan environment.")

    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_object_client')
    @mock.patch('tripleo_common.utils.overcloudrc.create_overcloudrc')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    def test_success(self, mock_get_orchestration, mock_create_overcloudrc,
                     mock_get_object):
        mock_ctx = mock.MagicMock()

        mock_env = """
        version: 1.0

        template: overcloud.yaml
        environments:
        - path: overcloud-resource-registry-puppet.yaml
        - path: environments/services/sahara.yaml
        parameter_defaults:
          BlockStorageCount: 42
          OvercloudControlFlavor: yummy
        passwords:
          AdminPassword: SUPERSECUREPASSWORD
        """
        mock_get_object.return_value.get_object.return_value = ({}, mock_env)
        mock_create_overcloudrc.return_value = {
            "overcloudrc": "fake overcloudrc"
        }

        action = deployment.OvercloudRcAction("overcast")
        result = action.run(mock_ctx)

        self.assertEqual(result, {"overcloudrc": "fake overcloudrc"})


class DeploymentStatusActionTest(base.TestCase):

    def setUp(self):
        super(DeploymentStatusActionTest, self).setUp()
        self.plan = 'overcloud'
        self.ctx = mock.MagicMock()

    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_workflow_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    def test_get_deployment_status(
            self, heat, mistral, swift):

        mock_stack = mock.Mock()
        mock_stack.stack_status = 'COMPLETE'
        heat().stacks.get.return_value = mock_stack

        body = 'deployment_status: DEPLOY_SUCCESS'
        swift().get_object.return_value = [mock.Mock(), body]

        execution = mock.Mock()
        execution.updated_at = 1
        execution.state = 'SUCCESS'
        execution.output = '{"deployment_status":"DEPLOY_SUCCESS"}'
        mistral().executions.get.return_value = execution
        mistral().executions.find.return_value = [execution]

        action = deployment.DeploymentStatusAction(self.plan)
        result = action.run(self.ctx)

        self.assertEqual(result['stack_status'], 'COMPLETE')
        self.assertEqual(result['cd_status'], 'SUCCESS')
        self.assertEqual(result['deployment_status'], 'DEPLOY_SUCCESS')
        self.assertEqual(result['status_update'], None)

    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_workflow_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    def test_get_deployment_status_update_failed(
            self, heat, mistral, swift):

        mock_stack = mock.Mock()
        mock_stack.stack_status = 'FAILED'
        heat().stacks.get.return_value = mock_stack

        body = 'deployment_status: DEPLOY_SUCCESS'
        swift().get_object.return_value = [mock.Mock(), body]

        execution = mock.Mock()
        execution.updated_at = 1
        execution.state = 'SUCCESS'
        execution.output = '{"deployment_status":"DEPLOY_SUCCESS"}'
        mistral().executions.get.return_value = execution
        mistral().executions.find.return_value = [execution]

        action = deployment.DeploymentStatusAction(self.plan)
        result = action.run(self.ctx)

        self.assertEqual(result['stack_status'], 'FAILED')
        self.assertEqual(result['cd_status'], 'SUCCESS')
        self.assertEqual(result['deployment_status'], 'DEPLOY_SUCCESS')
        self.assertEqual(result['status_update'], 'DEPLOY_FAILED')

    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_workflow_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    def test_get_deployment_status_update_deploying(
            self, heat, mistral, swift):

        mock_stack = mock.Mock()
        mock_stack.stack_status = 'IN_PROGRESS'
        heat().stacks.get.return_value = mock_stack

        body = 'deployment_status: DEPLOY_SUCCESS'
        swift().get_object.return_value = [mock.Mock(), body]

        execution = mock.Mock()
        execution.updated_at = 1
        execution.state = 'SUCCESS'
        execution.output = '{"deployment_status":"DEPLOY_SUCCESS"}'
        mistral().executions.get.return_value = execution
        mistral().executions.find.return_value = [execution]

        action = deployment.DeploymentStatusAction(self.plan)
        result = action.run(self.ctx)

        self.assertEqual(result['stack_status'], 'IN_PROGRESS')
        self.assertEqual(result['cd_status'], 'SUCCESS')
        self.assertEqual(result['deployment_status'], 'DEPLOY_SUCCESS')
        self.assertEqual(result['status_update'], 'DEPLOYING')

    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_workflow_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    def test_get_deployment_status_update_success(
            self, heat, mistral, swift):

        mock_stack = mock.Mock()
        mock_stack.stack_status = 'COMPLETE'
        heat().stacks.get.return_value = mock_stack

        body = 'deployment_status: DEPLOYING'
        swift().get_object.return_value = [mock.Mock(), body]

        execution = mock.Mock()
        execution.updated_at = 1
        execution.state = 'SUCCESS'
        execution.output = '{"deployment_status":"DEPLOY_SUCCESS"}'
        mistral().executions.get.return_value = execution
        mistral().executions.find.return_value = [execution]

        action = deployment.DeploymentStatusAction(self.plan)
        result = action.run(self.ctx)

        self.assertEqual(result['stack_status'], 'COMPLETE')
        self.assertEqual(result['cd_status'], 'SUCCESS')
        self.assertEqual(result['deployment_status'], 'DEPLOYING')
        self.assertEqual(result['status_update'], 'DEPLOY_SUCCESS')

    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_workflow_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    def test_get_deployment_status_ansible_failed(
            self, heat, mistral, swift):

        mock_stack = mock.Mock()
        mock_stack.stack_status = 'COMPLETE'
        heat().stacks.get.return_value = mock_stack

        body = 'deployment_status: DEPLOYING'
        swift().get_object.return_value = [mock.Mock(), body]

        execution = mock.Mock()
        execution.updated_at = 1
        execution.state = 'SUCCESS'
        execution.output = '{"deployment_status":"DEPLOY_FAILED"}'
        mistral().executions.get.return_value = execution
        mistral().executions.find.return_value = [execution]

        action = deployment.DeploymentStatusAction(self.plan)
        result = action.run(self.ctx)

        self.assertEqual(result['stack_status'], 'COMPLETE')
        self.assertEqual(result['cd_status'], 'SUCCESS')
        self.assertEqual(result['deployment_status'], 'DEPLOYING')
        self.assertEqual(result['status_update'], 'DEPLOY_FAILED')

    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_object_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_workflow_client')
    @mock.patch('tripleo_common.actions.base.TripleOAction.'
                'get_orchestration_client')
    def test_get_deployment_status_no_heat_stack(
            self, heat, mistral, swift):

        mock_stack = mock.Mock()
        mock_stack.stack_status = 'COMPLETE'
        heat().stacks.get.side_effect = heat_exc.HTTPNotFound()

        body = 'deployment_status: DEPLOY_SUCCESS'
        swift().get_object.return_value = [mock.Mock(), body]

        execution = mock.Mock()
        execution.updated_at = 1
        execution.state = 'SUCCESS'
        execution.output = '{"deployment_status":"DEPLOY_SUCCESS"}'
        mistral().executions.get.return_value = execution
        mistral().executions.find.return_value = [execution]

        action = deployment.DeploymentStatusAction(self.plan)
        result = action.run(self.ctx)

        self.assertEqual(result['status_update'], None)
        self.assertEqual(result['deployment_status'], None)


class DeploymentFailuresActionTest(base.TestCase):

    def setUp(self):
        super(DeploymentFailuresActionTest, self).setUp()
        self.plan = 'overcloud'
        self.ctx = mock.MagicMock()

    @mock.patch('tripleo_common.actions.deployment.open')
    def test_get_deployment_failures(self, mock_open):

        test_result = dict(host0=["a", "b", "c"])
        mock_read = mock.MagicMock()
        mock_read.read.return_value = json.dumps(test_result)
        mock_open.return_value = mock_read

        action = deployment.DeploymentFailuresAction(self.plan)
        result = action.run(self.ctx)

        self.assertEqual(result['failures'], test_result)

    @mock.patch('tripleo_common.actions.deployment.open')
    def test_get_deployment_failures_no_file(self, mock_open):

        mock_open.side_effect = IOError()

        action = deployment.DeploymentFailuresAction(self.plan)
        result = action.run(self.ctx)

        self.assertTrue(result['message'].startswith(
                        "Ansible errors file not found at"))
        self.assertEqual({}, result['failures'])
