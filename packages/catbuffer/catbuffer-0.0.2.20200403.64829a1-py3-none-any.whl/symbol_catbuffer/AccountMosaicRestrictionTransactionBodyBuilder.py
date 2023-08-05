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
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto


class AccountMosaicRestrictionTransactionBodyBuilder:
    """Binary layout for an account mosaic restriction transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, restrictionFlags: int, restrictionAdditions: List[UnresolvedMosaicIdDto], restrictionDeletions: List[UnresolvedMosaicIdDto]):
        """Constructor.
        Args:
            restrictionFlags: Account restriction flags.
            restrictionAdditions: Account restriction additions.
            restrictionDeletions: Account restriction deletions.
        """
        self.restrictionFlags = restrictionFlags
        self.accountRestrictionTransactionBody_Reserved1 = 0
        self.restrictionAdditions = restrictionAdditions
        self.restrictionDeletions = restrictionDeletions

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountMosaicRestrictionTransactionBodyBuilder:
        """Creates an instance of AccountMosaicRestrictionTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountMosaicRestrictionTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_flags
        restrictionFlags = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))
        bytes_ = bytes_[2:]
        restrictionAdditionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        restrictionDeletionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        # gen: _load_from_binary_simple
        # pylint: disable=unused-variable
        accountRestrictionTransactionBody_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        bytes_ = bytes_[4:]
        # gen: _load_from_binary_array
        restrictionAdditions: List[UnresolvedMosaicIdDto] = []
        for _ in range(restrictionAdditionsCount):
            item = UnresolvedMosaicIdDto.loadFromBinary(bytes_)
            restrictionAdditions.append(item)
            bytes_ = bytes_[item.getSize():]
        # gen: _load_from_binary_array
        restrictionDeletions: List[UnresolvedMosaicIdDto] = []
        for _ in range(restrictionDeletionsCount):
            item = UnresolvedMosaicIdDto.loadFromBinary(bytes_)
            restrictionDeletions.append(item)
            bytes_ = bytes_[item.getSize():]
        return AccountMosaicRestrictionTransactionBodyBuilder(restrictionFlags, restrictionAdditions, restrictionDeletions)

    def getRestrictionFlags(self) -> int:
        """Gets account restriction flags.
        Returns:
            Account restriction flags.
        """
        return self.restrictionFlags

    def getAccountRestrictionTransactionBody_Reserved1(self) -> int:
        """Gets reserved padding to align restrictionAdditions on 8-byte boundary.
        Returns:
            Reserved padding to align restrictionAdditions on 8-byte boundary.
        """
        return self.accountRestrictionTransactionBody_Reserved1

    def getRestrictionAdditions(self) -> List[UnresolvedMosaicIdDto]:
        """Gets account restriction additions.
        Returns:
            Account restriction additions.
        """
        return self.restrictionAdditions

    def getRestrictionDeletions(self) -> List[UnresolvedMosaicIdDto]:
        """Gets account restriction deletions.
        Returns:
            Account restriction deletions.
        """
        return self.restrictionDeletions

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 2  # restrictionFlags
        size += 1  # restrictionAdditionsCount
        size += 1  # restrictionDeletionsCount
        size += 4  # accountRestrictionTransactionBody_Reserved1
        for _ in self.restrictionAdditions:
            size += _.getSize()
        for _ in self.restrictionDeletions:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        restrictionFlagsBytes = GeneratorUtils.uintToBuffer(self.getRestrictionFlags(), 2)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, restrictionFlagsBytes)
        restrictionAdditionsCountBytes = GeneratorUtils.uintToBuffer(len(self.restrictionAdditions), 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, restrictionAdditionsCountBytes)
        restrictionDeletionsCountBytes = GeneratorUtils.uintToBuffer(len(self.restrictionDeletions), 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, restrictionDeletionsCountBytes)
        accountRestrictionTransactionBody_Reserved1Bytes = GeneratorUtils.uintToBuffer(self.getAccountRestrictionTransactionBody_Reserved1(), 4)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, accountRestrictionTransactionBody_Reserved1Bytes)
        for item in self.restrictionAdditions:
            restrictionAdditionsBytes = item.serialize()
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, restrictionAdditionsBytes)
        for item in self.restrictionDeletions:
            restrictionDeletionsBytes = item.serialize()
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, restrictionDeletionsBytes)
        return bytes_
