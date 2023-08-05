"""Server component for the radar API."""
import typing
import uuid

from flask import Blueprint, request

import mlre
from mlre.radar import radar_common, radar_database


# type: ignore
def create_api_server_blueprint(database: radar_database.RadarDatabase) -> Blueprint:
    """Creates an instance of the API server.

    Args:
        database: An instance of the radar event and client info database.
    """
    api_server = Blueprint(__name__, __name__)

    @api_server.route('/version')  # type: ignore
    def get_version() -> typing.Dict[str, str]:  # pylint: disable=W0612
        """Give api server and mlre versions."""
        return {'api': '1', 'mlre': mlre.__version__}

    @api_server.route('/report_event', methods=['POST'])  # type: ignore
    def report_event() -> str:  # pylint: disable=W0612
        # Decode request
        request_json = request.json  # type: ignore
        session_id: uuid.UUID = uuid.UUID(
            request_json['session_id'])  # type: ignore
        event_identifier: radar_common.EventIdentifier =\
            radar_common.EventIdentifier(
                *request_json['event_identifier'])  # type: ignore

        freeze_frame: radar_common.FreezeFrameData =\
            request_json['freeze_frame']  # type: ignore

        # Make database call
        database.insert_event(session_id, event_identifier, freeze_frame)
        return ''

    @api_server.route('/report_client_info', methods=['POST'])  # type: ignore
    def report_client_info() -> str:  # pylint: disable=W0612
        # Decode request
        request_json = request.json  # type: ignore
        session_id: uuid.UUID = uuid.UUID(
            request_json['session_id'])  # type: ignore
        client_info: radar_common.ClientInfo =\
            radar_common.ClientInfo(
                *request_json['client_info'])  # type: ignore

        # Make database call
        database.insert_client_info(session_id, client_info)
        return ''

    @api_server.route('/event_identifiers')  # type: ignore
    # pylint: disable=W0612
    def event_identifiers() ->\
            typing.Dict[str,
                        typing.Sequence[
                            typing.Mapping[str,
                                           typing.Union[int, radar_common.EventIdentifier]]]]:
        response_data = [{"event_index": event_index, "event_identifier": event_identifier}
                         for event_index, event_identifier in database.event_identifiers()]
        return {"event_identifiers": response_data}  # type: ignore

    @api_server.route('/event/<event_index>')  # type: ignore
    # pylint: disable=W0612
    def event(event_index: int) ->  \
            typing.Dict[str,
                        typing.Union[radar_common.EventIdentifier,
                                     typing.Sequence[typing.Tuple[uuid.UUID,
                                                                  radar_common.FreezeFrameData]]]]:

        event_identifier, freeze_frames = database.event(int(event_index))
        # type: ignore
        return {"event_identifier": event_identifier, "freeze_frames": freeze_frames}

    return api_server


__all__ = ["create_api_server_blueprint"]
