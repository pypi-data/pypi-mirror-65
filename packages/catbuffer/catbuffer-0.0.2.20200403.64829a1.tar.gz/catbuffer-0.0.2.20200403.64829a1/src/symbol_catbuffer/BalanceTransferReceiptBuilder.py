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
from .AddressDto import AddressDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .MosaicBuilder import MosaicBuilder
from .ReceiptBuilder import ReceiptBuilder
from .ReceiptTypeDto import ReceiptTypeDto


class BalanceTransferReceiptBuilder(ReceiptBuilder):
    """Binary layout for a balance transfer receipt."""

    # pylint: disable-msg=line-too-long
    def __init__(self, version: int, type_: ReceiptTypeDto, mosaic: MosaicBuilder, senderPublicKey: KeyDto, recipientAddress: AddressDto):
        """Constructor.
        Args:
            version: Receipt version.
            type_: Receipt type.
            mosaic: Mosaic.
            senderPublicKey: Mosaic sender public key.
            recipientAddress: Mosaic recipient address.
        """
        super().__init__(version, type_)
        self.mosaic = mosaic
        self.senderPublicKey = senderPublicKey
        self.recipientAddress = recipientAddress

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> BalanceTransferReceiptBuilder:
        """Creates an instance of BalanceTransferReceiptBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of BalanceTransferReceiptBuilder.
        """
        bytes_ = bytes(payload)
        superObject = ReceiptBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        mosaic = MosaicBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[mosaic.getSize():]
        # gen: _load_from_binary_custom
        senderPublicKey = KeyDto.loadFromBinary(bytes_)
        bytes_ = bytes_[senderPublicKey.getSize():]
        # gen: _load_from_binary_custom
        recipientAddress = AddressDto.loadFromBinary(bytes_)
        bytes_ = bytes_[recipientAddress.getSize():]
        return BalanceTransferReceiptBuilder(superObject.version, superObject.type_, mosaic, senderPublicKey, recipientAddress)

    def getMosaic(self) -> MosaicBuilder:
        """Gets mosaic.
        Returns:
            Mosaic.
        """
        return self.mosaic

    def getSenderPublicKey(self) -> KeyDto:
        """Gets mosaic sender public key.
        Returns:
            Mosaic sender public key.
        """
        return self.senderPublicKey

    def getRecipientAddress(self) -> AddressDto:
        """Gets mosaic recipient address.
        Returns:
            Mosaic recipient address.
        """
        return self.recipientAddress

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.mosaic.getSize()
        size += self.senderPublicKey.getSize()
        size += self.recipientAddress.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        mosaicBytes = self.mosaic.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicBytes)
        senderPublicKeyBytes = self.senderPublicKey.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, senderPublicKeyBytes)
        recipientAddressBytes = self.recipientAddress.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, recipientAddressBytes)
        return bytes_
