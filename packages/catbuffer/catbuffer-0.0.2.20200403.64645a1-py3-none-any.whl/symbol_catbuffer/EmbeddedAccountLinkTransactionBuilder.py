#!/usr/bin/python
"""
    Copyright (c) 2016-present,
    Jaguar0625, gimre, BloodyRookie, Tech Bureau, Corp. All rights reserved.

    This file is part of Catapult.

    Catapult is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Catapult is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Catapult. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations
from .AccountLinkActionDto import AccountLinkActionDto
from .AccountLinkTransactionBodyBuilder import AccountLinkTransactionBodyBuilder
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto


class EmbeddedAccountLinkTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded account link transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, remotePublicKey: KeyDto, linkAction: AccountLinkActionDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            remotePublicKey: Remote public key.
            linkAction: Account link action.
        """
        super().__init__(signerPublicKey, version, network, type_)
        self.accountLinkTransactionBody = AccountLinkTransactionBodyBuilder(remotePublicKey, linkAction)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedAccountLinkTransactionBuilder:
        """Creates an instance of EmbeddedAccountLinkTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedAccountLinkTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        accountLinkTransactionBody = AccountLinkTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[accountLinkTransactionBody.getSize():]
        return EmbeddedAccountLinkTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, accountLinkTransactionBody.remotePublicKey, accountLinkTransactionBody.linkAction)

    def getRemotePublicKey(self) -> KeyDto:
        """Gets remote public key.
        Returns:
            Remote public key.
        """
        return self.accountLinkTransactionBody.getRemotePublicKey()

    def getLinkAction(self) -> AccountLinkActionDto:
        """Gets account link action.
        Returns:
            Account link action.
        """
        return self.accountLinkTransactionBody.getLinkAction()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.accountLinkTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        accountLinkTransactionBodyBytes = self.accountLinkTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, accountLinkTransactionBodyBytes)
        return bytes_
