#
# All Rights Reserved 2020
#

from strongdoc import client, constants
from strongdoc.proto import document_pb2, documentNoStore_pb2, strongdoc_pb2_grpc

import io

BLOCK_SIZE = 1024*1024 # 1 MB

class DocumentMetadata:
    """
    Attributes:
        docid: :class:`str`
        doc_name: :class:`str`
        size: :class:`int`

    """
    def __init__(self, _doc):
        self.docid = _doc.docID
        self.doc_name = _doc.docName
        self.size = _doc.size

    def __repr__(self):
        result = "\n".join(["{}: {}".format(key, str(value).replace('\n', '\n{}'.format(' '*(2+len(key))))) for key, value in self.__dict__.items()])
        return result

    def __str__(self):
        return self.__repr__()

def _stream_upload_request_generator(doc_name, plaintext, block_size=BLOCK_SIZE):
    request = document_pb2.UploadDocStreamReq(docName=doc_name)

    yield request

    if isinstance(plaintext, bytes):
        for i in range(0, len(plaintext), block_size):
            block = plaintext[i: i + block_size]
            request = document_pb2.UploadDocStreamReq(plaintext=block)

            yield request
    elif isinstance(plaintext, io.BufferedIOBase) and plaintext.readable():
        block = plaintext.read(block_size)
        while block:
            request = document_pb2.UploadDocStreamReq(plaintext=block)

            yield request

            block = plaintext.read(block_size)
    else:
        raise TypeError("Plaintext is not of type bytes or readable io.BufferedIOBase.")

def _stream_encrypt_request_generator(doc_name, plaintext, block_size=BLOCK_SIZE):
    request = documentNoStore_pb2.EncryptDocStreamReq(docName=doc_name)

    yield request

    if isinstance(plaintext, bytes):
        for i in range(0, len(plaintext), block_size):
            block = plaintext[i: i + block_size]
            request = documentNoStore_pb2.EncryptDocStreamReq(plaintext=block)

            yield request
    elif isinstance(plaintext, io.BufferedIOBase) and plaintext.readable():
        block = plaintext.read(block_size)
        while block:
            request = documentNoStore_pb2.EncryptDocStreamReq(plaintext=block)

            yield request

            block = plaintext.read(block_size)
    else:
        raise TypeError("Plaintext is not of type bytes or readable io.BufferedIOBase.")

def _stream_decrypt_request_generator(docid, ciphertext, block_size=BLOCK_SIZE):
    request = documentNoStore_pb2.DecryptDocStreamReq(docID=docid)

    yield request

    if isinstance(ciphertext, bytes):
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i: i + block_size]
            request = documentNoStore_pb2.DecryptDocStreamReq(ciphertext=block)

            yield request
    elif isinstance(ciphertext, io.BufferedIOBase) and ciphertext.readable():
        block = ciphertext.read(block_size)
        while block:
            request = documentNoStore_pb2.DecryptDocStreamReq(ciphertext=block)

            yield request
            
            block = ciphertext.read(block_size)
    else:
        raise TypeError("Ciphertext is not of type bytes or readable io.BufferedIOBase.")

