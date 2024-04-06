"""Module to render the template for the configured sites."""

import yaml
from pathlib import Path
import shutil
from jinja2 import Environment, FileSystemLoader
from loguru import logger

TEMPLATE_SRC: Path = Path("./template/src/")
CONF_PATH: Path = Path("./conf/config.yaml")
STATIC_PAGES_DIR: Path = Path("./static_pages")

if __name__ == "__main__":
    with open(CONF_PATH, "r") as conf_file:
        conf = yaml.safe_load(conf_file)

    for site in conf["sites"]:
        page_identifier = site["page_identifier"]
        logger.info(f"Rendering site: {page_identifier}")
        site_path: Path = STATIC_PAGES_DIR / page_identifier

        # recursive copy of template files to site directory
        shutil.copytree(TEMPLATE_SRC, site_path)

        # replace jinja variables in index.html
        env = Environment(loader=FileSystemLoader(site_path))
        template = env.get_template("index.html")
        rendered = template.render(**site)

        with open(site_path / "index.html", "w") as f:
            f.write(rendered)
