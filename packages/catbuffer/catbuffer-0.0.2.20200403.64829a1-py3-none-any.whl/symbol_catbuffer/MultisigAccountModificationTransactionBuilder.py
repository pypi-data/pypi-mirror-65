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
from .AmountDto import AmountDto
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .MultisigAccountModificationTransactionBodyBuilder import MultisigAccountModificationTransactionBodyBuilder
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder


class MultisigAccountModificationTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded multisig account modification transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, minRemovalDelta: int, minApprovalDelta: int, publicKeyAdditions: List[KeyDto], publicKeyDeletions: List[KeyDto]):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            minRemovalDelta: Relative change of the minimal number of cosignatories required when removing an account.
            minApprovalDelta: Relative change of the minimal number of cosignatories required when approving a transaction.
            publicKeyAdditions: Cosignatory public key additions.
            publicKeyDeletions: Cosignatory public key deletions.
        """
        super().__init__(signature, signerPublicKey, version, network, type_, fee, deadline)
        self.multisigAccountModificationTransactionBody = MultisigAccountModificationTransactionBodyBuilder(minRemovalDelta, minApprovalDelta, publicKeyAdditions, publicKeyDeletions)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MultisigAccountModificationTransactionBuilder:
        """Creates an instance of MultisigAccountModificationTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MultisigAccountModificationTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        multisigAccountModificationTransactionBody = MultisigAccountModificationTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[multisigAccountModificationTransactionBody.getSize():]
        return MultisigAccountModificationTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, superObject.fee, superObject.deadline, multisigAccountModificationTransactionBody.minRemovalDelta, multisigAccountModificationTransactionBody.minApprovalDelta, multisigAccountModificationTransactionBody.publicKeyAdditions, multisigAccountModificationTransactionBody.publicKeyDeletions)

    def getMinRemovalDelta(self) -> int:
        """Gets relative change of the minimal number of cosignatories required when removing an account.
        Returns:
            Relative change of the minimal number of cosignatories required when removing an account.
        """
        return self.multisigAccountModificationTransactionBody.getMinRemovalDelta()

    def getMinApprovalDelta(self) -> int:
        """Gets relative change of the minimal number of cosignatories required when approving a transaction.
        Returns:
            Relative change of the minimal number of cosignatories required when approving a transaction.
        """
        return self.multisigAccountModificationTransactionBody.getMinApprovalDelta()

    def getMultisigAccountModificationTransactionBody_Reserved1(self) -> int:
        """Gets reserved padding to align publicKeyAdditions on 8-byte boundary.
        Returns:
            Reserved padding to align publicKeyAdditions on 8-byte boundary.
        """
        return self.multisigAccountModificationTransactionBody.getMultisigAccountModificationTransactionBody_Reserved1()

    def getPublicKeyAdditions(self) -> List[KeyDto]:
        """Gets cosignatory public key additions.
        Returns:
            Cosignatory public key additions.
        """
        return self.multisigAccountModificationTransactionBody.getPublicKeyAdditions()

    def getPublicKeyDeletions(self) -> List[KeyDto]:
        """Gets cosignatory public key deletions.
        Returns:
            Cosignatory public key deletions.
        """
        return self.multisigAccountModificationTransactionBody.getPublicKeyDeletions()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.multisigAccountModificationTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        multisigAccountModificationTransactionBodyBytes = self.multisigAccountModificationTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, multisigAccountModificationTransactionBodyBytes)
        return bytes_
