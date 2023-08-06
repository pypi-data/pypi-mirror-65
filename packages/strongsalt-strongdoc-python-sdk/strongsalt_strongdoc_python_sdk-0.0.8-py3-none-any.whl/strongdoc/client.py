#
# All Rights Reserved 2020
#

from os import path
from strongdoc import constants

import grpc


def _open_cert():
    with open(constants.CERT, 'rb') as f:
        return f.read()


def connect_to_server_with_no_auth():
    """
    Creates a secure channel to the StrongDoc Server

    :returns: channel -- A secure gRPC SSL channel.
    """
    trusted_certs = _open_cert()

    # Create the SSL and authorization token credentials
    channel_credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    # Create a secure channel to the server
    channel = grpc.secure_channel('{}:{}'.format(constants.HOST, constants.PORT), channel_credentials)

    return channel


def connect_to_server_with_auth(token):
    """
    Creates a secure channel with an authentication token to the StrongDoc Server

    :param token: The user JWT token
    :type token: str
    :returns: channel -- A secure gRPC SSL channel.
    """
    trusted_certs = _open_cert()

    # Create the SSL and authorization token credentials
    channel_credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    call_credentials = grpc.access_token_call_credentials(token)
    composite_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)

    # Create a secure channel to the server
    channel = grpc.secure_channel('{}:{}'.format(constants.HOST, constants.PORT), composite_credentials)

    return channel
