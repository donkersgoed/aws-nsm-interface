"""Main NSM interface module."""

# Standard library imports
import ctypes
import fcntl
import typing

# Related third party imports
import cbor2
from ioctl_opt import IOC, IOC_READ, IOC_WRITE

# Project imports
from .structs import *
from .exceptions import IoctlError

NSM_DEV_FILE = '/dev/nsm'
NSM_IOCTL_MAGIC = 0x0A
NSM_IOCTL_NUMBER = 0x00
NSM_REQUEST_MAX_SIZE = 0x1000
NSM_RESPONSE_MAX_SIZE = 0x3000

def open_nsm_device() -> typing.TextIO:
    """Open the /dev/nsm file and return the file handle."""
    return open(NSM_DEV_FILE, 'r')

def close_nsm_device(file_handle: typing.TextIO) -> None:
    """Close the /dev/nsm file."""
    file_handle.close()

def lock_pcr(file_handle: typing.TextIO, index: int) -> bool:
    """Lock PCR at index."""
    nsm_key = 'LockPCR'
    request_data = cbor2.dumps({nsm_key: {'index': index}})

    # Prepare the request and response buffers. The request buffer is the
    # size of the request data, the response buffer is sized at NSM_RESPONSE_MAX_SIZE.
    # This code is repeated for every type of request, because moving it to a separate
    # function creates garbage collection issues.
    request_buffer = ctypes.create_string_buffer(request_data, len(request_data))
    response_buffer = (NSM_RESPONSE_MAX_SIZE * ctypes.c_uint8)()

    # Prepare a new NsmMessage struct.
    nsm_message = NsmMessage()
    # Create new IoVecs pointing to the request and response buffer.
    _prepare_nsm_message_iovecs(nsm_message, request_buffer, response_buffer)

    # Send the message to /dev/nsm through an ioctl call.
    # When the call is complete, the response_buffer will
    # be filled with response data.
    _execute_ioctl(file_handle, nsm_message)

    # Take the CBOR response and translate it to a Python dict. Return the values
    # for this request's key.
    decoded_response = _decode_response(nsm_message)
    if isinstance(decoded_response, dict) and 'Error' in decoded_response:
        raise IoctlError(decoded_response.get('Error'))
    return True

def lock_pcrs(file_handle: typing.TextIO, lock_range: int) -> bool:
    """Lock PCRs in range(0, lock_range)."""
    nsm_key = 'LockPCRs'
    request_data = cbor2.dumps({nsm_key: {'range': lock_range}})

    # Prepare the request and response buffers. The request buffer is the
    # size of the request data, the response buffer is sized at NSM_RESPONSE_MAX_SIZE.
    # This code is repeated for every type of request, because moving it to a separate
    # function creates garbage collection issues.
    request_buffer = ctypes.create_string_buffer(request_data, len(request_data))
    response_buffer = (NSM_RESPONSE_MAX_SIZE * ctypes.c_uint8)()

    # Prepare a new NsmMessage struct.
    nsm_message = NsmMessage()
    # Create new IoVecs pointing to the request and response buffer.
    _prepare_nsm_message_iovecs(nsm_message, request_buffer, response_buffer)

    # Send the message to /dev/nsm through an ioctl call.
    # When the call is complete, the response_buffer will
    # be filled with response data.
    _execute_ioctl(file_handle, nsm_message)

    # Take the CBOR response and translate it to a Python dict. Return the values
    # for this request's key.
    decoded_response = _decode_response(nsm_message)
    if isinstance(decoded_response, dict) and 'Error' in decoded_response:
        raise IoctlError(decoded_response.get('Error'))
    return True

def describe_pcr(file_handle: typing.TextIO, index: int) -> dict:
    """Request PCR description from /dev/nsm."""
    nsm_key = 'DescribePCR'
    request_data = cbor2.dumps({nsm_key: {'index': index}})

    # Prepare the request and response buffers. The request buffer is the
    # size of the request data, the response buffer is sized at NSM_RESPONSE_MAX_SIZE.
    # This code is repeated for every type of request, because moving it to a separate
    # function creates garbage collection issues.
    request_buffer = ctypes.create_string_buffer(request_data, len(request_data))
    response_buffer = (NSM_RESPONSE_MAX_SIZE * ctypes.c_uint8)()

    # Prepare a new NsmMessage struct.
    nsm_message = NsmMessage()
    # Create new IoVecs pointing to the request and response buffer.
    _prepare_nsm_message_iovecs(nsm_message, request_buffer, response_buffer)

    # Send the message to /dev/nsm through an ioctl call.
    # When the call is complete, the response_buffer will
    # be filled with response data.
    _execute_ioctl(file_handle, nsm_message)

    # Take the CBOR response and translate it to a Python dict. Return the values
    # for this request's key.
    decoded_response = _decode_response(nsm_message)
    if nsm_key not in decoded_response:
        raise IoctlError(decoded_response.get('Error'))
    return decoded_response.get(nsm_key)

