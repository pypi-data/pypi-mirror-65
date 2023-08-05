# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains the handlers."""

from typing import Optional, cast

from aea.configurations.base import ProtocolId
from aea.crypto.base import LedgerApi
from aea.decision_maker.messages.transaction import TransactionMessage
from aea.protocols.base import Message
from aea.skills.base import Handler

from packages.fetchai.protocols.oef_search.message import OefSearchMessage
from packages.fetchai.protocols.tac.message import TacMessage
from packages.fetchai.protocols.tac.serialization import TacSerializer
from packages.fetchai.skills.tac_control_contract.game import Game, Phase
from packages.fetchai.skills.tac_control_contract.parameters import Parameters


class TACHandler(Handler):
    """This class handles oef messages."""

    SUPPORTED_PROTOCOL = TacMessage.protocol_id

    def setup(self) -> None:
        """
        Implement the handler setup.

        :return: None
        """
        pass

    def handle(self, message: Message) -> None:
        """
        Handle a register message.

        If the address is already registered, answer with an error message.

        :param message: the 'get agent state' TacMessage.
        :return: None
        """
        tac_message = cast(TacMessage, message)
        tac_type = tac_message.performative

        game = cast(Game, self.context.game)

        self.context.logger.debug(
            "[{}]: Handling TAC message. type={}".format(
                self.context.agent_name, tac_type
            )
        )
        if (
            tac_type == TacMessage.Performative.REGISTER
            and game.phase == Phase.GAME_REGISTRATION
        ):
            self._on_register(tac_message)
        elif (
            tac_type == TacMessage.Performative.UNREGISTER
            and game.phase == Phase.GAME_REGISTRATION
        ):
            self._on_unregister(tac_message)
        else:
            self.context.logger.warning(
                "[{}]: TAC Message type not recognized or not permitted.".format(
                    self.context.agent_name
                )
            )

    def _on_register(self, message: TacMessage) -> None:
        """
        Handle a register message.

        If the address is not registered, answer with an error message.

        :param message: the 'get agent state' TacMessage.
        :return: None
        """
        parameters = cast(Parameters, self.context.parameters)
        agent_name = message.agent_name
        if len(parameters.whitelist) != 0 and agent_name not in parameters.whitelist:
            self.context.logger.error(
                "[{}]: Agent name not in whitelist: '{}'".format(
                    self.context.agent_name, agent_name
                )
            )
            tac_msg = TacMessage(
                performative=TacMessage.Performative.TAC_ERROR,
                error_code=TacMessage.ErrorCode.AGENT_NAME_NOT_IN_WHITELIST,
            )
            self.context.outbox.put_message(
                to=message.counterparty,
                sender=self.context.agent_address,
                protocol_id=TacMessage.protocol_id,
                message=TacSerializer().encode(tac_msg),
            )
            return

        game = cast(Game, self.context.game)
        if message.counterparty in game.registration.agent_addr_to_name:
            self.context.logger.error(
                "[{}]: Agent already registered: '{}'".format(
                    self.context.agent_name,
                    game.registration.agent_addr_to_name[message.counterparty],
                )
            )
            tac_msg = TacMessage(
                performative=TacMessage.Performative.TAC_ERROR,
                error_code=TacMessage.ErrorCode.AGENT_ADDR_ALREADY_REGISTERED,
            )
            self.context.outbox.put_message(
                to=message.counterparty,
                sender=self.context.agent_address,
                protocol_id=TacMessage.protocol_id,
                message=TacSerializer().encode(tac_msg),
            )

        if agent_name in game.registration.agent_addr_to_name.values():
            self.context.logger.error(
                "[{}]: Agent with this name already registered: '{}'".format(
                    self.context.agent_name, agent_name
                )
            )
            tac_msg = TacMessage(
                performative=TacMessage.Performative.TAC_ERROR,
                error_code=TacMessage.ErrorCode.AGENT_NAME_ALREADY_REGISTERED,
            )
            self.context.outbox.put_message(
                to=message.counterparty,
                sender=self.context.agent_address,
                protocol_id=TacMessage.protocol_id,
                message=TacSerializer().encode(tac_msg),
            )
        self.context.shared_state["agents_participants_counter"] += 1
        game.registration.register_agent(message.counterparty, agent_name)
        self.context.logger.info(
            "[{}]: Agent registered: '{}'".format(self.context.agent_name, agent_name)
        )

    def _on_unregister(self, message: TacMessage) -> None:
        """
        Handle a unregister message.

        If the address is not registered, answer with an error message.

        :param message: the 'get agent state' TacMessage.
        :return: None
        """
        game = cast(Game, self.context.game)
        if message.counterparty not in game.registration.agent_addr_to_name:
            self.context.logger.error(
                "[{}]: Agent not registered: '{}'".format(
                    self.context.agent_name, message.counterparty
                )
            )
            tac_msg = TacMessage(
                performative=TacMessage.Performative.TAC_ERROR,
                error_code=TacMessage.ErrorCode.AGENT_NOT_REGISTERED,
            )
            self.context.outbox.put_message(
                to=message.counterparty,
                sender=self.context.agent_address,
                protocol_id=TacMessage.protocol_id,
                message=TacSerializer().encode(tac_msg),
            )
        else:
            self.context.logger.debug(
                "[{}]: Agent unregistered: '{}'".format(
                    self.context.agent_name,
                    game.configuration.agent_addr_to_name[message.counterparty],
                )
            )
            game.registration.unregister_agent(message.counterparty)

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass


