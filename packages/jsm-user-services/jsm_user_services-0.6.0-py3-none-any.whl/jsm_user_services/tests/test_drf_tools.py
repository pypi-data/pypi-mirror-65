"""
Module with tests for the DRF tools.
"""
from unittest import mock

import pytest
from django.test import TestCase
from requests.exceptions import HTTPError

from jsm_user_services.drf_tools.permissions import RoleBasedPermission
from jsm_user_services.drf_tools.permissions import StatusBasedPermission


class TestDRFPermissionClasses(TestCase):
    def setUp(self):
        self.role_based_permission = RoleBasedPermission()
        self.status_based_permission = StatusBasedPermission()

    @mock.patch("jsm_user_services.drf_tools.permissions.get_user_data_from_server")
    def test_role_based_permission_should_validate_request_data_and_append_it_to_request(
        self, mocked_get_user_data_from_server
    ):
        request = mock.MagicMock()
        del request.user_data
        append_user_data_to_request = True
        remote_user_data = {"name": "Igor G Peternella", "roles": ["professional"]}

        # get_user_data_from_server answers with an http 200 status
        mocked_get_user_data_from_server.return_value = remote_user_data
        user_data = self.role_based_permission._validate_request_against_user_service(
            request, append_user_data_to_request
        )

        expected_user_data = remote_user_data

        self.assertDictEqual(user_data, expected_user_data)
        self.assertDictEqual(request.user_data, expected_user_data)

    @mock.patch("jsm_user_services.drf_tools.permissions.get_user_data_from_server")
    def test_role_based_permission_should_return_empty_dict_upon_401_from_user_service(
        self, mocked_get_user_data_from_server
    ):
        request = mock.MagicMock()
        del request.user_data
        append_user_data_to_request = True

        # get_user_data_from_server answers with an http 401 status
        error = HTTPError("Unauthorized error!")
        response = mock.MagicMock()
        response.status_code = 401
        setattr(error, "response", response)

        mocked_get_user_data_from_server.side_effect = error

        user_data = self.role_based_permission._validate_request_against_user_service(
            request, append_user_data_to_request
        )

        expected_user_data = {}

        self.assertDictEqual(user_data, expected_user_data)

    @mock.patch("jsm_user_services.drf_tools.permissions.get_user_data_from_server")
    def test_role_based_permission_should_reraise_exception_when_user_service_returns_500(
        self, mocked_get_user_data_from_server
    ):
        request = mock.MagicMock()
        del request.user_data
        append_user_data_to_request = True

        # get_user_data_from_server answers with an http 500 status
        error = HTTPError("A 500 was returned!")
        response = mock.MagicMock()
        response.status_code = 500
        setattr(error, "response", response)

        mocked_get_user_data_from_server.side_effect = error

        with pytest.raises(HTTPError) as e:
            self.role_based_permission._validate_request_against_user_service(request, append_user_data_to_request)
            assert str(e.value) == "A 500 was returned!"

    @mock.patch("jsm_user_services.drf_tools.permissions.get_user_data_from_server")
    def test_permission_shouldnt_call_get_user_data_from_server_when_user_data_is_already_appended_to_request(
        self, mocked_get_user_data_from_server
    ):
        request = mock.MagicMock()
        remote_user_data = {"name": "Remote User", "roles": ["professional"]}
        request.user_data = remote_user_data

        user_data = self.role_based_permission._validate_request_against_user_service(request)

        self.assertDictEqual(user_data, remote_user_data)
        mocked_get_user_data_from_server.assert_not_called()

    @mock.patch("jsm_user_services.drf_tools.permissions.RoleBasedPermission._validate_request_against_user_service")
    def test_validate_user_role_should_return_false_if_user_data_is_an_empty_dict(
        self, mocked___validate_request_against_user_service
    ):
        request = mock.MagicMock()
        mocked___validate_request_against_user_service.return_value = {}

        permission_rslt = self.role_based_permission._validate_user_role(request, allowed_roles=["professional"])
        self.assertFalse(permission_rslt)

    @mock.patch("jsm_user_services.drf_tools.permissions.RoleBasedPermission._validate_request_against_user_service")
    def test_validate_user_role_should_return_false_if_user_data_has_disallowed_role(
        self, mocked___validate_request_against_user_service
    ):
        request = mock.MagicMock()
        mocked___validate_request_against_user_service.return_value = {
            "roles": ["owner"]  # only 'professional' role is allowed
        }

        permission_rslt = self.role_based_permission._validate_user_role(request, allowed_roles=["professional"])
        self.assertFalse(permission_rslt)

    @mock.patch("jsm_user_services.drf_tools.permissions.RoleBasedPermission._validate_request_against_user_service")
    def test_validate_user_role_should_return_true_if_user_data_has_allowed_role(
        self, mocked___validate_request_against_user_service
    ):
        request = mock.MagicMock()
        mocked___validate_request_against_user_service.return_value = {
            "roles": ["professional"]  # only 'professional' role is allowed
        }

        permission_rslt = self.role_based_permission._validate_user_role(request, allowed_roles=["professional"])
        self.assertTrue(permission_rslt)

    @mock.patch("jsm_user_services.drf_tools.permissions.RoleBasedPermission._validate_request_against_user_service")
    def test_validate_user_role_should_return_true_if_user_data_has_allowed_role_when_more_than_one_role_is_allowed(
        self, mocked___validate_request_against_user_service
    ):
        request = mock.MagicMock()
        mocked___validate_request_against_user_service.return_value = {
            "roles": ["manager"]  # only 'manager' and 'employee' roles are allowed
        }

        permission_rslt = self.role_based_permission._validate_user_role(request, allowed_roles=["employee", "manager"])
        self.assertTrue(permission_rslt)

    @mock.patch("jsm_user_services.drf_tools.permissions.StatusBasedPermission._validate_request_against_user_service")
    def test_validate_user_status_should_return_true_if_user_data_has_allowed_status(
        self, mocked___validate_request_against_user_service
    ):
        request = mock.MagicMock()
        mocked___validate_request_against_user_service.return_value = {
            "status": "active"
        }  # only 'active' status is allowed

        permission_rslt = self.status_based_permission._validate_user_status(request, allowed_status=["active"])
        self.assertTrue(permission_rslt)

    @mock.patch("jsm_user_services.drf_tools.permissions.StatusBasedPermission._validate_request_against_user_service")
    def test_validate_user_status_should_return_true_if_user_data_has_allowed_status_when_more_than_one_status_is_allowed(
        self, mocked___validate_request_against_user_service
    ):
        request = mock.MagicMock()
        mocked___validate_request_against_user_service.return_value = {
            "status": "pending-validation"
        }  # only 'active' and 'pending-validation' status are allowed

        permission_rslt = self.status_based_permission._validate_user_status(
            request, allowed_status=["active", "pending-validation"]
        )
        self.assertTrue(permission_rslt)

    @mock.patch("jsm_user_services.drf_tools.permissions.StatusBasedPermission._validate_request_against_user_service")
    def test_validate_user_status_should_return_false_if_user_data_has_disallowed_status(
        self, mocked___validate_request_against_user_service
    ):
        request = mock.MagicMock()
        mocked___validate_request_against_user_service.return_value = {
            "status": "blocked"
        }  # only pending-validation' status is allowed

        permission_rslt = self.status_based_permission._validate_user_status(
            request, allowed_status=["pending-validation"]
        )
        self.assertFalse(permission_rslt)

    @mock.patch("jsm_user_services.drf_tools.permissions.StatusBasedPermission._validate_request_against_user_service")
    def test_validate_user_status_should_return_false_if_user_data_is_an_empty_dict(
        self, mocked___validate_request_against_user_service
    ):
        request = mock.MagicMock()
        mocked___validate_request_against_user_service.return_value = {}

        permission_rslt = self.status_based_permission._validate_user_status(request, allowed_status=["active"])
        self.assertFalse(permission_rslt)
