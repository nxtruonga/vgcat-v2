from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetIfmReq(_message.Message):
    __slots__ = ("messages",)
    class MsgItem(_message.Message):
        __slots__ = ("role", "content")
        ROLE_FIELD_NUMBER: _ClassVar[int]
        CONTENT_FIELD_NUMBER: _ClassVar[int]
        role: str
        content: str
        def __init__(self, role: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[GetIfmReq.MsgItem]
    def __init__(self, messages: _Optional[_Iterable[_Union[GetIfmReq.MsgItem, _Mapping]]] = ...) -> None: ...

class GetIfmResp(_message.Message):
    __slots__ = ("id", "role", "type", "model", "messages")
    class MsgItem(_message.Message):
        __slots__ = ("type", "text")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        TEXT_FIELD_NUMBER: _ClassVar[int]
        type: str
        text: str
        def __init__(self, type: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    id: str
    role: str
    type: str
    model: str
    messages: _containers.RepeatedCompositeFieldContainer[GetIfmResp.MsgItem]
    def __init__(self, id: _Optional[str] = ..., role: _Optional[str] = ..., type: _Optional[str] = ..., model: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[GetIfmResp.MsgItem, _Mapping]]] = ...) -> None: ...
