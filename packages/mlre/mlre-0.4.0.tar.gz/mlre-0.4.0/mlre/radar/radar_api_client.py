"""Handles to client->server connection."""
import typing
import urllib.parse
import uuid

import requests

from . import radar_common


class APIClient:
    """Represents an active connection to a radar server."""

    def __init__(self,
                 endpoint_url: str,
                 session_id: uuid.UUID):
        """Connects to a radar server.

        Args:
            endpoint_url: URL to send requests to.
            session_id: UUID (self-generated) of the current session.
        """
        self._endpoint_url: str = endpoint_url
        self._session_id: uuid.UUID = session_id
        self._has_reported_client_info: bool = False

    def get_api_version(self) -> typing.Optional[str]:
        """Gets the server's API version."""
        return self._get_version()[0]

    def get_mlre_version(self) -> typing.Optional[str]:
        """Gets the server's MLRE version."""
        return self._get_version()[1]

    def _get_version(self) -> typing.Tuple[str, str]:
        """Gets the server's API and MLRE version."""
        request_url = urllib.parse.urljoin(self._endpoint_url, "version")
        response: typing.Dict[str, str] = requests.get(request_url).json()

        return response['api'], response['mlre']

    def report_client_info(
            self,
            client_info: radar_common.ClientInfo) -> None:
        """Reports information about the client to the server.

        This method should only be called once per session, and before
        any events are reported.

        Args:
            client_info: Client information object.
        """
        if self._has_reported_client_info:
            raise ValueError(
                "This method should only be called once per session.")

        request_url = urllib.parse.urljoin(
            self._endpoint_url, "report_client_info")
        request_body = {"session_id": str(self._session_id),
                        "client_info": client_info}

        requests.post(request_url, json=request_body)

        # Remember having reported client information
        self._has_reported_client_info = True

    def report_event(
            self,
            event_identifier: radar_common.EventIdentifier,
            freeze_frame: radar_common.FreezeFrameData,
    ) -> None:
        """Reports an event to the server.

        Make sure to report the client information before reporting any events.

        Args:
            event_identifier: Unique identifier of the event.
            freeze_frame: A dictionary of helpful measurements.
        """
        if not self._has_reported_client_info:
            raise ValueError(
                "Make sure to report the client information before reporting any events.")

        request_url = urllib.parse.urljoin(self._endpoint_url, "report_event")
        request_body = {"session_id": str(self._session_id),
                        "event_identifier": event_identifier,
                        "freeze_frame": freeze_frame}

        requests.post(request_url, json=request_body)


__all__ = ["APIClient"]
