from os import path

"""
Location of StrongDoc Service
"""
HOST = 'api.strongsalt.com'
PORT = 9090
CERT = path.join(path.dirname(__file__), "data", "certs", "grpc.root.pem")

"""
Timeout value for the gRPC connection
"""
GRPC_TIMEOUT = 60
