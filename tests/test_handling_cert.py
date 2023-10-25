import unittest
from unittest.mock import patch

import requests_mock

from evervault.http.requestintercept import RequestIntercept
from evervault.http.request import Request
from evervault.services.timeservice import TimeService


class TestHandlingCerts(unittest.TestCase):
    @requests_mock.Mocker()
    def test_cert_is_expired(self, mock_request):
        mock_request.get(
            "https://ca.evervault.com",
            text="-----BEGIN CERTIFICATE-----\n"
            "MIIDgzCCAmugAwIBAgIUEL9SyDnNVvLXq8opJM2nrLgoFpgwDQYJKoZIhvcNAQEL\n"
            "BQAwUTELMAkGA1UEBhMCSUUxEzARBgNVBAgMCkR1YmxpbiBDby4xDzANBgNVBAcM\n"
            "BlN3b3JkczEcMBoGA1UECgwTRGVmYXVsdCBDb21wYW55IEx0ZDAeFw0wODEyMjQw\n"
            "ODE2MDhaFw0wOTAxMDMwODE2MDhaMFExCzAJBgNVBAYTAklFMRMwEQYDVQQIDApE\n"
            "dWJsaW4gQ28uMQ8wDQYDVQQHDAZTd29yZHMxHDAaBgNVBAoME0RlZmF1bHQgQ29t\n"
            "cGFueSBMdGQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDoCOTOgSCf\n"
            "wsbSefJQwu51Krbz9jTFic4tbaM3B2BROtqAxDHdDIE5HQ1nhuZ06XyL9aLjDI2J\n"
            "9WOWTkN/iXh0XcUJmIlBgErs7EQbIeXjO6pTa4S+tjBtbnVF8Aaz2Bj2AuD4O9VJ\n"
            "AP8HmS654dOWjhqnEsRbv9IJo+ccvy699afWsoYePILZOJmoeiGXvQ/ZTbj4cYDx\n"
            "CxZOkYK5HK3Zv0VfK5B+hsz3buuijkPdIG46o6DAE2nmNjrTxaz1/BuiWDEvC8RK\n"
            "8NOY92LoiDMSxWVP2/UDDsKqWlGS7KmpdmIx1ndH6eYyYJut5xvLE7vlkr6s96O2\n"
            "AN5EQ28oQNNHAgMBAAGjUzBRMB0GA1UdDgQWBBQDqdmoCx8KJdc6giTS69YtlAsc\n"
            "vDAfBgNVHSMEGDAWgBQDqdmoCx8KJdc6giTS69YtlAscvDAPBgNVHRMBAf8EBTAD\n"
            "AQH/MA0GCSqGSIb3DQEBCwUAA4IBAQAiBFVUOI07QOVbMAMWNk5D3L308wx6avqI\n"
            "4FY6aSfmIGp898ab6L3XOrz54ztOuIyjdUaQ8/U1yFGxTBe66zPKDyorHm0a+kNp\n"
            "2h5luIXRsm6IZrpGblO7CD+ZzYZ04qWkHgugLSieKhO3GVKObdkdfnJIf2O5KW7j\n"
            "PulHfTQ3MNd/qXhOBNUXgI0rcWeI5xGKzAVWRoiAcAHU9UmNrunVg9CQMh0i6nYA\n"
            "i7xFTBvY5QrZGK/Y6mEAdGCRoGusOputz1MHn721sIyH5DtCAMXdJ/s94Ki7m557\n"
            "qLZdvkgx0KBRnP/JPZ55VgjZ8ipH9+SGxsZeTg9sX6nw+x/Plncz\n"
            "-----END CERTIFICATE-----\n",
        )

        base_url_default = "https://api.evervault.com/"
        ca_host_default = "https://ca.evervault.com"

        app_uuid = "testapp"
        api_key = "testing"

        request = Request(app_uuid, api_key, 30, False)
        time_service = TimeService()

        cert = RequestIntercept(
            request,
            ca_host_default,
            base_url_default,
            api_key,
            api_key,
            time_service,
        )

        cert.setup()

        assert cert.is_certificate_expired()

    @requests_mock.Mocker()
    def test_not_available_cert_is_not_expired(self, mock_request):
        mock_request.get("https://ca.evervault.com", text="")
        base_url_default = "https://api.evervault.com/"
        ca_host_default = "https://ca.evervault.com"

        app_uuid = "testapp"
        api_key = "testing"

        request = Request(app_uuid, api_key, 30, False)

        time_service = TimeService()

        cert = RequestIntercept(
            request,
            ca_host_default,
            base_url_default,
            api_key,
            api_key,
            time_service,
        )
        cert.setup()

        assert cert.is_certificate_expired() is False

    @requests_mock.Mocker()
    def test_updated_cert_keeps_path_changes_timestamp(self, mock_request):
        mock_request.get(
            "https://ca.evervault.com",
            text="-----BEGIN CERTIFICATE-----\n"
            "MIIDgzCCAmugAwIBAgIUEL9SyDnNVvLXq8opJM2nrLgoFpgwDQYJKoZIhvcNAQEL\n"
            "BQAwUTELMAkGA1UEBhMCSUUxEzARBgNVBAgMCkR1YmxpbiBDby4xDzANBgNVBAcM\n"
            "BlN3b3JkczEcMBoGA1UECgwTRGVmYXVsdCBDb21wYW55IEx0ZDAeFw0wODEyMjQw\n"
            "ODE2MDhaFw0wOTAxMDMwODE2MDhaMFExCzAJBgNVBAYTAklFMRMwEQYDVQQIDApE\n"
            "dWJsaW4gQ28uMQ8wDQYDVQQHDAZTd29yZHMxHDAaBgNVBAoME0RlZmF1bHQgQ29t\n"
            "cGFueSBMdGQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDoCOTOgSCf\n"
            "wsbSefJQwu51Krbz9jTFic4tbaM3B2BROtqAxDHdDIE5HQ1nhuZ06XyL9aLjDI2J\n"
            "9WOWTkN/iXh0XcUJmIlBgErs7EQbIeXjO6pTa4S+tjBtbnVF8Aaz2Bj2AuD4O9VJ\n"
            "AP8HmS654dOWjhqnEsRbv9IJo+ccvy699afWsoYePILZOJmoeiGXvQ/ZTbj4cYDx\n"
            "CxZOkYK5HK3Zv0VfK5B+hsz3buuijkPdIG46o6DAE2nmNjrTxaz1/BuiWDEvC8RK\n"
            "8NOY92LoiDMSxWVP2/UDDsKqWlGS7KmpdmIx1ndH6eYyYJut5xvLE7vlkr6s96O2\n"
            "AN5EQ28oQNNHAgMBAAGjUzBRMB0GA1UdDgQWBBQDqdmoCx8KJdc6giTS69YtlAsc\n"
            "vDAfBgNVHSMEGDAWgBQDqdmoCx8KJdc6giTS69YtlAscvDAPBgNVHRMBAf8EBTAD\n"
            "AQH/MA0GCSqGSIb3DQEBCwUAA4IBAQAiBFVUOI07QOVbMAMWNk5D3L308wx6avqI\n"
            "4FY6aSfmIGp898ab6L3XOrz54ztOuIyjdUaQ8/U1yFGxTBe66zPKDyorHm0a+kNp\n"
            "2h5luIXRsm6IZrpGblO7CD+ZzYZ04qWkHgugLSieKhO3GVKObdkdfnJIf2O5KW7j\n"
            "PulHfTQ3MNd/qXhOBNUXgI0rcWeI5xGKzAVWRoiAcAHU9UmNrunVg9CQMh0i6nYA\n"
            "i7xFTBvY5QrZGK/Y6mEAdGCRoGusOputz1MHn721sIyH5DtCAMXdJ/s94Ki7m557\n"
            "qLZdvkgx0KBRnP/JPZ55VgjZ8ipH9+SGxsZeTg9sX6nw+x/Plncz\n"
            "-----END CERTIFICATE-----\n",
        )

        base_url_default = "https://api.evervault.com/"
        ca_host_default = "https://ca.evervault.com"

        app_uuid = "testapp"
        api_key = "testing"

        request = Request(app_uuid, api_key, 30, False)

        time_service = TimeService()

        cert = RequestIntercept(
            request,
            ca_host_default,
            base_url_default,
            api_key,
            api_key,
            time_service,
        )
        cert.setup()

        original_cert_path = cert.cert_path
        original_cert_expire_date = cert.expire_date

        mock_request.get(
            "https://ca.evervault.com",
            text="-----BEGIN CERTIFICATE-----\n"
            "MIIDgTCCAmmgAwIBAgIUZxUXJ7UgViht43KnCbgcYVBZJVwwDQYJKoZIhvcNAQEL\n"
            "BQAwUDELMAkGA1UEBhMCSUUxEjAQBgNVBAgMCUR1YmxpbiBDbzEPMA0GA1UEBwwG\n"
            "U3dvcmRzMRwwGgYDVQQKDBNEZWZhdWx0IENvbXBhbnkgTHRkMB4XDTEwMTIyNDA4\n"
            "MTU1NFoXDTExMDEwMzA4MTU1NFowUDELMAkGA1UEBhMCSUUxEjAQBgNVBAgMCUR1\n"
            "YmxpbiBDbzEPMA0GA1UEBwwGU3dvcmRzMRwwGgYDVQQKDBNEZWZhdWx0IENvbXBh\n"
            "bnkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoxC4j0d+iazR\n"
            "jnjHar3DRQQSuRlbb+XBKnWUJKibESikZ5bT8lUTTVlrBk53g3z1xlQ45Y3iBMfc\n"
            "B2JnUq0CKcka9Hdcf1WDHsvFFNl7q0YsZW/phMrq7xWSSdRjv2KacQUiVGbAG4ea\n"
            "LNy3b1BvnW2GR4uJbDYxePl4mik8hdBIPuEfRUjcxBe4RSMStEDQ+1fbqrgp8qUn\n"
            "rHJyMzJOD1OzyKY39derreAQp/VeUeZhfvufnOLcpfr8j/G78W5FKeHr03uyVtec\n"
            "2/aAoZdCIwnSdZ2o2Er8HbNpjB13Vhzr3FCXMxtF+/8ODLhggUYA7tADZ78yhmvU\n"
            "ApAHEtP0BwIDAQABo1MwUTAdBgNVHQ4EFgQUX5G/150Ma37PkdzvvdI+zRlxHYEw\n"
            "HwYDVR0jBBgwFoAUX5G/150Ma37PkdzvvdI+zRlxHYEwDwYDVR0TAQH/BAUwAwEB\n"
            "/zANBgkqhkiG9w0BAQsFAAOCAQEAWxc4uYoLbVjSscnGevLM3TBdz4G0ww27+zvg\n"
            "561f7WtHUxRDw99ayUzp+K6/0FXiwGvMne6i16Qhnfa9OFO78oPd6BkxMhMWrMaV\n"
            "p2iYaQutXPB47vvq9OgTMCrUMuhy2e9Wkm4qVRb09rXgkLL2PWuZH2h6hI1ahjPt\n"
            "UpL2gjfRFUi9+V9iU11K4+t79N270jGrdHhhNCS8c6zm70qt67DcgunfvOzKAa8U\n"
            "QbIQJBpqQvhz3WKWOBhesua5g9f66GsEQsSv+TSN3NSEytR9KFS+HBLPI5UIoL2L\n"
            "es4FxviSu5lEdwzfsp4EhjoQ8TutVPdwP/W2T7b2xKkiAXDsug==\n"
            "-----END CERTIFICATE-----\n",
        )

        cert.setup()

        assert original_cert_path != cert.cert_path
        assert original_cert_expire_date != cert.expire_date

    @requests_mock.Mocker()
    @patch("evervault.services.timeservice.TimeService")
    def test_current_date_before_cert_validation_requires_update(
        self, mock_request, time_service
    ):
        mock_request.get(
            "https://ca.evervault.com",
            text="-----BEGIN CERTIFICATE-----\n"
            "MIIDgzCCAmugAwIBAgIUEL9SyDnNVvLXq8opJM2nrLgoFpgwDQYJKoZIhvcNAQEL\n"
            "BQAwUTELMAkGA1UEBhMCSUUxEzARBgNVBAgMCkR1YmxpbiBDby4xDzANBgNVBAcM\n"
            "BlN3b3JkczEcMBoGA1UECgwTRGVmYXVsdCBDb21wYW55IEx0ZDAeFw0wODEyMjQw\n"
            "ODE2MDhaFw0wOTAxMDMwODE2MDhaMFExCzAJBgNVBAYTAklFMRMwEQYDVQQIDApE\n"
            "dWJsaW4gQ28uMQ8wDQYDVQQHDAZTd29yZHMxHDAaBgNVBAoME0RlZmF1bHQgQ29t\n"
            "cGFueSBMdGQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDoCOTOgSCf\n"
            "wsbSefJQwu51Krbz9jTFic4tbaM3B2BROtqAxDHdDIE5HQ1nhuZ06XyL9aLjDI2J\n"
            "9WOWTkN/iXh0XcUJmIlBgErs7EQbIeXjO6pTa4S+tjBtbnVF8Aaz2Bj2AuD4O9VJ\n"
            "AP8HmS654dOWjhqnEsRbv9IJo+ccvy699afWsoYePILZOJmoeiGXvQ/ZTbj4cYDx\n"
            "CxZOkYK5HK3Zv0VfK5B+hsz3buuijkPdIG46o6DAE2nmNjrTxaz1/BuiWDEvC8RK\n"
            "8NOY92LoiDMSxWVP2/UDDsKqWlGS7KmpdmIx1ndH6eYyYJut5xvLE7vlkr6s96O2\n"
            "AN5EQ28oQNNHAgMBAAGjUzBRMB0GA1UdDgQWBBQDqdmoCx8KJdc6giTS69YtlAsc\n"
            "vDAfBgNVHSMEGDAWgBQDqdmoCx8KJdc6giTS69YtlAscvDAPBgNVHRMBAf8EBTAD\n"
            "AQH/MA0GCSqGSIb3DQEBCwUAA4IBAQAiBFVUOI07QOVbMAMWNk5D3L308wx6avqI\n"
            "4FY6aSfmIGp898ab6L3XOrz54ztOuIyjdUaQ8/U1yFGxTBe66zPKDyorHm0a+kNp\n"
            "2h5luIXRsm6IZrpGblO7CD+ZzYZ04qWkHgugLSieKhO3GVKObdkdfnJIf2O5KW7j\n"
            "PulHfTQ3MNd/qXhOBNUXgI0rcWeI5xGKzAVWRoiAcAHU9UmNrunVg9CQMh0i6nYA\n"
            "i7xFTBvY5QrZGK/Y6mEAdGCRoGusOputz1MHn721sIyH5DtCAMXdJ/s94Ki7m557\n"
            "qLZdvkgx0KBRnP/JPZ55VgjZ8ipH9+SGxsZeTg9sX6nw+x/Plncz\n"
            "-----END CERTIFICATE-----\n",
        )

        base_url_default = "https://api.evervault.com/"
        ca_host_default = "https://ca.evervault.com"

        app_uuid = "testapp"
        api_key = "testing"

        request = Request(app_uuid, api_key, 30, False)

        time_service.get_datetime_now.return_value = 1171894763

        cert = RequestIntercept(
            request,
            ca_host_default,
            base_url_default,
            api_key,
            api_key,
            time_service,
        )

        cert.setup()

        assert cert.is_certificate_expired()
