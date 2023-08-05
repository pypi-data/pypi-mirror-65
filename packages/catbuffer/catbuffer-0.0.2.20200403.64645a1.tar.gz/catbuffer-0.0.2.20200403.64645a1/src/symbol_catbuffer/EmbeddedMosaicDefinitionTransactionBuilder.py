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
from .KeyDto import KeyDto
from .MosaicDefinitionTransactionBodyBuilder import MosaicDefinitionTransactionBodyBuilder
from .MosaicIdDto import MosaicIdDto
from .MosaicNonceDto import MosaicNonceDto
from .NetworkTypeDto import NetworkTypeDto


class EmbeddedMosaicDefinitionTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded mosaic definition transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, id_: MosaicIdDto, duration: BlockDurationDto, nonce: MosaicNonceDto, flags: int, divisibility: int):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            id_: Mosaic identifier.
            duration: Mosaic duration.
            nonce: Mosaic nonce.
            flags: Mosaic flags.
            divisibility: Mosaic divisibility.
        """
        super().__init__(signerPublicKey, version, network, type_)
        self.mosaicDefinitionTransactionBody = MosaicDefinitionTransactionBodyBuilder(id_, duration, nonce, flags, divisibility)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedMosaicDefinitionTransactionBuilder:
        """Creates an instance of EmbeddedMosaicDefinitionTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedMosaicDefinitionTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        mosaicDefinitionTransactionBody = MosaicDefinitionTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaicDefinitionTransactionBody.getSize():]
        return EmbeddedMosaicDefinitionTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, mosaicDefinitionTransactionBody.id_, mosaicDefinitionTransactionBody.duration, mosaicDefinitionTransactionBody.nonce, mosaicDefinitionTransactionBody.flags, mosaicDefinitionTransactionBody.divisibility)

    def getId_(self) -> MosaicIdDto:
        """Gets mosaic identifier.
        Returns:
            Mosaic identifier.
        """
        return self.mosaicDefinitionTransactionBody.getId_()

    def getDuration(self) -> BlockDurationDto:
        """Gets mosaic duration.
        Returns:
            Mosaic duration.
        """
        return self.mosaicDefinitionTransactionBody.getDuration()

    def getNonce(self) -> MosaicNonceDto:
        """Gets mosaic nonce.
        Returns:
            Mosaic nonce.
        """
        return self.mosaicDefinitionTransactionBody.getNonce()

    def getFlags(self) -> int:
        """Gets mosaic flags.
        Returns:
            Mosaic flags.
        """
        return self.mosaicDefinitionTransactionBody.getFlags()

    def getDivisibility(self) -> int:
        """Gets mosaic divisibility.
        Returns:
            Mosaic divisibility.
        """
        return self.mosaicDefinitionTransactionBody.getDivisibility()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.mosaicDefinitionTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        mosaicDefinitionTransactionBodyBytes = self.mosaicDefinitionTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicDefinitionTransactionBodyBytes)
        return bytes_
