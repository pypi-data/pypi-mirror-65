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
from .AmountDto import AmountDto
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .MosaicSupplyChangeActionDto import MosaicSupplyChangeActionDto
from .MosaicSupplyChangeTransactionBodyBuilder import MosaicSupplyChangeTransactionBodyBuilder
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto


class MosaicSupplyChangeTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded mosaic supply change transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, mosaicId: UnresolvedMosaicIdDto, delta: AmountDto, action: MosaicSupplyChangeActionDto):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            mosaicId: Affected mosaic identifier.
            delta: Change amount.
            action: Supply change action.
        """
        super().__init__(signature, signerPublicKey, version, network, type_, fee, deadline)
        self.mosaicSupplyChangeTransactionBody = MosaicSupplyChangeTransactionBodyBuilder(mosaicId, delta, action)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicSupplyChangeTransactionBuilder:
        """Creates an instance of MosaicSupplyChangeTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicSupplyChangeTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        mosaicSupplyChangeTransactionBody = MosaicSupplyChangeTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaicSupplyChangeTransactionBody.getSize():]
        return MosaicSupplyChangeTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, superObject.fee, superObject.deadline, mosaicSupplyChangeTransactionBody.mosaicId, mosaicSupplyChangeTransactionBody.delta, mosaicSupplyChangeTransactionBody.action)

    def getMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets affected mosaic identifier.
        Returns:
            Affected mosaic identifier.
        """
        return self.mosaicSupplyChangeTransactionBody.getMosaicId()

    def getDelta(self) -> AmountDto:
        """Gets change amount.
        Returns:
            Change amount.
        """
        return self.mosaicSupplyChangeTransactionBody.getDelta()

    def getAction(self) -> MosaicSupplyChangeActionDto:
        """Gets supply change action.
        Returns:
            Supply change action.
        """
        return self.mosaicSupplyChangeTransactionBody.getAction()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.mosaicSupplyChangeTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        mosaicSupplyChangeTransactionBodyBytes = self.mosaicSupplyChangeTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicSupplyChangeTransactionBodyBytes)
        return bytes_
