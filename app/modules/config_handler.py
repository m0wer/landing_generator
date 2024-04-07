from pathlib import Path

from modules.site_renderer import SiteRenderer
from watchdog.events import FileSystemEventHandler

TEMPLATE_SRC: Path = Path("./template/src/")
CONF_PATH: Path = Path("./conf/config.yaml")
STATIC_PAGES_DIR: Path = Path("./static_pages")


class ConfigHandler(FileSystemEventHandler):
    def __init__(self):
        self.site_renderer = SiteRenderer(CONF_PATH, TEMPLATE_SRC, STATIC_PAGES_DIR)

    def on_modified(self, event):
        if event.src_path == str(CONF_PATH):
            self.site_renderer.render_sites()
