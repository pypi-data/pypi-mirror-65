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


class Hash512Dto:
    """Hash512."""

    def __init__(self, hash512: bytes):
        """Constructor.
        Args:
            hash512: Hash512.
        """
        self.hash512 = hash512

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> Hash512Dto:
        """Creates an instance of Hash512Dto from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of Hash512Dto.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_buffer
        hash512 = GeneratorUtils.getBytes(bytes_, 64)
        bytes_ = bytes_[64:]
        return Hash512Dto(hash512)

    def getHash512(self) -> bytes:
        """Gets Hash512.
        Returns:
            Hash512.
        """
        return self.hash512

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 64

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.hash512)
        return bytes_
