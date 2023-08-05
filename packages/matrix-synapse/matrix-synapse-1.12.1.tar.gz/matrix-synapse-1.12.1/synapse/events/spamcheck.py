# -*- coding: utf-8 -*-
# Copyright 2017 New Vector Ltd
# Copyright 2019 The Matrix.org Foundation C.I.C.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect
from typing import Dict

from synapse.spam_checker_api import SpamCheckerApi

MYPY = False
if MYPY:
    import synapse.server


class SpamChecker(object):
    def __init__(self, hs: "synapse.server.HomeServer"):
        self.spam_checker = None

        module = None
        config = None
        try:
            module, config = hs.config.spam_checker
        except Exception:
            pass

        if module is not None:
            # Older spam checkers don't accept the `api` argument, so we
            # try and detect support.
            spam_args = inspect.getfullargspec(module)
            if "api" in spam_args.args:
                api = SpamCheckerApi(hs)
                self.spam_checker = module(config=config, api=api)
            else:
                self.spam_checker = module(config=config)

    def check_event_for_spam(self, event: "synapse.events.EventBase") -> bool:
        """Checks if a given event is considered "spammy" by this server.

        If the server considers an event spammy, then it will be rejected if
        sent by a local user. If it is sent by a user on another server, then
        users receive a blank event.

        Args:
            event: the event to be checked

        Returns:
            True if the event is spammy.
        """
        if self.spam_checker is None:
            return False

        return self.spam_checker.check_event_for_spam(event)

    def user_may_invite(
        self, inviter_userid: str, invitee_userid: str, room_id: str
    ) -> bool:
        """Checks if a given user may send an invite

        If this method returns false, the invite will be rejected.

        Args:
            inviter_userid: The user ID of the sender of the invitation
            invitee_userid: The user ID targeted in the invitation
            room_id: The room ID

        Returns:
            True if the user may send an invite, otherwise False
        """
        if self.spam_checker is None:
            return True

        return self.spam_checker.user_may_invite(
            inviter_userid, invitee_userid, room_id
        )

    def user_may_create_room(self, userid: str) -> bool:
        """Checks if a given user may create a room

        If this method returns false, the creation request will be rejected.

        Args:
            userid: The ID of the user attempting to create a room

        Returns:
            True if the user may create a room, otherwise False
        """
        if self.spam_checker is None:
            return True

        return self.spam_checker.user_may_create_room(userid)

    def user_may_create_room_alias(self, userid: str, room_alias: str) -> bool:
        """Checks if a given user may create a room alias

        If this method returns false, the association request will be rejected.

        Args:
            userid: The ID of the user attempting to create a room alias
            room_alias: The alias to be created

        Returns:
            True if the user may create a room alias, otherwise False
        """
        if self.spam_checker is None:
            return True

        return self.spam_checker.user_may_create_room_alias(userid, room_alias)

    def user_may_publish_room(self, userid: str, room_id: str) -> bool:
        """Checks if a given user may publish a room to the directory

        If this method returns false, the publish request will be rejected.

        Args:
            userid: The user ID attempting to publish the room
            room_id: The ID of the room that would be published

        Returns:
            True if the user may publish the room, otherwise False
        """
        if self.spam_checker is None:
            return True

        return self.spam_checker.user_may_publish_room(userid, room_id)

    def check_username_for_spam(self, user_profile: Dict[str, str]) -> bool:
        """Checks if a user ID or display name are considered "spammy" by this server.

        If the server considers a username spammy, then it will not be included in
        user directory results.

        Args:
            user_profile: The user information to check, it contains the keys:
                * user_id
                * display_name
                * avatar_url

        Returns:
            True if the user is spammy.
        """
        if self.spam_checker is None:
            return False

        # For backwards compatibility, if the method does not exist on the spam checker, fallback to not interfering.
        checker = getattr(self.spam_checker, "check_username_for_spam", None)
        if not checker:
            return False
        # Make a copy of the user profile object to ensure the spam checker
        # cannot modify it.
        return checker(user_profile.copy())
