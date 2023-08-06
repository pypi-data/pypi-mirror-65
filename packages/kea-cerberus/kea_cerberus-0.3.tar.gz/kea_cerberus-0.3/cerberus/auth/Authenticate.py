from flask import Flask

from werkzeug.security import generate_password_hash, check_password_hash
from cerberus.requests.Request import Request
from cerberus.requests.LoginUserRQ import LoginUserRQ
from cerberus.requests.CreateUserRQ import CreateUserRQ
from cerberus.responses.Response import Response
from cerberus.responses.BodyRS import BodyRS
from cerberus.responses.LoginClientRS import LoginClientRS
from cerberus.responses.SessionRS import SessionRS
from cerberus.responses.HeaderRS import HeaderRS
from cerberus.responses.CreateUserRS import CreateUserRS
from cerberus.responses.CreateUserAccessTokenRS import CreateUserAccessTokenRS
from cerberus.entities.entities import KsmClient, KsmConnection
from cerberus.dtos.Connection import Connection
from cerberus.dtos.AuthenticationType import AuthenticationType
from cerberus.dtos.Session import Session
from cerberus.dtos.Error import Error
from cerberus.dtos.User import User
from cerberus.dtos.SecurityHash import SecurityHash
from cerberus.services.ConnectionService import ConnectionService
from cerberus.services.SessionService import SessionService
from cerberus.services.UserService import UserService
from cerberus.mappers.HeaderMapper import HeaderMapper
from cerberus.services.SecurityHashService import SecurityHashService

from cerberus.exceptions.exceptions import InvalidClientCredentialsException, InvalidUserCredentialsException, NotFoundUserException
from cerberus.exceptions.exceptions import InvalidClientConnectionException, ClientConnectionExpiredException, RequiredParamException, NullClientConnectionException
from cerberus.exceptions.exceptions import UserCredentialsExpiredException, InternalErrorException, MaxUserSessionException, InvalidUserSessionException, InvalidParamException
from cerberus.exceptions.exceptions import NotFoundRoleException, UserAlreadyExistException, SecurityHashExpiredException, InvalidSecurityHashException


