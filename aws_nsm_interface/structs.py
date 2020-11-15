"""Structs for NSM API."""

# Standard library imports
import ctypes

class IoVec(ctypes.Structure):
    """
    IoVec struct for use in the NsmMessage struct.

    The IoVec struct has two fields: iov_base, which is a pointer to a buffer,
    and iov_len, which defines the length of the contents in the buffer.

    The IoVec is used both to send data to /dev/nsm (in which case the length
    of the buffer is defined by the sender) and to receive data from /dev/nsm
    (in which case the length is set by /dev/nsm).
    """

    iov_base: ctypes.c_void_p
    iov_len: ctypes.c_size_t

    _fields_ = [
        ('iov_base', ctypes.c_void_p),
        ('iov_len', ctypes.c_size_t)
    ]

class NsmMessage(ctypes.Structure):
    """
    NsmMessage struct to interface with /dev/nsm.

    The NsmMessage struct has two fields: request, which contains the data
    sent to /dev/nsm, and response, which contains the data returned by /dev/nsm
    after the call has completed.
    """

    request: IoVec
    response: IoVec

    _fields_ = [
        ('request', IoVec),
        ('response', IoVec)
    ]
