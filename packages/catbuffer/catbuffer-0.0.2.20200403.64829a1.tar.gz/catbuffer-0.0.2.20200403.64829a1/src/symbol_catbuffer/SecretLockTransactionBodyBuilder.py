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
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder


class SecretLockTransactionBodyBuilder:
    """Binary layout for a secret lock transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, secret: Hash256Dto, mosaic: UnresolvedMosaicBuilder, duration: BlockDurationDto, hashAlgorithm: LockHashAlgorithmDto, recipientAddress: UnresolvedAddressDto):
        """Constructor.
        Args:
            secret: Secret.
            mosaic: Locked mosaic.
            duration: Number of blocks for which a lock should be valid.
            hashAlgorithm: Hash algorithm.
            recipientAddress: Locked mosaic recipient address.
        """
        self.secret = secret
        self.mosaic = mosaic
        self.duration = duration
        self.hashAlgorithm = hashAlgorithm
        self.recipientAddress = recipientAddress

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> SecretLockTransactionBodyBuilder:
        """Creates an instance of SecretLockTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of SecretLockTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        secret = Hash256Dto.loadFromBinary(bytes_)
        bytes_ = bytes_[secret.getSize():]
        # gen: _load_from_binary_custom
        mosaic = UnresolvedMosaicBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaic.getSize():]
        # gen: _load_from_binary_custom
        duration = BlockDurationDto.loadFromBinary(bytes_)
        bytes_ = bytes_[duration.getSize():]
        # gen: _load_from_binary_custom
        hashAlgorithm = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        # gen: _load_from_binary_custom
        recipientAddress = UnresolvedAddressDto.loadFromBinary(bytes_)
        bytes_ = bytes_[recipientAddress.getSize():]
        return SecretLockTransactionBodyBuilder(secret, mosaic, duration, hashAlgorithm, recipientAddress)

    def getSecret(self) -> Hash256Dto:
        """Gets secret.
        Returns:
            Secret.
        """
        return self.secret

    def getMosaic(self) -> UnresolvedMosaicBuilder:
        """Gets locked mosaic.
        Returns:
            Locked mosaic.
        """
        return self.mosaic

    def getDuration(self) -> BlockDurationDto:
        """Gets number of blocks for which a lock should be valid.
        Returns:
            Number of blocks for which a lock should be valid.
        """
        return self.duration

    def getHashAlgorithm(self) -> LockHashAlgorithmDto:
        """Gets hash algorithm.
        Returns:
            Hash algorithm.
        """
        return self.hashAlgorithm

    def getRecipientAddress(self) -> UnresolvedAddressDto:
        """Gets locked mosaic recipient address.
        Returns:
            Locked mosaic recipient address.
        """
        return self.recipientAddress

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.secret.getSize()
        size += self.mosaic.getSize()
        size += self.duration.getSize()
        size += 1  # hashAlgorithm
        size += self.recipientAddress.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        secretBytes = self.secret.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, secretBytes)
        mosaicBytes = self.mosaic.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicBytes)
        durationBytes = self.duration.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, durationBytes)
        hashAlgorithmBytes = GeneratorUtils.uintToBuffer(self.hashAlgorithm, 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, hashAlgorithmBytes)
        recipientAddressBytes = self.recipientAddress.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, recipientAddressBytes)
        return bytes_
