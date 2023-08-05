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

from functools import reduce
from typing import List
from .EmbeddedAccountAddressRestrictionTransactionBuilder import EmbeddedAccountAddressRestrictionTransactionBuilder
from .EmbeddedAccountLinkTransactionBuilder import EmbeddedAccountLinkTransactionBuilder
from .EmbeddedAccountMetadataTransactionBuilder import EmbeddedAccountMetadataTransactionBuilder
from .EmbeddedAccountMosaicRestrictionTransactionBuilder import EmbeddedAccountMosaicRestrictionTransactionBuilder
from .EmbeddedAccountOperationRestrictionTransactionBuilder import EmbeddedAccountOperationRestrictionTransactionBuilder
from .EmbeddedAddressAliasTransactionBuilder import EmbeddedAddressAliasTransactionBuilder
from .EmbeddedHashLockTransactionBuilder import EmbeddedHashLockTransactionBuilder
from .EmbeddedMosaicAddressRestrictionTransactionBuilder import EmbeddedMosaicAddressRestrictionTransactionBuilder
from .EmbeddedMosaicAliasTransactionBuilder import EmbeddedMosaicAliasTransactionBuilder
from .EmbeddedMosaicDefinitionTransactionBuilder import EmbeddedMosaicDefinitionTransactionBuilder
from .EmbeddedMosaicGlobalRestrictionTransactionBuilder import EmbeddedMosaicGlobalRestrictionTransactionBuilder
from .EmbeddedMosaicMetadataTransactionBuilder import EmbeddedMosaicMetadataTransactionBuilder
from .EmbeddedMosaicSupplyChangeTransactionBuilder import EmbeddedMosaicSupplyChangeTransactionBuilder
from .EmbeddedMultisigAccountModificationTransactionBuilder import EmbeddedMultisigAccountModificationTransactionBuilder
from .EmbeddedNamespaceMetadataTransactionBuilder import EmbeddedNamespaceMetadataTransactionBuilder
from .EmbeddedNamespaceRegistrationTransactionBuilder import EmbeddedNamespaceRegistrationTransactionBuilder
from .EmbeddedSecretLockTransactionBuilder import EmbeddedSecretLockTransactionBuilder
from .EmbeddedSecretProofTransactionBuilder import EmbeddedSecretProofTransactionBuilder
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EmbeddedTransferTransactionBuilder import EmbeddedTransferTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .GeneratorUtils import GeneratorUtils


class EmbeddedTransactionHelper:
    """Helper class for embedded transaction serialization"""

    @classmethod
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    def loadFromBinary(cls, payload: bytes) -> EmbeddedTransactionBuilder:
        """Deserialize an embedded transaction from binary"""
        header = EmbeddedTransactionBuilder.loadFromBinary(payload)
        entityType = header.getType_()
        # pylint: disable=no-else-return
        if entityType == EntityTypeDto.ACCOUNT_LINK_TRANSACTION_BUILDER:
            return EmbeddedAccountLinkTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.HASH_LOCK_TRANSACTION_BUILDER:
            return EmbeddedHashLockTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.SECRET_LOCK_TRANSACTION_BUILDER:
            return EmbeddedSecretLockTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.SECRET_PROOF_TRANSACTION_BUILDER:
            return EmbeddedSecretProofTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.ACCOUNT_METADATA_TRANSACTION_BUILDER:
            return EmbeddedAccountMetadataTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_METADATA_TRANSACTION_BUILDER:
            return EmbeddedMosaicMetadataTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.NAMESPACE_METADATA_TRANSACTION_BUILDER:
            return EmbeddedNamespaceMetadataTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_DEFINITION_TRANSACTION_BUILDER:
            return EmbeddedMosaicDefinitionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_SUPPLY_CHANGE_TRANSACTION_BUILDER:
            return EmbeddedMosaicSupplyChangeTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MULTISIG_ACCOUNT_MODIFICATION_TRANSACTION_BUILDER:
            return EmbeddedMultisigAccountModificationTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.ADDRESS_ALIAS_TRANSACTION_BUILDER:
            return EmbeddedAddressAliasTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_ALIAS_TRANSACTION_BUILDER:
            return EmbeddedMosaicAliasTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.NAMESPACE_REGISTRATION_TRANSACTION_BUILDER:
            return EmbeddedNamespaceRegistrationTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.ACCOUNT_ADDRESS_RESTRICTION_TRANSACTION_BUILDER:
            return EmbeddedAccountAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.ACCOUNT_MOSAIC_RESTRICTION_TRANSACTION_BUILDER:
            return EmbeddedAccountMosaicRestrictionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.ACCOUNT_OPERATION_RESTRICTION_TRANSACTION_BUILDER:
            return EmbeddedAccountOperationRestrictionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_ADDRESS_RESTRICTION_TRANSACTION_BUILDER:
            return EmbeddedMosaicAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_GLOBAL_RESTRICTION_TRANSACTION_BUILDER:
            return EmbeddedMosaicGlobalRestrictionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.TRANSFER_TRANSACTION_BUILDER:
            return EmbeddedTransferTransactionBuilder.loadFromBinary(payload)
        else:
            raise Exception('Transaction type: {0} not recognized.'.format(entityType))

    @classmethod
    def serialize(cls, transaction: EmbeddedTransactionBuilder) -> bytes:
        """Serialize an embedded transaction"""
        bytes_ = transaction.serialize()
        padding = bytes(GeneratorUtils.getTransactionPaddingSize(len(bytes_), 8))
        return GeneratorUtils.concatTypedArrays(bytes_, padding)

    @classmethod
    def getEmbeddedTransactionSize(cls, transactions: List[EmbeddedTransactionBuilder]) -> int:
        """Get actual embedded transaction size"""
        return reduce(lambda a, b: a + b, map(lambda x: len(EmbeddedTransactionHelper.serialize(x)), transactions), 0)
