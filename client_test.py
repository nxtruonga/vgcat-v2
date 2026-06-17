import asyncio

from proto.agen.zservice.zservice_connect import SoServiceClient
from proto.agen.zservice.zservice_pb2 import GetIfmReq


# https://connectrpc.com/docs/python/getting-started/
async def main():
    client = SoServiceClient("http://localhost:8000")
    res = await client.get_ifm(GetIfmReq(messages=None))
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
