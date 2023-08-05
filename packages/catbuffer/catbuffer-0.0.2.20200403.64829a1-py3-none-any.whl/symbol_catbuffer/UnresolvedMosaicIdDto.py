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
from .GeneratorUtils import GeneratorUtils


class UnresolvedMosaicIdDto:
    """Unresolved mosaic id."""

    def __init__(self, unresolvedMosaicId: int):
        """Constructor.
        Args:
            unresolvedMosaicId: Unresolved mosaic id.
        """
        self.unresolvedMosaicId = unresolvedMosaicId

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> UnresolvedMosaicIdDto:
        """Creates an instance of UnresolvedMosaicIdDto from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of UnresolvedMosaicIdDto.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_simple
        unresolvedMosaicId = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))
        bytes_ = bytes_[8:]
        return UnresolvedMosaicIdDto(unresolvedMosaicId)

    def getUnresolvedMosaicId(self) -> int:
        """Gets Unresolved mosaic id.
        Returns:
            Unresolved mosaic id.
        """
        return self.unresolvedMosaicId

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 8

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        unresolvedMosaicIdBytes = GeneratorUtils.uintToBuffer(self.getUnresolvedMosaicId(), 8)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, unresolvedMosaicIdBytes)
        return bytes_
