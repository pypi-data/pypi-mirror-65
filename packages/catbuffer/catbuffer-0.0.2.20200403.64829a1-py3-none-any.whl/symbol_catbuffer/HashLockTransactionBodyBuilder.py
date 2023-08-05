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
from .Hash256Dto import Hash256Dto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder


class HashLockTransactionBodyBuilder:
    """Binary layout for a hash lock transaction."""

    def __init__(self, mosaic: UnresolvedMosaicBuilder, duration: BlockDurationDto, hash_: Hash256Dto):
        """Constructor.
        Args:
            mosaic: Lock mosaic.
            duration: Number of blocks for which a lock should be valid.
            hash_: Lock hash.
        """
        self.mosaic = mosaic
        self.duration = duration
        self.hash_ = hash_

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> HashLockTransactionBodyBuilder:
        """Creates an instance of HashLockTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of HashLockTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        mosaic = UnresolvedMosaicBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaic.getSize():]
        # gen: _load_from_binary_custom
        duration = BlockDurationDto.loadFromBinary(bytes_)
        bytes_ = bytes_[duration.getSize():]
        # gen: _load_from_binary_custom
        hash_ = Hash256Dto.loadFromBinary(bytes_)
        bytes_ = bytes_[hash_.getSize():]
        return HashLockTransactionBodyBuilder(mosaic, duration, hash_)

    def getMosaic(self) -> UnresolvedMosaicBuilder:
        """Gets lock mosaic.
        Returns:
            Lock mosaic.
        """
        return self.mosaic

    def getDuration(self) -> BlockDurationDto:
        """Gets number of blocks for which a lock should be valid.
        Returns:
            Number of blocks for which a lock should be valid.
        """
        return self.duration

    def getHash_(self) -> Hash256Dto:
        """Gets lock hash.
        Returns:
            Lock hash.
        """
        return self.hash_

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.mosaic.getSize()
        size += self.duration.getSize()
        size += self.hash_.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        mosaicBytes = self.mosaic.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicBytes)
        durationBytes = self.duration.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, durationBytes)
        hash_Bytes = self.hash_.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, hash_Bytes)
        return bytes_
