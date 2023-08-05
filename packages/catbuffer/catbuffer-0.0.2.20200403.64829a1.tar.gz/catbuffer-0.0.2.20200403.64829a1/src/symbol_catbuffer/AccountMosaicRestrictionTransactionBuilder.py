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
from .AccountMosaicRestrictionTransactionBodyBuilder import AccountMosaicRestrictionTransactionBodyBuilder
from .AmountDto import AmountDto
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto


class AccountMosaicRestrictionTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded account mosaic restriction transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, restrictionFlags: int, restrictionAdditions: List[UnresolvedMosaicIdDto], restrictionDeletions: List[UnresolvedMosaicIdDto]):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            restrictionFlags: Account restriction flags.
            restrictionAdditions: Account restriction additions.
            restrictionDeletions: Account restriction deletions.
        """
        super().__init__(signature, signerPublicKey, version, network, type_, fee, deadline)
        self.accountMosaicRestrictionTransactionBody = AccountMosaicRestrictionTransactionBodyBuilder(restrictionFlags, restrictionAdditions, restrictionDeletions)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountMosaicRestrictionTransactionBuilder:
        """Creates an instance of AccountMosaicRestrictionTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountMosaicRestrictionTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        accountMosaicRestrictionTransactionBody = AccountMosaicRestrictionTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[accountMosaicRestrictionTransactionBody.getSize():]
        return AccountMosaicRestrictionTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, superObject.fee, superObject.deadline, accountMosaicRestrictionTransactionBody.restrictionFlags, accountMosaicRestrictionTransactionBody.restrictionAdditions, accountMosaicRestrictionTransactionBody.restrictionDeletions)

    def getRestrictionFlags(self) -> int:
        """Gets account restriction flags.
        Returns:
            Account restriction flags.
        """
        return self.accountMosaicRestrictionTransactionBody.getRestrictionFlags()

    def getAccountRestrictionTransactionBody_Reserved1(self) -> int:
        """Gets reserved padding to align restrictionAdditions on 8-byte boundary.
        Returns:
            Reserved padding to align restrictionAdditions on 8-byte boundary.
        """
        return self.accountMosaicRestrictionTransactionBody.getAccountRestrictionTransactionBody_Reserved1()

    def getRestrictionAdditions(self) -> List[UnresolvedMosaicIdDto]:
        """Gets account restriction additions.
        Returns:
            Account restriction additions.
        """
        return self.accountMosaicRestrictionTransactionBody.getRestrictionAdditions()

    def getRestrictionDeletions(self) -> List[UnresolvedMosaicIdDto]:
        """Gets account restriction deletions.
        Returns:
            Account restriction deletions.
        """
        return self.accountMosaicRestrictionTransactionBody.getRestrictionDeletions()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.accountMosaicRestrictionTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        accountMosaicRestrictionTransactionBodyBytes = self.accountMosaicRestrictionTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, accountMosaicRestrictionTransactionBodyBytes)
        return bytes_
