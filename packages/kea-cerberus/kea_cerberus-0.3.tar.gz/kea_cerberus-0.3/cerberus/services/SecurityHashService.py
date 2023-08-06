from datetime import datetime
import uuid

from cerberus.dtos.SecurityHash import SecurityHash
from cerberus.entities.entities import KsmSecurityHash, KsmSecurityHashType, Database

from cerberus.mappers.SecurityHashMapper import SecurityHashMapper
from cerberus.exceptions.exceptions import InvalidParamException, RequiredParamException, SecurityHashExpiredException, InvalidSecurityHashException

class SecurityHashService():

    def createHash(type):

        if type is None:
            raise RequiredParamException("type")

        ksmSecurityHashType = KsmSecurityHashType.query.filter(KsmSecurityHashType.id == type).first()
        if ksmSecurityHashType is None:
            raise InvalidParamException("type")

        createdAt = datetime.now()
        ksmSecurityHash = KsmSecurityHash()
        ksmSecurityHash.setToken(str(uuid.uuid4()))
        ksmSecurityHash.setUsed(False)
        ksmSecurityHash.setActive(True)
        ksmSecurityHash.setSecurityHashTypeId(type)
        ksmSecurityHash.setCreatedAt(createdAt)
        ksmSecurityHash.setUpdatedAt(createdAt)

        Database.insert(ksmSecurityHash)

        return SecurityHashMapper.mapToSecurityHash(ksmSecurityHash);

    def validateHash(token):

        if token is None:
            raise RequiredParamException("token")

        ksmSecurityHash = KsmSecurityHash.query.filter(KsmSecurityHash.token == token).first()
        if ksmSecurityHash is None:
            raise InvalidSecurityHashException()

        if ksmSecurityHash.getActive() == False or ksmSecurityHash.getUsed() == True:
            raise SecurityHashExpiredException()


        ksmSecurityHash.setUsed(True)
        Database.update(ksmSecurityHash)

        return SecurityHashMapper.mapToSecurityHash(ksmSecurityHash);
