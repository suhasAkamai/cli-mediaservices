# Python edgegrid module - CONFIG for ImgMan CLI module
""" Copyright 2017 Akamai Technologies, Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.

 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import sys
import os
import argparse
import logging

if sys.version_info[0] >= 3:
    # python3
    from configparser import ConfigParser
    import http.client as http_client
else:
    # python2.7
    from ConfigParser import ConfigParser
    import httplib as http_client

PACKAGE_VERSION = "0.1.8"

logger = logging.getLogger(__name__)


class EdgeGridConfig():

    parser = argparse.ArgumentParser(description='Process command line options.')

    def __init__(self, config_values, configuration, flags=None):
        parser = self.parser
        parser.add_argument('--verbose', '-v', default=False, action='count', help=' Verbose mode')
        parser.add_argument('--debug', '-d', default=False, action='count',
                            help=' Debug mode (prints HTTP headers)')
        parser.add_argument('--edgerc', '-e', default='~/.edgerc', metavar='credentials_file',
                            help=' Location of the credentials file (default is ~/.edgerc)')
        parser.add_argument('--section', '-c', default='mediaservices', metavar='credentials_file_section',
                            action='store', help=' Credentials file Section\'s name to use')
        parser.add_argument('--accountSwitchKey', '-a', metavar='Account Switch Key',
                            action='store', help=' Switch key to different account')

        subparsers = parser.add_subparsers(help='commands', dest="command")

        list_domains_parser = subparsers.add_parser("list-domains", help="List all Domains")
        list_domains_parser.add_argument('--output-type', '-t', default='text', choices=[
                                         'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        list_streams_parser = subparsers.add_parser("list-streams", help="List all Streams.")
        list_streams_parser.add_argument(
            'domainName', help="Domain Name for which streams has to be fetched.", action='store')
        list_streams_parser.add_argument('--output-type', '-t', default='text', choices=[
                                         'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        list_events_parser = subparsers.add_parser("list-events", help="List all Events.")
        list_events_parser.add_argument(
            'domainName', help="Domain Name for which streams has to be fetched.", action='store')
        list_events_parser.add_argument(
            'streamId', help="Stream Id for which events has to be fetched.", action='store')
        list_events_parser.add_argument('--output-type', '-t', default='text', choices=[
                                        'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        list_rtmp_config_parser = subparsers.add_parser(
            "list-rtmp-configs", help="List all RTMP Configs.")
        list_rtmp_config_parser.add_argument('--output-type', '-t', default='text', choices=[
                                             'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        list_rtmp_streams_parser = subparsers.add_parser(
            "list-rtmp-streams", help="List all RTMP Streams.")
        list_rtmp_streams_parser.add_argument('--output-type', '-t', default='text', choices=[
                                              'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        list_storage_group_parser = subparsers.add_parser(
            "list-storage-group", help="List all Storage Groups.")
        list_storage_group_parser.add_argument('--output-type', '-t', default='text', choices=[
                                               'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        get_domain_parser = subparsers.add_parser("get-domain", help="Get Domain.")
        get_domain_parser.add_argument(
            'domain', help="Domain Name for which info has to be fetched.", action='store')
        get_domain_parser.add_argument('--output-type', '-t', default='text', choices=[
                                       'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        get_stream_parser = subparsers.add_parser("get-stream", help="Get Stream.")
        get_stream_parser.add_argument('domain', help="Domain Name", action='store')
        get_stream_parser.add_argument('streamid', help="Stream Id", action='store')
        get_stream_parser.add_argument('--output-type', '-t', default='text', choices=[
                                       'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        get_event_parser = subparsers.add_parser("get-event", help="Get Event.")
        get_event_parser.add_argument('domain', help="Domain Name", action='store')
        get_event_parser.add_argument('streamid', help="Stream Id", action='store')
        get_event_parser.add_argument('eventname', help="Stream Id", action='store')
        get_event_parser.add_argument('--output-type', '-t', default='text', choices=[
                                      'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        get_rtmp_config_parser = subparsers.add_parser("get-rtmp-config", help="Get RTMP Config.")
        get_rtmp_config_parser.add_argument(
            'cp-code', help="CP Code of the RTMP Config to be fetched.", action='store')
        get_rtmp_config_parser.add_argument('--output-type', '-t', default='text', choices=[
                                            'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        get_rtmp_stream_parser = subparsers.add_parser("get-rtmp-stream", help="Get RTMP Stream.")
        get_rtmp_stream_parser.add_argument(
            'streamid', help="Stream id of the RTMP Stream", action='store')
        get_rtmp_stream_parser.add_argument('--output-type', '-t', default='text', choices=[
                                            'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        list_msl_streams_parser = subparsers.add_parser(
            "list-msl-streams", help="List all MSL Streams.")
        list_msl_streams_parser.add_argument('--output-type', '-t', default='text', choices=[
                                             'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        get_msl_stream_parser = subparsers.add_parser(
            "get-msl-streams", help="Get MSL Stream details.")
        get_msl_stream_parser.add_argument('streamid', help="Stream Id", action='store')
        get_msl_stream_parser.add_argument('--output-type', '-t', default='text', choices=[
            'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        get_cdn_list_parser = subparsers.add_parser("list-CDNs", help="Get list of CDN's")
        get_cdn_list_parser.add_argument('--output-type', '-t', default='text', choices=[
            'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        get_cpcode_list_parser = subparsers.add_parser("list-cpcodes", help="Get list of cpcodes")
        get_cpcode_list_parser.add_argument('--type', default='INGEST', choices=[
            'INGEST', 'STORAGE', 'DELIVERY'], help='Identify the cpcode type')
        get_cpcode_list_parser.add_argument('--unused', default='true', choices=[
            'true', 'false'], help=' lists only CP codes that have not already been used to provision an origin')
        get_cpcode_list_parser.add_argument('--output-type', '-t', default='text', choices=[
            'json', 'text'], metavar='json/text', help=' Output type {json, text}. Default is text')

        if flags:
            for argument in flags.keys():
                parser.add_argument('--' + argument, action=flags[argument])

        arguments = {}
        for argument in config_values:
            if config_values[argument]:
                if config_values[argument] == "False" or config_values[argument] == "True":
                    parser.add_argument('--' + argument, action='count')
                parser.add_argument('--' + argument)
                arguments[argument] = config_values[argument]

        try:
            args = parser.parse_args()
        except:
            sys.exit()

        arguments = vars(args)

        if arguments['debug']:
            http_client.HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

        if "section" in arguments and arguments["section"]:
            configuration = arguments["section"]

        arguments["edgerc"] = os.path.expanduser(arguments["edgerc"])

        if os.path.isfile(arguments["edgerc"]):
            config = ConfigParser()
            config.readfp(open(arguments["edgerc"]))
            if not config.has_section(configuration):
                err_msg = "ERROR: No section named %s was found in your %s file\n" % (
                    configuration, arguments["edgerc"])
                err_msg += "ERROR: Please generate credentials for the script functionality\n"
                err_msg += "ERROR: and run 'python gen_edgerc.py %s' to generate the credential file\n" % configuration
                sys.exit(err_msg)
            for key, value in config.items(configuration):
                # ConfigParser lowercases magically
                if key not in arguments or arguments[key] is None:
                    arguments[key] = value
                else:
                    print("Missing configuration file.  Run python gen_edgerc.py to get your credentials file set up once you've provisioned credentials in LUNA.")
                    return None

        for option in arguments:
            setattr(self, option, arguments[option])

        self.create_base_url()

    def create_base_url(self):
        self.base_url = "https://%s" % self.host
