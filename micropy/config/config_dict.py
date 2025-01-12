# -*- coding: utf-8 -*-

from .config_source import ConfigSource


class DictConfigSource(ConfigSource):

    def __init__(self, config: dict = {}):
        """Dict Config Source.

        Args:
            config (dict, optional): Initial Config.
                Defaults to {}.

        """
        super().__init__(initial_config=config)

    def process(self) -> dict:
        return {}

    def prepare(self):
        return super().prepare()

    def save(self, content: dict) -> dict:
        return content
