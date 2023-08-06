from cerberus.exceptions.exceptions import ServiceNotAllowedException, ClientServiceNotAllowedException, UserServiceNotAllowedException, NullClientConnectionException, InvalidClientConnectionException, ClientConnectionExpiredException
from cerberus.entities.entities import KsmRoleService, KsmClientService, KsmUserService, KsmRoleUser, KsmService
from cerberus.management.ConnectionExecuteService import ConnectionExecuteService
from cerberus.management.SessionExecuteService import SessionExecuteService
from cerberus.services.ConnectionService import ConnectionService
from cerberus.services.SessionService import SessionService

class AccessControlList():

    def validateExecuteService(service):
        if isinstance(service, ConnectionExecuteService):
            return AccessControlList.validateConnectionExecuteService(service)
        elif isinstance(service, SessionExecuteService):
            return AccessControlList.validateSessionExecuteService(service)

    def validateConnectionExecuteService(service):
        connection = ConnectionService.getValidConnection(service.getRequest().getHeaderRQ().getToken())

        ksmService = KsmService.query.filter(KsmService.name == service.__class__.__name__).first()
        if ksmService is None:
            raise ServiceNotAllowedException(service.__class__.__name__)

        ksmClientService = KsmClientService.query.filter(KsmClientService.client_id == connection.getClientId()).filter(KsmClientService.service_id == ksmService.getId()).first()
        if ksmClientService is None:
            print("ksmClientService is None: " + service.__class__.__name__)
            raise ClientServiceNotAllowedException(service.__class__.__name__)

        return connection

    def validateSessionExecuteService(service):

        session = SessionService.getValidSession(service.getRequest().getHeaderRQ().getToken())
        connectionId = SessionService.getConnectionIdBySession(service.getRequest().getHeaderRQ().getToken())
        connection = ConnectionService.getValidConnection(connectionId)
        session.setConnection(connection)

        ksmService = KsmService.query.filter(KsmService.name == service.__class__.__name__).first()
        if ksmService is None:
            raise ServiceNotAllowedException(service.__class__.__name__)

        ksmClientService = KsmClientService.query.filter(KsmClientService.client_id == connection.getClientId()).filter(KsmClientService.service_id == ksmService.getId()).first()
        if ksmClientService is None:
            raise ClientServiceNotAllowedException(service.__class__.__name__)


        rolesUser = KsmRoleUser.query.filter(KsmRoleUser.user_id == session.getUserId()).all()
        allowedExecution = False
        if not rolesUser is None:
            for roleUser in rolesUser:
                ksmRoleService = KsmRoleService.query.filter(KsmRoleService.role_id == roleUser.getRoleId()).filter(KsmRoleService.service_id == ksmService.getId()).first()
                if not ksmRoleService is None:
                    allowedExecution = True

        if allowedExecution == True:
            return session

        ksmUserService = KsmUserService.query.filter(KsmUserService.user_id == session.getUserId()).filter(KsmUserService.service_id == ksmClientService.getServiceId()).first()
        if ksmUserService is None:
            raise UserServiceNotAllowedException(service.__class__.__name__)

        return session
