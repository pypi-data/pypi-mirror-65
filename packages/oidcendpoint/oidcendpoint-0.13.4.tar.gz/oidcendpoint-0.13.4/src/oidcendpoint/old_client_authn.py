import base64
import logging
from urllib.parse import unquote_plus

from cryptojwt.exception import BadSignature
from cryptojwt.exception import Invalid
from cryptojwt.exception import MissingKey
from cryptojwt.jwt import JWT
from cryptojwt.jwt import utc_time_sans_frac
from cryptojwt.utils import as_bytes
from cryptojwt.utils import as_unicode
from oidcmsg.oidc import verified_claim_name

from oidcendpoint import JWT_BEARER
from oidcendpoint import sanitize
from oidcendpoint.exception import InvalidClient
from oidcendpoint.exception import MultipleUsage
from oidcendpoint.exception import NotForMe
from oidcendpoint.exception import UnknownClient

logger = logging.getLogger(__name__)

__author__ = "roland hedberg"


class AuthnFailure(Exception):
    pass


class NoMatchingKey(Exception):
    pass


class UnknownOrNoAuthnMethod(Exception):
    pass


class WrongAuthnMethod(Exception):
    pass


class ClientAuthnMethod(object):
    def __init__(self, endpoint_context=None):
        """
        :param endpoint_context: Server info, a
            :py:class:`oidcendpoint.endpoint_context.EndpointContext` instance
        """
        self.endpoint_context = endpoint_context

    def verify(self, **kwargs):
        """
        Verify authentication information in a request
        :param kwargs:
        :return:
        """
        raise NotImplementedError


def basic_authn(authn):
    if not authn.startswith("Basic "):
        raise AuthnFailure("Wrong type of authorization token")

    _tok = as_bytes(authn[6:])
    # Will raise ValueError type exception if not base64 encoded
    _tok = base64.b64decode(_tok)
    part = [unquote_plus(p) for p in as_unicode(_tok).split(":")]
    if len(part) == 2:
        return dict(zip(["id", "secret"], part))
    else:
        raise ValueError("Illegal token")


class ClientSecretBasic(ClientAuthnMethod):
    """
    Clients that have received a client_secret value from the Authorization
    Server, authenticate with the Authorization Server in accordance with
    Section 3.2.1 of OAuth 2.0 [RFC6749] using HTTP Basic authentication scheme.
    """

    def verify(self, request, authorization_info, **kwargs):
        client_info = basic_authn(authorization_info)

        if (
                self.endpoint_context.cdb[client_info["id"]]["client_secret"]
                == client_info["secret"]
        ):
            return {"client_id": client_info["id"]}
        else:
            raise AuthnFailure()


class ClientSecretPost(ClientSecretBasic):
    """
    Clients that have received a client_secret value from the Authorization
    Server, authenticate with the Authorization Server in accordance with
    Section 3.2.1 of OAuth 2.0 [RFC6749] by including the Client Credentials in
    the request body.
    """

    def verify(self, request, **kwargs):
        if (
                self.endpoint_context.cdb[request["client_id"]]["client_secret"]
                == request["client_secret"]
        ):
            return {"client_id": request["client_id"]}
        else:
            raise AuthnFailure("secrets doesn't match")


class BearerHeader(ClientSecretBasic):
    """
    """

    def verify(self, request, authorization_info, **kwargs):
        if not authorization_info.startswith("Bearer "):
            raise AuthnFailure("Wrong type of authorization token")

        return {"token": authorization_info.split(" ", 1)[1]}


class BearerBody(ClientSecretPost):
    """
    Same as Client Secret Post
    """

    def verify(self, request, **kwargs):
        try:
            return {"token": request["access_token"]}
        except KeyError:
            raise AuthnFailure("No access token")


class JWSAuthnMethod(ClientAuthnMethod):
    def verify(self, request, **kwargs):
        _jwt = JWT(self.endpoint_context.keyjar)
        try:
            ca_jwt = _jwt.unpack(request["client_assertion"])
        except (Invalid, MissingKey, BadSignature) as err:
            logger.info("%s" % sanitize(err))
            raise AuthnFailure("Could not verify client_assertion.")

        authtoken = sanitize(ca_jwt)
        if hasattr(ca_jwt, "to_dict") and callable(ca_jwt, "to_dict"):
            authtoken = sanitize(ca_jwt.to_dict())
        logger.debug("authntoken: {}".format(authtoken))

        _endpoint = kwargs.get("endpoint")
        if _endpoint is None or not _endpoint:
            if self.endpoint_context.issuer in ca_jwt["aud"]:
                pass
            else:
                raise NotForMe("Not for me!")
        else:
            if set(ca_jwt["aud"]).intersection(
                    self.endpoint_context.endpoint[_endpoint].allowed_target_uris()):
                pass
            else:
                raise NotForMe("Not for me!")

        # If there is a jti use it to make sure one-time usage is true
        _jti = ca_jwt.get('jti')
        if _jti:
            _key = "{}:{}".format(ca_jwt['iss'], _jti)
            if _key in self.endpoint_context.jti_db:
                raise MultipleUsage("Have seen this token once before")
            else:
                self.endpoint_context.jti_db.set(_key, utc_time_sans_frac())

        request[verified_claim_name("client_assertion")] = ca_jwt
        client_id = kwargs.get("client_id") or ca_jwt["iss"]

        return {"client_id": client_id, "jwt": ca_jwt}


