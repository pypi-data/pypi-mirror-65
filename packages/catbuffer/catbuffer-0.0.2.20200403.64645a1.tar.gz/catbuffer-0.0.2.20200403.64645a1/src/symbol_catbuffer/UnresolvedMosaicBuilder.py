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
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto


class UnresolvedMosaicBuilder:
    """Binary layout for an unresolved mosaic."""

    def __init__(self, mosaicId: UnresolvedMosaicIdDto, amount: AmountDto):
        """Constructor.
        Args:
            mosaicId: Mosaic identifier.
            amount: Mosaic amount.
        """
        self.mosaicId = mosaicId
        self.amount = amount

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> UnresolvedMosaicBuilder:
        """Creates an instance of UnresolvedMosaicBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of UnresolvedMosaicBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        mosaicId = UnresolvedMosaicIdDto.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaicId.getSize():]
        # gen: _load_from_binary_custom
        amount = AmountDto.loadFromBinary(bytes_)
        bytes_ = bytes_[amount.getSize():]
        return UnresolvedMosaicBuilder(mosaicId, amount)

    def getMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets mosaic identifier.
        Returns:
            Mosaic identifier.
        """
        return self.mosaicId

    def getAmount(self) -> AmountDto:
        """Gets mosaic amount.
        Returns:
            Mosaic amount.
        """
        return self.amount

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.mosaicId.getSize()
        size += self.amount.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        mosaicIdBytes = self.mosaicId.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicIdBytes)
        amountBytes = self.amount.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, amountBytes)
        return bytes_
