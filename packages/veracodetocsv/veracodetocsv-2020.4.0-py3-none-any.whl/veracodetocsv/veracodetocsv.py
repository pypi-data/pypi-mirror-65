# Purpose:  This script outputs one CSV file per scan per application profile visible in a Veracode platform account.
#           The CSV files can be imported into a SIEM tool such as Splunk. Configuration options are set in config.py
from __future__ import print_function
from __future__ import absolute_import

try:
    import importlib.util
except ImportError:
    import imp

import os
import re
import sys
import codecs
import argparse
import logging
from datetime import datetime

from veracodetocsv.helpers import log
from veracodetocsv.helpers import api
from veracodetocsv.helpers import unicodecsv
from veracodetocsv.helpers.data import DataLoader
from veracodetocsv.helpers.build import BuildTools
from veracodetocsv.helpers.exceptions import VeracodeError


class EmptyConfig(object):
    def __getattr__(self, name):
        raise AttributeError(name)


def main():
    parser = argparse.ArgumentParser(
        description="Outputs one CSV file per scan per application profile visible in a Veracode platform account")
    parser.add_argument("-c", "--config", help="Configuration file")
    parser.add_argument("-o", "--outputdir", help="Output directory")
    parser.add_argument("-a", "--appincludelist", help="Text file containing list of application profile names to include")
    parser.add_argument("-d", "--debug", help="Enable debug logging", action="store_true")
    args = parser.parse_args()

    if args.config:
        if sys.version_info >= (3, 5):
            spec = importlib.util.spec_from_file_location("config", args.config)
            config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config)
        else:
            config = imp.load_source("config", args.config)
    else:
        config = EmptyConfig()

    include_static_builds = getattr(config, "include_static_flaws", True)
    include_dynamic_builds = getattr(config, "include_dynamic_flaws", True)
    include_sandboxes = getattr(config, "include_sandboxes", True)
    include_csv_headers = getattr(config, "include_csv_headers", True)
    output_directory = args.outputdir if args.outputdir else getattr(config, "output_directory", "output")
    proxies = getattr(config, "proxies", None)
    debug_logging = args.debug if args.debug else getattr(config, "debug_logging", False)

    log.setup_logging(debug_logging)

    logging.log(logging.INFO, "Starting data download")
    print("Starting data download")

    if not (os.path.exists(output_directory) and
            os.path.exists(os.path.join(output_directory, "static")) and
            os.path.exists(os.path.join(output_directory, "dynamic"))):
        try:
            os.makedirs(os.path.join(output_directory, "static"))
            os.makedirs(os.path.join(output_directory, "dynamic"))
        except OSError:
            logging.exception("Cannot create output directory")
            print("Cannot create output directory, check log file for details.")
            sys.exit(2)

    try:
        build_tools = BuildTools()
    except VeracodeError:
        print("Error getting processed build history, check log file for details.")
        sys.exit(2)

    veracode_api = api.VeracodeAPI(proxies=proxies)
    data_loader = DataLoader(veracode_api, build_tools)

    app_include_list_file = args.appincludelist if args.appincludelist else getattr(config, "app_include_list", None)
    if app_include_list_file:
        try:
            with codecs.open(app_include_list_file, "r", "utf-8") as f:
                app_include_list = f.read().splitlines()
        except (IOError, UnicodeDecodeError):
            logging.exception("Error opening app include list file")
            print("Error opening app include list file, check log file for details.")
            sys.exit(2)
    else:
        app_include_list = []

    if len(app_include_list) > 0:
        print("{} applications in app include list".format(len(app_include_list)))

    try:
        data = data_loader.get_data(include_static_builds, include_dynamic_builds, app_include_list,
                                    include_sandboxes)
    except VeracodeError:
        print("Failed to get app data, check log file for details.")
        sys.exit(2)

    def make_filepath(app, build, sandbox=None):
        scan_type_output_directory = os.path.join(output_directory, build.type)
        clean_app_name = re.sub(r'(?u)[^-\w]', '', app.name.strip())
        now = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
        if sandbox is None:
            filename = "{}-{}-{}.csv".format(clean_app_name, build.id, now)
        else:
            filename = "{}-{}-{}-{}.csv".format(clean_app_name, sandbox.id, build.id, now)
        return os.path.join(scan_type_output_directory, filename)

    def process_build(app, build, sandbox=None):
        flaw_rows = []
        if include_csv_headers:
            flaw_rows.append(data_loader.get_headers(build.type, sandbox is not None))
        for flaw in build.flaws:
            if sandbox is None:
                flaw_rows.append(app.to_list() + build.to_list() + flaw.to_list())
            else:
                flaw_rows.append(app.to_list() + build.to_list() + flaw.to_list() + sandbox.to_list())
        filepath = make_filepath(app, build, sandbox)
        unicodecsv.create_csv(flaw_rows, filepath)
        build_tools.update_and_save_processed_builds_file(app.id, build.id, build.policy_updated_date)

    logging.log(logging.INFO, "Writing CSV files")
    print("Writing CSV files")

    for app in data:
        # Iterate over policy builds
        for build in app.builds:
            try:
                process_build(app, build)
            except VeracodeError:
                logging.exception("Failed to process build")

        # Iterate over sandbox builds
        if include_sandboxes:
            for sandbox in app.sandboxes:
                for build in sandbox.builds:
                    try:
                        process_build(app, build, sandbox)
                    except VeracodeError:
                        logging.exception("Failed to process build")


def run():
    try:
        main()
    except KeyboardInterrupt:
        print("\r\nExiting")


if __name__ == "__main__":
    run()
