from datetime import datetime
from typing import Iterable, Optional

from voximplant_client import exceptions, helpers


class VoximplantHistory:

    def __init__(self, client: 'VoximplantClient'):  # noqa:F821
        self.client = client

    def _get_application_id(self, app) -> int:
        application_id = self.client.applications.get_id(app)
        if application_id is None:
            raise exceptions.VoximplantBadApplicationNameException('Non-existant application name given: {}'.format(app))
        return application_id

    @staticmethod
    def _convert_datetime(t: datetime) -> str:
        return t.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def _convert_history_ids(session_ids: Iterable[int]) -> str:
        ids = [str(session_id) for session_id in session_ids]
        ids_str = '%3B'.join(ids)
        return f'{ids_str}%3B'

    def get_call_history(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        call_session_history_id: Optional[Iterable[int]] = None,
        app: str = None,
        with_calls: bool = True,
        with_records: bool = False,
        count: int = 20,
        offset: int = 0,
    ) -> 'VoximplantAPIResult':  # noqa:F821
        """Gets the call history.

        https://voximplant.com/docs/references/httpapi/managing_history#getcallhistory
        """

        params = {
            'from_date': self._convert_datetime(from_date) if from_date else None,
            'to_date': self._convert_datetime(to_date) if to_date else None,
            'call_session_history_id': self._convert_history_ids(call_session_history_id) if call_session_history_id else None,
            'application_id': self._get_application_id(app) if app else None,
            'with_calls': with_calls,
            'with_records': with_records,
            'count': count,
            'offset': offset,
        }

        params = {key: val for key, val in params.items() if val is not None}

        url = helpers.append_to_querytring('GetCallHistory', **params)
        return self.client.http.get(url)
