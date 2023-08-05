"""
Main interface for lakeformation service type definitions.

Usage::

    from mypy_boto3.lakeformation.type_defs import DataLakePrincipalTypeDef

    data: DataLakePrincipalTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Any, Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DataLakePrincipalTypeDef",
    "DataLocationResourceTypeDef",
    "DatabaseResourceTypeDef",
    "TableResourceTypeDef",
    "ColumnWildcardTypeDef",
    "TableWithColumnsResourceTypeDef",
    "ResourceTypeDef",
    "BatchPermissionsRequestEntryTypeDef",
    "ErrorDetailTypeDef",
    "BatchPermissionsFailureEntryTypeDef",
    "BatchGrantPermissionsResponseTypeDef",
    "BatchRevokePermissionsResponseTypeDef",
    "PrincipalPermissionsTypeDef",
    "DataLakeSettingsTypeDef",
    "ResourceInfoTypeDef",
    "DescribeResourceResponseTypeDef",
    "FilterConditionTypeDef",
    "GetDataLakeSettingsResponseTypeDef",
    "PrincipalResourcePermissionsTypeDef",
    "GetEffectivePermissionsForPathResponseTypeDef",
    "ListPermissionsResponseTypeDef",
    "ListResourcesResponseTypeDef",
)

DataLakePrincipalTypeDef = TypedDict(
    "DataLakePrincipalTypeDef", {"DataLakePrincipalIdentifier": str}, total=False
)

DataLocationResourceTypeDef = TypedDict("DataLocationResourceTypeDef", {"ResourceArn": str})

DatabaseResourceTypeDef = TypedDict("DatabaseResourceTypeDef", {"Name": str})

TableResourceTypeDef = TypedDict("TableResourceTypeDef", {"DatabaseName": str, "Name": str})

ColumnWildcardTypeDef = TypedDict(
    "ColumnWildcardTypeDef", {"ExcludedColumnNames": List[str]}, total=False
)

TableWithColumnsResourceTypeDef = TypedDict(
    "TableWithColumnsResourceTypeDef",
    {
        "DatabaseName": str,
        "Name": str,
        "ColumnNames": List[str],
        "ColumnWildcard": ColumnWildcardTypeDef,
    },
    total=False,
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "Catalog": Dict[str, Any],
        "Database": DatabaseResourceTypeDef,
        "Table": TableResourceTypeDef,
        "TableWithColumns": TableWithColumnsResourceTypeDef,
        "DataLocation": DataLocationResourceTypeDef,
    },
    total=False,
)

_RequiredBatchPermissionsRequestEntryTypeDef = TypedDict(
    "_RequiredBatchPermissionsRequestEntryTypeDef", {"Id": str}
)
_OptionalBatchPermissionsRequestEntryTypeDef = TypedDict(
    "_OptionalBatchPermissionsRequestEntryTypeDef",
    {
        "Principal": DataLakePrincipalTypeDef,
        "Resource": ResourceTypeDef,
        "Permissions": List[
            Literal[
                "ALL",
                "SELECT",
                "ALTER",
                "DROP",
                "DELETE",
                "INSERT",
                "CREATE_DATABASE",
                "CREATE_TABLE",
                "DATA_LOCATION_ACCESS",
            ]
        ],
        "PermissionsWithGrantOption": List[
            Literal[
                "ALL",
                "SELECT",
                "ALTER",
                "DROP",
                "DELETE",
                "INSERT",
                "CREATE_DATABASE",
                "CREATE_TABLE",
                "DATA_LOCATION_ACCESS",
            ]
        ],
    },
    total=False,
)


class BatchPermissionsRequestEntryTypeDef(
    _RequiredBatchPermissionsRequestEntryTypeDef, _OptionalBatchPermissionsRequestEntryTypeDef
):
    pass


ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef", {"ErrorCode": str, "ErrorMessage": str}, total=False
)

BatchPermissionsFailureEntryTypeDef = TypedDict(
    "BatchPermissionsFailureEntryTypeDef",
    {"RequestEntry": BatchPermissionsRequestEntryTypeDef, "Error": ErrorDetailTypeDef},
    total=False,
)

BatchGrantPermissionsResponseTypeDef = TypedDict(
    "BatchGrantPermissionsResponseTypeDef",
    {"Failures": List[BatchPermissionsFailureEntryTypeDef]},
    total=False,
)

BatchRevokePermissionsResponseTypeDef = TypedDict(
    "BatchRevokePermissionsResponseTypeDef",
    {"Failures": List[BatchPermissionsFailureEntryTypeDef]},
    total=False,
)

PrincipalPermissionsTypeDef = TypedDict(
    "PrincipalPermissionsTypeDef",
    {
        "Principal": DataLakePrincipalTypeDef,
        "Permissions": List[
            Literal[
                "ALL",
                "SELECT",
                "ALTER",
                "DROP",
                "DELETE",
                "INSERT",
                "CREATE_DATABASE",
                "CREATE_TABLE",
                "DATA_LOCATION_ACCESS",
            ]
        ],
    },
    total=False,
)

DataLakeSettingsTypeDef = TypedDict(
    "DataLakeSettingsTypeDef",
    {
        "DataLakeAdmins": List[DataLakePrincipalTypeDef],
        "CreateDatabaseDefaultPermissions": List[PrincipalPermissionsTypeDef],
        "CreateTableDefaultPermissions": List[PrincipalPermissionsTypeDef],
    },
    total=False,
)

ResourceInfoTypeDef = TypedDict(
    "ResourceInfoTypeDef",
    {"ResourceArn": str, "RoleArn": str, "LastModified": datetime},
    total=False,
)

DescribeResourceResponseTypeDef = TypedDict(
    "DescribeResourceResponseTypeDef", {"ResourceInfo": ResourceInfoTypeDef}, total=False
)

FilterConditionTypeDef = TypedDict(
    "FilterConditionTypeDef",
    {
        "Field": Literal["RESOURCE_ARN", "ROLE_ARN", "LAST_MODIFIED"],
        "ComparisonOperator": Literal[
            "EQ",
            "NE",
            "LE",
            "LT",
            "GE",
            "GT",
            "CONTAINS",
            "NOT_CONTAINS",
            "BEGINS_WITH",
            "IN",
            "BETWEEN",
        ],
        "StringValueList": List[str],
    },
    total=False,
)

GetDataLakeSettingsResponseTypeDef = TypedDict(
    "GetDataLakeSettingsResponseTypeDef", {"DataLakeSettings": DataLakeSettingsTypeDef}, total=False
)

PrincipalResourcePermissionsTypeDef = TypedDict(
    "PrincipalResourcePermissionsTypeDef",
    {
        "Principal": DataLakePrincipalTypeDef,
        "Resource": ResourceTypeDef,
        "Permissions": List[
            Literal[
                "ALL",
                "SELECT",
                "ALTER",
                "DROP",
                "DELETE",
                "INSERT",
                "CREATE_DATABASE",
                "CREATE_TABLE",
                "DATA_LOCATION_ACCESS",
            ]
        ],
        "PermissionsWithGrantOption": List[
            Literal[
                "ALL",
                "SELECT",
                "ALTER",
                "DROP",
                "DELETE",
                "INSERT",
                "CREATE_DATABASE",
                "CREATE_TABLE",
                "DATA_LOCATION_ACCESS",
            ]
        ],
    },
    total=False,
)

GetEffectivePermissionsForPathResponseTypeDef = TypedDict(
    "GetEffectivePermissionsForPathResponseTypeDef",
    {"Permissions": List[PrincipalResourcePermissionsTypeDef], "NextToken": str},
    total=False,
)

ListPermissionsResponseTypeDef = TypedDict(
    "ListPermissionsResponseTypeDef",
    {"PrincipalResourcePermissions": List[PrincipalResourcePermissionsTypeDef], "NextToken": str},
    total=False,
)

ListResourcesResponseTypeDef = TypedDict(
    "ListResourcesResponseTypeDef",
    {"ResourceInfoList": List[ResourceInfoTypeDef], "NextToken": str},
    total=False,
)
