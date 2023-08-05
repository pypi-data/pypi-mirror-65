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
from .AddressAliasTransactionBodyBuilder import AddressAliasTransactionBodyBuilder
from .AddressDto import AddressDto
from .AliasActionDto import AliasActionDto
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .NamespaceIdDto import NamespaceIdDto
from .NetworkTypeDto import NetworkTypeDto


class EmbeddedAddressAliasTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded address alias transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, namespaceId: NamespaceIdDto, address: AddressDto, aliasAction: AliasActionDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            namespaceId: Identifier of the namespace that will become an alias.
            address: Aliased address.
            aliasAction: Alias action.
        """
        super().__init__(signerPublicKey, version, network, type_)
        self.addressAliasTransactionBody = AddressAliasTransactionBodyBuilder(namespaceId, address, aliasAction)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedAddressAliasTransactionBuilder:
        """Creates an instance of EmbeddedAddressAliasTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedAddressAliasTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        addressAliasTransactionBody = AddressAliasTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[addressAliasTransactionBody.getSize():]
        return EmbeddedAddressAliasTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, addressAliasTransactionBody.namespaceId, addressAliasTransactionBody.address, addressAliasTransactionBody.aliasAction)

    def getNamespaceId(self) -> NamespaceIdDto:
        """Gets identifier of the namespace that will become an alias.
        Returns:
            Identifier of the namespace that will become an alias.
        """
        return self.addressAliasTransactionBody.getNamespaceId()

    def getAddress(self) -> AddressDto:
        """Gets aliased address.
        Returns:
            Aliased address.
        """
        return self.addressAliasTransactionBody.getAddress()

    def getAliasAction(self) -> AliasActionDto:
        """Gets alias action.
        Returns:
            Alias action.
        """
        return self.addressAliasTransactionBody.getAliasAction()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.addressAliasTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        addressAliasTransactionBodyBytes = self.addressAliasTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, addressAliasTransactionBodyBytes)
        return bytes_
