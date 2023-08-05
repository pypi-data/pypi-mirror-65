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
from .KeyDto import KeyDto
from .MosaicAddressRestrictionTransactionBodyBuilder import MosaicAddressRestrictionTransactionBodyBuilder
from .NetworkTypeDto import NetworkTypeDto
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto


class EmbeddedMosaicAddressRestrictionTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded mosaic address restriction transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, mosaicId: UnresolvedMosaicIdDto, restrictionKey: int, previousRestrictionValue: int, newRestrictionValue: int, targetAddress: UnresolvedAddressDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            mosaicId: Identifier of the mosaic to which the restriction applies.
            restrictionKey: Restriction key.
            previousRestrictionValue: Previous restriction value.
            newRestrictionValue: New restriction value.
            targetAddress: Address being restricted.
        """
        super().__init__(signerPublicKey, version, network, type_)
        self.mosaicAddressRestrictionTransactionBody = MosaicAddressRestrictionTransactionBodyBuilder(mosaicId, restrictionKey, previousRestrictionValue, newRestrictionValue, targetAddress)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedMosaicAddressRestrictionTransactionBuilder:
        """Creates an instance of EmbeddedMosaicAddressRestrictionTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedMosaicAddressRestrictionTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        mosaicAddressRestrictionTransactionBody = MosaicAddressRestrictionTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaicAddressRestrictionTransactionBody.getSize():]
        return EmbeddedMosaicAddressRestrictionTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, mosaicAddressRestrictionTransactionBody.mosaicId, mosaicAddressRestrictionTransactionBody.restrictionKey, mosaicAddressRestrictionTransactionBody.previousRestrictionValue, mosaicAddressRestrictionTransactionBody.newRestrictionValue, mosaicAddressRestrictionTransactionBody.targetAddress)

    def getMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets identifier of the mosaic to which the restriction applies.
        Returns:
            Identifier of the mosaic to which the restriction applies.
        """
        return self.mosaicAddressRestrictionTransactionBody.getMosaicId()

    def getRestrictionKey(self) -> int:
        """Gets restriction key.
        Returns:
            Restriction key.
        """
        return self.mosaicAddressRestrictionTransactionBody.getRestrictionKey()

    def getPreviousRestrictionValue(self) -> int:
        """Gets previous restriction value.
        Returns:
            Previous restriction value.
        """
        return self.mosaicAddressRestrictionTransactionBody.getPreviousRestrictionValue()

    def getNewRestrictionValue(self) -> int:
        """Gets new restriction value.
        Returns:
            New restriction value.
        """
        return self.mosaicAddressRestrictionTransactionBody.getNewRestrictionValue()

    def getTargetAddress(self) -> UnresolvedAddressDto:
        """Gets address being restricted.
        Returns:
            Address being restricted.
        """
        return self.mosaicAddressRestrictionTransactionBody.getTargetAddress()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.mosaicAddressRestrictionTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        mosaicAddressRestrictionTransactionBodyBytes = self.mosaicAddressRestrictionTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicAddressRestrictionTransactionBodyBytes)
        return bytes_
