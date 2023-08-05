"""Radar session object. This should be used by clients such as plausibility etc.

It also handles Radar server discovery.
"""
import os
import socket
import typing
import uuid

from mlre.radar import radar_api_client, radar_common


class RadarSession:
    """Radar session object, to be used by clients."""

    def __enter__(self) -> None:
        """Creates a radar session by entering its context."""
        self.session_id = uuid.uuid4()  # pylint: disable=W0201

        if 'RADAR_SERVER' in os.environ.keys():
            endpoint = os.environ['RADAR_SERVER']
        else:
            endpoint = "https://127.0.0.1:5000/"

        self.api_client =\
            radar_api_client.APIClient(  # pylint: disable=W0201
                endpoint, self.session_id)

        # Report client info
        client_info = self.collect_client_info()
        self.api_client.report_client_info(client_info)

        # Report that the session has started
        event_identifier = radar_common.EventIdentifier(severity=radar_common.Severity.INFO,
                                                        location=__name__,
                                                        description="Session started")
        self.api_client.report_event(event_identifier, {})

    def __exit__(self, exc_type: type,  # type: ignore
                 exc_val: Exception,
                 exc_tb: typing.Any) -> None:

        # Report that the session has ended
        event_identifier = radar_common.EventIdentifier(severity=radar_common.Severity.INFO,
                                                        location=__name__,
                                                        description="Session ended")
        self.api_client.report_event(event_identifier, {})

    @staticmethod
    def collect_client_info() -> radar_common.ClientInfo:
        """Collects information on the running client."""
        return radar_common.ClientInfo(socket.gethostname(), os.environ)  # type: ignore
