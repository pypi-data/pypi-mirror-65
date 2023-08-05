"""
Main interface for managedblockchain service type definitions.

Usage::

    from mypy_boto3.managedblockchain.type_defs import CreateMemberOutputTypeDef

    data: CreateMemberOutputTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CreateMemberOutputTypeDef",
    "CreateNetworkOutputTypeDef",
    "CreateNodeOutputTypeDef",
    "CreateProposalOutputTypeDef",
    "MemberFabricAttributesTypeDef",
    "MemberFrameworkAttributesTypeDef",
    "LogConfigurationTypeDef",
    "LogConfigurationsTypeDef",
    "MemberFabricLogPublishingConfigurationTypeDef",
    "MemberLogPublishingConfigurationTypeDef",
    "MemberTypeDef",
    "GetMemberOutputTypeDef",
    "NetworkFabricAttributesTypeDef",
    "NetworkFrameworkAttributesTypeDef",
    "ApprovalThresholdPolicyTypeDef",
    "VotingPolicyTypeDef",
    "NetworkTypeDef",
    "GetNetworkOutputTypeDef",
    "NodeFabricAttributesTypeDef",
    "NodeFrameworkAttributesTypeDef",
    "NodeFabricLogPublishingConfigurationTypeDef",
    "NodeLogPublishingConfigurationTypeDef",
    "NodeTypeDef",
    "GetNodeOutputTypeDef",
    "InviteActionTypeDef",
    "RemoveActionTypeDef",
    "ProposalActionsTypeDef",
    "ProposalTypeDef",
    "GetProposalOutputTypeDef",
    "NetworkSummaryTypeDef",
    "InvitationTypeDef",
    "ListInvitationsOutputTypeDef",
    "MemberSummaryTypeDef",
    "ListMembersOutputTypeDef",
    "ListNetworksOutputTypeDef",
    "NodeSummaryTypeDef",
    "ListNodesOutputTypeDef",
    "VoteSummaryTypeDef",
    "ListProposalVotesOutputTypeDef",
    "ProposalSummaryTypeDef",
    "ListProposalsOutputTypeDef",
    "MemberFabricConfigurationTypeDef",
    "MemberFrameworkConfigurationTypeDef",
    "MemberConfigurationTypeDef",
    "NetworkFabricConfigurationTypeDef",
    "NetworkFrameworkConfigurationTypeDef",
    "NodeConfigurationTypeDef",
)

CreateMemberOutputTypeDef = TypedDict("CreateMemberOutputTypeDef", {"MemberId": str}, total=False)

CreateNetworkOutputTypeDef = TypedDict(
    "CreateNetworkOutputTypeDef", {"NetworkId": str, "MemberId": str}, total=False
)

CreateNodeOutputTypeDef = TypedDict("CreateNodeOutputTypeDef", {"NodeId": str}, total=False)

CreateProposalOutputTypeDef = TypedDict(
    "CreateProposalOutputTypeDef", {"ProposalId": str}, total=False
)

MemberFabricAttributesTypeDef = TypedDict(
    "MemberFabricAttributesTypeDef", {"AdminUsername": str, "CaEndpoint": str}, total=False
)

MemberFrameworkAttributesTypeDef = TypedDict(
    "MemberFrameworkAttributesTypeDef", {"Fabric": MemberFabricAttributesTypeDef}, total=False
)

LogConfigurationTypeDef = TypedDict("LogConfigurationTypeDef", {"Enabled": bool}, total=False)

LogConfigurationsTypeDef = TypedDict(
    "LogConfigurationsTypeDef", {"Cloudwatch": LogConfigurationTypeDef}, total=False
)

MemberFabricLogPublishingConfigurationTypeDef = TypedDict(
    "MemberFabricLogPublishingConfigurationTypeDef",
    {"CaLogs": LogConfigurationsTypeDef},
    total=False,
)

MemberLogPublishingConfigurationTypeDef = TypedDict(
    "MemberLogPublishingConfigurationTypeDef",
    {"Fabric": MemberFabricLogPublishingConfigurationTypeDef},
    total=False,
)

MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "NetworkId": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "FrameworkAttributes": MemberFrameworkAttributesTypeDef,
        "LogPublishingConfiguration": MemberLogPublishingConfigurationTypeDef,
        "Status": Literal[
            "CREATING", "AVAILABLE", "CREATE_FAILED", "UPDATING", "DELETING", "DELETED"
        ],
        "CreationDate": datetime,
    },
    total=False,
)

GetMemberOutputTypeDef = TypedDict("GetMemberOutputTypeDef", {"Member": MemberTypeDef}, total=False)

NetworkFabricAttributesTypeDef = TypedDict(
    "NetworkFabricAttributesTypeDef",
    {"OrderingServiceEndpoint": str, "Edition": Literal["STARTER", "STANDARD"]},
    total=False,
)

NetworkFrameworkAttributesTypeDef = TypedDict(
    "NetworkFrameworkAttributesTypeDef", {"Fabric": NetworkFabricAttributesTypeDef}, total=False
)

ApprovalThresholdPolicyTypeDef = TypedDict(
    "ApprovalThresholdPolicyTypeDef",
    {
        "ThresholdPercentage": int,
        "ProposalDurationInHours": int,
        "ThresholdComparator": Literal["GREATER_THAN", "GREATER_THAN_OR_EQUAL_TO"],
    },
    total=False,
)

VotingPolicyTypeDef = TypedDict(
    "VotingPolicyTypeDef", {"ApprovalThresholdPolicy": ApprovalThresholdPolicyTypeDef}, total=False
)

NetworkTypeDef = TypedDict(
    "NetworkTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "Framework": Literal["HYPERLEDGER_FABRIC"],
        "FrameworkVersion": str,
        "FrameworkAttributes": NetworkFrameworkAttributesTypeDef,
        "VpcEndpointServiceName": str,
        "VotingPolicy": VotingPolicyTypeDef,
        "Status": Literal["CREATING", "AVAILABLE", "CREATE_FAILED", "DELETING", "DELETED"],
        "CreationDate": datetime,
    },
    total=False,
)

GetNetworkOutputTypeDef = TypedDict(
    "GetNetworkOutputTypeDef", {"Network": NetworkTypeDef}, total=False
)

NodeFabricAttributesTypeDef = TypedDict(
    "NodeFabricAttributesTypeDef", {"PeerEndpoint": str, "PeerEventEndpoint": str}, total=False
)

NodeFrameworkAttributesTypeDef = TypedDict(
    "NodeFrameworkAttributesTypeDef", {"Fabric": NodeFabricAttributesTypeDef}, total=False
)

NodeFabricLogPublishingConfigurationTypeDef = TypedDict(
    "NodeFabricLogPublishingConfigurationTypeDef",
    {"ChaincodeLogs": LogConfigurationsTypeDef, "PeerLogs": LogConfigurationsTypeDef},
    total=False,
)

NodeLogPublishingConfigurationTypeDef = TypedDict(
    "NodeLogPublishingConfigurationTypeDef",
    {"Fabric": NodeFabricLogPublishingConfigurationTypeDef},
    total=False,
)

NodeTypeDef = TypedDict(
    "NodeTypeDef",
    {
        "NetworkId": str,
        "MemberId": str,
        "Id": str,
        "InstanceType": str,
        "AvailabilityZone": str,
        "FrameworkAttributes": NodeFrameworkAttributesTypeDef,
        "LogPublishingConfiguration": NodeLogPublishingConfigurationTypeDef,
        "Status": Literal[
            "CREATING", "AVAILABLE", "CREATE_FAILED", "UPDATING", "DELETING", "DELETED", "FAILED"
        ],
        "CreationDate": datetime,
    },
    total=False,
)

GetNodeOutputTypeDef = TypedDict("GetNodeOutputTypeDef", {"Node": NodeTypeDef}, total=False)

InviteActionTypeDef = TypedDict("InviteActionTypeDef", {"Principal": str})

RemoveActionTypeDef = TypedDict("RemoveActionTypeDef", {"MemberId": str})

ProposalActionsTypeDef = TypedDict(
    "ProposalActionsTypeDef",
    {"Invitations": List[InviteActionTypeDef], "Removals": List[RemoveActionTypeDef]},
    total=False,
)

ProposalTypeDef = TypedDict(
    "ProposalTypeDef",
    {
        "ProposalId": str,
        "NetworkId": str,
        "Description": str,
        "Actions": ProposalActionsTypeDef,
        "ProposedByMemberId": str,
        "ProposedByMemberName": str,
        "Status": Literal["IN_PROGRESS", "APPROVED", "REJECTED", "EXPIRED", "ACTION_FAILED"],
        "CreationDate": datetime,
        "ExpirationDate": datetime,
        "YesVoteCount": int,
        "NoVoteCount": int,
        "OutstandingVoteCount": int,
    },
    total=False,
)

GetProposalOutputTypeDef = TypedDict(
    "GetProposalOutputTypeDef", {"Proposal": ProposalTypeDef}, total=False
)

NetworkSummaryTypeDef = TypedDict(
    "NetworkSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "Framework": Literal["HYPERLEDGER_FABRIC"],
        "FrameworkVersion": str,
        "Status": Literal["CREATING", "AVAILABLE", "CREATE_FAILED", "DELETING", "DELETED"],
        "CreationDate": datetime,
    },
    total=False,
)

InvitationTypeDef = TypedDict(
    "InvitationTypeDef",
    {
        "InvitationId": str,
        "CreationDate": datetime,
        "ExpirationDate": datetime,
        "Status": Literal["PENDING", "ACCEPTED", "ACCEPTING", "REJECTED", "EXPIRED"],
        "NetworkSummary": NetworkSummaryTypeDef,
    },
    total=False,
)

ListInvitationsOutputTypeDef = TypedDict(
    "ListInvitationsOutputTypeDef",
    {"Invitations": List[InvitationTypeDef], "NextToken": str},
    total=False,
)

MemberSummaryTypeDef = TypedDict(
    "MemberSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "Status": Literal[
            "CREATING", "AVAILABLE", "CREATE_FAILED", "UPDATING", "DELETING", "DELETED"
        ],
        "CreationDate": datetime,
        "IsOwned": bool,
    },
    total=False,
)

ListMembersOutputTypeDef = TypedDict(
    "ListMembersOutputTypeDef",
    {"Members": List[MemberSummaryTypeDef], "NextToken": str},
    total=False,
)

ListNetworksOutputTypeDef = TypedDict(
    "ListNetworksOutputTypeDef",
    {"Networks": List[NetworkSummaryTypeDef], "NextToken": str},
    total=False,
)

NodeSummaryTypeDef = TypedDict(
    "NodeSummaryTypeDef",
    {
        "Id": str,
        "Status": Literal[
            "CREATING", "AVAILABLE", "CREATE_FAILED", "UPDATING", "DELETING", "DELETED", "FAILED"
        ],
        "CreationDate": datetime,
        "AvailabilityZone": str,
        "InstanceType": str,
    },
    total=False,
)

ListNodesOutputTypeDef = TypedDict(
    "ListNodesOutputTypeDef", {"Nodes": List[NodeSummaryTypeDef], "NextToken": str}, total=False
)

VoteSummaryTypeDef = TypedDict(
    "VoteSummaryTypeDef",
    {"Vote": Literal["YES", "NO"], "MemberName": str, "MemberId": str},
    total=False,
)

ListProposalVotesOutputTypeDef = TypedDict(
    "ListProposalVotesOutputTypeDef",
    {"ProposalVotes": List[VoteSummaryTypeDef], "NextToken": str},
    total=False,
)

ProposalSummaryTypeDef = TypedDict(
    "ProposalSummaryTypeDef",
    {
        "ProposalId": str,
        "Description": str,
        "ProposedByMemberId": str,
        "ProposedByMemberName": str,
        "Status": Literal["IN_PROGRESS", "APPROVED", "REJECTED", "EXPIRED", "ACTION_FAILED"],
        "CreationDate": datetime,
        "ExpirationDate": datetime,
    },
    total=False,
)

ListProposalsOutputTypeDef = TypedDict(
    "ListProposalsOutputTypeDef",
    {"Proposals": List[ProposalSummaryTypeDef], "NextToken": str},
    total=False,
)

MemberFabricConfigurationTypeDef = TypedDict(
    "MemberFabricConfigurationTypeDef", {"AdminUsername": str, "AdminPassword": str}
)

MemberFrameworkConfigurationTypeDef = TypedDict(
    "MemberFrameworkConfigurationTypeDef", {"Fabric": MemberFabricConfigurationTypeDef}, total=False
)

_RequiredMemberConfigurationTypeDef = TypedDict(
    "_RequiredMemberConfigurationTypeDef",
    {"Name": str, "FrameworkConfiguration": MemberFrameworkConfigurationTypeDef},
)
_OptionalMemberConfigurationTypeDef = TypedDict(
    "_OptionalMemberConfigurationTypeDef",
    {"Description": str, "LogPublishingConfiguration": MemberLogPublishingConfigurationTypeDef},
    total=False,
)


class MemberConfigurationTypeDef(
    _RequiredMemberConfigurationTypeDef, _OptionalMemberConfigurationTypeDef
):
    pass


NetworkFabricConfigurationTypeDef = TypedDict(
    "NetworkFabricConfigurationTypeDef", {"Edition": Literal["STARTER", "STANDARD"]}
)

NetworkFrameworkConfigurationTypeDef = TypedDict(
    "NetworkFrameworkConfigurationTypeDef",
    {"Fabric": NetworkFabricConfigurationTypeDef},
    total=False,
)

_RequiredNodeConfigurationTypeDef = TypedDict(
    "_RequiredNodeConfigurationTypeDef", {"InstanceType": str, "AvailabilityZone": str}
)
_OptionalNodeConfigurationTypeDef = TypedDict(
    "_OptionalNodeConfigurationTypeDef",
    {"LogPublishingConfiguration": NodeLogPublishingConfigurationTypeDef},
    total=False,
)


class NodeConfigurationTypeDef(
    _RequiredNodeConfigurationTypeDef, _OptionalNodeConfigurationTypeDef
):
    pass
