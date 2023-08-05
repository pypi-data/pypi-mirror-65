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
from .AccountLinkActionDto import AccountLinkActionDto
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto


class AccountLinkTransactionBodyBuilder:
    """Binary layout for an account link transaction."""

    def __init__(self, remotePublicKey: KeyDto, linkAction: AccountLinkActionDto):
        """Constructor.
        Args:
            remotePublicKey: Remote public key.
            linkAction: Account link action.
        """
        self.remotePublicKey = remotePublicKey
        self.linkAction = linkAction

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountLinkTransactionBodyBuilder:
        """Creates an instance of AccountLinkTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountLinkTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        # gen: _load_from_binary_custom
        remotePublicKey = KeyDto.loadFromBinary(bytes_)
        bytes_ = bytes_[remotePublicKey.getSize():]
        # gen: _load_from_binary_custom
        linkAction = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        return AccountLinkTransactionBodyBuilder(remotePublicKey, linkAction)

    def getRemotePublicKey(self) -> KeyDto:
        """Gets remote public key.
        Returns:
            Remote public key.
        """
        return self.remotePublicKey

    def getLinkAction(self) -> AccountLinkActionDto:
        """Gets account link action.
        Returns:
            Account link action.
        """
        return self.linkAction

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.remotePublicKey.getSize()
        size += 1  # linkAction
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        remotePublicKeyBytes = self.remotePublicKey.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, remotePublicKeyBytes)
        linkActionBytes = GeneratorUtils.uintToBuffer(self.linkAction, 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, linkActionBytes)
        return bytes_
