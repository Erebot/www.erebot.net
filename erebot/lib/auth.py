"""Example of a simplistic, importable authenticator plugin

Intended to work like a quick-started SQLAlchemy plugin"""
from zope.interface import implements
from repoze.who.interfaces import IIdentifier, IAuthenticator

from repoze.who.plugins.sa import (
    SQLAlchemyAuthenticatorPlugin,
    SQLAlchemyUserMDPlugin,
)
from repoze.what.plugins.sql import configure_sql_adapters
from repoze.what.middleware import AuthorizationMetadata

from erebot import model
auth_plugin = SQLAlchemyAuthenticatorPlugin(model.User, model.DBSession)
md_plugin = SQLAlchemyUserMDPlugin(model.User, model.DBSession )
_source_adapters = configure_sql_adapters(
    model.User,
    model.Group,
    model.Permission,
    model.DBSession,
)
md_group_plugin = AuthorizationMetadata(
    {'sqlauth': _source_adapters['group']},
    {'sqlauth': _source_adapters['permission']},
)

class CertificatePlugin(object):
    implements(IIdentifier, IAuthenticator)

    def __init__(self, validity_header, identity_header, login_field):
        self.validity_header = validity_header
        self.identity_header = identity_header
        self.login_field = login_field

    def __adapt(self, header):
        return 'HTTP_' + header.replace('-', '_').upper()

    def __validate(self, environ):
        return environ.get(self.__adapt(self.validity_header))

    def __check(self, identity):
        return self.login_field in identity and \
            len(identity[self.login_field]) == 1

    def identify(self, environ):
        if not self.__validate(environ):
            return None
        cert = environ.get(self.__adapt(self.identity_header))
        if not cert or not cert.startswith('/'):
            return None
        cert = cert[1:]

        result = {}
        for part in cert.split('/'):
            key, sep, value = part.partition('=')
            if not sep:
                return None
            if key not in result:
                result[key] = []
            result[key].append(value)

        if not self.__check(result):
            return None

        result['login'] = result[self.login_field][0]
        return result

    def remember(self, environ, identity):
        pass

    def forget(self, environ, identity):
        pass

    def authenticate(self, environ, identity):
        if not self.__validate(environ):
            return None
        if not 'login' in identity:
            return None

        if not self.__check(identity) or \
            identity['login'] != identity[self.login_field][0]:
            return None

        return identity['login']

# THIS IS CRITICALLY IMPORTANT!  Without this your site will
# consider every repoze.what predicate True!
from repoze.what.plugins.pylonshq import booleanize_predicates
booleanize_predicates()