class OEFRegistrationHandler(Handler):
    """Handle the message exchange with the OEF search node."""

    SUPPORTED_PROTOCOL = OefSearchMessage.protocol_id

    def setup(self) -> None:
        """
        Implement the handler setup.

        :return: None
        """
        pass

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        :return: None
        """
        oef_message = cast(OefSearchMessage, message)
        oef_type = oef_message.performative

        self.context.logger.debug(
            "[{}]: Handling OEF message. type={}".format(
                self.context.agent_name, oef_type
            )
        )
        if oef_type == OefSearchMessage.Performative.OEF_ERROR:
            self._on_oef_error(oef_message)
        else:
            self.context.logger.warning(
                "[{}]: OEF Message type not recognized.".format(self.context.agent_name)
            )

    def _on_oef_error(self, oef_error: OefSearchMessage) -> None:
        """
        Handle an OEF error message.

        :param oef_error: the oef error

        :return: None
        """
        self.context.logger.error(
            "[{}]: Received OEF error: dialogue_reference={}, operation={}".format(
                self.context.agent_name,
                oef_error.dialogue_reference,
                oef_error.oef_error_operation,
            )
        )

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass


class TransactionHandler(Handler):
    """Implement the transaction handler."""

    SUPPORTED_PROTOCOL = TransactionMessage.protocol_id  # type: Optional[ProtocolId]

    def __init__(self, **kwargs):
        """Instantiate the handler."""
        super().__init__(**kwargs)
        self.counter = 0

    def setup(self) -> None:
        """Implement the setup for the handler."""
        self.context.shared_state["agents_participants_counter"] = 0

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        :return: None
        """
        tx_msg_response = cast(TransactionMessage, message)
        contract = self.context.contracts.erc1155
        game = cast(Game, self.context.game)
        ledger_api = cast(LedgerApi, self.context.ledger_apis.apis.get("ethereum"))
        tac_behaviour = self.context.behaviours.tac
        if tx_msg_response.tx_id == "contract_deploy":
            self.context.logger.info("Sending deployment transaction to the ledger!")
            tx_signed = tx_msg_response.signed_payload.get("tx_signed")
            tx_digest = ledger_api.send_signed_transaction(
                is_waiting_for_confirmation=True, tx_signed=tx_signed
            )
            transaction = ledger_api.get_transaction_status(  # type: ignore
                tx_digest=tx_digest
            )
            if transaction.status != 1:
                self.context.is_active = False
                self.context.info(
                    "The contract did not deployed successfully aborting."
                )
            else:
                self.context.logger.info(
                    "The contract was successfully deployed. Contract address: {} and transaction hash: {}".format(
                        transaction.contractAddress, transaction.transactionHash.hex()
                    )
                )
                contract.set_address(ledger_api, transaction.contractAddress)
        elif tx_msg_response.tx_id == "contract_create_single":
            self.context.logger.info(
                "Sending single creation transaction to the ledger!"
            )
            tx_signed = tx_msg_response.signed_payload.get("tx_signed")
            ledger_api = cast(LedgerApi, self.context.ledger_apis.apis.get("ethereum"))
            tx_digest = ledger_api.send_signed_transaction(
                is_waiting_for_confirmation=True, tx_signed=tx_signed
            )
            transaction = ledger_api.get_transaction_status(  # type: ignore
                tx_digest=tx_digest
            )
            if transaction.status != 1:
                self.context.is_active = False
                self.context.info("The creation command wasn't successful. Aborting.")
            else:
                tac_behaviour.is_items_created = True
                self.context.logger.info(
                    "Successfully created the item. Transaction hash: {}".format(
                        transaction.transactionHash.hex()
                    )
                )
        elif tx_msg_response.tx_id == "contract_create_batch":
            self.context.logger.info("Sending creation transaction to the ledger!")
            tx_signed = tx_msg_response.signed_payload.get("tx_signed")
            ledger_api = cast(LedgerApi, self.context.ledger_apis.apis.get("ethereum"))
            tx_digest = ledger_api.send_signed_transaction(
                is_waiting_for_confirmation=True, tx_signed=tx_signed
            )
            transaction = ledger_api.get_transaction_status(  # type: ignore
                tx_digest=tx_digest
            )
            if transaction.status != 1:
                self.context.is_active = False
                self.context.info("The creation command wasn't successful. Aborting.")
            else:
                self.context.logger.info(
                    "Successfully created the items. Transaction hash: {}".format(
                        transaction.transactionHash.hex()
                    )
                )
        elif tx_msg_response.tx_id == "contract_mint_batch":
            self.context.logger.info("Sending minting transaction to the ledger!")
            tx_signed = tx_msg_response.signed_payload.get("tx_signed")
            ledger_api = cast(LedgerApi, self.context.ledger_apis.apis.get("ethereum"))
            tx_digest = ledger_api.send_signed_transaction(
                is_waiting_for_confirmation=True, tx_signed=tx_signed
            )
            transaction = ledger_api.get_transaction_status(  # type: ignore
                tx_digest=tx_digest
            )
            if transaction.status != 1:
                self.context.is_active = False
                self.context.logger.info(
                    "The mint command wasn't successful. Aborting."
                )
                self.context.logger.info(transaction)
            else:
                self.counter += 1
                self.context.logger.info(
                    "Successfully minted the items. Transaction hash: {}".format(
                        transaction.transactionHash.hex()
                    )
                )
                if tac_behaviour.agent_counter == game.registration.nb_agents:
                    self.context.logger.info("Can start the game.!")
                    tac_behaviour.can_start = True

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass
