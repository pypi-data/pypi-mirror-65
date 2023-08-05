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
from .Hash256Dto import Hash256Dto
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .UnresolvedAddressDto import UnresolvedAddressDto


class SecretProofTransactionBodyBuilder:
    """Binary layout for a secret proof transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, secret: Hash256Dto, hashAlgorithm: LockHashAlgorithmDto, recipientAddress: UnresolvedAddressDto, proof: bytes):
        """Constructor.
        Args:
            secret: Secret.
            hashAlgorithm: Hash algorithm.
            recipientAddress: Locked mosaic recipient address.
            proof: Proof data.
        """
        self.secret = secret
        self.hashAlgorithm = hashAlgorithm
        self.recipientAddress = recipientAddress
        self.proof = proof

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> SecretProofTransactionBodyBuilder:
        """Creates an instance of SecretProofTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of SecretProofTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        secret = Hash256Dto.loadFromBinary(bytes_)
        bytes_ = bytes_[secret.getSize():]
        proofSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))
        bytes_ = bytes_[2:]
        # gen: _load_from_binary_custom
        hashAlgorithm = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        # gen: _load_from_binary_custom
        recipientAddress = UnresolvedAddressDto.loadFromBinary(bytes_)
        bytes_ = bytes_[recipientAddress.getSize():]
        # gen: _load_from_binary_buffer
        proof = GeneratorUtils.getBytes(bytes_, proofSize)
        bytes_ = bytes_[proofSize:]
        return SecretProofTransactionBodyBuilder(secret, hashAlgorithm, recipientAddress, proof)

    def getSecret(self) -> Hash256Dto:
        """Gets secret.
        Returns:
            Secret.
        """
        return self.secret

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

    def getProof(self) -> bytes:
        """Gets proof data.
        Returns:
            Proof data.
        """
        return self.proof

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.secret.getSize()
        size += 2  # proofSize
        size += 1  # hashAlgorithm
        size += self.recipientAddress.getSize()
        size += len(self.proof)
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        secretBytes = self.secret.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, secretBytes)
        proofSizeBytes = GeneratorUtils.uintToBuffer(len(self.proof), 2)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, proofSizeBytes)
        hashAlgorithmBytes = GeneratorUtils.uintToBuffer(self.hashAlgorithm, 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, hashAlgorithmBytes)
        recipientAddressBytes = self.recipientAddress.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, recipientAddressBytes)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.proof)
        return bytes_
