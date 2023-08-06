#
# All Rights Reserved 2020
#

from typing import List

from strongdoc import client
from strongdoc import constants
from strongdoc.proto import search_pb2, strongdoc_pb2_grpc


def search(token, query):
    """
    Search for document that contains a specific word.
    A gRPC connection timeout will be implemented.
    
    :param token:
        The user JWT token.
    :type token:
        str
    :param query:
        The query string.
    :type query:
        str
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        The hit list of the search.
    :rtype:
        list(DocumentResult)
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = search_pb2.SearchReq(query=query)

        response = client_stub.Search(request, timeout=constants.GRPC_TIMEOUT)

        hits: List[DocumentResult] = []
        for hit_result in response.hits:
            hits.append(DocumentResult(hit_result.docID, hit_result.score))

        return hits


class DocumentResult:
    """
    A class that will hold a single document that matches the search result from the Search query.

    Attributes:
        docid: :class:`str` - The matching document ID.
        score: :class:`float` - The score of the matching document.
    """

    def __init__(self, docid, score):
        """
        Constructs a document that matches the search result

        :param docid:
            The matching document ID
        :type docid:
            `str`
        :param score:
            The score of the matching document
        :type score:
            `float`
        """
        self.docid = docid
        self.score = score

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()
