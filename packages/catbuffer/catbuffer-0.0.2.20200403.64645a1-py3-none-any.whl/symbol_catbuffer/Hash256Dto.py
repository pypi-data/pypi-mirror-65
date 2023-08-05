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


class Hash256Dto:
    """Hash256."""

    def __init__(self, hash256: bytes):
        """Constructor.
        Args:
            hash256: Hash256.
        """
        self.hash256 = hash256

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> Hash256Dto:
        """Creates an instance of Hash256Dto from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of Hash256Dto.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_buffer
        hash256 = GeneratorUtils.getBytes(bytes_, 32)
        bytes_ = bytes_[32:]
        return Hash256Dto(hash256)

    def getHash256(self) -> bytes:
        """Gets Hash256.
        Returns:
            Hash256.
        """
        return self.hash256

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 32

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.hash256)
        return bytes_
