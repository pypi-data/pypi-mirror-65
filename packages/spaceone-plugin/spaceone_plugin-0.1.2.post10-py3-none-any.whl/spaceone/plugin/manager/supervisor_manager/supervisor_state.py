# -*- coding: utf-8 -*-

import abc

from spaceone.core.manager import BaseManager
from spaceone.plugin.error.custom import ERROR_SUPERVISOR_STATE

__all__ = [
    'SupervisorState',
    'PendingState',
    'EnabledState',
    'DisabledState',
    'DisconnectedState',
    'SupvrStateMachine'
]


def _compute_state(state):
    if state == 'PENDING':
        return PendingState()
    elif state == 'DISABLED':
        return DisabledState()
    elif state == 'ENABLED':
        return EnabledState()
    elif state == 'DISCONNECTED':
        return DisconnectedState()


class SupvrStateMachine(BaseManager):

    def __init__(self, supvr_id, state):
        super().__init__()
        self.supvr_id = supvr_id
        self.state = _compute_state(state)

    def register(self):
        """
        The register action enables state from only 'PENDING'.
        """
        if isinstance(self.state, PendingState):
            self.state = EnabledState()
        else:
            raise ERROR_SUPERVISOR_STATE(action='register', supervisor_id=self.supvr_id, state=str(self.state))

    def enable(self):
        if isinstance(self.state, (DisabledState, DisconnectedState)):
            self.state = EnabledState()
        elif isinstance(self.state, EnabledState):
            pass
        else:
            raise ERROR_SUPERVISOR_STATE(action='enable', supervisor_id=self.supvr_id, state=str(self.state))

    def disable(self):
        if isinstance(self.state, (EnabledState, DisconnectedState)):
            self.state = DisabledState()
        elif isinstance(self.state, DisabledState):
            pass
        else:
            raise ERROR_SUPERVISOR_STATE(action='disable', supervisor_id=self.supvr_id, state=str(self.state))


class SupervisorState(metaclass=abc.ABCMeta):

    def __init__(self):
        self.handle()

    @abc.abstractmethod
    def handle(self):
        pass


class PendingState(SupervisorState):

    def handle(self):
        # TODO: Send notification? maybe?
        pass

    def __str__(self):
        return 'PENDING'


class EnabledState(SupervisorState):

    def handle(self):
        # TODO: add this supvr_id to watching list.
        pass

    def __str__(self):
        return 'ENABLED'


class DisabledState(SupervisorState):

    def handle(self):
        pass

    def __str__(self):
        return 'DISABLED'


class DisconnectedState(SupervisorState):

    def handle(self):
        # TODO: Send notification? maybe?
        pass

    def __str__(self):
        return 'DISCONNECTED'
