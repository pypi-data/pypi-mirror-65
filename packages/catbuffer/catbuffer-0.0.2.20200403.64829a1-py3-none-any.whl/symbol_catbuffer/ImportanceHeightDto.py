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


class ImportanceHeightDto:
    """Importance height."""

    def __init__(self, importanceHeight: int):
        """Constructor.
        Args:
            importanceHeight: Importance height.
        """
        self.importanceHeight = importanceHeight

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> ImportanceHeightDto:
        """Creates an instance of ImportanceHeightDto from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of ImportanceHeightDto.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_simple
        importanceHeight = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))
        bytes_ = bytes_[8:]
        return ImportanceHeightDto(importanceHeight)

    def getImportanceHeight(self) -> int:
        """Gets Importance height.
        Returns:
            Importance height.
        """
        return self.importanceHeight

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 8

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        importanceHeightBytes = GeneratorUtils.uintToBuffer(self.getImportanceHeight(), 8)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, importanceHeightBytes)
        return bytes_