def get_attestation_doc(
    file_handle: typing.TextIO,
    user_data: bytes = None,
    nonce: bytes = None,
    public_key: bytes = None
) -> dict:
    """Request Attestation document from /dev/nsm."""
    nsm_key = 'Attestation'
    request_data = cbor2.dumps({nsm_key: {
        'user_data': user_data,
        'nonce': nonce,
        'public_key': public_key,
    }})

    # Prepare the request and response buffers. The request buffer is the
    # size of the request data, the response buffer is sized at NSM_RESPONSE_MAX_SIZE.
    # This code is repeated for every type of request, because moving it to a separate
    # function creates garbage collection issues.
    request_buffer = ctypes.create_string_buffer(request_data, len(request_data))
    response_buffer = (NSM_RESPONSE_MAX_SIZE * ctypes.c_uint8)()

    # Prepare a new NsmMessage struct.
    nsm_message = NsmMessage()
    # Create new IoVecs pointing to the request and response buffer.
    _prepare_nsm_message_iovecs(nsm_message, request_buffer, response_buffer)

    # Send the message to /dev/nsm through an ioctl call.
    # When the call is complete, the response_buffer will
    # be filled with response data.
    _execute_ioctl(file_handle, nsm_message)

    # Take the CBOR response and translate it to a Python dict. Return the values
    # for this request's key.
    decoded_response = _decode_response(nsm_message)
    if nsm_key not in decoded_response:
        raise IoctlError(decoded_response.get('Error'))
    return decoded_response.get(nsm_key)

def extend_pcr(file_handle: typing.TextIO, index: int, data: bytes) -> dict:
    """Extend the PCR at the given index."""
    nsm_key = 'ExtendPCR'
    request_data = cbor2.dumps({nsm_key: {'index': index, 'data': data}})

    # Prepare the request and response buffers. The request buffer is the
    # size of the request data, the response buffer is sized at NSM_RESPONSE_MAX_SIZE.
    # This code is repeated for every type of request, because moving it to a separate
    # function creates garbage collection issues.
    request_buffer = ctypes.create_string_buffer(request_data, len(request_data))
    response_buffer = (NSM_RESPONSE_MAX_SIZE * ctypes.c_uint8)()

    # Prepare a new NsmMessage struct.
    nsm_message = NsmMessage()
    # Create new IoVecs pointing to the request and response buffer.
    _prepare_nsm_message_iovecs(nsm_message, request_buffer, response_buffer)

    # Send the message to /dev/nsm through an ioctl call.
    # When the call is complete, the response_buffer will
    # be filled with response data.
    _execute_ioctl(file_handle, nsm_message)

    # Take the CBOR response and translate it to a Python dict. Return the values
    # for this request's key.
    decoded_response = _decode_response(nsm_message)
    if nsm_key not in decoded_response:
        raise IoctlError(decoded_response.get('Error'))
    return decoded_response.get(nsm_key)

def describe_nsm(file_handle: typing.TextIO) -> dict:
    """Request NSM description from /dev/nsm."""
    nsm_key = 'DescribeNSM'
    request_data = cbor2.dumps(nsm_key)

    # Prepare the request and response buffers. The request buffer is the
    # size of the request data, the response buffer is sized at NSM_RESPONSE_MAX_SIZE.
    # This code is repeated for every type of request, because moving it to a separate
    # function creates garbage collection issues.
    request_buffer = ctypes.create_string_buffer(request_data, len(request_data))
    response_buffer = (NSM_RESPONSE_MAX_SIZE * ctypes.c_uint8)()

    # Prepare a new NsmMessage struct.
    nsm_message = NsmMessage()
    # Create new IoVecs pointing to the request and response buffer.
    _prepare_nsm_message_iovecs(nsm_message, request_buffer, response_buffer)

    # Send the message to /dev/nsm through an ioctl call.
    # When the call is complete, the response_buffer will
    # be filled with response data.
    _execute_ioctl(file_handle, nsm_message)

    # Take the CBOR response and translate it to a Python dict. Return the values
    # for this request's key.
    decoded_response = _decode_response(nsm_message)
    if nsm_key not in decoded_response:
        raise IoctlError(decoded_response.get('Error'))
    return decoded_response.get(nsm_key)

