from cerberus.dtos.Session import Session
from cerberus.entities.entities import KsmRoleUser

class SessionMapper():
    def mapToSession(ksmSession, connection):
        roleUser = KsmRoleUser.query.filter(KsmRoleUser.user_id == ksmSession.getUserId()).first()
        return Session(ksmSession.getId(), ksmSession.getUserId(), ksmSession.getActive(), ksmSession.getAuthenticationTypeId(), roleUser.getRoleId(), connection, ksmSession.getCreatedAt(), ksmSession.getUpdatedAt())
