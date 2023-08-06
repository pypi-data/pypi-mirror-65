

import uuid
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from cerberus.mappers.UserMapper import UserMapper
from cerberus.entities.entities import KsmUserAuthenticationType, KsmRole, KsmUser, KsmRoleUser, Database
from cerberus.exceptions.exceptions import UserAlreadyExistException, NotFoundRoleException, InternalErrorException, NotFoundUserException
from cerberus.dtos.AuthenticationType import AuthenticationType
from cerberus.dtos.SecurityHash import SecurityHash
from cerberus.services.SecurityHashService import SecurityHashService
from cerberus.services.FirebaseService import FirebaseService

class UserService():

    def createUser(username, token, authenticationTypeId, roleId):

        ksmUser = None
        kuat = KsmUserAuthenticationType.query.filter(KsmUserAuthenticationType.username == username).filter(KsmUserAuthenticationType.authentication_type_id == authenticationTypeId).first()

        if not kuat is None:
            raise UserAlreadyExistException()

        kuat = KsmUserAuthenticationType.query.filter(KsmUserAuthenticationType.username == username).first()
        if not kuat is None:
            ksmUser = KsmUser.query.filter(KsmUser.id == kuat.getUserId()).first()

        ksmRole = KsmRole.query.filter(KsmRole.id == roleId).first()

        if ksmRole is None:
            raise NotFoundRoleException()

        if authenticationTypeId == AuthenticationType.GOOGLE:
            decoded_token = FirebaseService().getDecoded_token(token)

            res_uid = decoded_token['uid']
            if res_uid != username:
                print("Error:")
                print(res_uid)
                print(username)
                raise InvalidUserCredentialsException()

        try:
            createdAt = datetime.now()

            #Create Ksm User
            if ksmUser is None:
                ksmUser = KsmUser()
                ksmUser.setId(str(uuid.uuid4()))
                ksmUser.setCreatedAt(createdAt)
                ksmUser.setUpdatedAt(createdAt)
                Database.insert(ksmUser)

            #Create Ksm User Authentication Type
            UserService.createKsmUserAuthenticationType(ksmUser.getId(), username, token, authenticationTypeId)
            if authenticationTypeId == AuthenticationType.GOOGLE:
                email = decoded_token['email']
                UserService.createKsmUserAuthenticationType(ksmUser.getId(), email, token, AuthenticationType.TOKEN)

            #Add Role to User
            ksmRoleUser = KsmRoleUser()
            ksmRoleUser.setUserId(ksmUser.getId())
            ksmRoleUser.setRoleId(roleId)
            ksmRoleUser.setCreatedAt(createdAt)
            ksmRoleUser.setUpdatedAt(createdAt)
            Database.insert(ksmRoleUser)

        except Exception as ex:
            print(ex)
            raise InternalErrorException("Error creating user")

        return UserMapper.mapToUser(ksmUser)

    def createKsmUserAuthenticationType(userId, username, token, authenticationTypeId):
        createdAt = datetime.now()
        ksmUserAuthenticationType = KsmUserAuthenticationType()
        ksmUserAuthenticationType.setAuthenticationTypeId(authenticationTypeId)
        ksmUserAuthenticationType.setUserId(userId)
        ksmUserAuthenticationType.setUserName(username)
        ksmUserAuthenticationType.setCreatedAt(createdAt)
        ksmUserAuthenticationType.setUpdatedAt(createdAt)

        if authenticationTypeId == AuthenticationType.LOCAL:
            token = generate_password_hash(userId + token)

        ksmUserAuthenticationType.setToken(token)
        Database.insert(ksmUserAuthenticationType)

    def createUserAccessToken(email):

        ksmUserAuthenticationType = KsmUserAuthenticationType.query.filter(KsmUserAuthenticationType.username == email).first()
        if ksmUserAuthenticationType is None:
            raise NotFoundUserException()

        ksmUser = KsmUser.query.filter(KsmUser.id == ksmUserAuthenticationType.getUserId()).first()
        securityHash = SecurityHashService.createHash(SecurityHash.AUTH_TOKEN)

        createdAt = datetime.now()
        ksmUserAuthenticationType = KsmUserAuthenticationType.query.filter(KsmUserAuthenticationType.user_id == ksmUserAuthenticationType.getUserId()).filter(KsmUserAuthenticationType.authentication_type_id == AuthenticationType.TOKEN).first()
        if ksmUserAuthenticationType is None:
            ksmUserAuthenticationType = KsmUserAuthenticationType()
            ksmUserAuthenticationType.setAuthenticationTypeId(AuthenticationType.TOKEN)
            ksmUserAuthenticationType.setUserId(ksmUser.getId())
            ksmUserAuthenticationType.setUserName(username)
            ksmUserAuthenticationType.setCreatedAt(createdAt)
            ksmUserAuthenticationType.setUpdatedAt(createdAt)
            ksmUserAuthenticationType.setToken(generate_password_hash(securityHash.getToken()))
            Database.insert(ksmUserAuthenticationType)
        else:
            ksmUserAuthenticationType.setToken(generate_password_hash(securityHash.getToken()))
            ksmUserAuthenticationType.setUpdatedAt(createdAt)
            Database.update(ksmUserAuthenticationType)

        return securityHash
        
