"""This module contains the detection code for potentially insecure low-level
calls."""

from mythril.analysis.potential_issues import (
    PotentialIssue,
    get_potential_issues_annotation,
)
from mythril.analysis.swc_data import ASSERT_VIOLATION
from mythril.analysis.module.base import DetectionModule, EntryPoint
from mythril.laser.ethereum.state.global_state import GlobalState
import logging
import eth_abi

log = logging.getLogger(__name__)

DESCRIPTION = """

Search for reachable user-supplied exceptions.
Report a warning if an log message is emitted: 'emit AssertionFailed(string)'

"""

assertion_failed_hash = (
    0xB42604CB105A16C8F6DB8A41E6B00C0C1B4826465E8BC504B3EB3E88B3E6A4A0
)


class UserAssertions(DetectionModule):
    """This module searches for user supplied exceptions: emit AssertionFailed("Error")."""

    name = "A user-defined assertion has been triggered"
    swc_id = ASSERT_VIOLATION
    description = DESCRIPTION
    entry_point = EntryPoint.CALLBACK
    pre_hooks = ["LOG1"]

    def _execute(self, state: GlobalState) -> None:
        """

        :param state:
        :return:
        """
        potential_issues = self._analyze_state(state)

        annotation = get_potential_issues_annotation(state)
        annotation.potential_issues.extend(potential_issues)

    def _analyze_state(self, state: GlobalState):
        """

        :param state:
        :return:
        """
        topic, size, mem_start = state.mstate.stack[-3:]

        if topic.symbolic or topic.value != assertion_failed_hash:
            return []

        message = None
        if not mem_start.symbolic and not size.symbolic:
            message = eth_abi.decode_single(
                "string",
                bytes(
                    state.mstate.memory[
                        mem_start.value + 32 : mem_start.value + size.value
                    ]
                ),
            ).decode("utf8")

        description_head = "A user-provided assertion failed."
        if message:
            description_tail = "A user-provided assertion failed with the message '{}'".format(
                message
            )
        else:
            description_tail = "A user-provided assertion failed."

        address = state.get_current_instruction()["address"]
        issue = PotentialIssue(
            contract=state.environment.active_account.contract_name,
            function_name=state.environment.active_function_name,
            address=address,
            swc_id=ASSERT_VIOLATION,
            title="Assertion Failed",
            bytecode=state.environment.code.bytecode,
            severity="Medium",
            description_head=description_head,
            description_tail=description_tail,
            constraints=[],
            detector=self,
        )

        return [issue]


detector = UserAssertions()
