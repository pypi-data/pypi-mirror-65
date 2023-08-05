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
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto


class TransactionBuilder:
    """Binary layout for a transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, fee: AmountDto, deadline: TimestampDto):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
        """
        self.verifiableEntityHeader_Reserved1 = 0
        self.signature = signature
        self.signerPublicKey = signerPublicKey
        self.entityBody_Reserved1 = 0
        self.version = version
        self.network = network
        self.type_ = type_
        self.fee = fee
        self.deadline = deadline

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> TransactionBuilder:
        """Creates an instance of TransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of TransactionBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_simple
        # pylint: disable=unused-variable
        size = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        bytes_ = bytes_[4:]
        # gen: _load_from_binary_simple
        # pylint: disable=unused-variable
        verifiableEntityHeader_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        bytes_ = bytes_[4:]
        # gen: _load_from_binary_custom
        signature = SignatureDto.loadFromBinary(bytes_)
        bytes_ = bytes_[signature.getSize():]
        # gen: _load_from_binary_custom
        signerPublicKey = KeyDto.loadFromBinary(bytes_)
        bytes_ = bytes_[signerPublicKey.getSize():]
        # gen: _load_from_binary_simple
        # pylint: disable=unused-variable
        entityBody_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        bytes_ = bytes_[4:]
        # gen: _load_from_binary_simple
        version = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        # gen: _load_from_binary_custom
        network = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        # gen: _load_from_binary_custom
        type_ = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))
        bytes_ = bytes_[2:]
        # gen: _load_from_binary_custom
        fee = AmountDto.loadFromBinary(bytes_)
        bytes_ = bytes_[fee.getSize():]
        # gen: _load_from_binary_custom
        deadline = TimestampDto.loadFromBinary(bytes_)
        bytes_ = bytes_[deadline.getSize():]
        return TransactionBuilder(signature, signerPublicKey, version, network, type_, fee, deadline)

    def getVerifiableEntityHeader_Reserved1(self) -> int:
        """Gets reserved padding to align Signature on 8-byte boundary.
        Returns:
            Reserved padding to align Signature on 8-byte boundary.
        """
        return self.verifiableEntityHeader_Reserved1

    def getSignature(self) -> SignatureDto:
        """Gets entity signature.
        Returns:
            Entity signature.
        """
        return self.signature

    def getSignerPublicKey(self) -> KeyDto:
        """Gets entity signer's public key.
        Returns:
            Entity signer's public key.
        """
        return self.signerPublicKey

    def getEntityBody_Reserved1(self) -> int:
        """Gets reserved padding to align end of EntityBody on 8-byte boundary.
        Returns:
            Reserved padding to align end of EntityBody on 8-byte boundary.
        """
        return self.entityBody_Reserved1

    def getVersion(self) -> int:
        """Gets entity version.
        Returns:
            Entity version.
        """
        return self.version

    def getNetwork(self) -> NetworkTypeDto:
        """Gets entity network.
        Returns:
            Entity network.
        """
        return self.network

    def getType_(self) -> EntityTypeDto:
        """Gets entity type.
        Returns:
            Entity type.
        """
        return self.type_

    def getFee(self) -> AmountDto:
        """Gets transaction fee.
        Returns:
            Transaction fee.
        """
        return self.fee

    def getDeadline(self) -> TimestampDto:
        """Gets transaction deadline.
        Returns:
            Transaction deadline.
        """
        return self.deadline

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 4  # size
        size += 4  # verifiableEntityHeader_Reserved1
        size += self.signature.getSize()
        size += self.signerPublicKey.getSize()
        size += 4  # entityBody_Reserved1
        size += 1  # version
        size += 1  # network
        size += 2  # type_
        size += self.fee.getSize()
        size += self.deadline.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        sizeBytes = GeneratorUtils.uintToBuffer(self.getSize(), 4)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, sizeBytes)
        verifiableEntityHeader_Reserved1Bytes = GeneratorUtils.uintToBuffer(self.getVerifiableEntityHeader_Reserved1(), 4)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, verifiableEntityHeader_Reserved1Bytes)
        signatureBytes = self.signature.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, signatureBytes)
        signerPublicKeyBytes = self.signerPublicKey.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, signerPublicKeyBytes)
        entityBody_Reserved1Bytes = GeneratorUtils.uintToBuffer(self.getEntityBody_Reserved1(), 4)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, entityBody_Reserved1Bytes)
        versionBytes = GeneratorUtils.uintToBuffer(self.getVersion(), 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, versionBytes)
        networkBytes = GeneratorUtils.uintToBuffer(self.network, 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, networkBytes)
        type_Bytes = GeneratorUtils.uintToBuffer(self.type_, 2)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, type_Bytes)
        feeBytes = self.fee.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, feeBytes)
        deadlineBytes = self.deadline.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, deadlineBytes)
        return bytes_
