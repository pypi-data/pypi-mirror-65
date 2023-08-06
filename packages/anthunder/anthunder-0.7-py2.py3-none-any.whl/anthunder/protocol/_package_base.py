# coding=utf-8
"""
    Copyright (c) 2018-present, Ant Financial Service Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
   ------------------------------------------------------
   File Name : bolt_request
   Author : jiaqi.hjq
   Create Time : 2018/4/28 11:38
   Description : description what the main function of this file
   Change Activity:
        version0 : 2018/4/28 11:38 by jiaqi.hjq  init
"""
import struct

from .exceptions import DecodeError, ParamTypeError
from ._sofa_header import SofaHeader
from .constants import PROTO, VER2, CODEC, PTYPE, CMDCODE, RESPSTATUS


class BoltPackage(object):
    fmt = ""
    class_name = b""
    bolt_headers = ()

    def __init__(self, header, content,
                 proto=PROTO.BOLT, ptype=None, cmdcode=None, ver2=VER2.REMOTING, request_id=None,
                 codec=CODEC.PROTOBUF, timeout=None, respstatus=0, **kwargs):
        """
        See init's docstring for definition of params
        :param class_name:
        :param header:
        :type header: SofaHeader
        :param content:
        :type content: bytes
        :param proto:
        :param ptype:
        :param cmdcode:
        :param ver2:
        :param request_id:
        :type request_id: int
        :param codec:
        :param timeout: optional, only in request pkg, milliseconds
        :type timeout: int
        :param respstatus: optional, only in response pkg
        :type respstatus: int
        """
        self.header = header
        self._header_bytes = header.to_bytes()
        self.content = content

        self.proto = PROTO(proto)
        self.ptype = PTYPE(ptype)
        self.cmdcode = CMDCODE(cmdcode)
        self.ver2 = VER2(ver2)
        self.request_id = request_id
        self.codec = CODEC(codec)
        self.timeout = timeout or 0
        self.respstatus = RESPSTATUS(respstatus)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, ",".join(map("{0[0]}={0[1]}".format, self.__dict__.items())))

    __str__ = __repr__

    @property
    def class_len(self):
        return len(self.class_name)

    @property
    def header_len(self):
        return len(self._header_bytes)

    @property
    def content_len(self):
        return len(self.content)

    @property
    def body_len(self):
        """total length of classname + header + content"""
        return self.class_len + self.header_len + self.content_len

    def validate(self):
        def _check(obj, need_type):
            if not isinstance(obj, need_type):
                raise ParamTypeError("TypeError: must be {}, not {}".format(need_type.__name__, type(obj)))

        _check(self.proto, PROTO)
        _check(self.ptype, PTYPE)
        _check(self.cmdcode, CMDCODE)
        _check(self.ver2, VER2)
        _check(self.request_id, int)
        _check(self.codec, CODEC)
        _check(self.class_name, bytes)
        _check(self.header, SofaHeader)
        _check(self.content, bytes)

    def to_stream(self):  # pragma: no cover
        raise NotImplementedError

    @classmethod
    def bolt_content_from_stream(cls, stream, bolt_headers):
        try:
            bodyfmt = "%ds%ds%ds" % (bolt_headers['class_len'], bolt_headers['header_len'], bolt_headers['content_len'])
            class_name, header, content = struct.unpack(bodyfmt, stream)

            return cls(SofaHeader.from_bytes(header), content, **bolt_headers)
        except Exception as e:  # pragma: no cover
            raise DecodeError(e)

    @classmethod
    def bolt_header_from_stream(cls, stream):
        try:
            values = struct.unpack(cls.fmt, stream[:cls.bolt_header_size()])
            return dict(zip(cls.bolt_headers, values))

        except Exception as e:  # pragma: no cover
            raise DecodeError(e)

    @classmethod
    def from_stream(cls, stream):
        bh = cls.bolt_header_from_stream(stream)
        return cls.bolt_content_from_stream(stream[cls.bolt_header_size():], bh)

    @classmethod
    def bolt_header_size(cls):
        return struct.calcsize(cls.fmt)