# list_documents 
def list_documents(token):
    """
    Lists the documents that are accessible to the active user.

    :param token:
        The user JWT token.
    :type token:
        str

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        A list of documents
    :rtype:
        list(DocumentMetadata)
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = document_pb2.ListDocumentsReq()

        response = client_stub.ListDocuments(request, timeout=constants.GRPC_TIMEOUT)

        return [DocumentMetadata(doc) for doc in response.documents]

# upload_document uploads a document to be stored by strongdoc
def upload_document(token, doc_name, plaintext):
    """
    Uploads a document to the service for storage.

    :param token:
        The user JWT token.
    :type token:
        str
    :param doc_name:
        The name of the document.
    :type doc_name:
        str
    :param plaintext:
        The text of the document. 
    :type plaintext:
        bytes or io.BufferedIOBase (must be readable)

    :returns:
        The uploaded document ID.
    :rtype:
        str

    :raises TypeError:
        If `plaintext` is not of type :class:`bytes` or type :class:`io.BufferedIOBase` and readable.
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    """
    if not (isinstance(plaintext, bytes) or (isinstance(plaintext, io.BufferedIOBase) and plaintext.readable())):
        raise TypeError("Plaintext is not of type bytes or readable io.BufferedIOBase.")

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request_iterator = _stream_upload_request_generator(doc_name, plaintext)

        response = client_stub.UploadDocumentStream(request_iterator)

        return response.docID


# download_document downloads a document stored in strongdoc
def download_document(token, docid):
    """
    Download a document from the service.

    :param token:
        The user JWT token.
    :type token:
        str
    :param docid:
        The ID of the document.
    :type docid:
        str

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        The downloaded document.
    :rtype:
        bytes
    """
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = document_pb2.DownloadDocStreamReq(docID=docid)

        plaintext = b""
        response_iterator = client_stub.DownloadDocumentStream(request)

        for res in response_iterator:
            plaintext += res.plaintext

        return plaintext

# download_document_stream downloads a document stored in strongdoc
def download_document_stream(token, docid, output_stream):
    """
    Download a document from the service.

    :param token:
        The user JWT token.
    :type token:
        str
    :param docid:
        The ID of the document.
    :type docid:
        str
    :param output_stream:
        The output stream the document will be written to.
    :type output_stream:
        io.BufferedIOBase (must be writable)

    :rtype:
        None

    :raises TypeError:
        If output_stream is not type :class:`io.BufferedIOBase` and writable.
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    """
    if not isinstance(output_stream, io.BufferedIOBase) or not output_stream.writable():
        raise TypeError("Supplied output stream is not a writable io.BufferedIOBase.")

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = document_pb2.DownloadDocStreamReq(docID=docid)

        response_iterator = client_stub.DownloadDocumentStream(request)

        for res in response_iterator:
            output_stream.write(res.plaintext)

# encrypt_document encrypts a document with strongdoc, but does not store the actual document
def encrypt_document(token, doc_name, plaintext):
    """
    Encrypts a document using the service, but do not store it.
    Instead return the encrypted ciphertext.

    :param token:
        The user JWT token.
    :type token:
        str
    :param doc_name:
        The name of the document.
    :type doc_name:
        str
    :param plaintext:
        The text of the document.
    :type plaintext:
        bytes or io.BufferedIOBase (must be readable)

    :raises TypeError:
        If `plaintext` is not of type :class:`bytes` or type :class:`io.BufferedIOBase` and readable.
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    Returns
    -------
    docID: :class:`str`
        The document ID for the uploaded document.
        This ID is needed to decrypt the document.
    ciphertext: :class:`bytes`
        The encrypted ciphertext of the document.
    """
    if not (isinstance(plaintext, bytes) or (isinstance(plaintext, io.BufferedIOBase) and plaintext.readable())):
        raise TypeError("Plaintext is not of type bytes or readable io.BufferedIOBase.")

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request_iterator = _stream_encrypt_request_generator(doc_name, plaintext)

        response_iterator = client_stub.EncryptDocumentStream(request_iterator)

        res = response_iterator.next()
        docid = res.docID

        ciphertext = b""

        for res in response_iterator:
            ciphertext += res.ciphertext

        return docid, ciphertext

# encrypt_document_stream encrypts a document with strongdoc, but does not store the actual document
def encrypt_document_stream(token, doc_name, plaintext, output_stream):
    """
    Encrypts a document using the service, but do not store it.
    Instead return the encrypted ciphertext.

    :param token:
        The user JWT token.
    :type token:
        str
    :param doc_name:
        The name of the document.
    :type doc_name:
        str
    :param plaintext:
        The text of the document.
    :type plaintext:
        bytes or io.BufferedIOBase (must be readable)
    :param output_stream:
        The output stream the ciphertext will be written to.
    :type output_stream:
        io.BufferedIOBase (must be writable)

    :raises TypeError:
        If `plaintext` is not of type :class:`bytes` or type :class:`io.BufferedIOBase` and readable,
        or output_stream is not type :class:`io.BufferedIOBase` and writable.
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        The document ID for the uploaded document. This ID is needed to decrypt the document.
    :rtype:
        str

    """
    if not (isinstance(plaintext, bytes) or (isinstance(plaintext, io.BufferedIOBase) and plaintext.readable())):
        raise TypeError("Plaintext is not of type bytes or readable io.BufferedIOBase.")
    if not isinstance(output_stream, io.BufferedIOBase) or not output_stream.writable():
        raise TypeError("Supplied output stream is not a writable io.BufferedIOBase.")

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request_iterator = _stream_encrypt_request_generator(doc_name, plaintext)

        response_iterator = client_stub.EncryptDocumentStream(request_iterator)

        res = response_iterator.next()
        docid = res.docID

        for res in response_iterator:
            output_stream.write(res.ciphertext)

        return docid

# decrypt_document encrypts a document with strongdoc. It requires original ciphertext, since the document is not stored
def decrypt_document(token, docid, ciphertext):
    """
    Decrypt a document using the service.
    The user must provide the ciphertext returned during the encryptDocument API call.

    :param token:
        The user JWT token.
    :type token:
        str
    :param docid:
        The ID of the document.
    :type docid:
        str
    :param ciphertext:
        The document ciphertext to be decrypted.
    :type ciphertext:
        bytes or io.BufferedIOBase (must be readable)

    :returns:
        The decrypted plaintext content of the document.
    :rtype:
        bytes

    :raises TypeError:
        If `ciphertext` is not of type :class:`bytes` or type :class:`io.BufferedIOBase` and readable.
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    """
    if not (isinstance(ciphertext, bytes) or (isinstance(ciphertext, io.BufferedIOBase) and ciphertext.readable())):
        raise TypeError("Ciphertext is not of type bytes or readable io.BufferedIOBase.")

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request_iterator = _stream_decrypt_request_generator(docid, ciphertext)

        plaintext = b""
        response_iterator = client_stub.DecryptDocumentStream(request_iterator)

        for res in response_iterator:
            plaintext += res.plaintext

        return plaintext


# decrypt_document_stream encrypts a document with strongdoc. It requires original ciphertext, since the document is not stored
def decrypt_document_stream(token, docid, ciphertext, output_stream):
    """
    Decrypt a document using the service.
    The user must provide the ciphertext returned during the encryptDocument API call.

    :param token:
        The user JWT token.
    :type token:
        str
    :param docid:
        The ID of the document.
    :type docid:
        str
    :param ciphertext:
        The document ciphertext to be decrypted.
    :type ciphertext:
        bytes or io.BufferedIOBase (must be readable)
    :param output_stream:
        The output stream the plaintext will be written to.
    :type output_stream:
        io.BufferedIOBase (must be writable)
    
    :rtype:
        None

    :raises TypeError:
        If `ciphertext` is not of type :class:`bytes` or type :class:`io.BufferedIOBase` and readable,
        or output_stream is not type :class:`io.BufferedIOBase` and writable.
    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.
    """
    if not (isinstance(ciphertext, bytes) or (isinstance(ciphertext, io.BufferedIOBase) and ciphertext.readable())):
        raise TypeError("Ciphertext is not of type bytes or readable io.BufferedIOBase.")
    if not (isinstance(output_stream, io.BufferedIOBase) and output_stream.writable()):
        raise TypeError("Supplied output stream is not a writable io.BufferedIOBase.")

    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request_iterator = _stream_decrypt_request_generator(docid, ciphertext)

        response_iterator = client_stub.DecryptDocumentStream(request_iterator)

        for res in response_iterator:
            output_stream.write(res.plaintext)


# remove_document deletes the document from strongdoc storage
def remove_document(token, docid):
    """
    Remove a document from the service.

    :param token:
        The user JWT token.
    :type token:
        str
    :param docid:
        The ID of the document.
    :type docid:
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

        request = document_pb2.RemoveDocumentReq(docID=docid)

        response = client_stub.RemoveDocument(request, timeout=constants.GRPC_TIMEOUT)
        
        return response.status

