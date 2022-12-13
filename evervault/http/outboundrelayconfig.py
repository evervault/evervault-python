import logging
from evervault.threading.repeatedtimer import RepeatedTimer

DEFAULT_POLL_INTERVAL = 5

logger = logging.getLogger(__name__)


class RelayOutboundConfig:

    request = None
    base_url = None
    debug_requests = False
    config_cache = None
    repeated_timer = None
    poll_interval = None

    def init(request, base_url, debug_requests=False):
        RelayOutboundConfig.request = request
        RelayOutboundConfig.base_url = base_url
        RelayOutboundConfig.debug_requests = debug_requests
        RelayOutboundConfig.poll_interval = DEFAULT_POLL_INTERVAL

        if RelayOutboundConfig.config_cache is None:
            RelayOutboundConfig.__get_relay_outbound_config()

        if RelayOutboundConfig.repeated_timer is None:
            RelayOutboundConfig.repeated_timer = RepeatedTimer(
                RelayOutboundConfig.poll_interval,
                RelayOutboundConfig.__get_relay_outbound_config,
            )

    def get_decryption_domains() -> list:
        return RelayOutboundConfig.config_cache

    def get_poll_interval() -> list:
        return RelayOutboundConfig.repeated_timer.get_interval()

    def disable_polling():
        if RelayOutboundConfig.repeated_timer is not None:
            RelayOutboundConfig.repeated_timer.stop()
            RelayOutboundConfig.repeated_timer = None

    def clear_cache():
        RelayOutboundConfig.config_cache = None

    def __get_relay_outbound_config():
        logger.debug("EVERVAULT :: Retrieving Outbound Relay Config from API")
        res = RelayOutboundConfig.request.make_request(
            "GET", RelayOutboundConfig.base_url + "v2/relay-outbound"
        )
        poll_interval = res.headers["X-Poll-Interval"]
        if poll_interval is not None:
            RelayOutboundConfig.poll_interval = float(poll_interval)
            if RelayOutboundConfig.repeated_timer is not None:
                RelayOutboundConfig.repeated_timer.update_interval(
                    RelayOutboundConfig.poll_interval
                )
        RelayOutboundConfig.config_cache = list(
            map(
                lambda destination: destination["destinationDomain"],
                res.parsed_body["outboundDestinations"].values(),
            )
        )
