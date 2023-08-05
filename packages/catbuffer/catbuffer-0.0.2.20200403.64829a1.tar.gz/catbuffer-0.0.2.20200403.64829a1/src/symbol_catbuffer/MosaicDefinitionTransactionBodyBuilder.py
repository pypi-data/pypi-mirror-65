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
from .BlockDurationDto import BlockDurationDto
from .GeneratorUtils import GeneratorUtils
from .MosaicIdDto import MosaicIdDto
from .MosaicNonceDto import MosaicNonceDto


class MosaicDefinitionTransactionBodyBuilder:
    """Binary layout for a mosaic definition transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, id_: MosaicIdDto, duration: BlockDurationDto, nonce: MosaicNonceDto, flags: int, divisibility: int):
        """Constructor.
        Args:
            id_: Mosaic identifier.
            duration: Mosaic duration.
            nonce: Mosaic nonce.
            flags: Mosaic flags.
            divisibility: Mosaic divisibility.
        """
        self.id_ = id_
        self.duration = duration
        self.nonce = nonce
        self.flags = flags
        self.divisibility = divisibility

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicDefinitionTransactionBodyBuilder:
        """Creates an instance of MosaicDefinitionTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicDefinitionTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        id_ = MosaicIdDto.loadFromBinary(bytes_)
        bytes_ = bytes_[id_.getSize():]
        # gen: _load_from_binary_custom
        duration = BlockDurationDto.loadFromBinary(bytes_)
        bytes_ = bytes_[duration.getSize():]
        # gen: _load_from_binary_custom
        nonce = MosaicNonceDto.loadFromBinary(bytes_)
        bytes_ = bytes_[nonce.getSize():]
        # gen: _load_from_binary_flags
        flags = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        # gen: _load_from_binary_simple
        divisibility = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        return MosaicDefinitionTransactionBodyBuilder(id_, duration, nonce, flags, divisibility)

    def getId_(self) -> MosaicIdDto:
        """Gets mosaic identifier.
        Returns:
            Mosaic identifier.
        """
        return self.id_

    def getDuration(self) -> BlockDurationDto:
        """Gets mosaic duration.
        Returns:
            Mosaic duration.
        """
        return self.duration

    def getNonce(self) -> MosaicNonceDto:
        """Gets mosaic nonce.
        Returns:
            Mosaic nonce.
        """
        return self.nonce

    def getFlags(self) -> int:
        """Gets mosaic flags.
        Returns:
            Mosaic flags.
        """
        return self.flags

    def getDivisibility(self) -> int:
        """Gets mosaic divisibility.
        Returns:
            Mosaic divisibility.
        """
        return self.divisibility

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.id_.getSize()
        size += self.duration.getSize()
        size += self.nonce.getSize()
        size += 1  # flags
        size += 1  # divisibility
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        id_Bytes = self.id_.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, id_Bytes)
        durationBytes = self.duration.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, durationBytes)
        nonceBytes = self.nonce.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, nonceBytes)
        flagsBytes = GeneratorUtils.uintToBuffer(self.getFlags(), 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, flagsBytes)
        divisibilityBytes = GeneratorUtils.uintToBuffer(self.getDivisibility(), 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, divisibilityBytes)
        return bytes_
