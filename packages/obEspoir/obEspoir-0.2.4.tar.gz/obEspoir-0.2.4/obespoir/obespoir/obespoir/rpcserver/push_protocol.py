# coding=utf-8
"""
author = jamon
"""

import asyncio
import ujson
import struct

from obespoir.base.common_define import ConnectionStatus
from obespoir.base.global_object import GlobalObject
from obespoir.base.ob_protocol import ObProtocol
from obespoir.rpcserver.connection_manager import RpcConnectionManager
from obespoir.rpcserver.route import rpc_message_handle
from obespoir.share.encodeutil import AesEncoder
from obespoir.share.ob_log import logger


class RpcPushProtocol(ObProtocol):

    def __init__(self):
        super().__init__()
        self.host = None
        self.port = None
        self.handfrt = "iii"  # (int, int, int)  -> (message_length, command_id, version)
        self.head_len = struct.calcsize(self.handfrt)
        self.identifier = 0

        self.encode_ins = AesEncoder(GlobalObject().rpc_password, encode_type=GlobalObject().rpc_encode_type)
        self.version = 0

        self._buffer = b""    # 数据缓冲buffer
        self._head = None     # 消息头, list,   [message_length, command_id, version]
        self.transport = None

    async def send_message(self, command_id, message, session_id, to=None):
        logger.debug("rpc push:{}".format([message, type(message)]))
        data = self.pack(message, command_id, session_id, to)
        logger.debug("rpc_push send_message:{}".format([data, type(data)]))
        self.transport.write(data)

    async def message_handle(self, command_id, version, data):
        """
        实际处理消息
        :param command_id:
        :param version:
        :param data:
        :return:
        """
        logger.debug("rpc push receive response message_handle:{}".format([command_id, data]))
        result = await rpc_message_handle(command_id, data)
        logger.debug("rpc result={}".format(result))

    def connection_made(self, transport):
        self.transport = transport
        address = transport.get_extra_info('peername')
        self.host, self.port = address
        RpcConnectionManager().store_connection(*address, self, status=ConnectionStatus.ESTABLISHED)
        logger.debug(
            'connected to {} port {}'.format(*address)
        )

    def data_received(self, data):
        logger.debug('rpc_push received response {}'.format(data))
        super().data_received(data)

    def eof_received(self):
        logger.debug('rpc_push received EOF')
        if self.transport and self.transport.can_write_eof():
            self.transport.write_eof()
        RpcConnectionManager().lost_connection(self.host, self.port)

    def connnection_lost(self, exc):
        logger.debug('server closed connection')
        RpcConnectionManager().lost_connection(self.host, self.port)
        super(RpcPushProtocol, self).connection_lost(exc)


