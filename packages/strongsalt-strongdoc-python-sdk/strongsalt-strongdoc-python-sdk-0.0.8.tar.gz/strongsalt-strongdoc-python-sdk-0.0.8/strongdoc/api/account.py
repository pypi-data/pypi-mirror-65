#
# All Rights Reserved 2020
#

from strongdoc import client
from strongdoc import constants
from strongdoc.proto import strongdoc_pb2_grpc, accounts_pb2

from datetime import timezone

class AccountInfo:
    """
    Attributes:
        orgid: :class:`str`
        subscription: :class:`Subscription`
        payments: list(:class:`Payment`)
        org_address: :class:`str`
        multilevel_sharing: :class:`bool`
        sharable_orgs: list(:class:`str`)
    """

    def __init__(self, proto_account_info):
        self.orgid = proto_account_info.orgID
        self.subscription = Subscription(proto_account_info.subscription)
        self.payments = [Payment(payment) for payment in proto_account_info.payments]
        self.org_address = proto_account_info.orgAddress
        self.multilevel_sharing = proto_account_info.multiLevelShare
        self.sharable_orgs = [sharable_org for sharable_org in proto_account_info.sharableOrgs]

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()

class UserInfo:
    """
    Attributes:
        userid: :class:`str`
        name: :class:`str`
        email: optional :class:`str`, otherwise :class:`None`
        orgid: optional :class:`str`, otherwise :class:`None`
        is_admin: :class:`bool`
    
    """
    def __init__(self, proto_user):
        self.userid = proto_user.userID
        self.name = proto_user.userName
        try:
            self.email = proto_user.email
        except:
            self.email = None
        try:
            self.orgid = proto_user.orgID
        except:
            self.orgid = None
        self.is_admin = proto_user.isAdmin


    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()

class Subscription:
    """
    Attributes:
        type: :class:`str`
        status: :class:`str`

    """
    def __init__(self, proto_subscription):
        self.type = proto_subscription.type
        self.status = proto_subscription.status

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()

class Payment:
    """
    Attributes:
        billed_at: :class:`datetime.datetime`
        period_start: :class:`datetime.datetime`
        period_end: :class:`datetime.datetime`
        amount: :class:`float`
        status: :class:`str`
    
    """
    def __init__(self, proto_payment):
        self.billed_at = proto_payment.billedAt.ToDatetime().replace(tzinfo=timezone.utc)
        self.period_start = proto_payment.periodStart.ToDatetime().replace(tzinfo=timezone.utc)
        self.period_end = proto_payment.periodEnd.ToDatetime().replace(tzinfo=timezone.utc)
        self.amount = proto_payment.amount
        self.status = proto_payment.status

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()


# _register_organization creates an organization
def _register_organization(org_name, org_addr, admin_name, admin_password, admin_email, source, source_data):
    """
    Registers a new organization. A new administrator user will also be created.
    New users can be added using this administrator account.
    A gRPC connection timeout will be implemented.

    :param org_name:
        The organization name to create.
    :type org_name:
        str
    :param org_addr:
        The organization address.
    :type org_addr:
        str
    :param admin_name:
        The organization administrator name.
    :type admin_name:
        str
    :param admin_password:
        The organization administrator password.
    :type admin_password:
        str
    :param admin_email:
        The organization administrator email.
    :type admin_email:
        str
    :param source:
        The subscription source, such as "AWS Marketplace".
    :type source:
        str
    :param source_data:
        The registration data for the supplied source.
    :type source:
        str
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    Returns
    -------
    orgID : :class:`str`
        The newly created organization ID.
    userID : :class:`str`
        The newly created user ID.
    """
    with client.connect_to_server_with_no_auth() as no_auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(no_auth_conn)

        request = accounts_pb2.RegisterOrganizationReq(orgName=org_name,
                                                           orgAddr=org_addr, userName=admin_name,
                                                           password=admin_password, email=admin_email, 
                                                           source=source, sourceData=source_data)

        response = client_stub.RegisterOrganization(request, timeout=constants.GRPC_TIMEOUT)

        return response.orgID, response.userID


# remove_organization removes an organization
#    :returns bool: Whether the removal was a success
def remove_organization(token, force):
    """
    Removes an organization, deleting all data stored with the organization.
    This requires an administrator privilege.
    A gRPC connection timeout will be implemented.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param force: 
        If this is false, removal will fail if there are still data stored with the organization.
        This prevents accidental deletion.
    :type force: 
        bool
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        Whether the removal was a success.
    :rtype:
        bool
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.RemoveOrganizationReq(force=force)

        response = client_stub.RemoveOrganization(request, timeout=constants.GRPC_TIMEOUT)

        return response.success

# register_user registers a user for the active organization
def register_user(token, name, password, email, make_admin):
    """
    Registers a user for the active organization.
    This requires an administrator privilege.
    A gRPC connection timeout will be implemented.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param name:
        The new user's name.
    :type name:
        str
    :param password:
        The new user's password.
    :type password:
        str
    :param email:
        The new user's email address.
    :type email:
        str
    :param make_admin:
        Whether or not the new user will be an admin.
    :type make_admin:
        bool

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        The userID of the new user.
    :rtype:
        str
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.RegisterUserReq(userName=name, password=password, email=email, admin=make_admin)

        response = client_stub.RegisterUser(request, timeout=constants.GRPC_TIMEOUT)

        return response.userID

