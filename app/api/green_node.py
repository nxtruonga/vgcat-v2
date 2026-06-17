import logging
from collections.abc import Iterable
from typing import List

import requests
from connectrpc.code import Code
from connectrpc.errors import ConnectError
from pydantic import BaseModel, ValidationError
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from proto.agen.zservice.zservice_pb2 import GetIfmReq

logger = logging.getLogger(__name__)


class GnResponse(BaseModel):
    id: str
    role: str | None
    type: str | None
    model: str | None
    content: list[GnRespContentItem]


class GnRespContentItem(BaseModel):
    text: str
    type: str | None


class GnReqPayload(BaseModel):
    model: str = "google/gemma-4-31b-it"
    messages: List[GnReqMessage]
    max_tokens: int = 2000


class GnReqMessage(BaseModel):
    role: str
    content: str


def connErr_internal(msg):
    return ConnectError(Code.INTERNAL, msg)


def call_green_node(reqMsgList: Iterable[GetIfmReq.MsgItem]) -> GnResponse:
    try:
        resp = requests.post(
            "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1/messages",
            headers=createHeaders_Authorization_cgn(),
            json=createPayload_cgn(reqMsgList),
            timeout=30,  # seconds
        )
        resp.raise_for_status()
    except Timeout as e:
        raise ConnectError(Code.DEADLINE_EXCEEDED, f"failed to Timeout: {e}")
    except ConnectionError as e:
        raise ConnectError(Code.UNAVAILABLE, f"failed to ConnectionError: {e}")
    except HTTPError as e:
        raise ConnectError(Code.INTERNAL, f"failed to HTTPError: {e}")
    except RequestException as e:
        raise ConnectError(Code.INTERNAL, f"failed to RequestException: {e}")
    try:
        logger.info(f"resp.text={resp.text[:20]}")
        return GnResponse.model_validate(resp.json())
    except ValidationError as e:
        raise ConnectError(Code.INTERNAL, f"failed to model_validate: {e}")


def createHeaders_Authorization_cgn():
    return {"Authorization": "Bearer SECRET_API_KEY"}


def createPayload_cgn(reqMsgList: Iterable[GetIfmReq.MsgItem]):
    reqMsg_1 = list(reqMsgList)[1]
    messages = [
        GnReqMessage(
            role="assistant",
            content="You are an AI assistant tasked with providing information to users.",
        ),
        GnReqMessage(role=reqMsg_1.role, content=reqMsg_1.content),
    ]
    return GnReqPayload(messages=messages).model_dump()
