"""Module to render the template for the configured sites."""

import os
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from loguru import logger

TEMPLATE_SRC: Path = Path("./template/src/")
CONF_PATH: Path = Path("./conf/config.yaml")
STATIC_PAGES_DIR: Path = Path("./static_pages")


class SiteRenderer:
    def __init__(self, conf_path: Path, template_src: Path, static_pages_dir: Path):
        self.conf_path = conf_path
        self.template_src = template_src
        self.static_pages_dir = static_pages_dir

    def render_site(self, site: dict) -> None:
        page_identifier = site["page_identifier"]
        logger.info(f"Rendering site: {page_identifier}")
        site_path: Path = self.static_pages_dir / page_identifier

        # recursive copy of template files to site directory
        if os.path.exists(site_path):
            shutil.rmtree(site_path)
        shutil.copytree(self.template_src, site_path)

        # replace jinja variables in index.html
        env = Environment(loader=FileSystemLoader(site_path))
        template = env.get_template("index.html")
        rendered = template.render(**site)

        with open(site_path / "index.html", "w") as f:
            f.write(rendered)

    def render_sites(self) -> None:
        with open(self.conf_path, "r") as conf_file:
            conf = yaml.safe_load(conf_file)

        for site in conf["sites"]:
            self.render_site(site)


if __name__ == "__main__":
    SiteRenderer(CONF_PATH, TEMPLATE_SRC, STATIC_PAGES_DIR).render_sites()
