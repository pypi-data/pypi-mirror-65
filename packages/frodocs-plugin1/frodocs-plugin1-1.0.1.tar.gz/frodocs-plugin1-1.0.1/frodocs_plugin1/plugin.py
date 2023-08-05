from frodocs.config import config_options, Config
from frodocs.plugins import BasePlugin
from frodocs.structure.files import Files
from frodocs.structure.nav import Navigation as FrodocsNavigation

from .navigation import AwesomeNavigation
from .options import Options


class FrodocsPlugin1(BasePlugin):

    DEFAULT_META_FILENAME = '.pages'

    config_scheme = (
        ('filename', config_options.Type(str, default=DEFAULT_META_FILENAME)),
        ('collapse_single_pages', config_options.Type(bool, default=False)),
        ('strict', config_options.Type(bool, default=True))
    )

    def on_nav(self, nav: ForocsNavigation, config: Config, files: Files):
        return AwesomeNavigation(nav, Options(**self.config)).to_frodocs()
