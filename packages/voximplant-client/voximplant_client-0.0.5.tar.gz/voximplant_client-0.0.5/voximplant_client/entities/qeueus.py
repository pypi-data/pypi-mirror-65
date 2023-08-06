from typing import Optional

from voximplant_client import exceptions, helpers
from voximplant_client.entities.base import BaseVoximplantEntity
from voximplant_client.result import VoximplantAPIResult


class VoximplantQueues(BaseVoximplantEntity):
    def _get_application_id(self, app: str) -> int:
        application_id = self.client.applications.get_id(app)
        if application_id is None:
            raise exceptions.VoximplantBadApplicationNameException(f'Non-existant application name given: {app}')

        return application_id

    def _get_user_id(self, app: str, user_name: str) -> int:
        user_id = self.client.users.get_id(app, user_name)
        if user_id is None:
            raise exceptions.VoximplantUserDoesNotExistsException(f'Non-existant username given: {user_name}')

        return user_id

    def get_id(self, app: str, queue_name: str) -> Optional[int]:
        for queue in self.list(app).result:
            if queue['acd_queue_name'] == queue_name:
                return int(queue['acd_queue_id'])

    def list(self, app: str) -> VoximplantAPIResult:
        application_id = self._get_application_id(app)
        url = helpers.append_to_querytring('GetQueues', application_id=application_id)
        return self.http.get_list(url)

    def bind_user(self, app: str, queue_name: str, user_name: str, bind: bool = True) -> VoximplantAPIResult:
        queue_id = self.get_id(app, queue_name)
        if not queue_id:
            raise exceptions.VoximplantQueueDoesNotExistsException(queue_name)

        result = self.http.post('BindUserToQueue', payload=dict(
            application_id=self._get_application_id(app),
            user_id=self._get_user_id(app, user_name),
            acd_queue_id=queue_id,
            bind=bind,
        ))

        if result.isError:
            raise exceptions.VoximplantQueueBindException(
                f'Error when bind user {user_name} to queue {queue_name}: {result.error["msg"]}',
            )

        return result
