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
from .GeneratorUtils import GeneratorUtils
from .MosaicIdDto import MosaicIdDto
from .NamespaceIdDto import NamespaceIdDto


class MosaicAliasTransactionBodyBuilder:
    """Binary layout for an mosaic alias transaction."""

    def __init__(self, namespaceId: NamespaceIdDto, mosaicId: MosaicIdDto, aliasAction: AliasActionDto):
        """Constructor.
        Args:
            namespaceId: Identifier of the namespace that will become an alias.
            mosaicId: Aliased mosaic identifier.
            aliasAction: Alias action.
        """
        self.namespaceId = namespaceId
        self.mosaicId = mosaicId
        self.aliasAction = aliasAction

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicAliasTransactionBodyBuilder:
        """Creates an instance of MosaicAliasTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicAliasTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        namespaceId = NamespaceIdDto.loadFromBinary(bytes_)
        bytes_ = bytes_[namespaceId.getSize():]
        # gen: _load_from_binary_custom
        mosaicId = MosaicIdDto.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaicId.getSize():]
        # gen: _load_from_binary_custom
        aliasAction = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        return MosaicAliasTransactionBodyBuilder(namespaceId, mosaicId, aliasAction)

    def getNamespaceId(self) -> NamespaceIdDto:
        """Gets identifier of the namespace that will become an alias.
        Returns:
            Identifier of the namespace that will become an alias.
        """
        return self.namespaceId

    def getMosaicId(self) -> MosaicIdDto:
        """Gets aliased mosaic identifier.
        Returns:
            Aliased mosaic identifier.
        """
        return self.mosaicId

    def getAliasAction(self) -> AliasActionDto:
        """Gets alias action.
        Returns:
            Alias action.
        """
        return self.aliasAction

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.namespaceId.getSize()
        size += self.mosaicId.getSize()
        size += 1  # aliasAction
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        namespaceIdBytes = self.namespaceId.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, namespaceIdBytes)
        mosaicIdBytes = self.mosaicId.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicIdBytes)
        aliasActionBytes = GeneratorUtils.uintToBuffer(self.aliasAction, 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, aliasActionBytes)
        return bytes_