def get_random(file_handle: typing.TextIO, length: int = 32) -> bytes:
    """Request random bytes from /dev/nsm."""
    if length < 1 or length > 256:
        raise ValueError('GetRandom supports length between 1 and 256 inclusive.')

    nsm_key = 'GetRandom'
    request_data = cbor2.dumps(nsm_key)

    # Prepare the request and response buffers. The request buffer is the
    # size of the request data, the response buffer is sized at NSM_RESPONSE_MAX_SIZE.
    # This code is repeated for every type of request, because moving it to a separate
    # function creates garbage collection issues.
    request_buffer = ctypes.create_string_buffer(request_data, len(request_data))
    response_buffer = (NSM_RESPONSE_MAX_SIZE * ctypes.c_uint8)()

    # Prepare a new NsmMessage struct.
    nsm_message = NsmMessage()
    # Create new IoVecs pointing to the request and response buffer.
    _prepare_nsm_message_iovecs(nsm_message, request_buffer, response_buffer)

    # Send the message to /dev/nsm through an ioctl call.
    # When the call is complete, the response_buffer will
    # be filled with response data.
    _execute_ioctl(file_handle, nsm_message)

    # Read the binary reponse from NSM, fetch the bytes stored under the key 'random'
    # and return them to the user.
    decoded_response = _decode_response(nsm_message)
    random_bytes = decoded_response.get(nsm_key).get('random')
    if nsm_key not in decoded_response:
        raise IoctlError(decoded_response.get('Error'))
    return random_bytes[:length]

def _decode_response(nsm_message: NsmMessage) -> dict:
    """Read the binary reponse from NSM and return it as a Python dict."""
    # Create a buffer with a size as defined in the IoVec.iov_len field.
    cbor_data = bytearray(nsm_message.response.iov_len)

    # Create a pointer to this buffer.
    cbor_data_pointer = (ctypes.c_char * nsm_message.response.iov_len).from_buffer(cbor_data)

    # Copy the data referenced to by the IoVec into this buffer.
    ctypes.memmove(
        cbor_data_pointer,
        nsm_message.response.iov_base,
        nsm_message.response.iov_len
    )

    # Decode the CBOR and return it.
    return cbor2.loads(cbor_data)

def _execute_ioctl(file_handle: typing.TextIO, nsm_message: NsmMessage) -> None:
    """Send an NsmMessage to /dev/nsm trough ioctl."""
    # Calculate the IOWR operation. Should always result in 3223325184.
    operation = IOC(
        IOC_READ|IOC_WRITE,
        NSM_IOCTL_MAGIC,
        NSM_IOCTL_NUMBER,
        ctypes.sizeof(NsmMessage)
    )
    # Execute the ioctl call.
    fcntl.ioctl(file_handle, operation, nsm_message)

def _prepare_nsm_message_iovecs(
    nsm_message: NsmMessage,
    request_buffer: bytes,
    response_buffer: bytes,
) -> None:
    """Generate the request and response IoVecs for an NsmMessage."""
    if len(request_buffer) > NSM_REQUEST_MAX_SIZE:
        raise ValueError('Request too large.')

    # Create a pointer to the request buffer.
    request_buffer_pointer = ctypes.cast(
        ctypes.byref(request_buffer),
        ctypes.c_void_p
    )

    # Create a pointer to the response buffer.
    response_buffer_pointer = ctypes.cast(
        ctypes.byref(response_buffer),
        ctypes.c_void_p
    )

    # Create a new IoVec pointing to the request buffer. Assign the
    # IoVec to the request field of the NsmMessage.
    nsm_message.request = IoVec(
        request_buffer_pointer,
        len(request_buffer)
    )

    # Create a new IoVec pointing to the response buffer. Assign the
    # IoVec to the response field of the NsmMessage.
    nsm_message.response = IoVec(
        response_buffer_pointer,
        len(response_buffer)
    )
