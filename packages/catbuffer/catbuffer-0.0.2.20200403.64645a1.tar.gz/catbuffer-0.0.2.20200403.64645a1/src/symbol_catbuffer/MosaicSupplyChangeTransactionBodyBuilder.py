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
from .GeneratorUtils import GeneratorUtils
from .MosaicSupplyChangeActionDto import MosaicSupplyChangeActionDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto


class MosaicSupplyChangeTransactionBodyBuilder:
    """Binary layout for a mosaic supply change transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, mosaicId: UnresolvedMosaicIdDto, delta: AmountDto, action: MosaicSupplyChangeActionDto):
        """Constructor.
        Args:
            mosaicId: Affected mosaic identifier.
            delta: Change amount.
            action: Supply change action.
        """
        self.mosaicId = mosaicId
        self.delta = delta
        self.action = action

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicSupplyChangeTransactionBodyBuilder:
        """Creates an instance of MosaicSupplyChangeTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicSupplyChangeTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        mosaicId = UnresolvedMosaicIdDto.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaicId.getSize():]
        # gen: _load_from_binary_custom
        delta = AmountDto.loadFromBinary(bytes_)
        bytes_ = bytes_[delta.getSize():]
        # gen: _load_from_binary_custom
        action = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        return MosaicSupplyChangeTransactionBodyBuilder(mosaicId, delta, action)

    def getMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets affected mosaic identifier.
        Returns:
            Affected mosaic identifier.
        """
        return self.mosaicId

    def getDelta(self) -> AmountDto:
        """Gets change amount.
        Returns:
            Change amount.
        """
        return self.delta

    def getAction(self) -> MosaicSupplyChangeActionDto:
        """Gets supply change action.
        Returns:
            Supply change action.
        """
        return self.action

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.mosaicId.getSize()
        size += self.delta.getSize()
        size += 1  # action
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        mosaicIdBytes = self.mosaicId.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicIdBytes)
        deltaBytes = self.delta.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, deltaBytes)
        actionBytes = GeneratorUtils.uintToBuffer(self.action, 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, actionBytes)
        return bytes_
