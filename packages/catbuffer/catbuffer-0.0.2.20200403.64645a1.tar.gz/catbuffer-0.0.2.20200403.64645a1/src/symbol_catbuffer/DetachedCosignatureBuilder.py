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
from .CosignatureBuilder import CosignatureBuilder
from .GeneratorUtils import GeneratorUtils
from .Hash256Dto import Hash256Dto
from .KeyDto import KeyDto
from .SignatureDto import SignatureDto


class DetachedCosignatureBuilder(CosignatureBuilder):
    """Cosignature detached from an aggregate transaction."""

    def __init__(self, signerPublicKey: KeyDto, signature: SignatureDto, parentHash: Hash256Dto):
        """Constructor.
        Args:
            signerPublicKey: Cosigner public key.
            signature: Cosigner signature.
            parentHash: Hash of the aggregate transaction that is signed by this cosignature.
        """
        super().__init__(signerPublicKey, signature)
        self.parentHash = parentHash

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> DetachedCosignatureBuilder:
        """Creates an instance of DetachedCosignatureBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of DetachedCosignatureBuilder.
        """
        bytes_ = bytes(payload)
        superObject = CosignatureBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        # gen: _load_from_binary_custom
        parentHash = Hash256Dto.loadFromBinary(bytes_)
        bytes_ = bytes_[parentHash.getSize():]
        return DetachedCosignatureBuilder(superObject.signerPublicKey, superObject.signature, parentHash)

    def getParentHash(self) -> Hash256Dto:
        """Gets hash of the aggregate transaction that is signed by this cosignature.
        Returns:
            Hash of the aggregate transaction that is signed by this cosignature.
        """
        return self.parentHash

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size: int = super().getSize()
        size += self.parentHash.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        superBytes = super().serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, superBytes)
        parentHashBytes = self.parentHash.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, parentHashBytes)
        return bytes_
