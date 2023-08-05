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
from .KeyDto import KeyDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto


class MosaicMetadataTransactionBodyBuilder:
    """Binary layout for a mosaic metadata transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, targetPublicKey: KeyDto, scopedMetadataKey: int, targetMosaicId: UnresolvedMosaicIdDto, valueSizeDelta: int, value: bytes):
        """Constructor.
        Args:
            targetPublicKey: Metadata target public key.
            scopedMetadataKey: Metadata key scoped to source, target and type.
            targetMosaicId: Target mosaic identifier.
            valueSizeDelta: Change in value size in bytes.
            value: Difference between existing value and new value.
        @note when there is no existing value, new value is same this value.
        @note when there is an existing value, new value is calculated as xor(previous-value, value).
        """
        self.targetPublicKey = targetPublicKey
        self.scopedMetadataKey = scopedMetadataKey
        self.targetMosaicId = targetMosaicId
        self.valueSizeDelta = valueSizeDelta
        self.value = value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicMetadataTransactionBodyBuilder:
        """Creates an instance of MosaicMetadataTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicMetadataTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        targetPublicKey = KeyDto.loadFromBinary(bytes_)
        bytes_ = bytes_[targetPublicKey.getSize():]
        # gen: _load_from_binary_simple
        scopedMetadataKey = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))
        bytes_ = bytes_[8:]
        # gen: _load_from_binary_custom
        targetMosaicId = UnresolvedMosaicIdDto.loadFromBinary(bytes_)
        bytes_ = bytes_[targetMosaicId.getSize():]
        # gen: _load_from_binary_simple
        valueSizeDelta = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))
        bytes_ = bytes_[2:]
        valueSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))
        bytes_ = bytes_[2:]
        # gen: _load_from_binary_buffer
        value = GeneratorUtils.getBytes(bytes_, valueSize)
        bytes_ = bytes_[valueSize:]
        return MosaicMetadataTransactionBodyBuilder(targetPublicKey, scopedMetadataKey, targetMosaicId, valueSizeDelta, value)

    def getTargetPublicKey(self) -> KeyDto:
        """Gets metadata target public key.
        Returns:
            Metadata target public key.
        """
        return self.targetPublicKey

    def getScopedMetadataKey(self) -> int:
        """Gets metadata key scoped to source, target and type.
        Returns:
            Metadata key scoped to source, target and type.
        """
        return self.scopedMetadataKey

    def getTargetMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets target mosaic identifier.
        Returns:
            Target mosaic identifier.
        """
        return self.targetMosaicId

    def getValueSizeDelta(self) -> int:
        """Gets change in value size in bytes.
        Returns:
            Change in value size in bytes.
        """
        return self.valueSizeDelta

    def getValue(self) -> bytes:
        """Gets difference between existing value and new value.
        @note when there is no existing value, new value is same this value.
        @note when there is an existing value, new value is calculated as xor(previous-value, value).
        Returns:
            Difference between existing value and new value.
        @note when there is no existing value, new value is same this value.
        @note when there is an existing value, new value is calculated as xor(previous-value, value).
        """
        return self.value

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.targetPublicKey.getSize()
        size += 8  # scopedMetadataKey
        size += self.targetMosaicId.getSize()
        size += 2  # valueSizeDelta
        size += 2  # valueSize
        size += len(self.value)
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        targetPublicKeyBytes = self.targetPublicKey.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, targetPublicKeyBytes)
        scopedMetadataKeyBytes = GeneratorUtils.uintToBuffer(self.getScopedMetadataKey(), 8)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, scopedMetadataKeyBytes)
        targetMosaicIdBytes = self.targetMosaicId.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, targetMosaicIdBytes)
        valueSizeDeltaBytes = GeneratorUtils.uintToBuffer(self.getValueSizeDelta(), 2)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, valueSizeDeltaBytes)
        valueSizeBytes = GeneratorUtils.uintToBuffer(len(self.value), 2)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, valueSizeBytes)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.value)
        return bytes_
