from __future__ import annotations

import logging
from typing import TYPE_CHECKING, TypeVar, cast

from connectrpc.code import Code
from connectrpc.codec import Codec, proto_binary_codec
from connectrpc.errors import ConnectError
from connectrpc.request import RequestContext
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse as MessageFromJson
from google.protobuf.message import Message
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from app.api.green_node import call_green_node
from proto.agen.zservice.zservice_connect import SoService, SoServiceASGIApplication
from proto.agen.zservice.zservice_pb2 import GetIfmReq, GetIfmResp

if TYPE_CHECKING:
    from connectrpc.request import RequestContext
    from starlette.types import ASGIApp

V = TypeVar("V", bound=Message)
logger = logging.getLogger(__name__)


class CustomProtoJSONCodec(Codec[Message, V]):
    """Codec for the Protocol Buffers JSON format."""

    def __init__(self, name: str = "json") -> None:
        self._name = name

    def name(self) -> str:
        return self._name

    def encode(self, message: Message) -> bytes:
        return MessageToJson(message, preserving_proto_field_name=True).encode()

    def decode(self, data: bytes | bytearray, message: V) -> V:
        # google.protobuf.json_format.Parse accepts the buffer protocol at
        # runtime, but typeshed declares only `bytes | str`. See
        # ProtoBinaryCodec.decode for the upstream tracking issue.
        MessageFromJson(data, message)  # ty: ignore[invalid-argument-type]
        return message


class SoServiceImpl(SoService):
    async def get_ifm(
        self,
        request: GetIfmReq,
        ctx: RequestContext[GetIfmReq, GetIfmResp],
    ) -> GetIfmResp:
        try:
            gnResp = call_green_node(request.messages)
        except ConnectError as e:
            logger.error(f"failed to ConnectError: {e}")
            raise e
        if not gnResp.content:
            raise ConnectError(Code.INTERNAL, "failed to check content_NOT")
        out = GetIfmResp(
            id=gnResp.id,
            role=gnResp.role,
            type=gnResp.type,
            model=gnResp.model,
            messages=[
                GetIfmResp.MsgItem(text=i.text, type=i.type) for i in gnResp.content
            ],
        )
        # ctx.response_headers()["Access-Control-Allow-Origin"] = "*"
        return out

    def connErr_invalidArg(self, msg):
        return ConnectError(Code.INVALID_ARGUMENT, msg)


application = SoServiceASGIApplication(
    SoServiceImpl(), codecs=[proto_binary_codec(), CustomProtoJSONCodec()]
)

# https://github.com/connectrpc/connect-python/blob/main/example/example/eliza_service.py
app = Starlette(
    routes=[
        Route("/health", lambda _: JSONResponse({"status": "ok"})),
        Mount(application.path, cast("ASGIApp", application)),
    ]
)

# https://github.com/connectrpc/connect-python
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[
    #     "http://localhost:3000",
    #     "https://endpoint-*.agentbase-runtime.aiplatform.vngcloud.vn",
    # ],
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
