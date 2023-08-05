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
from .BlockDurationDto import BlockDurationDto
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .NamespaceIdDto import NamespaceIdDto
from .NamespaceRegistrationTransactionBodyBuilder import NamespaceRegistrationTransactionBodyBuilder
from .NamespaceRegistrationTypeDto import NamespaceRegistrationTypeDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder


class NamespaceRegistrationTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded namespace registration transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, id_: NamespaceIdDto, name: bytes, duration: BlockDurationDto, parentId: NamespaceIdDto):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            duration: Namespace duration.
            parentId: Parent namespace identifier.
            id_: Namespace identifier.
            name: Namespace name.
        """
        super().__init__(signature, signerPublicKey, version, network, type_, fee, deadline)
        if (duration is None and parentId is None) or (duration is not None and parentId is not None):
            raise Exception('Invalid conditional parameters')
        self.namespaceRegistrationTransactionBody = NamespaceRegistrationTransactionBodyBuilder(id_, name, duration, parentId)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> NamespaceRegistrationTransactionBuilder:
        """Creates an instance of NamespaceRegistrationTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of NamespaceRegistrationTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        namespaceRegistrationTransactionBody = NamespaceRegistrationTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[namespaceRegistrationTransactionBody.getSize():]
        return NamespaceRegistrationTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, superObject.fee, superObject.deadline, namespaceRegistrationTransactionBody.id_, namespaceRegistrationTransactionBody.name, namespaceRegistrationTransactionBody.duration, namespaceRegistrationTransactionBody.parentId)

    def getDuration(self) -> BlockDurationDto:
        """Gets namespace duration.
        Returns:
            Namespace duration.
        """
        return self.namespaceRegistrationTransactionBody.getDuration()

    def getParentId(self) -> NamespaceIdDto:
        """Gets parent namespace identifier.
        Returns:
            Parent namespace identifier.
        """
        return self.namespaceRegistrationTransactionBody.getParentId()

    def getId_(self) -> NamespaceIdDto:
        """Gets namespace identifier.
        Returns:
            Namespace identifier.
        """
        return self.namespaceRegistrationTransactionBody.getId_()

    def getRegistrationType(self) -> NamespaceRegistrationTypeDto:
        """Gets namespace registration type.
        Returns:
            Namespace registration type.
        """
        return self.namespaceRegistrationTransactionBody.getRegistrationType()

    def getName(self) -> bytes:
        """Gets namespace name.
        Returns:
            Namespace name.
        """
        return self.namespaceRegistrationTransactionBody.getName()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.namespaceRegistrationTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        namespaceRegistrationTransactionBodyBytes = self.namespaceRegistrationTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, namespaceRegistrationTransactionBodyBytes)
        return bytes_
