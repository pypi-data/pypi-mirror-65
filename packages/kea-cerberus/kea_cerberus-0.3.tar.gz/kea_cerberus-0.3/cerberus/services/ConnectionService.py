from flask import Flask
from datetime import datetime
import uuid

from cerberus.entities.entities import KsmConnection, Database
from cerberus.responses.Response import Response
from cerberus.dtos.Connection import Connection
from cerberus.mappers.ConnectionMapper import ConnectionMapper
from cerberus.exceptions.exceptions import InvalidClientConnectionException, ClientConnectionExpiredException

class ConnectionService():

    def removeConnection(token):
        if token is None:
            raise NullClientConnectionException()

        ksmConnection = KsmConnection.query.filter(KsmConnection.id == token).first()
        if ksmConnection is None:
            raise InvalidClientConnectionException()

        ksmConnection.setUpdatedAt(datetime.now())
        ksmConnection.setActive(False)
        Database.update(ksmConnection)
        return ConnectionMapper.mapToConnection(ksmConnection)

    def createConnection(client):
        token = str(uuid.uuid4())
        ksmConnection = KsmConnection(token, True, client.getId(), datetime.now(), datetime.now())
        Database.insert(ksmConnection)
        connection = Connection(ksmConnection.getId(), ksmConnection.getClientId(), ksmConnection.getActive(), ksmConnection.getCreatedAt(), ksmConnection.getUpdatedAt())
        return ConnectionMapper.mapToConnection(ksmConnection)

    def validateConnection(token):

        if token is None:
            raise NullClientConnectionException()

        ksmConnection = KsmConnection.query.filter(KsmConnection.id == token).first()

        if ksmConnection is None:
            raise InvalidClientConnectionException()

        if ksmConnection.getActive() == False:
            raise ClientConnectionExpiredException()

        ksmConnection.setUpdatedAt(datetime.now())
        Database.update(ksmConnection)
        return ConnectionMapper.mapToConnection(ksmConnection)

    def getValidConnection(token):
        if token is None:
            raise NullClientConnectionException()

        ksmConnection = KsmConnection.query.filter(KsmConnection.id == token).first()

        if ksmConnection is None:
            raise InvalidClientConnectionException()

        if ksmConnection.getActive() == False:
            raise ClientConnectionExpiredException()

        ksmConnection.setUpdatedAt(datetime.now())
        Database.update(ksmConnection)
        return ConnectionMapper.mapToConnection(ksmConnection)
