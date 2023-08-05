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
from .NamespaceIdDto import NamespaceIdDto
from .NamespaceMetadataTransactionBodyBuilder import NamespaceMetadataTransactionBodyBuilder
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder


class NamespaceMetadataTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded namespace metadata transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, targetPublicKey: KeyDto, scopedMetadataKey: int, targetNamespaceId: NamespaceIdDto, valueSizeDelta: int, value: bytes):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            targetPublicKey: Metadata target public key.
            scopedMetadataKey: Metadata key scoped to source, target and type.
            targetNamespaceId: Target namespace identifier.
            valueSizeDelta: Change in value size in bytes.
            value: Difference between existing value and new value.
        @note when there is no existing value, new value is same this value.
        @note when there is an existing value, new value is calculated as xor(previous-value, value).
        """
        super().__init__(signature, signerPublicKey, version, network, type_, fee, deadline)
        self.namespaceMetadataTransactionBody = NamespaceMetadataTransactionBodyBuilder(targetPublicKey, scopedMetadataKey, targetNamespaceId, valueSizeDelta, value)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> NamespaceMetadataTransactionBuilder:
        """Creates an instance of NamespaceMetadataTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of NamespaceMetadataTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        namespaceMetadataTransactionBody = NamespaceMetadataTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[namespaceMetadataTransactionBody.getSize():]
        return NamespaceMetadataTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, superObject.fee, superObject.deadline, namespaceMetadataTransactionBody.targetPublicKey, namespaceMetadataTransactionBody.scopedMetadataKey, namespaceMetadataTransactionBody.targetNamespaceId, namespaceMetadataTransactionBody.valueSizeDelta, namespaceMetadataTransactionBody.value)

    def getTargetPublicKey(self) -> KeyDto:
        """Gets metadata target public key.
        Returns:
            Metadata target public key.
        """
        return self.namespaceMetadataTransactionBody.getTargetPublicKey()

    def getScopedMetadataKey(self) -> int:
        """Gets metadata key scoped to source, target and type.
        Returns:
            Metadata key scoped to source, target and type.
        """
        return self.namespaceMetadataTransactionBody.getScopedMetadataKey()

    def getTargetNamespaceId(self) -> NamespaceIdDto:
        """Gets target namespace identifier.
        Returns:
            Target namespace identifier.
        """
        return self.namespaceMetadataTransactionBody.getTargetNamespaceId()

    def getValueSizeDelta(self) -> int:
        """Gets change in value size in bytes.
        Returns:
            Change in value size in bytes.
        """
        return self.namespaceMetadataTransactionBody.getValueSizeDelta()

    def getValue(self) -> bytes:
        """Gets difference between existing value and new value.
        @note when there is no existing value, new value is same this value.
        @note when there is an existing value, new value is calculated as xor(previous-value, value).
        Returns:
            Difference between existing value and new value.
        @note when there is no existing value, new value is same this value.
        @note when there is an existing value, new value is calculated as xor(previous-value, value).
        """
        return self.namespaceMetadataTransactionBody.getValue()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.namespaceMetadataTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        namespaceMetadataTransactionBodyBytes = self.namespaceMetadataTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, namespaceMetadataTransactionBodyBytes)
        return bytes_
