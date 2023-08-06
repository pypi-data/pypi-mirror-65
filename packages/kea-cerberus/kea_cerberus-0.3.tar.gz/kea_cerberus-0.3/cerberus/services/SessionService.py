from flask import Flask
import uuid

from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from cerberus.entities.entities import KsmConnection, KsmSession, KsmUserAuthenticationType, Database
from cerberus.dtos.AuthenticationType import AuthenticationType
from cerberus.mappers.SessionMapper import SessionMapper
from cerberus.exceptions.exceptions import InvalidUserSessionException, InvalidUserCredentialsException, NotFoundUserException
from cerberus.services.SecurityHashService import SecurityHashService
from cerberus.services.FirebaseService import FirebaseService

class SessionService():

    def createSessionByLocalAuth(connection, username, password):

        if username is None:
            raise InvalidUserCredentialsException()

        if password is None:
            raise InvalidUserCredentialsException()

        kuat = KsmUserAuthenticationType.query.filter(KsmUserAuthenticationType.username == username).filter(KsmUserAuthenticationType.authentication_type_id == AuthenticationType.LOCAL).first()

        if kuat is None:
            raise NotFoundUserException()


        if not check_password_hash(kuat.getToken(), kuat.getUserId() + password):
            raise InvalidUserCredentialsException()

        return SessionService.createSession(connection, kuat)

    def createSessionByGoogleAuth(connection, uid, tokenId):

        if uid is None:
            raise InvalidUserCredentialsException()

        if tokenId is None:
            raise InvalidUserCredentialsException()

        decoded_token = FirebaseService().getDecoded_token(tokenId)

        res_uid = decoded_token['uid']
        if res_uid != uid:
            raise InvalidUserCredentialsException()

        kuat = KsmUserAuthenticationType.query.filter(KsmUserAuthenticationType.username == uid).filter(KsmUserAuthenticationType.authentication_type_id == AuthenticationType.GOOGLE).first()
        if kuat is None:
            user_email = decoded_token['email']
            kuat = KsmUserAuthenticationType.query.filter(KsmUserAuthenticationType.username == user_email).first()
            if kuat is None:
                raise InvalidUserCredentialsException()
            else:
                createdAt = datetime.now()
                ksmUserAuthenticationType = KsmUserAuthenticationType()
                ksmUserAuthenticationType.setAuthenticationTypeId(AuthenticationType.GOOGLE)
                ksmUserAuthenticationType.setUserId(kuat.getUserId())
                ksmUserAuthenticationType.setUserName(uid)
                ksmUserAuthenticationType.setCreatedAt(createdAt)
                ksmUserAuthenticationType.setUpdatedAt(createdAt)
                ksmUserAuthenticationType.setToken(uid)
                Database.insert(ksmUserAuthenticationType)
                return SessionService.createSession(connection, ksmUserAuthenticationType)

        return SessionService.createSession(connection, kuat)


    #def createSessionByFacebookAuth(self, connection, token):

    def createSessionByTokenAuth(connection, username, token):

        if username is None:
            raise InvalidUserCredentialsException()

        if token is None:
            raise InvalidUserCredentialsException()

        kuat = KsmUserAuthenticationType.query.filter(KsmUserAuthenticationType.username == username).filter(KsmUserAuthenticationType.authentication_type_id == AuthenticationType.TOKEN).first()

        if kuat is None:
            raise NotFoundUserException()

        SecurityHashService.validateHash(token)

        if not check_password_hash(kuat.getToken(), token):
            raise InvalidUserCredentialsException()

        return SessionService.createSession(connection, kuat)

    def createSession(connection, kuat):

        if kuat is None:
            return

        date = datetime.now()
        ksmSession = KsmSession(str(uuid.uuid4()), True, connection.getToken(), kuat.getUserId(), kuat.getAuthenticationTypeId(), date, date)
        Database.insert(ksmSession)
        return SessionMapper.mapToSession(ksmSession, connection)

    def getValidSession(token):

        if token is None:
            raise NullClientSessionException()

        ksmSession = KsmSession.query.filter(KsmSession.id == token).first()
        if ksmSession is None:
            raise InvalidUserSessionException()

        if ksmSession.getActive() == False:
            raise ClientSessionExpiredException()

        date = datetime.now()
        ksmSession.setUpdatedAt(date)
        Database.update(ksmSession)

        return SessionMapper.mapToSession(ksmSession, None)


    def getConnectionIdBySession(token):

        if token is None:
            raise NullClientSessionException()

        ksmSession = KsmSession.query.filter(KsmSession.id == token).first()
        if ksmSession is None:
            raise InvalidUserSessionException()

        return ksmSession.getConnectionId()
