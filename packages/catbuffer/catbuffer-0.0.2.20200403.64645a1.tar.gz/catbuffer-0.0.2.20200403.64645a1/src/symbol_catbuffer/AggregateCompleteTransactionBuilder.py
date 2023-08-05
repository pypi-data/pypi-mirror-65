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
from .AggregateTransactionBodyBuilder import AggregateTransactionBodyBuilder
from .AmountDto import AmountDto
from .CosignatureBuilder import CosignatureBuilder
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils
from .Hash256Dto import Hash256Dto
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder


class AggregateCompleteTransactionBuilder(TransactionBuilder):
    """Binary layout for an aggregate complete transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type_: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, transactionsHash: Hash256Dto, transactions: List[EmbeddedTransactionBuilder], cosignatures: List[CosignatureBuilder]):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type_: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            transactionsHash: Aggregate hash of an aggregate's transactions.
            transactions: Sub-transaction data (transactions are variable sized and payload size is in bytes).
            cosignatures: Cosignatures data (fills remaining body space after transactions).
        """
        super().__init__(signature, signerPublicKey, version, network, type_, fee, deadline)
        self.aggregateTransactionBody = AggregateTransactionBodyBuilder(transactionsHash, transactions, cosignatures)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AggregateCompleteTransactionBuilder:
        """Creates an instance of AggregateCompleteTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AggregateCompleteTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        aggregateTransactionBody = AggregateTransactionBodyBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[aggregateTransactionBody.getSize():]
        return AggregateCompleteTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type_, superObject.fee, superObject.deadline, aggregateTransactionBody.transactionsHash, aggregateTransactionBody.transactions, aggregateTransactionBody.cosignatures)

    def getTransactionsHash(self) -> Hash256Dto:
        """Gets aggregate hash of an aggregate's transactions.
        Returns:
            Aggregate hash of an aggregate's transactions.
        """
        return self.aggregateTransactionBody.getTransactionsHash()

    def getAggregateTransactionHeader_Reserved1(self) -> int:
        """Gets reserved padding to align end of AggregateTransactionHeader on 8-byte boundary.
        Returns:
            Reserved padding to align end of AggregateTransactionHeader on 8-byte boundary.
        """
        return self.aggregateTransactionBody.getAggregateTransactionHeader_Reserved1()

    def getTransactions(self) -> List[EmbeddedTransactionBuilder]:
        """Gets sub-transaction data (transactions are variable sized and payload size is in bytes).
        Returns:
            Sub-transaction data (transactions are variable sized and payload size is in bytes).
        """
        return self.aggregateTransactionBody.getTransactions()

    def getCosignatures(self) -> List[CosignatureBuilder]:
        """Gets cosignatures data (fills remaining body space after transactions).
        Returns:
            Cosignatures data (fills remaining body space after transactions).
        """
        return self.aggregateTransactionBody.getCosignatures()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.aggregateTransactionBody.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        aggregateTransactionBodyBytes = self.aggregateTransactionBody.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, aggregateTransactionBodyBytes)
        return bytes_
