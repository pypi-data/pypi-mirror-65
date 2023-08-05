"""
Main interface for medialive service client

Usage::

    import boto3
    from mypy_boto3.medialive import MediaLiveClient

    session = boto3.Session()

    client: MediaLiveClient = boto3.client("medialive")
    session_client: MediaLiveClient = session.client("medialive")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, List, TYPE_CHECKING, Type, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_medialive.paginator import (
    DescribeSchedulePaginator,
    ListChannelsPaginator,
    ListInputSecurityGroupsPaginator,
    ListInputsPaginator,
    ListMultiplexProgramsPaginator,
    ListMultiplexesPaginator,
    ListOfferingsPaginator,
    ListReservationsPaginator,
)
from mypy_boto3_medialive.type_defs import (
    BatchScheduleActionCreateRequestTypeDef,
    BatchScheduleActionDeleteRequestTypeDef,
    BatchUpdateScheduleResponseTypeDef,
    CreateChannelResponseTypeDef,
    CreateInputResponseTypeDef,
    CreateInputSecurityGroupResponseTypeDef,
    CreateMultiplexProgramResponseTypeDef,
    CreateMultiplexResponseTypeDef,
    DeleteChannelResponseTypeDef,
    DeleteMultiplexProgramResponseTypeDef,
    DeleteMultiplexResponseTypeDef,
    DeleteReservationResponseTypeDef,
    DescribeChannelResponseTypeDef,
    DescribeInputResponseTypeDef,
    DescribeInputSecurityGroupResponseTypeDef,
    DescribeMultiplexProgramResponseTypeDef,
    DescribeMultiplexResponseTypeDef,
    DescribeOfferingResponseTypeDef,
    DescribeReservationResponseTypeDef,
    DescribeScheduleResponseTypeDef,
    EncoderSettingsTypeDef,
    InputAttachmentTypeDef,
    InputDestinationRequestTypeDef,
    InputSourceRequestTypeDef,
    InputSpecificationTypeDef,
    InputVpcRequestTypeDef,
    InputWhitelistRuleCidrTypeDef,
    ListChannelsResponseTypeDef,
    ListInputSecurityGroupsResponseTypeDef,
    ListInputsResponseTypeDef,
    ListMultiplexProgramsResponseTypeDef,
    ListMultiplexesResponseTypeDef,
    ListOfferingsResponseTypeDef,
    ListReservationsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    MediaConnectFlowRequestTypeDef,
    MultiplexProgramSettingsTypeDef,
    MultiplexSettingsTypeDef,
    OutputDestinationTypeDef,
    PurchaseOfferingResponseTypeDef,
    StartChannelResponseTypeDef,
    StartMultiplexResponseTypeDef,
    StopChannelResponseTypeDef,
    StopMultiplexResponseTypeDef,
    UpdateChannelClassResponseTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateInputResponseTypeDef,
    UpdateInputSecurityGroupResponseTypeDef,
    UpdateMultiplexProgramResponseTypeDef,
    UpdateMultiplexResponseTypeDef,
    UpdateReservationResponseTypeDef,
)
from mypy_boto3_medialive.waiter import (
    ChannelCreatedWaiter,
    ChannelDeletedWaiter,
    ChannelRunningWaiter,
    ChannelStoppedWaiter,
    MultiplexCreatedWaiter,
    MultiplexDeletedWaiter,
    MultiplexRunningWaiter,
    MultiplexStoppedWaiter,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MediaLiveClient",)


class Exceptions:
    BadGatewayException: Type[Boto3ClientError]
    BadRequestException: Type[Boto3ClientError]
    ClientError: Type[Boto3ClientError]
    ConflictException: Type[Boto3ClientError]
    ForbiddenException: Type[Boto3ClientError]
    GatewayTimeoutException: Type[Boto3ClientError]
    InternalServerErrorException: Type[Boto3ClientError]
    NotFoundException: Type[Boto3ClientError]
    TooManyRequestsException: Type[Boto3ClientError]
    UnprocessableEntityException: Type[Boto3ClientError]


class MediaLiveClient:
    """
    [MediaLive.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client)
    """

    exceptions: Exceptions

    def batch_update_schedule(
        self,
        ChannelId: str,
        Creates: BatchScheduleActionCreateRequestTypeDef = None,
        Deletes: BatchScheduleActionDeleteRequestTypeDef = None,
    ) -> BatchUpdateScheduleResponseTypeDef:
        """
        [Client.batch_update_schedule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.batch_update_schedule)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.can_paginate)
        """

    def create_channel(
        self,
        ChannelClass: Literal["STANDARD", "SINGLE_PIPELINE"] = None,
        Destinations: List[OutputDestinationTypeDef] = None,
        EncoderSettings: EncoderSettingsTypeDef = None,
        InputAttachments: List[InputAttachmentTypeDef] = None,
        InputSpecification: InputSpecificationTypeDef = None,
        LogLevel: Literal["ERROR", "WARNING", "INFO", "DEBUG", "DISABLED"] = None,
        Name: str = None,
        RequestId: str = None,
        Reserved: str = None,
        RoleArn: str = None,
        Tags: Dict[str, str] = None,
    ) -> CreateChannelResponseTypeDef:
        """
        [Client.create_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.create_channel)
        """

    def create_input(
        self,
        Destinations: List[InputDestinationRequestTypeDef] = None,
        InputSecurityGroups: List[str] = None,
        MediaConnectFlows: List[MediaConnectFlowRequestTypeDef] = None,
        Name: str = None,
        RequestId: str = None,
        RoleArn: str = None,
        Sources: List[InputSourceRequestTypeDef] = None,
        Tags: Dict[str, str] = None,
        Type: Literal[
            "UDP_PUSH", "RTP_PUSH", "RTMP_PUSH", "RTMP_PULL", "URL_PULL", "MP4_FILE", "MEDIACONNECT"
        ] = None,
        Vpc: InputVpcRequestTypeDef = None,
    ) -> CreateInputResponseTypeDef:
        """
        [Client.create_input documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.create_input)
        """

    def create_input_security_group(
        self,
        Tags: Dict[str, str] = None,
        WhitelistRules: List[InputWhitelistRuleCidrTypeDef] = None,
    ) -> CreateInputSecurityGroupResponseTypeDef:
        """
        [Client.create_input_security_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.create_input_security_group)
        """

    def create_multiplex(
        self,
        AvailabilityZones: List[str],
        MultiplexSettings: MultiplexSettingsTypeDef,
        Name: str,
        RequestId: str,
        Tags: Dict[str, str] = None,
    ) -> CreateMultiplexResponseTypeDef:
        """
        [Client.create_multiplex documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.create_multiplex)
        """

    def create_multiplex_program(
        self,
        MultiplexId: str,
        MultiplexProgramSettings: MultiplexProgramSettingsTypeDef,
        ProgramName: str,
        RequestId: str,
    ) -> CreateMultiplexProgramResponseTypeDef:
        """
        [Client.create_multiplex_program documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.create_multiplex_program)
        """

    def create_tags(self, ResourceArn: str, Tags: Dict[str, str] = None) -> None:
        """
        [Client.create_tags documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.create_tags)
        """

    def delete_channel(self, ChannelId: str) -> DeleteChannelResponseTypeDef:
        """
        [Client.delete_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.delete_channel)
        """

    def delete_input(self, InputId: str) -> Dict[str, Any]:
        """
        [Client.delete_input documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.delete_input)
        """

    def delete_input_security_group(self, InputSecurityGroupId: str) -> Dict[str, Any]:
        """
        [Client.delete_input_security_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.delete_input_security_group)
        """

    def delete_multiplex(self, MultiplexId: str) -> DeleteMultiplexResponseTypeDef:
        """
        [Client.delete_multiplex documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.delete_multiplex)
        """

    def delete_multiplex_program(
        self, MultiplexId: str, ProgramName: str
    ) -> DeleteMultiplexProgramResponseTypeDef:
        """
        [Client.delete_multiplex_program documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.delete_multiplex_program)
        """

    def delete_reservation(self, ReservationId: str) -> DeleteReservationResponseTypeDef:
        """
        [Client.delete_reservation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.delete_reservation)
        """

    def delete_schedule(self, ChannelId: str) -> Dict[str, Any]:
        """
        [Client.delete_schedule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.delete_schedule)
        """

    def delete_tags(self, ResourceArn: str, TagKeys: List[str]) -> None:
        """
        [Client.delete_tags documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.delete_tags)
        """

    def describe_channel(self, ChannelId: str) -> DescribeChannelResponseTypeDef:
        """
        [Client.describe_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.describe_channel)
        """

    def describe_input(self, InputId: str) -> DescribeInputResponseTypeDef:
        """
        [Client.describe_input documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.describe_input)
        """

    def describe_input_security_group(
        self, InputSecurityGroupId: str
    ) -> DescribeInputSecurityGroupResponseTypeDef:
        """
        [Client.describe_input_security_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.describe_input_security_group)
        """

    def describe_multiplex(self, MultiplexId: str) -> DescribeMultiplexResponseTypeDef:
        """
        [Client.describe_multiplex documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.describe_multiplex)
        """

    def describe_multiplex_program(
        self, MultiplexId: str, ProgramName: str
    ) -> DescribeMultiplexProgramResponseTypeDef:
        """
        [Client.describe_multiplex_program documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.describe_multiplex_program)
        """

    def describe_offering(self, OfferingId: str) -> DescribeOfferingResponseTypeDef:
        """
        [Client.describe_offering documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.describe_offering)
        """

    def describe_reservation(self, ReservationId: str) -> DescribeReservationResponseTypeDef:
        """
        [Client.describe_reservation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.describe_reservation)
        """

    def describe_schedule(
        self, ChannelId: str, MaxResults: int = None, NextToken: str = None
    ) -> DescribeScheduleResponseTypeDef:
        """
        [Client.describe_schedule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.describe_schedule)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.generate_presigned_url)
        """

    def list_channels(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListChannelsResponseTypeDef:
        """
        [Client.list_channels documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.list_channels)
        """

    def list_input_security_groups(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListInputSecurityGroupsResponseTypeDef:
        """
        [Client.list_input_security_groups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.list_input_security_groups)
        """

    def list_inputs(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListInputsResponseTypeDef:
        """
        [Client.list_inputs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.list_inputs)
        """

    def list_multiplex_programs(
        self, MultiplexId: str, MaxResults: int = None, NextToken: str = None
    ) -> ListMultiplexProgramsResponseTypeDef:
        """
        [Client.list_multiplex_programs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.list_multiplex_programs)
        """

    def list_multiplexes(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListMultiplexesResponseTypeDef:
        """
        [Client.list_multiplexes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.list_multiplexes)
        """

    def list_offerings(
        self,
        ChannelClass: str = None,
        ChannelConfiguration: str = None,
        Codec: str = None,
        Duration: str = None,
        MaxResults: int = None,
        MaximumBitrate: str = None,
        MaximumFramerate: str = None,
        NextToken: str = None,
        Resolution: str = None,
        ResourceType: str = None,
        SpecialFeature: str = None,
        VideoQuality: str = None,
    ) -> ListOfferingsResponseTypeDef:
        """
        [Client.list_offerings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.list_offerings)
        """

    def list_reservations(
        self,
        ChannelClass: str = None,
        Codec: str = None,
        MaxResults: int = None,
        MaximumBitrate: str = None,
        MaximumFramerate: str = None,
        NextToken: str = None,
        Resolution: str = None,
        ResourceType: str = None,
        SpecialFeature: str = None,
        VideoQuality: str = None,
    ) -> ListReservationsResponseTypeDef:
        """
        [Client.list_reservations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.list_reservations)
        """

    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.list_tags_for_resource)
        """

    def purchase_offering(
        self,
        Count: int,
        OfferingId: str,
        Name: str = None,
        RequestId: str = None,
        Start: str = None,
        Tags: Dict[str, str] = None,
    ) -> PurchaseOfferingResponseTypeDef:
        """
        [Client.purchase_offering documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.purchase_offering)
        """

    def start_channel(self, ChannelId: str) -> StartChannelResponseTypeDef:
        """
        [Client.start_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.start_channel)
        """

    def start_multiplex(self, MultiplexId: str) -> StartMultiplexResponseTypeDef:
        """
        [Client.start_multiplex documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.start_multiplex)
        """

    def stop_channel(self, ChannelId: str) -> StopChannelResponseTypeDef:
        """
        [Client.stop_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.stop_channel)
        """

    def stop_multiplex(self, MultiplexId: str) -> StopMultiplexResponseTypeDef:
        """
        [Client.stop_multiplex documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.stop_multiplex)
        """

    def update_channel(
        self,
        ChannelId: str,
        Destinations: List[OutputDestinationTypeDef] = None,
        EncoderSettings: EncoderSettingsTypeDef = None,
        InputAttachments: List[InputAttachmentTypeDef] = None,
        InputSpecification: InputSpecificationTypeDef = None,
        LogLevel: Literal["ERROR", "WARNING", "INFO", "DEBUG", "DISABLED"] = None,
        Name: str = None,
        RoleArn: str = None,
    ) -> UpdateChannelResponseTypeDef:
        """
        [Client.update_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.update_channel)
        """

    def update_channel_class(
        self,
        ChannelClass: Literal["STANDARD", "SINGLE_PIPELINE"],
        ChannelId: str,
        Destinations: List[OutputDestinationTypeDef] = None,
    ) -> UpdateChannelClassResponseTypeDef:
        """
        [Client.update_channel_class documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.update_channel_class)
        """

    def update_input(
        self,
        InputId: str,
        Destinations: List[InputDestinationRequestTypeDef] = None,
        InputSecurityGroups: List[str] = None,
        MediaConnectFlows: List[MediaConnectFlowRequestTypeDef] = None,
        Name: str = None,
        RoleArn: str = None,
        Sources: List[InputSourceRequestTypeDef] = None,
    ) -> UpdateInputResponseTypeDef:
        """
        [Client.update_input documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.update_input)
        """

    def update_input_security_group(
        self,
        InputSecurityGroupId: str,
        Tags: Dict[str, str] = None,
        WhitelistRules: List[InputWhitelistRuleCidrTypeDef] = None,
    ) -> UpdateInputSecurityGroupResponseTypeDef:
        """
        [Client.update_input_security_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.update_input_security_group)
        """

    def update_multiplex(
        self, MultiplexId: str, MultiplexSettings: MultiplexSettingsTypeDef = None, Name: str = None
    ) -> UpdateMultiplexResponseTypeDef:
        """
        [Client.update_multiplex documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.update_multiplex)
        """

    def update_multiplex_program(
        self,
        MultiplexId: str,
        ProgramName: str,
        MultiplexProgramSettings: MultiplexProgramSettingsTypeDef = None,
    ) -> UpdateMultiplexProgramResponseTypeDef:
        """
        [Client.update_multiplex_program documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.update_multiplex_program)
        """

    def update_reservation(
        self, ReservationId: str, Name: str = None
    ) -> UpdateReservationResponseTypeDef:
        """
        [Client.update_reservation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Client.update_reservation)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_schedule"]
    ) -> DescribeSchedulePaginator:
        """
        [Paginator.DescribeSchedule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Paginator.DescribeSchedule)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        [Paginator.ListChannels documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Paginator.ListChannels)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_input_security_groups"]
    ) -> ListInputSecurityGroupsPaginator:
        """
        [Paginator.ListInputSecurityGroups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Paginator.ListInputSecurityGroups)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_inputs"]) -> ListInputsPaginator:
        """
        [Paginator.ListInputs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Paginator.ListInputs)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multiplex_programs"]
    ) -> ListMultiplexProgramsPaginator:
        """
        [Paginator.ListMultiplexPrograms documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Paginator.ListMultiplexPrograms)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multiplexes"]
    ) -> ListMultiplexesPaginator:
        """
        [Paginator.ListMultiplexes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Paginator.ListMultiplexes)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_offerings"]) -> ListOfferingsPaginator:
        """
        [Paginator.ListOfferings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Paginator.ListOfferings)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reservations"]
    ) -> ListReservationsPaginator:
        """
        [Paginator.ListReservations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Paginator.ListReservations)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_created"]) -> ChannelCreatedWaiter:
        """
        [Waiter.ChannelCreated documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Waiter.ChannelCreated)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_deleted"]) -> ChannelDeletedWaiter:
        """
        [Waiter.ChannelDeleted documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Waiter.ChannelDeleted)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_running"]) -> ChannelRunningWaiter:
        """
        [Waiter.ChannelRunning documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Waiter.ChannelRunning)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_stopped"]) -> ChannelStoppedWaiter:
        """
        [Waiter.ChannelStopped documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Waiter.ChannelStopped)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_created"]) -> MultiplexCreatedWaiter:
        """
        [Waiter.MultiplexCreated documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Waiter.MultiplexCreated)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_deleted"]) -> MultiplexDeletedWaiter:
        """
        [Waiter.MultiplexDeleted documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Waiter.MultiplexDeleted)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_running"]) -> MultiplexRunningWaiter:
        """
        [Waiter.MultiplexRunning documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Waiter.MultiplexRunning)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_stopped"]) -> MultiplexStoppedWaiter:
        """
        [Waiter.MultiplexStopped documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/medialive.html#MediaLive.Waiter.MultiplexStopped)
        """
