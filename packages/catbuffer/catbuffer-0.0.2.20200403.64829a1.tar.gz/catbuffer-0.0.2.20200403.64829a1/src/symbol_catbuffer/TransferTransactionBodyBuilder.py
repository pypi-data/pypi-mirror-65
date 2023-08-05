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
from typing import List
from .GeneratorUtils import GeneratorUtils
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder


class TransferTransactionBodyBuilder:
    """Binary layout for a transfer transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, recipientAddress: UnresolvedAddressDto, mosaics: List[UnresolvedMosaicBuilder], message: bytes):
        """Constructor.
        Args:
            recipientAddress: Recipient address.
            mosaics: Attached mosaics.
            message: Attached message.
        """
        self.recipientAddress = recipientAddress
        self.transferTransactionBody_Reserved1 = 0
        self.mosaics = mosaics
        self.message = message

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> TransferTransactionBodyBuilder:
        """Creates an instance of TransferTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of TransferTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        recipientAddress = UnresolvedAddressDto.loadFromBinary(bytes_)
        bytes_ = bytes_[recipientAddress.getSize():]
        mosaicsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        messageSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))
        bytes_ = bytes_[2:]
        # gen: _load_from_binary_simple
        # pylint: disable=unused-variable
        transferTransactionBody_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        bytes_ = bytes_[4:]
        # gen: _load_from_binary_array
        mosaics: List[UnresolvedMosaicBuilder] = []
        for _ in range(mosaicsCount):
            item = UnresolvedMosaicBuilder.loadFromBinary(bytes_)
            mosaics.append(item)
            bytes_ = bytes_[item.getSize():]
        # gen: _load_from_binary_buffer
        message = GeneratorUtils.getBytes(bytes_, messageSize)
        bytes_ = bytes_[messageSize:]
        return TransferTransactionBodyBuilder(recipientAddress, mosaics, message)

    def getRecipientAddress(self) -> UnresolvedAddressDto:
        """Gets recipient address.
        Returns:
            Recipient address.
        """
        return self.recipientAddress

    def getTransferTransactionBody_Reserved1(self) -> int:
        """Gets reserved padding to align mosaics on 8-byte boundary.
        Returns:
            Reserved padding to align mosaics on 8-byte boundary.
        """
        return self.transferTransactionBody_Reserved1

    def getMosaics(self) -> List[UnresolvedMosaicBuilder]:
        """Gets attached mosaics.
        Returns:
            Attached mosaics.
        """
        return self.mosaics

    def getMessage(self) -> bytes:
        """Gets attached message.
        Returns:
            Attached message.
        """
        return self.message

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.recipientAddress.getSize()
        size += 1  # mosaicsCount
        size += 2  # messageSize
        size += 4  # transferTransactionBody_Reserved1
        for _ in self.mosaics:
            size += _.getSize()
        size += len(self.message)
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        recipientAddressBytes = self.recipientAddress.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, recipientAddressBytes)
        mosaicsCountBytes = GeneratorUtils.uintToBuffer(len(self.mosaics), 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicsCountBytes)
        messageSizeBytes = GeneratorUtils.uintToBuffer(len(self.message), 2)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, messageSizeBytes)
        transferTransactionBody_Reserved1Bytes = GeneratorUtils.uintToBuffer(self.getTransferTransactionBody_Reserved1(), 4)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, transferTransactionBody_Reserved1Bytes)
        for item in self.mosaics:
            mosaicsBytes = item.serialize()
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, mosaicsBytes)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.message)
        return bytes_
