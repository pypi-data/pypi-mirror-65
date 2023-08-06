import firebase_admin
from firebase_admin import auth, credentials
from cerberus.exceptions.exceptions import InvalidUserCredentialsException, NotFoundUserException

class FirebaseService():

    def __init__(self):
        cred = credentials.Certificate("/Users/cesarocotitla/Projects/intranet_inovafit_web/key/intranet-inovafit-firebase-adminsdk-dbrq9-92b838f9a9.json")
        if (not len(firebase_admin._apps)):
            default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://intranet-inovafit.firebaseio.com'})

    def getDecoded_token(self, tokenId):
        try:
            decoded_token = auth.verify_id_token(tokenId)
        except Exception as error:
             raise InvalidUserCredentialsException()

        return decoded_token
