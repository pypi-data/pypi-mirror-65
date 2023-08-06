#!/usr/bin/env python

import argparse
from zygoat.utils.files import repository_root, use_dir
from zygoat.utils.shell import run
from zygoat.constants import Projects
from zygoat.utils.printing import log
from zygoat.config import Config


def main(args):
    config = Config()
    with repository_root():
        with use_dir(Projects.BACKEND):
            log.info(f"Updating {args.environment} backend")
            run(["zappa", "update", args.environment])

            log.info(f"Running migrations for {args.environment}")
            run(["zappa", "manage", args.environment, "migrate"])

        with use_dir(Projects.FRONTEND):
            log.info(f"Updating {args.environment} frontend")
            run(["eb", "deploy", f"{config.name}-{args.environment}"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("environment")
    main(parser.parse_args())