# share_document shares a document with a user
def share_document(token, docid, userid):
    """
    Shares a document with another user.

    :param token:
        The user JWT token.
    :type token:
        str
    :param docid:
        The DocID of the document.
    :type docid:
        str
    :param userid:
        The UserID of the user to be shared with.
    :type userid:
        str

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.

    :returns:
        Whether the share was a success.
    :rtype:
        bool
    """
    
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = document_pb2.ShareDocumentReq(docID=docid, userID=userid)

        response = client_stub.ShareDocument(request, timeout=constants.GRPC_TIMEOUT)

        return response.success

# unshare_document unshares a document from a user  
def unshare_document(token, docid, userid):
    """
    Unshares a document from another user.

    :param token:
        The user JWT token.
    :type token:
        str
    :param docid:
        The DocID of the document.
    :type docid:
        str
    :param userid:
        The UserID of the user to be unshared from.
    :type userid:
        str

    :raises grpc.RpcError:
        Raised by the gRPC library to indicate non-OK-status RPC termination.
        
    :returns:
        The number of users unshared with.
    :rtype:
        int
    """
    
    with client.connect_to_server_with_auth(token) as auth_conn:
        client_stub = strongdoc_pb2_grpc.StrongDocServiceStub(auth_conn)

        request = document_pb2.UnshareDocumentReq(docID=docid, userID=userid)

        response = client_stub.UnshareDocument(request, timeout=constants.GRPC_TIMEOUT)

        return response.count
