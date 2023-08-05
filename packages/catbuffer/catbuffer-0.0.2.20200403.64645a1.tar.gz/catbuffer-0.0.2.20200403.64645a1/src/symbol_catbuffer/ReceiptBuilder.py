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
from .GeneratorUtils import GeneratorUtils
from .ReceiptTypeDto import ReceiptTypeDto


class ReceiptBuilder:
    """Binary layout for a receipt entity."""

    def __init__(self, version: int, type_: ReceiptTypeDto):
        """Constructor.
        Args:
            version: Receipt version.
            type_: Receipt type.
        """
        self.version = version
        self.type_ = type_

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> ReceiptBuilder:
        """Creates an instance of ReceiptBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of ReceiptBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_simple
        # pylint: disable=unused-variable
        size = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        bytes_ = bytes_[4:]
        # gen: _load_from_binary_simple
        version = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))
        bytes_ = bytes_[2:]
        # gen: _load_from_binary_custom
        type_ = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))
        bytes_ = bytes_[2:]
        return ReceiptBuilder(version, type_)

    def getVersion(self) -> int:
        """Gets receipt version.
        Returns:
            Receipt version.
        """
        return self.version

    def getType_(self) -> ReceiptTypeDto:
        """Gets receipt type.
        Returns:
            Receipt type.
        """
        return self.type_

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 4  # size
        size += 2  # version
        size += 2  # type_
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        versionBytes = GeneratorUtils.uintToBuffer(self.getVersion(), 2)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, versionBytes)
        type_Bytes = GeneratorUtils.uintToBuffer(self.type_, 2)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, type_Bytes)
        return bytes_
