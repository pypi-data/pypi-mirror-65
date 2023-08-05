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
from .BlockDurationDto import BlockDurationDto
from .GeneratorUtils import GeneratorUtils
from .NamespaceIdDto import NamespaceIdDto
from .NamespaceRegistrationTypeDto import NamespaceRegistrationTypeDto


class NamespaceRegistrationTransactionBodyBuilder:
    """Binary layout for a namespace registration transaction."""

    # pylint: disable-msg=line-too-long
    def __init__(self, id_: NamespaceIdDto, name: bytes, duration: BlockDurationDto, parentId: NamespaceIdDto):
        """Constructor.
        Args:
            duration: Namespace duration.
            parentId: Parent namespace identifier.
            id_: Namespace identifier.
            name: Namespace name.
        """
        if (duration is None and parentId is None) or (duration is not None and parentId is not None):
            raise Exception('Invalid conditional parameters')
        self.duration = duration
        self.parentId = parentId
        self.id_ = id_
        self.name = name
        if duration:
            self.registrationType = NamespaceRegistrationTypeDto.ROOT
        else:
            self.registrationType = NamespaceRegistrationTypeDto.CHILD

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> NamespaceRegistrationTransactionBodyBuilder:
        """Creates an instance of NamespaceRegistrationTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of NamespaceRegistrationTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        registrationTypeConditionBytes = bytes_[0:8]
        bytes_ = bytes_[8:]
        # gen: _load_from_binary_custom
        id_ = NamespaceIdDto.loadFromBinary(bytes_)
        bytes_ = bytes_[id_.getSize():]
        # gen: _load_from_binary_custom
        registrationType = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        nameSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))
        bytes_ = bytes_[1:]
        # gen: _load_from_binary_buffer
        name = GeneratorUtils.getBytes(bytes_, nameSize)
        bytes_ = bytes_[nameSize:]
        duration = None  # BlockDurationDto
        if registrationType == NamespaceRegistrationTypeDto.ROOT:
            duration = BlockDurationDto.loadFromBinary(registrationTypeConditionBytes)
        parentId = None  # NamespaceIdDto
        if registrationType == NamespaceRegistrationTypeDto.CHILD:
            parentId = NamespaceIdDto.loadFromBinary(registrationTypeConditionBytes)
        return NamespaceRegistrationTransactionBodyBuilder(id_, name, duration, parentId)

    def getDuration(self) -> BlockDurationDto:
        """Gets namespace duration.
        Returns:
            Namespace duration.
        """
        if self.registrationType != NamespaceRegistrationTypeDto.ROOT:
            raise Exception('registrationType is not set to ROOT.')
        return self.duration

    def getParentId(self) -> NamespaceIdDto:
        """Gets parent namespace identifier.
        Returns:
            Parent namespace identifier.
        """
        if self.registrationType != NamespaceRegistrationTypeDto.CHILD:
            raise Exception('registrationType is not set to CHILD.')
        return self.parentId

    def getId_(self) -> NamespaceIdDto:
        """Gets namespace identifier.
        Returns:
            Namespace identifier.
        """
        return self.id_

    def getRegistrationType(self) -> NamespaceRegistrationTypeDto:
        """Gets namespace registration type.
        Returns:
            Namespace registration type.
        """
        return self.registrationType

    def getName(self) -> bytes:
        """Gets namespace name.
        Returns:
            Namespace name.
        """
        return self.name

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        if self.registrationType == NamespaceRegistrationTypeDto.ROOT:
            size += self.duration.getSize()
        if self.registrationType == NamespaceRegistrationTypeDto.CHILD:
            size += self.parentId.getSize()
        size += self.id_.getSize()
        size += 1  # registrationType
        size += 1  # nameSize
        size += len(self.name)
        return size

    def serialize(self) -> bytes:
        """Serializes an object to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        if self.registrationType == NamespaceRegistrationTypeDto.ROOT:
            durationBytes = self.duration.serialize()
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, durationBytes)
        if self.registrationType == NamespaceRegistrationTypeDto.CHILD:
            parentIdBytes = self.parentId.serialize()
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, parentIdBytes)
        id_Bytes = self.id_.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, id_Bytes)
        registrationTypeBytes = GeneratorUtils.uintToBuffer(self.registrationType, 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, registrationTypeBytes)
        nameSizeBytes = GeneratorUtils.uintToBuffer(len(self.name), 1)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, nameSizeBytes)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.name)
        return bytes_
