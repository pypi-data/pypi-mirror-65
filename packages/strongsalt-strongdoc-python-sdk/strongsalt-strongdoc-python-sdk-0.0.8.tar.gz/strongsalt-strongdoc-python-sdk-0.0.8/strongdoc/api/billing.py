#
# All Rights Reserved 2020
#

from strongdoc import client
from strongdoc import constants
from strongdoc.proto import strongdoc_pb2_grpc, billing_pb2

from google.protobuf.timestamp_pb2 import Timestamp
from grpc._channel import _InactiveRpcError
from grpc import StatusCode

from datetime import timezone
from enum import Enum

#:
FREQ_MONTHLY = 'MONTHLY'
#:
FREQ_YEARLY = 'YEARLY'

_interval_string = ' '.join(billing_pb2.TimeInterval.keys())
_TimeInterval = Enum('TimeInterval', _interval_string, start=0)

class BillingFrequency:
    """
    Attributes:
        frequency: :class:`str` (such as :data:`FREQ_MONTHLY` or :data:`FREQ_YEARLY`)
        valid_from: :class:`datetime.datetime`
        valid_to: :class:`datetime.datetime`
    
    """
    def __init__(self, _freq):
        self.frequency = _TimeInterval(_freq.frequency).name
        self.valid_from = _freq.validFrom.ToDatetime().replace(tzinfo=timezone.utc)
        self.valid_to = _freq.validTo.ToDatetime().replace(tzinfo=timezone.utc)

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()

class DocumentCosts:
    """
    Attributes:
        cost: :class:`float`
        size: :class:`float`
        tier: :class:`str`
    
    """
    def __init__(self, _costs):
        self.cost = _costs.cost
        self.size = _costs.size
        self.tier = _costs.tier

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()

class SearchCosts:
    """
    Attributes:
        cost: :class:`float`
        size: :class:`float`
        tier: :class:`str`
    
    """
    def __init__(self, _costs):
        self.cost = _costs.cost
        self.size = _costs.size
        self.tier = _costs.tier

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()
        
class TrafficCosts:
    """
    Attributes:
        cost: :class:`float`
        incoming: :class:`float` - Traffic sent to us, in MB
        outgoing: :class:`float` - Traffic sent to you, in MB
        tier: :class:`str`
    
    """
    def __init__(self, _costs):
        self.cost = _costs.cost
        self.incoming = _costs.incoming
        self.outgoing = _costs.outgoing
        self.tier = _costs.tier

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()

class BillingDetails:
    """
    Attributes:
        period_start: :class:`datetime.datetime`
        period_end: :class:`datetime.datetime`
        total_cost: :class:`float`
        documents: :class:`DocumentCosts`
        search: :class:`SearchCosts`
        traffic: :class:`TrafficCosts`
        billing_frequency: :class:`BillingFrequency`
    
    """
    def __init__(self, _details):
        self.period_start = _details.periodStart.ToDatetime().replace(tzinfo=timezone.utc)
        self.period_end = _details.periodEnd.ToDatetime().replace(tzinfo=timezone.utc)
        self.total_cost = _details.totalCost
        self.documents = DocumentCosts(_details.documents)
        self.search = SearchCosts(_details.search)
        self.traffic = TrafficCosts(_details.traffic)
        self.billing_frequency = BillingFrequency(_details.billingFrequency)

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()

class LargeTrafficDetails:
    """
    Attributes:
        large_traffic_list: list(:class:`TrafficDetails`)
        period_start: :class:`datetime.datetime` - Start of the billing period
        period_end: :class:`datetime.datetime` - End of the billing period
    """

    def __init__(self, proto_large_traffic):
        self.large_traffic_list = [TrafficDetails(traffic) for traffic in proto_large_traffic.largeTraffic]
        self.period_start = proto_large_traffic.periodStart.ToDatetime().replace(tzinfo=timezone.utc)
        self.period_end = proto_large_traffic.periodEnd.ToDatetime().replace(tzinfo=timezone.utc)

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()

class TrafficDetails:
    """
    Attributes:
        time: :class:`datetime.datetime`
        userid: :class:`str`
        method: :class:`str` - "STREAM" or "UNARY"
        uri: :class:`str` - The operation this traffic corresponds to
        incoming: :class:`float` - Traffic sent to us, in MB
        outgoing: :class:`float` - Traffic sent to you, in MB 
    """

    def __init__(self, proto_traffic):
        self.time = proto_traffic.time.ToDatetime().replace(tzinfo=timezone.utc)
        self.userid = proto_traffic.userID
        self.method = proto_traffic.method
        self.uri = proto_traffic.URI
        self.incoming = proto_traffic.incoming
        self.outgoing = proto_traffic.outgoing

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()

