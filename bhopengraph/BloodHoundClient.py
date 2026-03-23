#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : BloodHoundClient.py

import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class BloodHoundClientError(Exception):
    """Base exception for BloodHoundClient errors."""

    pass


class BloodHoundAuthError(BloodHoundClientError):
    """Raised on 401/403 authentication/authorization failures."""

    pass


class BloodHoundAPIError(BloodHoundClientError):
    """Raised on non-2xx API responses (other than 401/403)."""

    def __init__(self, message, status_code=None, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class BloodHoundClient:
    """Client for the BloodHound API with HMAC-signed authentication.

    Uses only stdlib modules. Supports CRUD operations on custom node icons.
    """

    def __init__(self, base_url: str, token_id: str, token_key: str):
        self.base_url = base_url.rstrip("/")
        self.token_id = token_id
        self.token_key = token_key

    def _sign_request(self, method: str, uri: str, body: bytes = None) -> dict:
        """Compute HMAC-SHA256 signature chain and return the 3 auth headers."""
        now = datetime.now(timezone.utc)
        request_date = now.isoformat(timespec="seconds").replace("+00:00", "Z")

        # Step 1: HMAC(token_key, method + path)
        digester = hmac.new(self.token_key.encode("utf-8"), digestmod=hashlib.sha256)
        digester.update((method.upper() + uri).encode("utf-8"))

        # Step 2: HMAC(operation_digest, datetime[:13])
        digester = hmac.new(digester.digest(), digestmod=hashlib.sha256)
        digester.update(request_date[:13].encode("utf-8"))

        # Step 3: HMAC(date_digest, body) — always chain, even without body
        digester = hmac.new(digester.digest(), digestmod=hashlib.sha256)
        if body is not None:
            digester.update(body)

        signature = base64.b64encode(digester.digest()).decode("utf-8")

        return {
            "Authorization": f"bhesignature {self.token_id}",
            "RequestDate": request_date,
            "Signature": signature,
        }

    def _request(
        self, method: str, path: str, body: dict = None, extra_headers: dict = None
    ) -> dict:
        """Make an authenticated HTTP request to the BloodHound API."""
        uri = path if path.startswith("/") else f"/{path}"
        url = self.base_url + uri

        body_bytes = None
        if body is not None:
            body_bytes = json.dumps(body).encode("utf-8")

        headers = self._sign_request(method, uri, body_bytes)
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        if extra_headers:
            headers.update(extra_headers)

        req = Request(url, data=body_bytes, headers=headers, method=method.upper())

        try:
            with urlopen(req) as response:
                response_body = response.read().decode("utf-8")
                if response_body:
                    return json.loads(response_body)
                return {}
        except HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode("utf-8")
            except Exception:
                pass

            if e.code in (401, 403):
                raise BloodHoundAuthError(
                    f"Authentication failed (HTTP {e.code}): {error_body}"
                )
            raise BloodHoundAPIError(
                f"API request failed (HTTP {e.code}): {error_body}",
                status_code=e.code,
                response_body=error_body,
            )

    def get_custom_nodes(self) -> dict:
        """Get all custom node types."""
        return self._request("GET", "/api/v2/custom-nodes")

    def get_custom_node(self, kind_name: str) -> dict:
        """Get a specific custom node type by kind name."""
        return self._request("GET", f"/api/v2/custom-nodes/{kind_name}")

    def create_custom_node(self, kind_name: str, icon_config: dict) -> dict:
        """Create a new custom node type."""
        payload = {"kind_name": kind_name, "config": {"icon": icon_config}}
        return self._request("POST", "/api/v2/custom-nodes", body=payload)

    def update_custom_node(self, kind_name: str, icon_config: dict) -> dict:
        """Update an existing custom node type."""
        payload = {"config": {"icon": icon_config}}
        return self._request("PUT", f"/api/v2/custom-nodes/{kind_name}", body=payload)

    def delete_custom_node(self, kind_name: str) -> dict:
        """Delete a custom node type."""
        return self._request("DELETE", f"/api/v2/custom-nodes/{kind_name}")

    # --- Extension management ---

    def list_extensions(self) -> list:
        """List all schema extensions.

        Returns:
            list: List of extension dicts with keys: id, name, version, is_builtin.
        """
        response = self._request("GET", "/api/v2/extensions")
        extensions = response.get("data", {}).get("extensions", [])
        return [
            {
                "id": int(ext["id"]),
                "name": ext["name"],
                "version": ext["version"],
                "is_builtin": ext.get("is_builtin", False),
            }
            for ext in extensions
        ]

    def upsert_schema_extension(self, schema: dict) -> dict:
        """Create or update a schema extension.

        Args:
            schema (dict): OpenGraph schema definition containing schema,
                node_kinds, relationship_kinds, environments, and
                relationship_findings.

        Returns:
            dict: API response.
        """
        return self._request("PUT", "/api/v2/extensions", body=schema)

    def delete_extension(self, extension_id: int) -> dict:
        """Delete a schema extension by ID.

        Args:
            extension_id (int): The extension ID to delete.

        Returns:
            dict: API response.
        """
        return self._request("DELETE", f"/api/v2/extensions/{extension_id}")

    # --- Source kind management ---

    def list_source_kinds(self) -> list:
        """List all source kinds.

        Returns:
            list: List of source kind dicts with keys: id, name.
        """
        response = self._request("GET", "/api/v2/graphs/source-kinds")
        kinds = response.get("data", {}).get("kinds", [])
        return [{"id": int(k["id"]), "name": k["name"]} for k in kinds]

    def delete_source_kind_data(self, source_kind_ids: list) -> dict:
        """Delete data for the given source kind IDs.

        Args:
            source_kind_ids (list): List of integer source kind IDs to clear.

        Returns:
            dict: API response.
        """
        return self._request(
            "POST",
            "/api/v2/clear-database",
            body={"deleteSourceKinds": source_kind_ids},
        )

    # --- Graph upload / ingest ---

    def upload_graph(
        self, graph_data: dict, file_name: str = "opengraph-ingest.json"
    ) -> int:
        """Upload an OpenGraph JSON payload to BloodHound via the file-upload API.

        This follows the three-step ingest protocol:
        1. POST /api/v2/file-upload/start  — create an upload job
        2. POST /api/v2/file-upload/{id}   — send the JSON payload
        3. POST /api/v2/file-upload/{id}/end — finalise the job

        Args:
            graph_data (dict): The graph payload dict (must contain a "graph" key
                with "nodes" and "edges"). Typically produced by
                ``OpenGraph.export_to_dict()``.
            file_name (str): Filename hint sent via X-File-Upload-Name header.

        Returns:
            int: The ingest job ID.

        Raises:
            BloodHoundAPIError: If any step of the upload fails.
            ValueError: If the job ID returned by the server is invalid.
        """
        # Step 1: start the upload job
        start_response = self._request("POST", "/api/v2/file-upload/start")
        try:
            job_id = int(start_response.get("data", {}).get("id", 0))
        except (TypeError, ValueError):
            job_id = 0
        if not job_id:
            raise ValueError("BloodHound returned an invalid ingest job ID.")

        # Step 2: upload the payload
        upload_error = None
        try:
            self._request(
                "POST",
                f"/api/v2/file-upload/{job_id}",
                body=graph_data,
                extra_headers={"X-File-Upload-Name": file_name},
            )
        except Exception as e:
            upload_error = e
            raise
        finally:
            # Step 3: always end the upload job
            try:
                self._request("POST", f"/api/v2/file-upload/{job_id}/end")
            except Exception as end_error:
                if upload_error is None:
                    raise end_error

        return job_id

    def upload_graph_from_file(self, filepath: str, file_name: str = None) -> int:
        """Load graph JSON from a file and upload it to BloodHound.

        Args:
            filepath (str): Path to the JSON file.
            file_name (str): Optional filename hint. Defaults to the basename of filepath.

        Returns:
            int: The ingest job ID.
        """
        import os

        with open(filepath, "r") as f:
            graph_data = json.load(f)
        if file_name is None:
            file_name = os.path.basename(filepath)
        return self.upload_graph(graph_data, file_name=file_name)

    # --- Cypher queries ---

    def cypher_query(self, query: str, include_properties: bool = True) -> dict:
        """Execute a Cypher query against the BloodHound instance.

        Args:
            query (str): The Cypher query string to execute.
            include_properties (bool): Whether to include node/edge properties
                in the response. Defaults to True.

        Returns:
            dict: Raw JSON response from the API.

        Raises:
            BloodHoundAPIError: If the query fails.
        """
        payload = {
            "query": query,
            "include_properties": include_properties,
        }
        return self._request("POST", "/api/v2/graphs/cypher", body=payload)

    # --- Icon management ---

    def upload_icons(self, icons_config: dict) -> list:
        """Upload icons from config dict. Upsert: tries PUT first, POST on 404.

        Accepts the API-aligned list format::

            {"custom_nodes": [{"kindName": "...", "config": {"icon": {...}}}]}

        """
        results = []
        for entry in icons_config.get("custom_nodes", []):
            kind_name = entry["kindName"]
            icon_config = entry["config"]["icon"]
            try:
                result = self.update_custom_node(kind_name, icon_config)
                results.append(
                    {"kind": kind_name, "action": "updated", "result": result}
                )
            except BloodHoundAPIError as e:
                if e.status_code == 404:
                    result = self.create_custom_node(kind_name, icon_config)
                    results.append(
                        {"kind": kind_name, "action": "created", "result": result}
                    )
                else:
                    raise
        return results

    def upload_icons_from_file(self, filepath: str) -> list:
        """Load icons from a JSON file and upload them."""
        icons_config = self.load_icons_from_file(filepath)
        return self.upload_icons(icons_config)

    @classmethod
    def load_icons_from_file(cls, filepath: str) -> dict:
        """Load and parse an icons JSON file."""
        with open(filepath, "r") as f:
            return json.load(f)

    def __repr__(self):
        return (
            f"BloodHoundClient(base_url='{self.base_url}', token_id='{self.token_id}')"
        )
