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
from .CosignatureBuilder import CosignatureBuilder
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EmbeddedTransactionHelper import EmbeddedTransactionHelper
from .GeneratorUtils import GeneratorUtils
from .Hash256Dto import Hash256Dto


class AggregateTransactionBodyBuilder:
    """Binary layout for an aggregate transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, transactionsHash: Hash256Dto, transactions: List[EmbeddedTransactionBuilder], cosignatures: List[CosignatureBuilder]):
        """Constructor.
        Args:
            transactionsHash: Aggregate hash of an aggregate's transactions.
            transactions: Sub-transaction data (transactions are variable sized and payload size is in bytes).
            cosignatures: Cosignatures data (fills remaining body space after transactions).
        """
        self.transactionsHash = transactionsHash
        self.aggregateTransactionHeader_Reserved1 = 0
        self.transactions = transactions
        self.cosignatures = cosignatures

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AggregateTransactionBodyBuilder:
        """Creates an instance of AggregateTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AggregateTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        transactionsHash = Hash256Dto.loadFromBinary(bytes_)
        bytes_ = bytes_[transactionsHash.getSize():]
        payloadSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        bytes_ = bytes_[4:]
        # gen: _load_from_binary_simple
        # pylint: disable=unused-variable
        aggregateTransactionHeader_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        bytes_ = bytes_[4:]
        # gen: _load_from_binary_var_fill_array
        transactionsByteSize = payloadSize
        transactions: List[EmbeddedTransactionBuilder] = []
        while transactionsByteSize > 0:
            item = EmbeddedTransactionHelper.loadFromBinary(bytes_)
            transactions.append(item)
            itemSize = item.getSize() + GeneratorUtils.getTransactionPaddingSize(item.getSize(), 8)
            transactionsByteSize -= itemSize
            bytes_ = bytes_[itemSize:]
        # gen: _load_from_binary_var_fill_array
        cosignaturesByteSize = len(bytes_)
        cosignatures: List[CosignatureBuilder] = []
        while cosignaturesByteSize > 0:
            item = CosignatureBuilder.loadFromBinary(bytes_)
            cosignatures.append(item)
            itemSize = item.getSize()
            cosignaturesByteSize -= itemSize
            bytes_ = bytes_[itemSize:]
        return AggregateTransactionBodyBuilder(transactionsHash, transactions, cosignatures)

    def getTransactionsHash(self) -> Hash256Dto:
        """Gets aggregate hash of an aggregate's transactions.
        Returns:
            Aggregate hash of an aggregate's transactions.
        """
        return self.transactionsHash

    def getAggregateTransactionHeader_Reserved1(self) -> int:
        """Gets reserved padding to align end of AggregateTransactionHeader on 8-byte boundary.
        Returns:
            Reserved padding to align end of AggregateTransactionHeader on 8-byte boundary.
        """
        return self.aggregateTransactionHeader_Reserved1

    def getTransactions(self) -> List[EmbeddedTransactionBuilder]:
        """Gets sub-transaction data (transactions are variable sized and payload size is in bytes).
        Returns:
            Sub-transaction data (transactions are variable sized and payload size is in bytes).
        """
        return self.transactions

    def getCosignatures(self) -> List[CosignatureBuilder]:
        """Gets cosignatures data (fills remaining body space after transactions).
        Returns:
            Cosignatures data (fills remaining body space after transactions).
        """
        return self.cosignatures

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.transactionsHash.getSize()
        size += 4  # payloadSize
        size += 4  # aggregateTransactionHeader_Reserved1
        for _ in self.transactions:
            size += len(EmbeddedTransactionHelper.serialize(_))
        for _ in self.cosignatures:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        transactionsHashBytes = self.transactionsHash.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, transactionsHashBytes)
        payloadSizeBytes = GeneratorUtils.uintToBuffer(EmbeddedTransactionHelper.getEmbeddedTransactionSize(self.transactions), 4)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, payloadSizeBytes)
        aggregateTransactionHeader_Reserved1Bytes = GeneratorUtils.uintToBuffer(self.getAggregateTransactionHeader_Reserved1(), 4)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, aggregateTransactionHeader_Reserved1Bytes)
        for item in self.transactions:
            transactionsBytes = EmbeddedTransactionHelper.serialize(item)
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, transactionsBytes)
        for item in self.cosignatures:
            cosignaturesBytes = item.serialize()
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, cosignaturesBytes)
        return bytes_
