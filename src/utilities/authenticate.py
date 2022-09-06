from email import message
from xml.dom import ValidationErr
from ..accounts.model.Tokens import Tokens
from ..accounts.model.UsersAccount import Users

def authenticate_requests(token: str):
    print("Authenticating requests.........")
    try:
        auth_token = token.split(":")[0]
        users_id = token.split(":")[1]
        print("\n\t auth_token.........", auth_token)
        print("\n\t users_id.........", users_id)
        if not users_id or not auth_token:
            return "Unrecognised token format"

        token_exists = None
        for token in Tokens.tokens.find():
            if str(token['token']) == auth_token:
                print("\n\t Token was found: ", token)
                token_exists = token 
                break
        error_message = "Could not find token"
        if token_exists:
            saved_users_id = token_exists["users_id"]
            saved_auth_token = token_exists["token"]
            error_message = "Failed to compare token"
            if users_id == str(saved_users_id):
                if str(saved_auth_token) == auth_token:
                    user_details = Users.find_one({"_id": saved_users_id})
                    print("\n\t token_exists-here", token_exists)
                    return {
                        "status": True,
                        "user": user_details,
                        "message": str("Successfully authenticated")
                    }
        raise ValidationErr(error_message)        
    except Exception as error:
        print(error)
        return {
            "status": False,
            "error": error,
            "message": str(error)
        }

