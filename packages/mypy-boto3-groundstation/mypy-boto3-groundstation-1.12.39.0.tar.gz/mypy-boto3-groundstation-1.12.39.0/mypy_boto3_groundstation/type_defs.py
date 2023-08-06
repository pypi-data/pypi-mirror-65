"""
Main interface for groundstation service type definitions.

Usage::

    from mypy_boto3.groundstation.type_defs import ConfigIdResponseTypeDef

    data: ConfigIdResponseTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ConfigIdResponseTypeDef",
    "FrequencyBandwidthTypeDef",
    "FrequencyTypeDef",
    "SpectrumConfigTypeDef",
    "AntennaDownlinkConfigTypeDef",
    "DecodeConfigTypeDef",
    "DemodulationConfigTypeDef",
    "AntennaDownlinkDemodDecodeConfigTypeDef",
    "EirpTypeDef",
    "UplinkSpectrumConfigTypeDef",
    "AntennaUplinkConfigTypeDef",
    "DataflowEndpointConfigTypeDef",
    "TrackingConfigTypeDef",
    "UplinkEchoConfigTypeDef",
    "ConfigTypeDataTypeDef",
    "ContactIdResponseTypeDef",
    "DataflowEndpointGroupIdResponseTypeDef",
    "ElevationTypeDef",
    "DescribeContactResponseTypeDef",
    "SocketAddressTypeDef",
    "DataflowEndpointTypeDef",
    "SecurityDetailsTypeDef",
    "EndpointDetailsTypeDef",
    "GetConfigResponseTypeDef",
    "GetDataflowEndpointGroupResponseTypeDef",
    "GetMinuteUsageResponseTypeDef",
    "GetMissionProfileResponseTypeDef",
    "GetSatelliteResponseTypeDef",
    "ConfigListItemTypeDef",
    "ListConfigsResponseTypeDef",
    "ContactDataTypeDef",
    "ListContactsResponseTypeDef",
    "DataflowEndpointListItemTypeDef",
    "ListDataflowEndpointGroupsResponseTypeDef",
    "GroundStationDataTypeDef",
    "ListGroundStationsResponseTypeDef",
    "MissionProfileListItemTypeDef",
    "ListMissionProfilesResponseTypeDef",
    "SatelliteListItemTypeDef",
    "ListSatellitesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MissionProfileIdResponseTypeDef",
    "PaginatorConfigTypeDef",
)

ConfigIdResponseTypeDef = TypedDict(
    "ConfigIdResponseTypeDef",
    {
        "configArn": str,
        "configId": str,
        "configType": Literal[
            "antenna-downlink",
            "antenna-downlink-demod-decode",
            "antenna-uplink",
            "dataflow-endpoint",
            "tracking",
            "uplink-echo",
        ],
    },
    total=False,
)

FrequencyBandwidthTypeDef = TypedDict(
    "FrequencyBandwidthTypeDef", {"units": Literal["GHz", "MHz", "kHz"], "value": float}
)

FrequencyTypeDef = TypedDict(
    "FrequencyTypeDef", {"units": Literal["GHz", "MHz", "kHz"], "value": float}
)

_RequiredSpectrumConfigTypeDef = TypedDict(
    "_RequiredSpectrumConfigTypeDef",
    {"bandwidth": FrequencyBandwidthTypeDef, "centerFrequency": FrequencyTypeDef},
)
_OptionalSpectrumConfigTypeDef = TypedDict(
    "_OptionalSpectrumConfigTypeDef",
    {"polarization": Literal["LEFT_HAND", "NONE", "RIGHT_HAND"]},
    total=False,
)


class SpectrumConfigTypeDef(_RequiredSpectrumConfigTypeDef, _OptionalSpectrumConfigTypeDef):
    pass


AntennaDownlinkConfigTypeDef = TypedDict(
    "AntennaDownlinkConfigTypeDef", {"spectrumConfig": SpectrumConfigTypeDef}
)

DecodeConfigTypeDef = TypedDict("DecodeConfigTypeDef", {"unvalidatedJSON": str})

DemodulationConfigTypeDef = TypedDict("DemodulationConfigTypeDef", {"unvalidatedJSON": str})

AntennaDownlinkDemodDecodeConfigTypeDef = TypedDict(
    "AntennaDownlinkDemodDecodeConfigTypeDef",
    {
        "decodeConfig": DecodeConfigTypeDef,
        "demodulationConfig": DemodulationConfigTypeDef,
        "spectrumConfig": SpectrumConfigTypeDef,
    },
)

EirpTypeDef = TypedDict("EirpTypeDef", {"units": Literal["dBW"], "value": float})

_RequiredUplinkSpectrumConfigTypeDef = TypedDict(
    "_RequiredUplinkSpectrumConfigTypeDef", {"centerFrequency": FrequencyTypeDef}
)
_OptionalUplinkSpectrumConfigTypeDef = TypedDict(
    "_OptionalUplinkSpectrumConfigTypeDef",
    {"polarization": Literal["LEFT_HAND", "NONE", "RIGHT_HAND"]},
    total=False,
)


class UplinkSpectrumConfigTypeDef(
    _RequiredUplinkSpectrumConfigTypeDef, _OptionalUplinkSpectrumConfigTypeDef
):
    pass


AntennaUplinkConfigTypeDef = TypedDict(
    "AntennaUplinkConfigTypeDef",
    {"spectrumConfig": UplinkSpectrumConfigTypeDef, "targetEirp": EirpTypeDef},
)

_RequiredDataflowEndpointConfigTypeDef = TypedDict(
    "_RequiredDataflowEndpointConfigTypeDef", {"dataflowEndpointName": str}
)
_OptionalDataflowEndpointConfigTypeDef = TypedDict(
    "_OptionalDataflowEndpointConfigTypeDef", {"dataflowEndpointRegion": str}, total=False
)


class DataflowEndpointConfigTypeDef(
    _RequiredDataflowEndpointConfigTypeDef, _OptionalDataflowEndpointConfigTypeDef
):
    pass


TrackingConfigTypeDef = TypedDict(
    "TrackingConfigTypeDef", {"autotrack": Literal["PREFERRED", "REMOVED", "REQUIRED"]}
)

UplinkEchoConfigTypeDef = TypedDict(
    "UplinkEchoConfigTypeDef", {"antennaUplinkConfigArn": str, "enabled": bool}
)

ConfigTypeDataTypeDef = TypedDict(
    "ConfigTypeDataTypeDef",
    {
        "antennaDownlinkConfig": AntennaDownlinkConfigTypeDef,
        "antennaDownlinkDemodDecodeConfig": AntennaDownlinkDemodDecodeConfigTypeDef,
        "antennaUplinkConfig": AntennaUplinkConfigTypeDef,
        "dataflowEndpointConfig": DataflowEndpointConfigTypeDef,
        "trackingConfig": TrackingConfigTypeDef,
        "uplinkEchoConfig": UplinkEchoConfigTypeDef,
    },
    total=False,
)

ContactIdResponseTypeDef = TypedDict("ContactIdResponseTypeDef", {"contactId": str}, total=False)

DataflowEndpointGroupIdResponseTypeDef = TypedDict(
    "DataflowEndpointGroupIdResponseTypeDef", {"dataflowEndpointGroupId": str}, total=False
)

ElevationTypeDef = TypedDict(
    "ElevationTypeDef", {"unit": Literal["DEGREE_ANGLE", "RADIAN"], "value": float}
)

DescribeContactResponseTypeDef = TypedDict(
    "DescribeContactResponseTypeDef",
    {
        "contactId": str,
        "contactStatus": Literal[
            "AVAILABLE",
            "AWS_CANCELLED",
            "CANCELLED",
            "CANCELLING",
            "COMPLETED",
            "FAILED",
            "FAILED_TO_SCHEDULE",
            "PASS",
            "POSTPASS",
            "PREPASS",
            "SCHEDULED",
            "SCHEDULING",
        ],
        "endTime": datetime,
        "errorMessage": str,
        "groundStation": str,
        "maximumElevation": ElevationTypeDef,
        "missionProfileArn": str,
        "postPassEndTime": datetime,
        "prePassStartTime": datetime,
        "region": str,
        "satelliteArn": str,
        "startTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

SocketAddressTypeDef = TypedDict("SocketAddressTypeDef", {"name": str, "port": int})

DataflowEndpointTypeDef = TypedDict(
    "DataflowEndpointTypeDef",
    {
        "address": SocketAddressTypeDef,
        "name": str,
        "status": Literal["created", "creating", "deleted", "deleting", "failed"],
    },
    total=False,
)

SecurityDetailsTypeDef = TypedDict(
    "SecurityDetailsTypeDef",
    {"roleArn": str, "securityGroupIds": List[str], "subnetIds": List[str]},
)

EndpointDetailsTypeDef = TypedDict(
    "EndpointDetailsTypeDef",
    {"endpoint": DataflowEndpointTypeDef, "securityDetails": SecurityDetailsTypeDef},
    total=False,
)

_RequiredGetConfigResponseTypeDef = TypedDict(
    "_RequiredGetConfigResponseTypeDef",
    {"configArn": str, "configData": ConfigTypeDataTypeDef, "configId": str, "name": str},
)
_OptionalGetConfigResponseTypeDef = TypedDict(
    "_OptionalGetConfigResponseTypeDef",
    {
        "configType": Literal[
            "antenna-downlink",
            "antenna-downlink-demod-decode",
            "antenna-uplink",
            "dataflow-endpoint",
            "tracking",
            "uplink-echo",
        ],
        "tags": Dict[str, str],
    },
    total=False,
)


class GetConfigResponseTypeDef(
    _RequiredGetConfigResponseTypeDef, _OptionalGetConfigResponseTypeDef
):
    pass


GetDataflowEndpointGroupResponseTypeDef = TypedDict(
    "GetDataflowEndpointGroupResponseTypeDef",
    {
        "dataflowEndpointGroupArn": str,
        "dataflowEndpointGroupId": str,
        "endpointsDetails": List[EndpointDetailsTypeDef],
        "tags": Dict[str, str],
    },
    total=False,
)

GetMinuteUsageResponseTypeDef = TypedDict(
    "GetMinuteUsageResponseTypeDef",
    {
        "estimatedMinutesRemaining": int,
        "isReservedMinutesCustomer": bool,
        "totalReservedMinuteAllocation": int,
        "totalScheduledMinutes": int,
        "upcomingMinutesScheduled": int,
    },
    total=False,
)

GetMissionProfileResponseTypeDef = TypedDict(
    "GetMissionProfileResponseTypeDef",
    {
        "contactPostPassDurationSeconds": int,
        "contactPrePassDurationSeconds": int,
        "dataflowEdges": List[List[str]],
        "minimumViableContactDurationSeconds": int,
        "missionProfileArn": str,
        "missionProfileId": str,
        "name": str,
        "region": str,
        "tags": Dict[str, str],
        "trackingConfigArn": str,
    },
    total=False,
)

GetSatelliteResponseTypeDef = TypedDict(
    "GetSatelliteResponseTypeDef",
    {"groundStations": List[str], "noradSatelliteID": int, "satelliteArn": str, "satelliteId": str},
    total=False,
)

ConfigListItemTypeDef = TypedDict(
    "ConfigListItemTypeDef",
    {
        "configArn": str,
        "configId": str,
        "configType": Literal[
            "antenna-downlink",
            "antenna-downlink-demod-decode",
            "antenna-uplink",
            "dataflow-endpoint",
            "tracking",
            "uplink-echo",
        ],
        "name": str,
    },
    total=False,
)

ListConfigsResponseTypeDef = TypedDict(
    "ListConfigsResponseTypeDef",
    {"configList": List[ConfigListItemTypeDef], "nextToken": str},
    total=False,
)

ContactDataTypeDef = TypedDict(
    "ContactDataTypeDef",
    {
        "contactId": str,
        "contactStatus": Literal[
            "AVAILABLE",
            "AWS_CANCELLED",
            "CANCELLED",
            "CANCELLING",
            "COMPLETED",
            "FAILED",
            "FAILED_TO_SCHEDULE",
            "PASS",
            "POSTPASS",
            "PREPASS",
            "SCHEDULED",
            "SCHEDULING",
        ],
        "endTime": datetime,
        "errorMessage": str,
        "groundStation": str,
        "maximumElevation": ElevationTypeDef,
        "missionProfileArn": str,
        "postPassEndTime": datetime,
        "prePassStartTime": datetime,
        "region": str,
        "satelliteArn": str,
        "startTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

ListContactsResponseTypeDef = TypedDict(
    "ListContactsResponseTypeDef",
    {"contactList": List[ContactDataTypeDef], "nextToken": str},
    total=False,
)

DataflowEndpointListItemTypeDef = TypedDict(
    "DataflowEndpointListItemTypeDef",
    {"dataflowEndpointGroupArn": str, "dataflowEndpointGroupId": str},
    total=False,
)

ListDataflowEndpointGroupsResponseTypeDef = TypedDict(
    "ListDataflowEndpointGroupsResponseTypeDef",
    {"dataflowEndpointGroupList": List[DataflowEndpointListItemTypeDef], "nextToken": str},
    total=False,
)

GroundStationDataTypeDef = TypedDict(
    "GroundStationDataTypeDef",
    {"groundStationId": str, "groundStationName": str, "region": str},
    total=False,
)

ListGroundStationsResponseTypeDef = TypedDict(
    "ListGroundStationsResponseTypeDef",
    {"groundStationList": List[GroundStationDataTypeDef], "nextToken": str},
    total=False,
)

MissionProfileListItemTypeDef = TypedDict(
    "MissionProfileListItemTypeDef",
    {"missionProfileArn": str, "missionProfileId": str, "name": str, "region": str},
    total=False,
)

ListMissionProfilesResponseTypeDef = TypedDict(
    "ListMissionProfilesResponseTypeDef",
    {"missionProfileList": List[MissionProfileListItemTypeDef], "nextToken": str},
    total=False,
)

SatelliteListItemTypeDef = TypedDict(
    "SatelliteListItemTypeDef",
    {"groundStations": List[str], "noradSatelliteID": int, "satelliteArn": str, "satelliteId": str},
    total=False,
)

ListSatellitesResponseTypeDef = TypedDict(
    "ListSatellitesResponseTypeDef",
    {"nextToken": str, "satellites": List[SatelliteListItemTypeDef]},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": Dict[str, str]}, total=False
)

MissionProfileIdResponseTypeDef = TypedDict(
    "MissionProfileIdResponseTypeDef", {"missionProfileId": str}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