# list_users lists the active organization's users
def list_users(token):
    """
    Lists the users of the active organization.

    :param token: 
        The user JWT token.
    :type token:
        str
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        A list of all the users in the organization.
    :rtype:
        list(UserInfo) 
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.ListUsersReq()

        response = client_stub.ListUsers(request, timeout=constants.GRPC_TIMEOUT)

        return [UserInfo(user) for user in response.orgUsers]

# remove_user removes a user from the active organization
def remove_user(token, userid):
    """
    Removes a user from the active organization. Deletes the user if this is the user's only organization.
    This requires an administrator privilege.
    A gRPC connection timeout will be implemented.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param userid:
        The userid of the user to remove.
    :type userid:
        str
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        The number of users removed.
    :rtype:
        int
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.RemoveUserReq(userID=userid)

        response = client_stub.RemoveUser(request, timeout=constants.GRPC_TIMEOUT)

        return response.count

# promote_user makes a user an admin of the active organization
def promote_user(token, userid):
    """
    Promotes a user to admin status.
    This requires an administrator privilege.
    A gRPC connection timeout will be implemented.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param userid:
        The userid of the user to promote.
    :type userid:
        str
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        Whether the promotion was a success.
    :rtype:
        bool
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.PromoteUserReq(userID=userid)

        response = client_stub.PromoteUser(request, timeout=constants.GRPC_TIMEOUT)

        return response.success

# demote_user removes admin privileges from a user
def demote_user(token, userid):
    """
    Removes admin privileges from a user.
    This requires an administrator privilege.
    A gRPC connection timeout will be implemented.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param userid:
        The userid of the user to demote.
    :type userid:
        str
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        Whether the demotion was a success.
    :rtype:
        bool
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.DemoteUserReq(userID=userid)

        response = client_stub.DemoteUser(request, timeout=constants.GRPC_TIMEOUT)

        return response.success

def add_sharable_org(token, orgid):
    """
    Adds another org as a sharable org.
    This requires an administrator privilege.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param orgid:
        The orgid of the org to add as a sharable org.
    :type orgid:
        str

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        Whether the addition was a success.
    :rtype:
        bool
    """

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.AddSharableOrgReq(newOrgID=orgid)

        response = client_stub.AddSharableOrg(request, timeout=constants.GRPC_TIMEOUT)

        return response.success

def remove_sharable_org(token, orgid):
    """
    Removes a sharable org.
    This requires an administrator privilege.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param orgid:
        The orgid of the org to remove as a sharable org.
    :type orgid:
        str

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.
        
    :returns:
        Whether the removal was a success.
    :rtype:
        bool
    """

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.RemoveSharableOrgReq(removeOrgID=orgid)

        response = client_stub.RemoveSharableOrg(request, timeout=constants.GRPC_TIMEOUT)

        return response.success

def set_multilevel_sharing(token, enable):
    """
    Enables or disables multi-level sharing.
    This requires an administrator privilege.

    :param token: 
        The user JWT token.
    :type token:
        str
    :param enable:
        Whether or not multi-level sharing should be enabled.
    :type enable:
        bool

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.
        
    :returns:
        Whether the change was a success.
    :rtype:
        bool
    """

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.SetMultiLevelSharingReq(enable=enable)

        response = client_stub.SetMultiLevelSharing(request, timeout=constants.GRPC_TIMEOUT)

        return response.success

def get_account_info(token):
    """
    Gets account information such as subscription details, payments, sharable orgs, etc.
    This requires an administrator privilege.

    :param token: 
        The user JWT token.
    :type token:
        str

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        The account information
    :rtype:
        AccountInfo
    """

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.GetAccountInfoReq()

        response = client_stub.GetAccountInfo(request, timeout=constants.GRPC_TIMEOUT)

        return AccountInfo(response)

def get_user_info(token):
    """
    Gets information about the active user.

    :param token: 
        The user JWT token.
    :type token:
        str

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        The user information
    :rtype:
        UserInfo
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = accounts_pb2.GetUserInfoReq()

        response = client_stub.GetUserInfo(request, timeout=constants.GRPC_TIMEOUT)

        return UserInfo(response)
