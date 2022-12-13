import logging
from evervault.threading.repeatedtimer import RepeatedTimer

DEFAULT_POLL_INTERVAL = 5

logger = logging.getLogger(__name__)


class OutboundRelayConfig:

    request = None
    base_url = None
    debug_requests = False
    config_cache = None
    repeated_timer = None
    poll_interval = None

    def init(request, base_url, debug_requests=False):
        OutboundRelayConfig.request = request
        OutboundRelayConfig.base_url = base_url
        OutboundRelayConfig.debug_requests = debug_requests
        OutboundRelayConfig.poll_interval = DEFAULT_POLL_INTERVAL

        if OutboundRelayConfig.config_cache is None:
            OutboundRelayConfig.__get_relay_outbound_config()

        if OutboundRelayConfig.repeated_timer is None:
            OutboundRelayConfig.repeated_timer = RepeatedTimer(
                OutboundRelayConfig.poll_interval,
                OutboundRelayConfig.__get_relay_outbound_config,
            )

    def get_decryption_domains() -> list:
        return OutboundRelayConfig.config_cache

    def get_poll_interval() -> list:
        return OutboundRelayConfig.repeated_timer.get_interval()

    def disable_polling():
        if OutboundRelayConfig.repeated_timer is not None:
            OutboundRelayConfig.repeated_timer.stop()
            OutboundRelayConfig.repeated_timer = None

    def clear_cache():
        OutboundRelayConfig.config_cache = None

    def __get_relay_outbound_config():
        logger.debug("EVERVAULT :: Retrieving Outbound Relay Config from API")
        res = OutboundRelayConfig.request.make_request(
            "GET", OutboundRelayConfig.base_url + "v2/relay-outbound"
        )
        poll_interval = res.headers["X-Poll-Interval"]
        if poll_interval is not None:
            OutboundRelayConfig.poll_interval = float(poll_interval)
            if OutboundRelayConfig.repeated_timer is not None:
                OutboundRelayConfig.repeated_timer.update_interval(
                    OutboundRelayConfig.poll_interval
                )
        OutboundRelayConfig.config_cache = list(
            map(
                lambda destination: destination["destinationDomain"],
                res.parsed_body["outboundDestinations"].values(),
            )
        )
