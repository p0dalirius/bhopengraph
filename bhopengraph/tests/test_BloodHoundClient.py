#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for the BloodHoundClient class.
"""

import base64
import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from bhopengraph.BloodHoundClient import (
    BloodHoundAPIError,
    BloodHoundAuthError,
    BloodHoundClient,
    BloodHoundClientError,
)


class TestBloodHoundClientConstructor(unittest.TestCase):
    """Test BloodHoundClient initialization."""

    def test_init_stores_url_stripped(self):
        client = BloodHoundClient("https://example.com/", "tid", "mykey")
        self.assertEqual(client.base_url, "https://example.com")

    def test_init_stores_token_key(self):
        client = BloodHoundClient("https://example.com", "tid", "my-secret-key")
        self.assertEqual(client.token_key, "my-secret-key")

    def test_init_stores_token_id(self):
        client = BloodHoundClient("https://example.com", "my-token-id", "mykey")
        self.assertEqual(client.token_id, "my-token-id")


class TestBloodHoundClientSigning(unittest.TestCase):
    """Test HMAC signing logic."""

    def setUp(self):
        self.client = BloodHoundClient(
            "https://bh.example.com", "token-123", "test-secret-key-1234"
        )

    def test_sign_request_returns_three_headers(self):
        headers = self.client._sign_request("GET", "/api/v2/custom-nodes")
        self.assertIn("Authorization", headers)
        self.assertIn("RequestDate", headers)
        self.assertIn("Signature", headers)

    def test_sign_request_authorization_format(self):
        headers = self.client._sign_request("GET", "/api/v2/custom-nodes")
        self.assertEqual(headers["Authorization"], "bhesignature token-123")

    def test_sign_request_date_format(self):
        headers = self.client._sign_request("GET", "/api/v2/custom-nodes")
        # Should be RFC3339-ish: YYYY-MM-DDTHH:MM:SS.mmmZ
        date = headers["RequestDate"]
        self.assertTrue(date.endswith("Z"))
        self.assertIn("T", date)

    def test_sign_request_signature_is_base64(self):
        headers = self.client._sign_request("GET", "/api/v2/custom-nodes")
        sig = headers["Signature"]
        # Should decode without error
        decoded = base64.b64decode(sig)
        self.assertEqual(len(decoded), 32)  # SHA256 digest

    def test_sign_request_with_body_differs_from_without(self):
        headers_no_body = self.client._sign_request("POST", "/api/v2/custom-nodes")
        headers_with_body = self.client._sign_request(
            "POST", "/api/v2/custom-nodes", b'{"name":"test"}'
        )
        self.assertNotEqual(
            headers_no_body["Signature"], headers_with_body["Signature"]
        )


class TestBloodHoundClientRequests(unittest.TestCase):
    """Test HTTP request methods with mocked urllib."""

    def setUp(self):
        self.client = BloodHoundClient(
            "https://bh.example.com", "tid", "test-secret-key"
        )

    def _mock_response(self, data, status=200):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(data).encode("utf-8")
        mock_resp.status = status
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_get_custom_nodes(self, mock_urlopen):
        expected = {"data": [{"name": "AWS_User"}]}
        mock_urlopen.return_value = self._mock_response(expected)
        result = self.client.get_custom_nodes()
        self.assertEqual(result, expected)

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_get_custom_node(self, mock_urlopen):
        expected = {"name": "AWS_User", "icon": {"type": "font-awesome"}}
        mock_urlopen.return_value = self._mock_response(expected)
        result = self.client.get_custom_node("AWS_User")
        self.assertEqual(result, expected)

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_create_custom_node(self, mock_urlopen):
        expected = {"name": "AWS_User"}
        mock_urlopen.return_value = self._mock_response(expected)
        icon = {"type": "font-awesome", "name": "user", "color": "#3B48CC"}
        result = self.client.create_custom_node("AWS_User", icon)
        self.assertEqual(result, expected)
        # Verify POST method
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.get_method(), "POST")

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_update_custom_node(self, mock_urlopen):
        expected = {"name": "AWS_User"}
        mock_urlopen.return_value = self._mock_response(expected)
        icon = {"type": "font-awesome", "name": "user", "color": "#3B48CC"}
        result = self.client.update_custom_node("AWS_User", icon)
        self.assertEqual(result, expected)
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.get_method(), "PUT")

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_delete_custom_node(self, mock_urlopen):
        expected = {}
        mock_urlopen.return_value = self._mock_response(expected)
        result = self.client.delete_custom_node("AWS_User")
        self.assertEqual(result, expected)
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.get_method(), "DELETE")

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_auth_error_on_401(self, mock_urlopen):
        from urllib.error import HTTPError

        error = HTTPError(
            "url",
            401,
            "Unauthorized",
            {},
            MagicMock(read=MagicMock(return_value=b"unauthorized")),
        )
        error.read = MagicMock(return_value=b"unauthorized")
        mock_urlopen.side_effect = error
        with self.assertRaises(BloodHoundAuthError):
            self.client.get_custom_nodes()

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_api_error_on_500(self, mock_urlopen):
        from urllib.error import HTTPError

        error = HTTPError(
            "url",
            500,
            "Server Error",
            {},
            MagicMock(read=MagicMock(return_value=b"error")),
        )
        error.read = MagicMock(return_value=b"error")
        mock_urlopen.side_effect = error
        with self.assertRaises(BloodHoundAPIError) as ctx:
            self.client.get_custom_nodes()
        self.assertEqual(ctx.exception.status_code, 500)


class TestBloodHoundClientExtensions(unittest.TestCase):
    """Test extension management methods."""

    def setUp(self):
        self.client = BloodHoundClient(
            "https://bh.example.com", "tid", "test-secret-key"
        )

    def _mock_response(self, data, status=200):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(data).encode("utf-8")
        mock_resp.status = status
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_list_extensions(self, mock_urlopen):
        payload = {
            "data": {
                "extensions": [
                    {
                        "id": 1,
                        "name": "my-ext",
                        "version": "1.0.0",
                        "is_builtin": False,
                    },
                    {
                        "id": "2",
                        "name": "builtin",
                        "version": "2.0.0",
                        "is_builtin": True,
                    },
                ]
            }
        }
        mock_urlopen.return_value = self._mock_response(payload)
        result = self.client.list_extensions()
        self.assertEqual(len(result), 2)
        self.assertEqual(
            result[0],
            {"id": 1, "name": "my-ext", "version": "1.0.0", "is_builtin": False},
        )
        self.assertEqual(result[1]["id"], 2)
        self.assertTrue(result[1]["is_builtin"])

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_upsert_schema_extension(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({})
        schema = {
            "schema": {
                "name": "test",
                "display_name": "Test",
                "version": "1.0",
                "namespace": "test",
            }
        }
        self.client.upsert_schema_extension(schema)
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.get_method(), "PUT")
        self.assertIn("/api/v2/extensions", req.full_url)

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_delete_extension(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({})
        self.client.delete_extension(42)
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.get_method(), "DELETE")
        self.assertIn("/api/v2/extensions/42", req.full_url)


class TestBloodHoundClientSourceKinds(unittest.TestCase):
    """Test source kind management methods."""

    def setUp(self):
        self.client = BloodHoundClient(
            "https://bh.example.com", "tid", "test-secret-key"
        )

    def _mock_response(self, data, status=200):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(data).encode("utf-8")
        mock_resp.status = status
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_list_source_kinds(self, mock_urlopen):
        payload = {
            "data": {"kinds": [{"id": 1, "name": "aws"}, {"id": 2, "name": "azure"}]}
        }
        mock_urlopen.return_value = self._mock_response(payload)
        result = self.client.list_source_kinds()
        self.assertEqual(result, [{"id": 1, "name": "aws"}, {"id": 2, "name": "azure"}])

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_delete_source_kind_data(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({})
        self.client.delete_source_kind_data([1, 2])
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.get_method(), "POST")
        body = json.loads(req.data.decode("utf-8"))
        self.assertEqual(body, {"deleteSourceKinds": [1, 2]})


class TestBloodHoundClientGraphUpload(unittest.TestCase):
    """Test graph upload (file-upload ingest) logic."""

    def setUp(self):
        self.client = BloodHoundClient(
            "https://bh.example.com", "tid", "test-secret-key"
        )

    def _mock_response(self, data, status=200):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(data).encode("utf-8")
        mock_resp.status = status
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_upload_graph_three_step_flow(self, mock_urlopen):
        """Verify the three API calls: start, upload, end."""
        mock_urlopen.return_value = self._mock_response({"data": {"id": 99}})
        graph_data = {"graph": {"nodes": [], "edges": []}}
        job_id = self.client.upload_graph(graph_data)
        self.assertEqual(job_id, 99)
        self.assertEqual(mock_urlopen.call_count, 3)
        # Check the three request paths
        calls = [mock_urlopen.call_args_list[i][0][0] for i in range(3)]
        self.assertIn("/api/v2/file-upload/start", calls[0].full_url)
        self.assertIn("/api/v2/file-upload/99", calls[1].full_url)
        self.assertIn("/api/v2/file-upload/99/end", calls[2].full_url)

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_upload_graph_sends_file_name_header(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"data": {"id": 1}})
        self.client.upload_graph(
            {"graph": {"nodes": [], "edges": []}}, file_name="test.json"
        )
        upload_req = mock_urlopen.call_args_list[1][0][0]
        self.assertEqual(upload_req.get_header("X-file-upload-name"), "test.json")

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_upload_graph_invalid_job_id(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"data": {}})
        with self.assertRaises(ValueError):
            self.client.upload_graph({"graph": {"nodes": [], "edges": []}})

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_upload_graph_from_file(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"data": {"id": 5}})
        data = {
            "graph": {"nodes": [], "edges": []},
            "metadata": {"source_kind": "test"},
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()
            filepath = f.name
        try:
            job_id = self.client.upload_graph_from_file(filepath)
            self.assertEqual(job_id, 5)
            self.assertEqual(mock_urlopen.call_count, 3)
        finally:
            os.unlink(filepath)

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_upload_graph_end_called_on_upload_error(self, mock_urlopen):
        """Verify /end is called even when the upload step fails."""
        start_resp = self._mock_response({"data": {"id": 7}})
        end_resp = self._mock_response({})

        from urllib.error import HTTPError

        upload_error = HTTPError(
            "url",
            500,
            "Server Error",
            {},
            MagicMock(read=MagicMock(return_value=b"error")),
        )
        upload_error.read = MagicMock(return_value=b"error")

        mock_urlopen.side_effect = [start_resp, upload_error, end_resp]
        with self.assertRaises(BloodHoundAPIError):
            self.client.upload_graph({"graph": {"nodes": [], "edges": []}})
        # /end should still be called (3 total calls)
        self.assertEqual(mock_urlopen.call_count, 3)


class TestBloodHoundClientCypherQuery(unittest.TestCase):
    """Test Cypher query method."""

    def setUp(self):
        self.client = BloodHoundClient(
            "https://bh.example.com", "tid", "test-secret-key"
        )

    def _mock_response(self, data, status=200):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(data).encode("utf-8")
        mock_resp.status = status
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_cypher_query_sends_post(self, mock_urlopen):
        expected = {"data": {"nodes": {}, "edges": []}}
        mock_urlopen.return_value = self._mock_response(expected)
        result = self.client.cypher_query("MATCH (n) RETURN n LIMIT 10")
        self.assertEqual(result, expected)
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.get_method(), "POST")
        self.assertIn("/api/v2/graphs/cypher", req.full_url)

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_cypher_query_sends_query_in_body(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"data": {}})
        self.client.cypher_query("MATCH (n:User) RETURN n")
        req = mock_urlopen.call_args[0][0]
        body = json.loads(req.data.decode("utf-8"))
        self.assertEqual(body["query"], "MATCH (n:User) RETURN n")
        self.assertTrue(body["include_properties"])

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_cypher_query_include_properties_false(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"data": {}})
        self.client.cypher_query("MATCH (n) RETURN n", include_properties=False)
        req = mock_urlopen.call_args[0][0]
        body = json.loads(req.data.decode("utf-8"))
        self.assertFalse(body["include_properties"])

    @patch("bhopengraph.BloodHoundClient.urlopen")
    def test_cypher_query_api_error(self, mock_urlopen):
        from urllib.error import HTTPError

        error = HTTPError(
            "url",
            400,
            "Bad Request",
            {},
            MagicMock(read=MagicMock(return_value=b"invalid query")),
        )
        error.read = MagicMock(return_value=b"invalid query")
        mock_urlopen.side_effect = error
        with self.assertRaises(BloodHoundAPIError) as ctx:
            self.client.cypher_query("INVALID CYPHER")
        self.assertEqual(ctx.exception.status_code, 400)


class TestBloodHoundClientUpload(unittest.TestCase):
    """Test bulk upload logic."""

    def setUp(self):
        self.client = BloodHoundClient(
            "https://bh.example.com", "tid", "test-secret-key"
        )

    @patch.object(BloodHoundClient, "update_custom_node")
    def test_upload_icons_updates_existing(self, mock_update):
        mock_update.return_value = {"name": "AWS_User"}
        config = {
            "custom_nodes": [
                {
                    "kindName": "AWS_User",
                    "config": {
                        "icon": {
                            "type": "font-awesome",
                            "name": "user",
                            "color": "#3B48CC",
                        }
                    },
                }
            ]
        }
        results = self.client.upload_icons(config)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["action"], "updated")

    @patch.object(BloodHoundClient, "create_custom_node")
    @patch.object(BloodHoundClient, "update_custom_node")
    def test_upload_icons_creates_on_404(self, mock_update, mock_create):
        mock_update.side_effect = BloodHoundAPIError(
            "Not found", status_code=404, response_body=""
        )
        mock_create.return_value = {"name": "AWS_User"}
        config = {
            "custom_nodes": [
                {
                    "kindName": "AWS_User",
                    "config": {
                        "icon": {
                            "type": "font-awesome",
                            "name": "user",
                            "color": "#3B48CC",
                        }
                    },
                }
            ]
        }
        results = self.client.upload_icons(config)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["action"], "created")

    @patch.object(BloodHoundClient, "update_custom_node")
    def test_upload_icons_raises_on_non_404_error(self, mock_update):
        mock_update.side_effect = BloodHoundAPIError(
            "Server error", status_code=500, response_body=""
        )
        config = {
            "custom_nodes": [
                {
                    "kindName": "AWS_User",
                    "config": {"icon": {"type": "font-awesome", "name": "user"}},
                }
            ]
        }
        with self.assertRaises(BloodHoundAPIError):
            self.client.upload_icons(config)


class TestBloodHoundClientFileLoading(unittest.TestCase):
    """Test file loading methods."""

    def test_load_icons_from_file(self):
        data = {
            "custom_nodes": [
                {
                    "kindName": "Test",
                    "config": {"icon": {"type": "font-awesome", "name": "star"}},
                }
            ]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()
            filepath = f.name
        try:
            result = BloodHoundClient.load_icons_from_file(filepath)
            self.assertEqual(result, data)
        finally:
            os.unlink(filepath)

    @patch.object(BloodHoundClient, "upload_icons")
    def test_upload_icons_from_file(self, mock_upload):
        mock_upload.return_value = [{"kind": "Test", "action": "created"}]
        data = {
            "custom_nodes": [
                {
                    "kindName": "Test",
                    "config": {"icon": {"type": "font-awesome", "name": "star"}},
                }
            ]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()
            filepath = f.name
        try:
            client = BloodHoundClient("https://bh.example.com", "tid", "testkey")
            result = client.upload_icons_from_file(filepath)
            self.assertEqual(len(result), 1)
            mock_upload.assert_called_once_with(data)
        finally:
            os.unlink(filepath)


class TestBloodHoundClientRepr(unittest.TestCase):
    """Test string representation."""

    def test_repr(self):
        client = BloodHoundClient("https://bh.example.com", "tid", "testkey")
        r = repr(client)
        self.assertIn("BloodHoundClient", r)
        self.assertIn("bh.example.com", r)
        self.assertIn("tid", r)


class TestExceptionHierarchy(unittest.TestCase):
    """Test exception class hierarchy."""

    def test_auth_error_is_client_error(self):
        self.assertTrue(issubclass(BloodHoundAuthError, BloodHoundClientError))

    def test_api_error_is_client_error(self):
        self.assertTrue(issubclass(BloodHoundAPIError, BloodHoundClientError))

    def test_api_error_stores_attributes(self):
        err = BloodHoundAPIError("msg", status_code=400, response_body="bad request")
        self.assertEqual(err.status_code, 400)
        self.assertEqual(err.response_body, "bad request")


if __name__ == "__main__":
    unittest.main()
