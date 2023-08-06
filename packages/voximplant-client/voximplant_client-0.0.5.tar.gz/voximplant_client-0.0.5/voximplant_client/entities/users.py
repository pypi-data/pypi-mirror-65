from typing import Optional

from voximplant_client import exceptions, helpers
from voximplant_client.entities.base import BaseVoximplantEntity
from voximplant_client.result import VoximplantAPIResult


class VoximplantUsers(BaseVoximplantEntity):
    def _get_application_id(self, app: str) -> int:
        application_id = self.client.applications.get_id(app)
        if application_id is None:
            raise exceptions.VoximplantBadApplicationNameException(f'Non-existant application name given: {app}')

        return application_id

    def get_id(self, app: str, user_name: str) -> Optional[int]:
        for user in self.list(app).result:
            if user['user_name'] == user_name:
                return int(user['user_id'])

    def list(self, app: str) -> VoximplantAPIResult:
        application_id = self._get_application_id(app)
        url = helpers.append_to_querytring('GetUsers', application_id=application_id)
        return self.http.get_list(url)

    def add(self, app: str, user_name: str, user_display_name: str, user_password: str) -> VoximplantAPIResult:
        user_id = self.get_id(app, user_name)
        if user_id:
            raise exceptions.VoximplantUserAlreadyExistsException(user_name)

        result = self.http.post('AddUser', payload=dict(
            application_id=self._get_application_id(app),
            user_name=user_name,
            user_display_name=user_display_name,
            user_password=user_password,
        ))

        if result.isError:
            raise exceptions.VoximplantUserCreationException(
                f'Error when creating user {user_name}: {result.error["msg"]}',
            )

        return result

    def update(self, app: str, user_name: str, **new_params) -> VoximplantAPIResult:
        user_id = self.get_id(app, user_name)
        if not user_id:
            raise exceptions.VoximplantUserDoesNotExistsException(user_name)

        result = self.http.post('SetUserInfo', payload=dict(
            application_id=self._get_application_id(app),
            user_name=user_name,
            **new_params,
        ))

        if result.isError:
            raise exceptions.VoximplantUserUpdateException(
                f'Error when updating user {user_name}: {result.error["msg"]}',
            )

        return result
