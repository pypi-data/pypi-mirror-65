from flask import Flask
from app import db

class KsmConnection(db.Model):
    __tablename__ = 'ksm_connection'
    __bind_key__ = 'intranet_inovafit'
    __table_args__ = {'schema': 'intranet_inovafit'}

    id = db.Column(db.String(60), primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, active, client_id,created_at, updated_at, deleted_at=None):
       self.id = id
       self.active = active
       self.client_id = client_id
       self.created_at = created_at
       self.updated_at = updated_at
       self.deleted_at = deleted_at

    def getId(self):
       return self.id

    def getActive(self):
       return self.active

    def setActive(self, active):
       self.active = active

    def getClientId(self):
       return self.client_id

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def setUpdatedAt(self, updated_at):
       self.updated_at = updated_at

    def getDeletedAt(self):
       return self.deleted_at

class KsmClient(db.Model):
    __tablename__ = 'ksm_client'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def getId(self):
       return self.id

    def getUsername(self):
       return self.username

    def getPassword(self):
       return self.password

    def getActive(self):
      return self.active

class KsmSession(db.Model):
    __tablename__ = 'ksm_session'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.String(60), primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    connection_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    authentication_type_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, active, connection_id, user_id, authentication_type_id, created_at, updated_at, deleted_at=None):
       self.id = id
       self.active = active
       self.connection_id = connection_id
       self.user_id = user_id
       self.authentication_type_id = authentication_type_id
       self.created_at = created_at
       self.updated_at = updated_at
       self.deleted_at = deleted_at

    def getId(self):
       return self.id

    def getActive(self):
       return self.active

    def getConnectionId(self):
       return self.connection_id

    def getUserId(self):
       return self.user_id

    def getAuthenticationTypeId(self):
       return self.authentication_type_id

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def setUpdatedAt(self, updated_at):
       self.updated_at = updated_at

    def getDeletedAt(self):
       return self.deleted_at

class KsmUserAuthenticationType(db.Model):
    __tablename__ = 'ksm_user_authentication_type'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(1500), nullable=False)
    authentication_type_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def getId(self):
       return self.id

    def getUserName(self):
       return self.username

    def getToken(self):
       return self.token

    def getAuthenticationTypeId(self):
       return self.authentication_type_id

    def getUserId(self):
       return self.user_id

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def setId(self, id):
       self.id = id

    def setUserName(self, username):
       self.username = username

    def setToken(self, token):
       self.token = token

    def setAuthenticationTypeId(self, authentication_type_id):
       self.authentication_type_id = authentication_type_id

    def setUserId(self, user_id):
       self.user_id = user_id

    def setCreatedAt(self, created_at):
       self.created_at = created_at

    def setUpdatedAt(self, updated_at):
       self.updated_at = updated_at

    def getDeletedAt(self):
       return self.deleted_at

class KsmRole(db.Model):
    __tablename__ = 'ksm_role'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def getId(self):
       return self.id

    def getDescription(self):
       return self.description

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def getDeletedAt(self):
       return self.deleted_at

class KsmUser(db.Model):
    __tablename__ = 'ksm_user'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.String(60), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def setId(self, id):
       self.id = id

    def getId(self):
       return self.id

    def setCreatedAt(self, created_at):
       self.created_at = created_at

    def setUpdatedAt(self, updated_at):
       self.updated_at = updated_at

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def getDeletedAt(self):
       return self.deleted_at

class KsmRoleUser(db.Model):
    __tablename__ = 'ksm_role_user'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def getId(self):
       return self.id

    def getRoleId(self):
       return self.role_id

    def getUserId(self):
       return self.user_id

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def getDeletedAt(self):
       return self.deleted_at

    def setRoleId(self, role_id):
       self.role_id = role_id

    def setUserId(self, user_id):
       self.user_id = user_id

    def setCreatedAt(self, created_at):
       self.created_at = created_at

    def setUpdatedAt(self, updated_at):
       self.updated_at = updated_at

class KsmRoleService(db.Model):
    __tablename__ = 'ksm_role_service'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def getId(self):
       return self.id

    def getRoleId(self):
       return self.role_id

    def getServiceId(self):
       return self.service_id

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def getDeletedAt(self):
       return self.deleted_at

    def setRoleId(self, role_id):
       self.role_id = role_id

    def setServiceId(self, user_id):
       self.service_id = user_id

    def setCreatedAt(self, created_at):
       self.created_at = created_at

    def setUpdatedAt(self, updated_at):
       self.updated_at = updated_at

class KsmSecurityHashType(db.Model):
    __tablename__ = 'ksm_security_hash_type'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def getId(self):
       return self.id

    def getName(self):
       return self.name

    def getCreatedAt(self):
       return self.created_at

class KsmSecurityHash(db.Model):

    __tablename__ = 'ksm_security_hash'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    used = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    security_hash_type_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def getId(self):
       return self.id

    def getToken(self):
       return self.token

    def getUsed(self):
       return self.used

    def getActive(self):
       return self.active

    def getSecurityHashTypeId(self):
       return self.security_hash_type_id

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def getDeletedAt(self):
       return self.deleted_at

    def setToken(self, token):
       self.token = token

    def setSecurityHashTypeId(self, security_hash_type_id):
       self.security_hash_type_id = security_hash_type_id

    def setUsed(self, used):
       self.used = used

    def setActive(self, active):
       self.active = active

    def setCreatedAt(self, created_at):
       self.created_at = created_at

    def setUpdatedAt(self, updated_at):
       self.updated_at = updated_at

class KsmClientService(db.Model):

    __tablename__ = 'ksm_client_service'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def getId(self):
       return self.id

    def getClientId(self):
       return self.client_id

    def getServiceId(self):
       return self.service_id

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def getDeletedAt(self):
       return self.deleted_at

class KsmUserService(db.Model):

    __tablename__ = 'ksm_user_service'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def getId(self):
       return self.id

    def getUserId(self):
       return self.user_id

    def getServiceId(self):
       return self.service_id

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def getDeletedAt(self):
       return self.deleted_at

class KsmService(db.Model):

    __tablename__ = 'ksm_service'
    __bind_key__ = 'intranet_inovafit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False)

    def getId(self):
       return self.id

    def getName(self):
       return self.name

    def getDescription(self):
       return self.description

    def getCreatedAt(self):
       return self.created_at

    def getUpdatedAt(self):
       return self.updated_at

    def getDeletedAt(self):
       return self.deleted_at


class Database():
    def update(obj):
        db.session.commit()

    def insert(obj):
        db.session.add(obj)
        db.session.commit()