def get_billing_details(token, at_time=None):
    """
    Gets the billing details at a specified time, or the current time if no time is specified.
    This requires an administrator privilege.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param at_time:
        Optional UTC timestamp to check for billing details at. Defaults to current time.
    :type at_time:
        datetime.datetime

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        The requested billing details, or `None` if none are found for the specified time.
    :rtype:
        BillingDetails or None

    :raises ValueError:
        If `at_time` is not a valid datetime.
    """

    if at_time:
        try:
            at_time_proto = Timestamp()
            at_time_proto.FromDatetime(at_time.astimezone(timezone.utc))
        except:
            raise ValueError("Invalid at_time datetime: ", at_time)

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = billing_pb2.GetBillingDetailsReq(at=at_time_proto) if at_time else billing_pb2.GetBillingDetailsReq()

        try:
            response = client_stub.GetBillingDetails(request, timeout=constants.GRPC_TIMEOUT)
        except _InactiveRpcError as err:
            if err.code() == StatusCode.NOT_FOUND:
                return None
            else:
                raise err

        return BillingDetails(response)

def get_billing_frequency_list(token):
    """
    Gets a list of billing frequencies.
    This requires an administrator privilege.

    :param token: 
        The user JWT token.
    :type token:
        str

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        A list of billing frequencies.
    :rtype:
        list(BillingFrequency)
    """

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = billing_pb2.GetBillingFrequencyListReq()

        response = client_stub.GetBillingFrequencyList(request, timeout=constants.GRPC_TIMEOUT)

        return [BillingFrequency(freq) for freq in response.billingFrequencyList]

def set_next_billing_frequency(token, frequency, valid_from):
    """
    Sets a new billing frequency to begin at the specified time.
    This is not allowed if you are subscribed using AWS, and will raise an error.
    This requires an administrator privilege.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param frequency:
        The new billing frequency. Must be a billing constant such as :data:`FREQ_MONTHLY` or :data:`FREQ_YEARLY`.
    :type frequency:
        str
    :param valid_from:
        The time (UTC) the specified billing frequency will be valid from.
        It must be after the start of the current frequency.
        It must be at the beginning of a new billing period based on the current frequency.
        For example, if the current frequency is monthly, it must be at the beginning of a month.
    :type valid_from:
        datetime.datetime

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        The new billing frequency details.
    :rtype:
        BillingFrequency

    :raises ValueError:
        If `frequency` is not a valid billing frequency constant or `valid_from` is not a valid datetime.
    """

    try:
        freq = _TimeInterval[frequency].value
    except KeyError:
        raise ValueError("Invalid frequency: ", frequency)

    try:
        valid_from_proto = Timestamp()
        valid_from_proto.FromDatetime(valid_from.astimezone(timezone.utc))
    except:
        raise ValueError("Invalid valid_from datetime: ", valid_from)

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = billing_pb2.SetNextBillingFrequencyReq(frequency=freq, validFrom=valid_from_proto)

        try:
            response = client_stub.SetNextBillingFrequency(request, timeout=constants.GRPC_TIMEOUT)
        except _InactiveRpcError as err:
            if err.code() == StatusCode.INVALID_ARGUMENT:
                raise ValueError("Argument valid_from must be after the beginning of the current billing period and at the beginning of what would be a new billing period based on the current billing frequency.")
            else:
                raise err

        return BillingFrequency(response.nextBillingFrequency)

def get_large_traffic(token, at_time=None):
    """
    Gets a list of large traffic events (at least 512 MB in one direction) within a specified billing period.
    This requires an administrator privilege.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param at_time:
        Optional UTC timestamp which falls within the desired billing period. Defaults to current time.
    :type at_time:
        datetime.datetime

    :returns:
        The requested large traffic details, or `None` if none are found for the specified time.
    :rtype:
        LargeTrafficDetails or None

    :raises ValueError:
        If `at_time` is not a valid datetime.
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.
    """
    if at_time:
        try:
            at_time_proto = Timestamp()
            at_time_proto.FromDatetime(at_time.astimezone(timezone.utc))
        except:
            raise ValueError("Invalid at_time datetime: ", at_time)

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = billing_pb2.GetLargeTrafficReq(at=at_time_proto) if at_time else billing_pb2.GetLargeTrafficReq()

        try:
            response = client_stub.GetLargeTraffic(request, timeout=constants.GRPC_TIMEOUT)
        except _InactiveRpcError as err:
            if err.code() == StatusCode.NOT_FOUND:
                return None
            else:
                raise err

        return LargeTrafficDetails(response)