class Authenticate():

    #Method to create client connection
    def login(username, password):
        bodyRS = LoginClientRS(True)
        headerRS = HeaderRS()

        try:
            if username is None:
                raise RequiredParamException("username")

            if password is None:
                raise RequiredParamException("password")

            #print("hash")
            #print(generate_password_hash(password))

            client = KsmClient.query.filter(KsmClient.username == username).filter(KsmClient.active == True).first()

            if client is None:
                raise InvalidClientCredentialsException()

            if not check_password_hash(client.getPassword(), password):
                raise InvalidClientCredentialsException()

            connection = ConnectionService.createConnection(client)
            headerRS = HeaderRS(connection.getToken(), connection.getCreatedAt(), connection.getUpdatedAt())
            bodyRS.setConnection(connection)


        except (RequiredParamException, InvalidClientCredentialsException) as e:
            error = Error(e.getCode(), e.getMessage())
            bodyRS = LoginClientRS(False, error)

        response = Response(headerRS, bodyRS)
        return response

    def logout(request):
        bodyRS = BodyRS(True)
        headerRS = HeaderRS()

        try:
            connection = ConnectionService.removeConnection(request.getHeaderRQ().getToken())
            headerRS = HeaderRS(connection.getToken(), connection.getCreatedAt(), connection.getUpdatedAt())
        except (NullClientConnectionException, InvalidClientCredentialsException) as e:
            error = Error(e.getCode(), e.getMessage())
            bodyRS = BodyRS(False, error)

        response = Response(headerRS, bodyRS)
        return response;


        return response

    def validate(request):
        bodyRS = BodyRS(True)
        headerRS = HeaderRS()

        try:
            connection = ConnectionService.validateConnection(request.getHeaderRQ().getToken())
            headerRS = HeaderRS(connection.getToken(), connection.getCreatedAt(), connection.getUpdatedAt())
        except (NullClientConnectionException, InvalidClientCredentialsException) as e:
            error = Error(e.getCode(), e.getMessage())
            bodyRS = BodyRS(False, error)

        response = Response(headerRS, bodyRS)
        return response;


        return response

    #Method to create user connection
    def loginUser(request):
        headerRS = HeaderRS()
        sessionRS = SessionRS(True)
        loginUserRQ = request.getBodyRQ()

        #Validate request inputs
        #bodyRS = new BodyRS()
        #bodyRS = Util.validateRQ(loginUserRQ);

        #if bodyRS is None:
        #    response.setBodyRS(bodyRS);
        #    response.setHeaderRS(new HeaderRS(request.getHeaderRQ().getToken()));
        #    return response;

        try:
            # Valid Connection Token
            connection = ConnectionService.validateConnection(request.getHeaderRQ().getToken());

            if loginUserRQ.getAuthenticationTypeId() == AuthenticationType.LOCAL:
                session = SessionService.createSessionByLocalAuth(connection, loginUserRQ.getUserName(), loginUserRQ.getToken())
            elif loginUserRQ.getAuthenticationTypeId() == AuthenticationType.GOOGLE:
                session = SessionService.createSessionByGoogleAuth(connection, loginUserRQ.getUserName(), loginUserRQ.getToken())
            elif loginUserRQ.getAuthenticationTypeId() == AuthenticationType.FACEBOOK:
                session = SessionService.createSessionByFacebookAuth(connection, loginUserRQ.getToken())
            elif loginUserRQ.getAuthenticationTypeId() == AuthenticationType.TOKEN:
                session = SessionService.createSessionByTokenAuth(connection, loginUserRQ.getUserName(), loginUserRQ.getToken())
            else:
                raise InvalidParamException("AuthenticationTypeId")

            sessionRS.setSession(session);
            #sessionRS.getRoles().addAll(userServiceLocal.getUserRoles(session.getUserId()));
            headerRS = HeaderMapper.mapToHeader(session);

        except (InvalidSecurityHashException, SecurityHashExpiredException, InvalidParamException, UserCredentialsExpiredException, NullClientConnectionException, InvalidClientConnectionException, ClientConnectionExpiredException, InternalErrorException, InvalidUserCredentialsException, NotFoundUserException, MaxUserSessionException, InvalidUserSessionException) as e:
            error = Error(e.getCode(), e.getMessage())
            sessionRS = SessionRS(False, error)

        response = Response(headerRS, sessionRS)
        return response

    def createUser(request):
        headerRS = HeaderRS()
        try:
            createUserRQ = request.getBodyRQ();

            SecurityHashService.validateHash(createUserRQ.getSecurityToken())

            user = UserService.createUser(createUserRQ.getUserName(), createUserRQ.getToken(), createUserRQ.getAuthenticationTypeId(), createUserRQ.getRoleId())
            headerRS = HeaderRS(request.getHeaderRQ().getToken())

            createUserRS = CreateUserRS(True)
            createUserRS.setUser(user)
        except  (InternalErrorException , NotFoundRoleException , UserAlreadyExistException) as e:
            error = Error(e.getCode(), e.getMessage())
            createUserRS = CreateUserRS(False, error)


        response = Response(headerRS, createUserRS)
        return response

    def createUserCreateToken(request):
        headerRS = HeaderRS()
        try:
            securityHash = SecurityHashService.createHash(SecurityHash.CREATE_USER_TOKEN)
            headerRS = HeaderRS(request.getHeaderRQ().getToken())
            createUserAccessTokenRS = CreateUserAccessTokenRS(True)
            createUserAccessTokenRS.setSecurityHash(securityHash)
        except  (InternalErrorException , NotFoundRoleException , UserAlreadyExistException) as e:
            error = Error(e.getCode(), e.getMessage())
            createUserAccessTokenRS = CreateUserTokenRS(False, error)

        response = Response(headerRS, createUserAccessTokenRS)
        return response

    def createUserAccessToken(request):
        headerRS = HeaderRS()
        try:
            createUserAccessTokenRQ = request.getBodyRQ();
            securityHash = UserService.createUserAccessToken(createUserAccessTokenRQ.getEmail())
            headerRS = HeaderRS(request.getHeaderRQ().getToken())
            createUserAccessTokenRS = CreateUserAccessTokenRS(True)
            createUserAccessTokenRS.setSecurityHash(securityHash)
        except  (InternalErrorException , NotFoundRoleException , UserAlreadyExistException) as e:
            error = Error(e.getCode(), e.getMessage())
            createUserAccessTokenRS = CreateUserTokenRS(False, error)


        response = Response(headerRS, createUserAccessTokenRS)
        return response
