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
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .Hash256Dto import Hash256Dto
from .KeyDto import KeyDto
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .NetworkTypeDto import NetworkTypeDto
from .SecretProofTransactionBodyBuilder import SecretProofTransactionBodyBuilder
from .UnresolvedAddressDto import UnresolvedAddressDto


class EmbeddedSecretProofTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded secret proof transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, secret: Hash256Dto, hashAlgorithm: LockHashAlgorithmDto, recipientAddress: UnresolvedAddressDto, proof: bytes):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            secret: Secret.
            hashAlgorithm: Hash algorithm.
            recipientAddress: Locked mosaic recipient address.
            proof: Proof data.
        """
        super().__init__(signerPublicKey, version, network, type_)
        self.secretProofTransactionBody = SecretProofTransactionBodyBuilder(secret, hashAlgorithm, recipientAddress, proof)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedSecretProofTransactionBuilder:
        """Creates an instance of EmbeddedSecretProofTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedSecretProofTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        secretProofTransactionBody = SecretProofTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[secretProofTransactionBody.getSize():]
        return EmbeddedSecretProofTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, secretProofTransactionBody.secret, secretProofTransactionBody.hashAlgorithm, secretProofTransactionBody.recipientAddress, secretProofTransactionBody.proof)

    def getSecret(self) -> Hash256Dto:
        """Gets secret.
        Returns:
            Secret.
        """
        return self.secretProofTransactionBody.getSecret()

    def getHashAlgorithm(self) -> LockHashAlgorithmDto:
        """Gets hash algorithm.
        Returns:
            Hash algorithm.
        """
        return self.secretProofTransactionBody.getHashAlgorithm()

    def getRecipientAddress(self) -> UnresolvedAddressDto:
        """Gets locked mosaic recipient address.
        Returns:
            Locked mosaic recipient address.
        """
        return self.secretProofTransactionBody.getRecipientAddress()

    def getProof(self) -> bytes:
        """Gets proof data.
        Returns:
            Proof data.
        """
        return self.secretProofTransactionBody.getProof()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.secretProofTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        secretProofTransactionBodyBytes = self.secretProofTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, secretProofTransactionBodyBytes)
        return bytes_
