# Python edgegrid module
""" Copyright 2015 Akamai Technologies, Inc. All Rights Reserved.

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

from __future__ import print_function
import sys
import os
import logging
import random
import re
import requests
import json
import urllib
import texttable as tt
from future import standard_library
from future.builtins import next
from future.builtins import object
from http_calls import EdgeGridHttpCaller
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from config import EdgeGridConfig
from subprocess import call
standard_library.install_aliases()
if sys.version_info[0] >= 3:
    # python3
    from urllib import parse
else:
    # python2.7
    import urlparse as parse

logger = logging.getLogger(__name__)

session = requests.Session()
debug = False
verbose = False
cache = False
format = "json"
section_name = "default"

# If all parameters are set already, use them.  Otherwise
# use the config
config = EdgeGridConfig({"verbose": False}, section_name)

if hasattr(config, "debug") and config.debug:
    debug = True

if hasattr(config, "verbose") and config.verbose:
    verbose = True

if hasattr(config, "cache") and config.cache:
    cache = True


# Set the config options
session.auth = EdgeGridAuth(
    client_token=config.client_token,
    client_secret=config.client_secret,
    access_token=config.access_token
)

if hasattr(config, 'headers'):
    session.headers.update(config.headers)

session.headers.update({'User-Agent': "AkamaiCLI"})

baseurl_prd = '%s://%s/' % ('https', config.host)
prdHttpCaller = EdgeGridHttpCaller(session, debug, verbose, baseurl_prd)


def listDomains(accountSwitchKey=None):
    """ List the Domains associated with the account """

    listDomainsEndpoint = '/config-media-live/v1/live'
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey}
        domainList = prdHttpCaller.getResult(listDomainsEndpoint, params)
    else:
        domainList = prdHttpCaller.getResult(listDomainsEndpoint)
    return domainList


def listStreams(domainName, accountSwitchKey=None):
    """ List the Streams associated with the account """

    listStreamsEndpoint = '/config-media-live/v1/live/{domain}/stream'.format(domain=domainName)
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey}
        streamList = prdHttpCaller.getResult(listStreamsEndpoint, params)
    else:
        streamList = prdHttpCaller.getResult(listStreamsEndpoint)
    return streamList


def listEvents(domainName, streamId, accountSwitchKey=None):
    """ List the Events associated with the account """
    listEventsEndpoint = '/config-media-live/v1/live/{domain}/stream/{streamId}/event'.format(
        domain=domainName, streamId=streamId)
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey}
        eventList = prdHttpCaller.getResult(listEventsEndpoint, params)
    else:
        eventList = prdHttpCaller.getResult(listEventsEndpoint)
    print(eventList)
    return eventList


def listRTMPConfigs(accountSwitchKey=None):
    """ List the RTMP Configs associated with the account """
    listRTMPConfigsEndpoint = '/config-media-live/v1/live/rtmp/configuration'
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey}
        rtmpConfigList = prdHttpCaller.getResult(listRTMPConfigsEndpoint, params)
    else:
        rtmpConfigList = prdHttpCaller.getResult(listRTMPConfigsEndpoint)
    return(rtmpConfigList)


def listRTMPStreams(accountSwitchKey=None):
    """ List the RTMP Streams associated with the account """
    listRTMPStreamsEndpoint = '/config-media-live/v1/live/rtmp/stream'
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey}
        rtmpStreamList = prdHttpCaller.getResult(listRTMPStreamsEndpoint, params)
    else:
        rtmpStreamList = prdHttpCaller.getResult(listRTMPStreamsEndpoint)
    return(rtmpStreamList)


def listStorageGroup(accountSwitchKey=None):
    """ List the Storage Groups associated with the account """
    listStorageGroupEndpoint = '/config-media-live/v1/live/rtmp/storage-group'
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey}
        storageGroupList = prdHttpCaller.getResult(listStorageGroupEndpoint, params)
    else:
        storageGroupList = prdHttpCaller.getResult(listStorageGroupEndpoint)
    return(storageGroupList)


def GetDomain(domainName, accountSwitchKey=None):
    """ Get the Domain Info  """
    getDomainEndpoint = '/config-media-live/v1/live/{domain}'.format(domain=domainName)
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey}
        domainInfo = prdHttpCaller.getResult(getDomainEndpoint, params)
    else:
        domainInfo = prdHttpCaller.getResult(getDomainEndpoint)
    return(domainInfo)


def GetStream(domainName, streamId, accountSwitchKey=None):
    """ Get the Stream Info  """
    getstreamEndpoint = '/config-media-live/v1/live/{domain}/stream/{streamId}'.format(
        domain=domainName, streamId=streamId)
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey}
        streamInfo = prdHttpCaller.getResult(getstreamEndpoint, params)
    else:
        streamInfo = prdHttpCaller.getResult(getstreamEndpoint)
    return(streamInfo)


def GetRTMPConfig(cpCode, accountSwitchKey=None):
    """ Get the RTMP Config Info  """
    getRTMPConfigEndpoint = '/config-media-live/v1/live/rtmp/configuration/{cpcode}'.format(
        cpcode=cpCode)
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey}
        rtmpConfigInfo = prdHttpCaller.getResult(getRTMPConfigEndpoint, params)
    else:
        rtmpConfigInfo = prdHttpCaller.getResult(getRTMPConfigEndpoint)
    return(rtmpConfigInfo)


def GetRTMPStream(streamId, accountSwitchKey=None):
    """ Get the RTMP Stream Info  """
    getRTMPStreamEndpoint = '/config-media-live/v1/live/rtmp/stream/{streamId}'.format(
        streamId=streamId)
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey}
        rtmpStreamInfo = prdHttpCaller.getResult(getRTMPStreamEndpoint, params)
    else:
        rtmpStreamInfo = prdHttpCaller.getResult(getRTMPStreamEndpoint)
    return(rtmpStreamInfo)


def listmslStreams(accountSwitchKey=None):
    """ Get list of MSL streams"""
    listStreamsEndpoint = '/config-media-live/v2/msl-origin/streams?sortKey=createdDate&sortOrder=DESC'
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey,
                  'sortKey': 'createdDate',
                  'sortOrder': 'DESC'
                  }
        streamList = prdHttpCaller.getResult(listStreamsEndpoint, params)
    else:
        streamList = prdHttpCaller.getResult(listStreamsEndpoint)
    return streamList


def getmslStreams(accountSwitchKey, streamid):
    "Get a stream details"
    getStreamsEndpoint = '/config-media-live/v2/msl-origin/streams/{streamId}'.format(
        streamId=streamid)
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey
                  }
        streaminfo = prdHttpCaller.getResult(getStreamsEndpoint, params)
    else:
        streaminfo = prdHttpCaller.getResult(getStreamsEndpoint)
    return streaminfo


def listcdns(accountSwitchKey=None):
    """ Get list of CDN's """
    listcdnsEndpoint = '/config-media-live/v2/msl-origin/cdns'
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey
                  }
        cdnList = prdHttpCaller.getResult(listcdnsEndpoint, params)
    else:
        cdnList = prdHttpCaller.getResult(listcdnsEndpoint)
    return cdnList


def listcpcodes(accountSwitchKey=None, type="INGEST", unused="true"):
    """ Get list of cpcodes """
    listcpcodeEndpoint = '/config-media-live/v2/msl-origin/cpcodes'
    if accountSwitchKey:
        params = {'accountSwitchKey': accountSwitchKey,
                  'type': type,
                  'unused': unused

                  }
        cpcodeList = prdHttpCaller.getResult(listcpcodeEndpoint, params)
    else:
        params = {
            'type': type,
            'unused': unused

        }
        cpcodeList = prdHttpCaller.getResult(listcpcodeEndpoint, params)
    return cpcodeList
