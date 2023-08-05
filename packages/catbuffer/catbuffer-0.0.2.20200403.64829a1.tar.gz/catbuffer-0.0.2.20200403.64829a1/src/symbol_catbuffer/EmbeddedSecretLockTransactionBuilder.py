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
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .Hash256Dto import Hash256Dto
from .KeyDto import KeyDto
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .NetworkTypeDto import NetworkTypeDto
from .SecretLockTransactionBodyBuilder import SecretLockTransactionBodyBuilder
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder


class EmbeddedSecretLockTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded secret lock transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, secret: Hash256Dto, mosaic: UnresolvedMosaicBuilder, duration: BlockDurationDto, hashAlgorithm: LockHashAlgorithmDto, recipientAddress: UnresolvedAddressDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            secret: Secret.
            mosaic: Locked mosaic.
            duration: Number of blocks for which a lock should be valid.
            hashAlgorithm: Hash algorithm.
            recipientAddress: Locked mosaic recipient address.
        """
        super().__init__(signerPublicKey, version, network, type_)
        self.secretLockTransactionBody = SecretLockTransactionBodyBuilder(secret, mosaic, duration, hashAlgorithm, recipientAddress)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedSecretLockTransactionBuilder:
        """Creates an instance of EmbeddedSecretLockTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedSecretLockTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        secretLockTransactionBody = SecretLockTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[secretLockTransactionBody.getSize():]
        return EmbeddedSecretLockTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, secretLockTransactionBody.secret, secretLockTransactionBody.mosaic, secretLockTransactionBody.duration, secretLockTransactionBody.hashAlgorithm, secretLockTransactionBody.recipientAddress)

    def getSecret(self) -> Hash256Dto:
        """Gets secret.
        Returns:
            Secret.
        """
        return self.secretLockTransactionBody.getSecret()

    def getMosaic(self) -> UnresolvedMosaicBuilder:
        """Gets locked mosaic.
        Returns:
            Locked mosaic.
        """
        return self.secretLockTransactionBody.getMosaic()

    def getDuration(self) -> BlockDurationDto:
        """Gets number of blocks for which a lock should be valid.
        Returns:
            Number of blocks for which a lock should be valid.
        """
        return self.secretLockTransactionBody.getDuration()

    def getHashAlgorithm(self) -> LockHashAlgorithmDto:
        """Gets hash algorithm.
        Returns:
            Hash algorithm.
        """
        return self.secretLockTransactionBody.getHashAlgorithm()

    def getRecipientAddress(self) -> UnresolvedAddressDto:
        """Gets locked mosaic recipient address.
        Returns:
            Locked mosaic recipient address.
        """
        return self.secretLockTransactionBody.getRecipientAddress()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.secretLockTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        secretLockTransactionBodyBytes = self.secretLockTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, secretLockTransactionBodyBytes)
        return bytes_
