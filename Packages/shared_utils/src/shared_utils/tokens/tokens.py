import os
from joserfc import jwt
from joserfc.jwk import OKPKey
from joserfc.errors import (
    JoseError,
    BadSignatureError,
    ConflictAlgorithmError,
    DecodeError,
    ExpiredTokenError,
    InvalidExchangeKeyError,
    ExceededSizeError,
)

from shared_utils.tokens.errors import (
    TokenTypeError,
    TokenExpiredError,
    TokenDecodeError,
)


JWT_ASYMETRIC_ALGORITHM = os.environ["JWT_ASYMETRIC_ALGORITHM"]

JWT_PUBLIC_KEY_FILE = "/run/secrets/jwt_public_key"
if not os.path.exists(JWT_PUBLIC_KEY_FILE):
    raise FileNotFoundError(f"JWT_PUBLIC_KEY_FILE file not found at {JWT_PUBLIC_KEY_FILE}")
with open(JWT_PUBLIC_KEY_FILE, "rb") as f:
    JWT_PUBLIC_KEY = OKPKey.import_key(f.read())


class TokenChecker:
    @staticmethod
    def decode_token(token: str, expected_type: str):
        """
        Decode a JWT and validate its type.
        expected_type: "access" | "refresh"
        """
        try:
            payload = jwt.decode(
                token, JWT_PUBLIC_KEY, algorithms=[JWT_ASYMETRIC_ALGORITHM]
            )
            if payload.claims.get("token_type") != expected_type:
                raise TokenTypeError(f"Token must be a {expected_type} token")
            return payload
        
        except BadSignatureError:
            raise TokenDecodeError(
                f"Error decoding {expected_type} token: Invalid signature"
            )

        except ConflictAlgorithmError:
            raise TokenDecodeError(
                f"Error decoding {expected_type} token: Invalid algorithm"
            )

        except DecodeError:
            raise TokenDecodeError(
                f"Error decoding {expected_type} token: Invalid token"
            )

        except ExpiredTokenError:
            raise TokenExpiredError(
                f"{expected_type.capitalize()} token expired"
            )

        except ExceededSizeError:
            raise TokenDecodeError(
                f"{expected_type.capitalize()} token exceeded size limit"
            )
        
        except InvalidExchangeKeyError:
            raise TokenDecodeError(
                f"Error decoding {expected_type} token: Invalid exchange key"
            )

        except JoseError as e:
            raise TokenDecodeError(f"Error decoding {expected_type} token: {str(e)}")
