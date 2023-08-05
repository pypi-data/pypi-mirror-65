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

from .AccountAddressRestrictionTransactionBuilder import AccountAddressRestrictionTransactionBuilder
from .AccountLinkTransactionBuilder import AccountLinkTransactionBuilder
from .AccountMetadataTransactionBuilder import AccountMetadataTransactionBuilder
from .AccountMosaicRestrictionTransactionBuilder import AccountMosaicRestrictionTransactionBuilder
from .AccountOperationRestrictionTransactionBuilder import AccountOperationRestrictionTransactionBuilder
from .AddressAliasTransactionBuilder import AddressAliasTransactionBuilder
from .AggregateBondedTransactionBuilder import AggregateBondedTransactionBuilder
from .AggregateCompleteTransactionBuilder import AggregateCompleteTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .HashLockTransactionBuilder import HashLockTransactionBuilder
from .MosaicAddressRestrictionTransactionBuilder import MosaicAddressRestrictionTransactionBuilder
from .MosaicAliasTransactionBuilder import MosaicAliasTransactionBuilder
from .MosaicDefinitionTransactionBuilder import MosaicDefinitionTransactionBuilder
from .MosaicGlobalRestrictionTransactionBuilder import MosaicGlobalRestrictionTransactionBuilder
from .MosaicMetadataTransactionBuilder import MosaicMetadataTransactionBuilder
from .MosaicSupplyChangeTransactionBuilder import MosaicSupplyChangeTransactionBuilder
from .MultisigAccountModificationTransactionBuilder import MultisigAccountModificationTransactionBuilder
from .NamespaceMetadataTransactionBuilder import NamespaceMetadataTransactionBuilder
from .NamespaceRegistrationTransactionBuilder import NamespaceRegistrationTransactionBuilder
from .SecretLockTransactionBuilder import SecretLockTransactionBuilder
from .SecretProofTransactionBuilder import SecretProofTransactionBuilder
from .TransactionBuilder import TransactionBuilder
from .TransferTransactionBuilder import TransferTransactionBuilder


class TransactionHelper:
    """Helper class for transaction serialization"""

    @classmethod
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    def loadFromBinary(cls, payload: bytes) -> TransactionBuilder:
        """Deserialize a transaction from binary"""
        header = TransactionBuilder.loadFromBinary(payload)
        entityType = header.getType_()
        # pylint: disable=no-else-return
        if entityType == EntityTypeDto.ACCOUNT_LINK_TRANSACTION_BUILDER:
            return AccountLinkTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.AGGREGATE_COMPLETE_TRANSACTION_BUILDER:
            return AggregateCompleteTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.AGGREGATE_BONDED_TRANSACTION_BUILDER:
            return AggregateBondedTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.HASH_LOCK_TRANSACTION_BUILDER:
            return HashLockTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.SECRET_LOCK_TRANSACTION_BUILDER:
            return SecretLockTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.SECRET_PROOF_TRANSACTION_BUILDER:
            return SecretProofTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.ACCOUNT_METADATA_TRANSACTION_BUILDER:
            return AccountMetadataTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_METADATA_TRANSACTION_BUILDER:
            return MosaicMetadataTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.NAMESPACE_METADATA_TRANSACTION_BUILDER:
            return NamespaceMetadataTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_DEFINITION_TRANSACTION_BUILDER:
            return MosaicDefinitionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_SUPPLY_CHANGE_TRANSACTION_BUILDER:
            return MosaicSupplyChangeTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MULTISIG_ACCOUNT_MODIFICATION_TRANSACTION_BUILDER:
            return MultisigAccountModificationTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.ADDRESS_ALIAS_TRANSACTION_BUILDER:
            return AddressAliasTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_ALIAS_TRANSACTION_BUILDER:
            return MosaicAliasTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.NAMESPACE_REGISTRATION_TRANSACTION_BUILDER:
            return NamespaceRegistrationTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.ACCOUNT_ADDRESS_RESTRICTION_TRANSACTION_BUILDER:
            return AccountAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.ACCOUNT_MOSAIC_RESTRICTION_TRANSACTION_BUILDER:
            return AccountMosaicRestrictionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.ACCOUNT_OPERATION_RESTRICTION_TRANSACTION_BUILDER:
            return AccountOperationRestrictionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_ADDRESS_RESTRICTION_TRANSACTION_BUILDER:
            return MosaicAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.MOSAIC_GLOBAL_RESTRICTION_TRANSACTION_BUILDER:
            return MosaicGlobalRestrictionTransactionBuilder.loadFromBinary(payload)
        elif entityType == EntityTypeDto.TRANSFER_TRANSACTION_BUILDER:
            return TransferTransactionBuilder.loadFromBinary(payload)
        else:
            raise Exception('Transaction type: {0} not recognized.'.format(entityType))
