#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.mturk.core.mturk_manager import MTurkManager
from parlai.mturk.core.worker_state import AssignState


class VotingManager(MTurkManager):
    def __init__(self, opt, mturk_agent_ids, is_test=False):
        super().__init__(opt, mturk_agent_ids, is_test)

    def _handle_worker_disconnect(self, worker_id, assignment_id):
        """Mark a player as disconnected, and possibly end the game for the
        remaining players. If we have enough players after the disconnect, we
        should continue the game.

        This overrides the standard method which simply ends for everyone if
        one player disconnects.
        """
        agent = self._get_agent(worker_id, assignment_id)
        if agent is None:
            self._log_missing_agent(worker_id, assignment_id)
        else:
            # Disconnect in conversation is not workable
            agent.state.status = AssignState.STATUS_DISCONNECT
            # in conversation, inform others about disconnect
            conversation_id = agent.conversation_id
            if conversation_id in self.conv_to_agent:
                if agent in self.conv_to_agent[conversation_id]:
                    alive_agents = 0
                    for other_agent in self.conv_to_agent[conversation_id]:
                        if agent.assignment_id != other_agent.assignment_id:
                            alive_agents += 1
                    if alive_agents < 3:
                        for other_agent in self.conv_to_agent[conversation_id]:
                            if agent.assignment_id != other_agent.assignment_id:
                                self._handle_partner_disconnect(
                                    other_agent.worker_id,
                                    other_agent.assignment_id
                                )
                # The user disconnected from inside a conversation with
                # another turker, record this as bad behavoir
                self._handle_bad_disconnect(worker_id)
