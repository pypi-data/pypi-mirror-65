# pylint: disable=too-few-public-methods

import sys
import urllib.parse

from http import HTTPStatus
from http.client import HTTPSConnection
from xmlrpc.client import SafeTransport, Transport, ServerProxy

import requests

from tcms_api.version import __version__

if sys.platform.startswith("win"):
    import winkerberos as kerberos  # pylint: disable=import-error
else:
    import kerberos  # pylint: disable=import-error

VERBOSE = 0


class CookieTransport(Transport):
    """A subclass of xmlrpc.client.Transport that supports cookies."""
    scheme = 'http'
    user_agent = 'tcms-api/%s' % __version__

    def __init__(self, use_datetime=False, use_builtin_types=False):
        super().__init__(use_datetime, use_builtin_types)
        self._cookies = []

    def send_headers(self, connection, headers):
        if self._cookies:
            connection.putheader("Cookie", "; ".join(self._cookies))
        super().send_headers(connection, headers)

    def parse_response(self, response):
        for header in response.msg.get_all("Set-Cookie", []):
            cookie = header.split(";", 1)[0]
            self._cookies.append(cookie)
        return super().parse_response(response)


class SafeCookieTransport(SafeTransport, CookieTransport):
    """SafeTransport subclass that supports cookies."""
    scheme = 'https'


# Taken from FreeIPA source freeipa-1.2.1/ipa-python/krbtransport.py
class KerbTransport(SafeCookieTransport):
    """Handles Kerberos Negotiation authentication to an XML-RPC server."""

    def get_host_info(self, host):
        host, extra_headers, x509 = Transport.get_host_info(self, host)

        # Set the remote host principal
        hostinfo = host.split(':')
        service = "HTTP@" + hostinfo[0]

        _result, context = kerberos.authGSSClientInit(service)
        kerberos.authGSSClientStep(context, "")

        extra_headers = [
            ("Authorization", "Negotiate %s" %
             kerberos.authGSSClientResponse(context))
        ]

        return host, extra_headers, x509

    def make_connection(self, host):
        """
            Return an individual HTTPS connection for each request.

            Fix https://bugzilla.redhat.com/show_bug.cgi?id=735937
        """
        chost, self._extra_headers, x509 = self.get_host_info(host)
        # Kiwi TCMS isn't ready to use HTTP/1.1 persistent connections,
        # so tell server current opened HTTP connection should be closed after
        # request is handled. And there will be a new connection for the next
        # request.
        self._extra_headers.append(('Connection', 'close'))
        self._connection = host, HTTPSConnection(  # nosec:B309:blacklist
            chost,
            None,
            **(x509 or {})
        )
        return self._connection[1]


def get_hostname(url):
    """
        Performs the same parsing of the URL as the Transport
        class and returns only the hostname which is used to
        generate the service principal name for Kiwi TCMS and
        the respective Authorize header!
    """
    _type, uri = urllib.parse.splittype(url)
    hostname, _path = urllib.parse.splithost(uri)
    return hostname


class TCMSXmlrpc:
    """
        XML-RPC client for username/password authentication.
    """
    session_cookie_name = 'sessionid'
    transport = None

    def __init__(self, username, password, url):
        if self.transport is None:
            if url.startswith('https://'):
                self.transport = SafeCookieTransport()
            elif url.startswith('http://'):
                self.transport = CookieTransport()
            else:
                raise Exception("Unrecognized URL scheme")

        self.server = ServerProxy(
            url,
            transport=self.transport,
            verbose=VERBOSE,
            allow_none=1
        )

        self.login(username, password, url)

    def login(
            self, username, password, url):  # pylint: disable=unused-argument
        """
            Login in the web app to save a session cookie in the cookie jar!
        """
        self.server.Auth.login(username, password)


class TCMSKerbXmlrpc(TCMSXmlrpc):
    """
        XML-RPC client for server deployed with python-social-auth-kerberos.

        Should also work for servers deployed with mod_auth_gssapi but
        that is not supported nor guaranteed!
    """
    transport = KerbTransport()

    def __init__(self, username, password, url):
        if not url.startswith('https://'):
            raise Exception("https:// required for GSSAPI authentication."
                            "URL provided: %s" % url)
        super().__init__(username, password, url)

    def login(self, username, password, url):
        url = url.replace('xml-rpc', 'login/kerberos')
        hostname = get_hostname(url)

        _, headers, _ = self.transport.get_host_info(hostname)
        # transport returns list of tuples but requests needs a dictionary
        headers = dict(headers)
        headers['User-Agent'] = self.transport.user_agent

        # note: by default will follow redirects
        with requests.sessions.Session() as session:
            response = session.get(url, headers=headers)
            assert response.status_code == HTTPStatus.OK
            self.transport._cookies.append(  # pylint: disable=protected-access
                self.session_cookie_name + '=' +
                session.cookies[self.session_cookie_name]
            )
