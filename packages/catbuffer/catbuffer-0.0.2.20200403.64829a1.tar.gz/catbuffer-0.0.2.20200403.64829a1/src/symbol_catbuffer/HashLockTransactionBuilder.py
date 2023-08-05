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
from .Hash256Dto import Hash256Dto
from .HashLockTransactionBodyBuilder import HashLockTransactionBodyBuilder
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder


class HashLockTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded hash lock transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, mosaic: UnresolvedMosaicBuilder, duration: BlockDurationDto, hash_: Hash256Dto):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            mosaic: Lock mosaic.
            duration: Number of blocks for which a lock should be valid.
            hash_: Lock hash.
        """
        super().__init__(signature, signerPublicKey, version, network, type_, fee, deadline)
        self.hashLockTransactionBody = HashLockTransactionBodyBuilder(mosaic, duration, hash_)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> HashLockTransactionBuilder:
        """Creates an instance of HashLockTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of HashLockTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        hashLockTransactionBody = HashLockTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[hashLockTransactionBody.getSize():]
        return HashLockTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, superObject.fee, superObject.deadline, hashLockTransactionBody.mosaic, hashLockTransactionBody.duration, hashLockTransactionBody.hash_)

    def getMosaic(self) -> UnresolvedMosaicBuilder:
        """Gets lock mosaic.
        Returns:
            Lock mosaic.
        """
        return self.hashLockTransactionBody.getMosaic()

    def getDuration(self) -> BlockDurationDto:
        """Gets number of blocks for which a lock should be valid.
        Returns:
            Number of blocks for which a lock should be valid.
        """
        return self.hashLockTransactionBody.getDuration()

    def getHash_(self) -> Hash256Dto:
        """Gets lock hash.
        Returns:
            Lock hash.
        """
        return self.hashLockTransactionBody.getHash_()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.hashLockTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        hashLockTransactionBodyBytes = self.hashLockTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, hashLockTransactionBodyBytes)
        return bytes_
