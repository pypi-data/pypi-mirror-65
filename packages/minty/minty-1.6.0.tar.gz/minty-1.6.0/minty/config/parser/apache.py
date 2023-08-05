from .base import ConfigParserBase
from apacheconfig import make_loader
from typing import Dict


class ApacheConfigParser(ConfigParserBase):
    __slots__ = ["content"]

    def parse(self, content: str) -> Dict:
        """Return a dict with the parsed config.

        :return: Parsed configuration
        :rtype: dict
        """
        preparsed_content = super().parse(content)

        if preparsed_content["content"] == "":
            raise ValueError("Cannot parse empty configuration")

        # statsd configuration needs to be loaded before it can be used,
        # so we can't measure the loading easily
        with make_loader() as loader:
            config = loader.loads(content)

        if "statsd" in config:
            self.statsd.get_counter().increment("parse")

        return config
