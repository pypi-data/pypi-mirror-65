from collections import namedtuple


class Config:
    branch: namedtuple("Branch", "env")
    credentials_secret: namedtuple("CredentialsSecret", ("name", "key_username", "key_password"))
