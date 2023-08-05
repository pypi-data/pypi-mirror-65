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
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .MosaicSupplyChangeActionDto import MosaicSupplyChangeActionDto
from .MosaicSupplyChangeTransactionBodyBuilder import MosaicSupplyChangeTransactionBodyBuilder
from .NetworkTypeDto import NetworkTypeDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto


class EmbeddedMosaicSupplyChangeTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded mosaic supply change transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, mosaicId: UnresolvedMosaicIdDto, delta: AmountDto, action: MosaicSupplyChangeActionDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            mosaicId: Affected mosaic identifier.
            delta: Change amount.
            action: Supply change action.
        """
        super().__init__(signerPublicKey, version, network, type_)
        self.mosaicSupplyChangeTransactionBody = MosaicSupplyChangeTransactionBodyBuilder(mosaicId, delta, action)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedMosaicSupplyChangeTransactionBuilder:
        """Creates an instance of EmbeddedMosaicSupplyChangeTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedMosaicSupplyChangeTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        mosaicSupplyChangeTransactionBody = MosaicSupplyChangeTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaicSupplyChangeTransactionBody.getSize():]
        return EmbeddedMosaicSupplyChangeTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, mosaicSupplyChangeTransactionBody.mosaicId, mosaicSupplyChangeTransactionBody.delta, mosaicSupplyChangeTransactionBody.action)

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