class ClientSecretJWT(JWSAuthnMethod):
    """
    Clients that have received a client_secret value from the Authorization
    Server create a JWT using an HMAC SHA algorithm, such as HMAC SHA-256.
    The HMAC (Hash-based Message Authentication Code) is calculated using the
    bytes of the UTF-8 representation of the client_secret as the shared key.
    """


class PrivateKeyJWT(JWSAuthnMethod):
    """
    Clients that have registered a public key sign a JWT using that key.
    """


CLIENT_AUTHN_METHOD = {
    "client_secret_basic": ClientSecretBasic,
    "client_secret_post": ClientSecretPost,
    "bearer_header": BearerHeader,
    "bearer_body": BearerBody,
    "client_secret_jwt": ClientSecretJWT,
    "private_key_jwt": PrivateKeyJWT,
    "none": None,
}

TYPE_METHOD = [(JWT_BEARER, JWSAuthnMethod)]


def valid_client_info(cinfo):
    eta = cinfo.get("client_secret_expires_at", 0)
    if eta != 0 and eta < utc_time_sans_frac():
        return False
    return True


def verify_client(
        endpoint_context, request, authorization_info=None, get_client_id_from_token=None,
        endpoint=None, also_known_as=None
):
    """
    Initiated Guessing !

    :param endpoint_context: SrvInfo instance
    :param request: The request
    :param authorization_info: Client authentication information
    :param get_client_id_from_token: Function that based on a token returns a client id.
    :return: dictionary containing client id, client authentication method and
        possibly access token.
    """

    # fixes request = {} instead of str
    # "AttributeError: 'dict' object has no attribute 'startswith'" in oidcendpoint/endpoint.py(
    # 158)client_authentication()
    if isinstance(authorization_info, dict):
        strings_parade = ("{} {}".format(k, v) for k, v in authorization_info.items())
        authorization_info = " ".join(strings_parade)

    # Two cases: either the information is in the request as claims or it's elsewhere.
    if authorization_info is None:
        if "client_id" in request and "client_secret" in request:
            auth_info = ClientSecretPost(endpoint_context).verify(request)
            auth_info["method"] = "client_secret_post"
        elif "client_assertion" in request:
            auth_info = JWSAuthnMethod(endpoint_context).verify(request, endpoint=endpoint)
            #  If symmetric key was used
            # auth_method = 'client_secret_jwt'
            #  If asymmetric key was used
            auth_info["method"] = "private_key_jwt"
        elif "access_token" in request:
            auth_info = BearerBody(endpoint_context).verify(request)
            auth_info["method"] = "bearer_body"
        else:
            raise UnknownOrNoAuthnMethod()
    else:
        if authorization_info.startswith("Basic "):
            auth_info = ClientSecretBasic(endpoint_context).verify(
                request, authorization_info
            )
            auth_info["method"] = "client_secret_basic"
        elif authorization_info.startswith("Bearer "):
            auth_info = BearerHeader(endpoint_context).verify(
                request, authorization_info
            )
            auth_info["method"] = "bearer_header"
        else:
            raise UnknownOrNoAuthnMethod(authorization_info)

    if also_known_as:
        client_id = also_known_as[auth_info.get("client_id")]
        auth_info["client_id"] = client_id
    else:
        client_id = auth_info.get("client_id")

    _token = auth_info.get("token")

    if client_id:
        if not client_id in endpoint_context.cdb:
            raise UnknownClient("Unknown Client ID")

        _cinfo = endpoint_context.cdb[client_id]
        if isinstance(_cinfo, str):
            if not _cinfo in endpoint_context.cdb:
                raise UnknownClient("Unknown Client ID")

        if not valid_client_info(_cinfo):
            logger.warning("Client registration has timed out")
            raise InvalidClient("Not valid client")

        # store what authn method was used
        if auth_info.get("method"):
            _request_type = request.__class__.__name__
            _used_authn_method = endpoint_context.cdb[client_id].get("auth_method")
            if _used_authn_method:
                endpoint_context.cdb[client_id]["auth_method"][_request_type] = auth_info["method"]
            else:
                endpoint_context.cdb[client_id]["auth_method"] = {
                    _request_type: auth_info["method"]
                }
    elif not client_id and get_client_id_from_token:
        if not _token:
            logger.warning("No token")
            raise ValueError("No token")

        try:
            # get_client_id_from_token is a callback... Do not abuse for code readability.
            auth_info["client_id"] = get_client_id_from_token(
                endpoint_context, _token, request
            )
        except KeyError:
            raise ValueError("Unknown token")

    return auth_info
