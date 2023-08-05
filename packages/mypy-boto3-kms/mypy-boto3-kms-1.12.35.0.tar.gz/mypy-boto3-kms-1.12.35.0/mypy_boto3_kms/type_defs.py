"""
Main interface for kms service type definitions.

Usage::

    from mypy_boto3.kms.type_defs import CancelKeyDeletionResponseTypeDef

    data: CancelKeyDeletionResponseTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CancelKeyDeletionResponseTypeDef",
    "CreateCustomKeyStoreResponseTypeDef",
    "CreateGrantResponseTypeDef",
    "KeyMetadataTypeDef",
    "CreateKeyResponseTypeDef",
    "DecryptResponseTypeDef",
    "CustomKeyStoresListEntryTypeDef",
    "DescribeCustomKeyStoresResponseTypeDef",
    "DescribeKeyResponseTypeDef",
    "EncryptResponseTypeDef",
    "GenerateDataKeyPairResponseTypeDef",
    "GenerateDataKeyPairWithoutPlaintextResponseTypeDef",
    "GenerateDataKeyResponseTypeDef",
    "GenerateDataKeyWithoutPlaintextResponseTypeDef",
    "GenerateRandomResponseTypeDef",
    "GetKeyPolicyResponseTypeDef",
    "GetKeyRotationStatusResponseTypeDef",
    "GetParametersForImportResponseTypeDef",
    "GetPublicKeyResponseTypeDef",
    "GrantConstraintsTypeDef",
    "AliasListEntryTypeDef",
    "ListAliasesResponseTypeDef",
    "GrantListEntryTypeDef",
    "ListGrantsResponseTypeDef",
    "ListKeyPoliciesResponseTypeDef",
    "KeyListEntryTypeDef",
    "ListKeysResponseTypeDef",
    "TagTypeDef",
    "ListResourceTagsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ReEncryptResponseTypeDef",
    "ScheduleKeyDeletionResponseTypeDef",
    "SignResponseTypeDef",
    "VerifyResponseTypeDef",
)

CancelKeyDeletionResponseTypeDef = TypedDict(
    "CancelKeyDeletionResponseTypeDef", {"KeyId": str}, total=False
)

CreateCustomKeyStoreResponseTypeDef = TypedDict(
    "CreateCustomKeyStoreResponseTypeDef", {"CustomKeyStoreId": str}, total=False
)

CreateGrantResponseTypeDef = TypedDict(
    "CreateGrantResponseTypeDef", {"GrantToken": str, "GrantId": str}, total=False
)

_RequiredKeyMetadataTypeDef = TypedDict("_RequiredKeyMetadataTypeDef", {"KeyId": str})
_OptionalKeyMetadataTypeDef = TypedDict(
    "_OptionalKeyMetadataTypeDef",
    {
        "AWSAccountId": str,
        "Arn": str,
        "CreationDate": datetime,
        "Enabled": bool,
        "Description": str,
        "KeyUsage": Literal["SIGN_VERIFY", "ENCRYPT_DECRYPT"],
        "KeyState": Literal[
            "Enabled", "Disabled", "PendingDeletion", "PendingImport", "Unavailable"
        ],
        "DeletionDate": datetime,
        "ValidTo": datetime,
        "Origin": Literal["AWS_KMS", "EXTERNAL", "AWS_CLOUDHSM"],
        "CustomKeyStoreId": str,
        "CloudHsmClusterId": str,
        "ExpirationModel": Literal["KEY_MATERIAL_EXPIRES", "KEY_MATERIAL_DOES_NOT_EXPIRE"],
        "KeyManager": Literal["AWS", "CUSTOMER"],
        "CustomerMasterKeySpec": Literal[
            "RSA_2048",
            "RSA_3072",
            "RSA_4096",
            "ECC_NIST_P256",
            "ECC_NIST_P384",
            "ECC_NIST_P521",
            "ECC_SECG_P256K1",
            "SYMMETRIC_DEFAULT",
        ],
        "EncryptionAlgorithms": List[
            Literal["SYMMETRIC_DEFAULT", "RSAES_OAEP_SHA_1", "RSAES_OAEP_SHA_256"]
        ],
        "SigningAlgorithms": List[
            Literal[
                "RSASSA_PSS_SHA_256",
                "RSASSA_PSS_SHA_384",
                "RSASSA_PSS_SHA_512",
                "RSASSA_PKCS1_V1_5_SHA_256",
                "RSASSA_PKCS1_V1_5_SHA_384",
                "RSASSA_PKCS1_V1_5_SHA_512",
                "ECDSA_SHA_256",
                "ECDSA_SHA_384",
                "ECDSA_SHA_512",
            ]
        ],
    },
    total=False,
)


class KeyMetadataTypeDef(_RequiredKeyMetadataTypeDef, _OptionalKeyMetadataTypeDef):
    pass


CreateKeyResponseTypeDef = TypedDict(
    "CreateKeyResponseTypeDef", {"KeyMetadata": KeyMetadataTypeDef}, total=False
)

DecryptResponseTypeDef = TypedDict(
    "DecryptResponseTypeDef",
    {
        "KeyId": str,
        "Plaintext": Union[bytes, IO],
        "EncryptionAlgorithm": Literal[
            "SYMMETRIC_DEFAULT", "RSAES_OAEP_SHA_1", "RSAES_OAEP_SHA_256"
        ],
    },
    total=False,
)

CustomKeyStoresListEntryTypeDef = TypedDict(
    "CustomKeyStoresListEntryTypeDef",
    {
        "CustomKeyStoreId": str,
        "CustomKeyStoreName": str,
        "CloudHsmClusterId": str,
        "TrustAnchorCertificate": str,
        "ConnectionState": Literal[
            "CONNECTED", "CONNECTING", "FAILED", "DISCONNECTED", "DISCONNECTING"
        ],
        "ConnectionErrorCode": Literal[
            "INVALID_CREDENTIALS",
            "CLUSTER_NOT_FOUND",
            "NETWORK_ERRORS",
            "INTERNAL_ERROR",
            "INSUFFICIENT_CLOUDHSM_HSMS",
            "USER_LOCKED_OUT",
            "USER_NOT_FOUND",
            "USER_LOGGED_IN",
            "SUBNET_NOT_FOUND",
        ],
        "CreationDate": datetime,
    },
    total=False,
)

DescribeCustomKeyStoresResponseTypeDef = TypedDict(
    "DescribeCustomKeyStoresResponseTypeDef",
    {
        "CustomKeyStores": List[CustomKeyStoresListEntryTypeDef],
        "NextMarker": str,
        "Truncated": bool,
    },
    total=False,
)

DescribeKeyResponseTypeDef = TypedDict(
    "DescribeKeyResponseTypeDef", {"KeyMetadata": KeyMetadataTypeDef}, total=False
)

EncryptResponseTypeDef = TypedDict(
    "EncryptResponseTypeDef",
    {
        "CiphertextBlob": Union[bytes, IO],
        "KeyId": str,
        "EncryptionAlgorithm": Literal[
            "SYMMETRIC_DEFAULT", "RSAES_OAEP_SHA_1", "RSAES_OAEP_SHA_256"
        ],
    },
    total=False,
)

GenerateDataKeyPairResponseTypeDef = TypedDict(
    "GenerateDataKeyPairResponseTypeDef",
    {
        "PrivateKeyCiphertextBlob": Union[bytes, IO],
        "PrivateKeyPlaintext": Union[bytes, IO],
        "PublicKey": Union[bytes, IO],
        "KeyId": str,
        "KeyPairSpec": Literal[
            "RSA_2048",
            "RSA_3072",
            "RSA_4096",
            "ECC_NIST_P256",
            "ECC_NIST_P384",
            "ECC_NIST_P521",
            "ECC_SECG_P256K1",
        ],
    },
    total=False,
)

GenerateDataKeyPairWithoutPlaintextResponseTypeDef = TypedDict(
    "GenerateDataKeyPairWithoutPlaintextResponseTypeDef",
    {
        "PrivateKeyCiphertextBlob": Union[bytes, IO],
        "PublicKey": Union[bytes, IO],
        "KeyId": str,
        "KeyPairSpec": Literal[
            "RSA_2048",
            "RSA_3072",
            "RSA_4096",
            "ECC_NIST_P256",
            "ECC_NIST_P384",
            "ECC_NIST_P521",
            "ECC_SECG_P256K1",
        ],
    },
    total=False,
)

GenerateDataKeyResponseTypeDef = TypedDict(
    "GenerateDataKeyResponseTypeDef",
    {"CiphertextBlob": Union[bytes, IO], "Plaintext": Union[bytes, IO], "KeyId": str},
    total=False,
)

GenerateDataKeyWithoutPlaintextResponseTypeDef = TypedDict(
    "GenerateDataKeyWithoutPlaintextResponseTypeDef",
    {"CiphertextBlob": Union[bytes, IO], "KeyId": str},
    total=False,
)

GenerateRandomResponseTypeDef = TypedDict(
    "GenerateRandomResponseTypeDef", {"Plaintext": Union[bytes, IO]}, total=False
)

GetKeyPolicyResponseTypeDef = TypedDict("GetKeyPolicyResponseTypeDef", {"Policy": str}, total=False)

GetKeyRotationStatusResponseTypeDef = TypedDict(
    "GetKeyRotationStatusResponseTypeDef", {"KeyRotationEnabled": bool}, total=False
)

GetParametersForImportResponseTypeDef = TypedDict(
    "GetParametersForImportResponseTypeDef",
    {
        "KeyId": str,
        "ImportToken": Union[bytes, IO],
        "PublicKey": Union[bytes, IO],
        "ParametersValidTo": datetime,
    },
    total=False,
)

GetPublicKeyResponseTypeDef = TypedDict(
    "GetPublicKeyResponseTypeDef",
    {
        "KeyId": str,
        "PublicKey": Union[bytes, IO],
        "CustomerMasterKeySpec": Literal[
            "RSA_2048",
            "RSA_3072",
            "RSA_4096",
            "ECC_NIST_P256",
            "ECC_NIST_P384",
            "ECC_NIST_P521",
            "ECC_SECG_P256K1",
            "SYMMETRIC_DEFAULT",
        ],
        "KeyUsage": Literal["SIGN_VERIFY", "ENCRYPT_DECRYPT"],
        "EncryptionAlgorithms": List[
            Literal["SYMMETRIC_DEFAULT", "RSAES_OAEP_SHA_1", "RSAES_OAEP_SHA_256"]
        ],
        "SigningAlgorithms": List[
            Literal[
                "RSASSA_PSS_SHA_256",
                "RSASSA_PSS_SHA_384",
                "RSASSA_PSS_SHA_512",
                "RSASSA_PKCS1_V1_5_SHA_256",
                "RSASSA_PKCS1_V1_5_SHA_384",
                "RSASSA_PKCS1_V1_5_SHA_512",
                "ECDSA_SHA_256",
                "ECDSA_SHA_384",
                "ECDSA_SHA_512",
            ]
        ],
    },
    total=False,
)

GrantConstraintsTypeDef = TypedDict(
    "GrantConstraintsTypeDef",
    {"EncryptionContextSubset": Dict[str, str], "EncryptionContextEquals": Dict[str, str]},
    total=False,
)

AliasListEntryTypeDef = TypedDict(
    "AliasListEntryTypeDef", {"AliasName": str, "AliasArn": str, "TargetKeyId": str}, total=False
)

ListAliasesResponseTypeDef = TypedDict(
    "ListAliasesResponseTypeDef",
    {"Aliases": List[AliasListEntryTypeDef], "NextMarker": str, "Truncated": bool},
    total=False,
)

GrantListEntryTypeDef = TypedDict(
    "GrantListEntryTypeDef",
    {
        "KeyId": str,
        "GrantId": str,
        "Name": str,
        "CreationDate": datetime,
        "GranteePrincipal": str,
        "RetiringPrincipal": str,
        "IssuingAccount": str,
        "Operations": List[
            Literal[
                "Decrypt",
                "Encrypt",
                "GenerateDataKey",
                "GenerateDataKeyWithoutPlaintext",
                "ReEncryptFrom",
                "ReEncryptTo",
                "Sign",
                "Verify",
                "GetPublicKey",
                "CreateGrant",
                "RetireGrant",
                "DescribeKey",
                "GenerateDataKeyPair",
                "GenerateDataKeyPairWithoutPlaintext",
            ]
        ],
        "Constraints": GrantConstraintsTypeDef,
    },
    total=False,
)

ListGrantsResponseTypeDef = TypedDict(
    "ListGrantsResponseTypeDef",
    {"Grants": List[GrantListEntryTypeDef], "NextMarker": str, "Truncated": bool},
    total=False,
)

ListKeyPoliciesResponseTypeDef = TypedDict(
    "ListKeyPoliciesResponseTypeDef",
    {"PolicyNames": List[str], "NextMarker": str, "Truncated": bool},
    total=False,
)

KeyListEntryTypeDef = TypedDict("KeyListEntryTypeDef", {"KeyId": str, "KeyArn": str}, total=False)

ListKeysResponseTypeDef = TypedDict(
    "ListKeysResponseTypeDef",
    {"Keys": List[KeyListEntryTypeDef], "NextMarker": str, "Truncated": bool},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"TagKey": str, "TagValue": str})

ListResourceTagsResponseTypeDef = TypedDict(
    "ListResourceTagsResponseTypeDef",
    {"Tags": List[TagTypeDef], "NextMarker": str, "Truncated": bool},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

ReEncryptResponseTypeDef = TypedDict(
    "ReEncryptResponseTypeDef",
    {
        "CiphertextBlob": Union[bytes, IO],
        "SourceKeyId": str,
        "KeyId": str,
        "SourceEncryptionAlgorithm": Literal[
            "SYMMETRIC_DEFAULT", "RSAES_OAEP_SHA_1", "RSAES_OAEP_SHA_256"
        ],
        "DestinationEncryptionAlgorithm": Literal[
            "SYMMETRIC_DEFAULT", "RSAES_OAEP_SHA_1", "RSAES_OAEP_SHA_256"
        ],
    },
    total=False,
)

ScheduleKeyDeletionResponseTypeDef = TypedDict(
    "ScheduleKeyDeletionResponseTypeDef", {"KeyId": str, "DeletionDate": datetime}, total=False
)

SignResponseTypeDef = TypedDict(
    "SignResponseTypeDef",
    {
        "KeyId": str,
        "Signature": Union[bytes, IO],
        "SigningAlgorithm": Literal[
            "RSASSA_PSS_SHA_256",
            "RSASSA_PSS_SHA_384",
            "RSASSA_PSS_SHA_512",
            "RSASSA_PKCS1_V1_5_SHA_256",
            "RSASSA_PKCS1_V1_5_SHA_384",
            "RSASSA_PKCS1_V1_5_SHA_512",
            "ECDSA_SHA_256",
            "ECDSA_SHA_384",
            "ECDSA_SHA_512",
        ],
    },
    total=False,
)

VerifyResponseTypeDef = TypedDict(
    "VerifyResponseTypeDef",
    {
        "KeyId": str,
        "SignatureValid": bool,
        "SigningAlgorithm": Literal[
            "RSASSA_PSS_SHA_256",
            "RSASSA_PSS_SHA_384",
            "RSASSA_PSS_SHA_512",
            "RSASSA_PKCS1_V1_5_SHA_256",
            "RSASSA_PKCS1_V1_5_SHA_384",
            "RSASSA_PKCS1_V1_5_SHA_512",
            "ECDSA_SHA_256",
            "ECDSA_SHA_384",
            "ECDSA_SHA_512",
        ],
    },
    total=False,
)
