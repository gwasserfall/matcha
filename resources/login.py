from flask import request

from flask import current_app as app

from flask_restful import Resource
from flask_jwt_extended import (
    JWTManager,
                jwt_required,
                create_access_token,
                create_refresh_token,
    get_jwt_identity
)

from models.user import User, get_full_user

from twisted.python import log

from helpers import Arguments, is_email


class LoginResource(Resource):
    def post(self):
        """
        GET /v1/login

        Description

        SUCCESS (200)

        ```json
        "access_token": "eyJ0eXAiOiJKK6I3lO1lk",
        "user": {
                        "id": 104,
                        "fname": "Glen",
                        "lname": "Wasserfall",
                        "email": "glen@wasserfallss.co.za",
                        "username": "aclone",
                        "email_verified": 1,
                        "bio": null,
                        "gender": "Male",
                        "dob": null,
                        "longitude": null,
                        "latitude": null,
                        "heat": null,
                        "online": null,
                        "date_lastseen": null,
                        "is_admin": null
}
        ```


        """
        args = Arguments(request.json)
        args.string("username", required=True)
        args.string("password", required=True)
        args.validate()

        log.msg("User " + args.username + " trying to sign in")

        if is_email(args.username):
            user = User.get(email=args.username)
        else:
            user = User.get(username=args.username)

        if user and not user.email_verified:
            return {"message" : "Account not validated"}, 401
        elif user and user.check_password(args.password):
            identity = {
                    "id" : user.id,
                    "username" : user.username,
                    "email" : user.email}
            access_token = create_refresh_token(identity=identity)
            return {"access_token" : access_token, "user": get_full_user(user.id)}, 200

        else:
            return {"message" : "Failed to authenticate"}, 401
