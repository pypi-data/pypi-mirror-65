#
# All Rights Reserved 2020
#

from strongdoc import client
from strongdoc import constants
from strongdoc.proto import accounts_pb2, strongdoc_pb2_grpc


def login(userid, password, orgid):
    """
    Verify the user and organization identity, and returns a JWT token for future API use.
    There must be a one second difference between logout and login.
    A gRPC connection timeout will be implemented.

    :param userid:
       The login user ID
    :type userid:
        str
    :param password:
       The login user password
    :type password:
        str
    :param orgid:
       The login organization ID
    :type orgid:
        str
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        The JWT token used to authenticate user/org when using StrongDoc APIs.
    :rtype:
        str
    """
    with client.connect_to_server_with_no_auth() as no_auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(no_auth_conn)

        # create login request message
        request = accounts_pb2.LoginReq(userID=userid, password=password, orgID=orgid)

        # make the call
        response = client_stub.Login(request, timeout=constants.GRPC_TIMEOUT)

        return response.token

def logout(token):
    """
    Logs out the user associated with the specified token.

    :param token:
        The user JWT token.
    :type token:
        str

    :returns:
        The logout status of the user.
    :rtype:
        str
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.LogoutReq()

        response = client_stub.Logout(request, timeout=constants.GRPC_TIMEOUT)

        return response.status
