#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from SocketServer import UnixStreamServer
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher, SimpleXMLRPCRequestHandler

from xmlrpclib import Transport, SafeTransport, dumps, _Method
from socket import socket, AF_UNIX, SOCK_STREAM

from httplib import HTTP, HTTPConnection



class UnixStreamXMLRPCServer(UnixStreamServer, SimpleXMLRPCDispatcher):
    def __init__(self, addr, requestHandler=SimpleXMLRPCRequestHandler):
        self.logRequests = False # critical, as logging fails with UnixStreamServer
        SimpleXMLRPCDispatcher.__init__(self)
        UnixStreamServer.__init__(self, addr, requestHandler)



class UnixStreamHTTPConnection(HTTPConnection):

    def connect(self):
        self.sock = socket(AF_UNIX, SOCK_STREAM)
        self.sock.connect(self.host)



class UnixStreamHTTP(HTTP):
    _connection_class = UnixStreamHTTPConnection


class UnixStreamTransport(Transport):

    def make_connection(self, host):
        return UnixStreamHTTP(host)



class UnixSocketServerProxy:

    def __init__(self, uri, transport=UnixStreamTransport, encoding=None, verbose=0,
                 allow_none=0, use_datetime=0):
        # establish a "logical" server connection

        # get the url
        import urllib
        type, uri = urllib.splittype(uri)
        if type != "unix":
            raise IOError, "unsupported XML-RPC protocol"
        self.__host, self.__handler = (uri, '/RPC2')

        self.__transport = transport

        self.__encoding = encoding
        self.__verbose = verbose
        self.__allow_none = allow_none

    def __request(self, methodname, params):
        # call a method on the remote server

        request = dumps(params, methodname, encoding=self.__encoding,
                        allow_none=self.__allow_none)

        response = self.__transport.request(
            self.__host,
            self.__handler,
            request,
            verbose=self.__verbose
            )

        if len(response) == 1:
            response = response[0]

        return response

    def __repr__(self):
        return (
            "<ServerProxy for %s%s>" %
            (self.__host, self.__handler)
            )

    __str__ = __repr__

    def __getattr__(self, name):
        # magic method dispatcher
        return _Method(self.__request, name)



