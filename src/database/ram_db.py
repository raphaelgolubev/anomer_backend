import src.security.hashing_encoding as jwt_utils
from src.api.v1.users.schemas import UserCredentials

john = UserCredentials(
    username="john",
    password=jwt_utils.hash_password("qwerty"),
    email="john@example.com",
)

sam = UserCredentials(username="sam", password=jwt_utils.hash_password("secret"))

user_db: dict[str, UserCredentials] = {john.username: john, sam.username: sam}
