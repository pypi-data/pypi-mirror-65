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
from typing import List
from .AmountDto import AmountDto
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder
from .TransferTransactionBodyBuilder import TransferTransactionBodyBuilder
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder


class TransferTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded transfer transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, recipientAddress: UnresolvedAddressDto, mosaics: List[UnresolvedMosaicBuilder], message: bytes):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            recipientAddress: Recipient address.
            mosaics: Attached mosaics.
            message: Attached message.
        """
        super().__init__(signature, signerPublicKey, version, network, type_, fee, deadline)
        self.transferTransactionBody = TransferTransactionBodyBuilder(recipientAddress, mosaics, message)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> TransferTransactionBuilder:
        """Creates an instance of TransferTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of TransferTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        transferTransactionBody = TransferTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[transferTransactionBody.getSize():]
        return TransferTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, superObject.fee, superObject.deadline, transferTransactionBody.recipientAddress, transferTransactionBody.mosaics, transferTransactionBody.message)

    def getRecipientAddress(self) -> UnresolvedAddressDto:
        """Gets recipient address.
        Returns:
            Recipient address.
        """
        return self.transferTransactionBody.getRecipientAddress()

    def getTransferTransactionBody_Reserved1(self) -> int:
        """Gets reserved padding to align mosaics on 8-byte boundary.
        Returns:
            Reserved padding to align mosaics on 8-byte boundary.
        """
        return self.transferTransactionBody.getTransferTransactionBody_Reserved1()

    def getMosaics(self) -> List[UnresolvedMosaicBuilder]:
        """Gets attached mosaics.
        Returns:
            Attached mosaics.
        """
        return self.transferTransactionBody.getMosaics()

    def getMessage(self) -> bytes:
        """Gets attached message.
        Returns:
            Attached message.
        """
        return self.transferTransactionBody.getMessage()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.transferTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        transferTransactionBodyBytes = self.transferTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, transferTransactionBodyBytes)
        return bytes_
