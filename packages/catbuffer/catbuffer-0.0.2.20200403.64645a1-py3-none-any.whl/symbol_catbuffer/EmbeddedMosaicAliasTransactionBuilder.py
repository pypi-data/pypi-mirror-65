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
from .AliasActionDto import AliasActionDto
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .MosaicAliasTransactionBodyBuilder import MosaicAliasTransactionBodyBuilder
from .MosaicIdDto import MosaicIdDto
from .NamespaceIdDto import NamespaceIdDto
from .NetworkTypeDto import NetworkTypeDto


class EmbeddedMosaicAliasTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded mosaic alias transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, namespaceId: NamespaceIdDto, mosaicId: MosaicIdDto, aliasAction: AliasActionDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            namespaceId: Identifier of the namespace that will become an alias.
            mosaicId: Aliased mosaic identifier.
            aliasAction: Alias action.
        """
        super().__init__(signerPublicKey, version, network, type_)
        self.mosaicAliasTransactionBody = MosaicAliasTransactionBodyBuilder(namespaceId, mosaicId, aliasAction)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedMosaicAliasTransactionBuilder:
        """Creates an instance of EmbeddedMosaicAliasTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedMosaicAliasTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        mosaicAliasTransactionBody = MosaicAliasTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaicAliasTransactionBody.getSize():]
        return EmbeddedMosaicAliasTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, mosaicAliasTransactionBody.namespaceId, mosaicAliasTransactionBody.mosaicId, mosaicAliasTransactionBody.aliasAction)

    def getNamespaceId(self) -> NamespaceIdDto:
        """Gets identifier of the namespace that will become an alias.
        Returns:
            Identifier of the namespace that will become an alias.
        """
        return self.mosaicAliasTransactionBody.getNamespaceId()

    def getMosaicId(self) -> MosaicIdDto:
        """Gets aliased mosaic identifier.
        Returns:
            Aliased mosaic identifier.
        """
        return self.mosaicAliasTransactionBody.getMosaicId()

    def getAliasAction(self) -> AliasActionDto:
        """Gets alias action.
        Returns:
            Alias action.
        """
        return self.mosaicAliasTransactionBody.getAliasAction()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.mosaicAliasTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        mosaicAliasTransactionBodyBytes = self.mosaicAliasTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicAliasTransactionBodyBytes)
        return bytes_
