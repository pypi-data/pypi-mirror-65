#!/usr/bin/env python3

import json
import requests


# -----------------------------------------------------------------
#  Python Library:
#  Library methods used to connect to Terbine's API
# -----------------------------------------------------------------

class PyLibrary:
    # constructor: Assigns base uri of API
    # param: base uri used in API calls
    def __init__(self, uri):
        self.baseUri = uri

    # login: Sets credentials, returns login response as json
    # param: username as email address, account password
    def login(self, username, password):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/auth/login')
        call.setCallType('POST')
        call.setHeader('Content-Type', 'application/json')
        call.setData(json.dumps({'username': username, 'password': password}))
        call.build()

        return call.response

    # search: Queries system using parameters, returns array of search results
    # param: query as text, page number, page size, sort type, order type
    def search(self, query=None, pageNum=None, pageSize=None, sort=None, order=None):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/search/v2/metadata')
        call.setPageNum(pageNum)
        call.setPageSize(pageSize)
        call.setSortType(sort)
        call.setOrder(order)
        call.setCallType('POST')
        call.setHeader('Content-Type', 'application/json')
        call.setData(json.dumps({"text": query}))
        call.build()

        return call.response

    # addToWorkspace: Adds metadata instance to account's workspace
    # param: token from login credentials, GUID of metadata instance, organization ID from credentials
    def addToWorkspace(self, token, guid, orgID):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/workspace/metadata/' + guid.replace(" ", "") + '?orgId=' + orgID)
        call.setCallType('POST')
        call.setHeader('Authorization', 'bearer ' + token)
        call.build()

        return call.response

    # istWorkspace: Returns list of metadata instances added to workspace
    # param: token from login credentials, organization ID from credentials, page number, page size, order, ordered by
    def listWorkspace(self, token, orgID, pageNum=None, pageSize=None, order=None, orderBy=None):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/dashboard/organization/' + orgID + '/workspace')
        call.setPageNum(pageNum)
        call.setPageSize(pageSize)
        call.setOrder(order)
        call.setOrderBy(orderBy)
        call.setCallType('GET')
        call.setHeader('Authorization', 'bearer ' + token)
        call.build()

        return call.response

    # lockToWorkspace: Locks dataset from workspace, activates dataset / stream
    # param: token from login credentials, organization ID from credentials, id of item in workspace
    def lockToWorkspace(self, token, orgID, workspaceID):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/dashboard/organization/' + orgID + '/workspace/' + workspaceID + '/locked')
        call.setCallType('PUT')
        call.setHeader('Authorization', 'bearer ' + token)
        call.build()

        return call.response

    # flagInWorkspace: Flag item in workspace\
    # param: token from login credentials, organization ID from credentials, id of item in workspace
    def flagWorkspace(self, token, orgID, workspaceID):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/dashboard/organization/' + orgID + '/workspace/' + workspaceID + '/flagged')
        call.setCallType('PUT')
        call.setHeader('Authorization', 'bearer ' + token)
        call.build()

        return call.response

    # deleteFromWorkspace: Delete item from workspace
    # param: token from login credentials, organization ID from credentials, id of item in workspace
    def deleteFromWorkspace(self, token, orgID, workspaceID):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/dashboard/organization/' + orgID + '/workspace/' + workspaceID)
        call.setCallType('DELETE')
        call.setHeader('Authorization', 'bearer ' + token)
        call.build()

        return call.response

    # metadata: Returns the metadata instance of a dataset as json
    # param: token from login credentials, GUID of metadata instance
    def metadata(self, token, guid):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/metadata/' + guid.replace(" ", ""))
        call.setCallType('GET')
        call.setHeader('Authorization', 'bearer ' + token)
        call.build()

        return call.response

    # list: Returns array of information on each file in dataset
    # param: token from login credentials, unique dataset ID
    def list(self, token, datasetID):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/dataset/' + datasetID + '/content')
        call.setCallType('GET')
        call.setHeader('Authorization', 'bearer ' + token)
        call.build()

        return call.response

    # downloadSingle: Returns download of single file from dataset
    # param: token from login credentials, file 's content ID
    def downloadSingle(self, token, contentID):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/dataset/content/' + contentID + '/download')
        call.setCallType('GET')
        call.setHeader('Authorization', 'bearer ' + token)
        call.setDownload(True)
        call.build()

        return call.response

    # downloadMultiple: Returns download of multiple files
    # param: token from login credentials, dataset ID, max amount of files to download
    def downloadMultiple(self, token, datasetID, maximum=None):
        call = CallBuilder(self.baseUri)
        call.setPath('/api/dataset/' + datasetID + '/content/download')
        call.setMax(maximum)
        call.setCallType('GET')
        call.setHeader('Authorization', 'bearer ' + token)
        call.setDownload(True)
        call.build()

        return call.response


# -----------------------------------------------------------------
# Call Builder:
# Methods used to build HTTP requests to API
# -----------------------------------------------------------------

class CallBuilder:
    # constructor: Sets base URI of API and initializes optional variables
    # param: base URI used in HTTP requet
    def __init__(self, uri):
        self.baseUri = uri
        self.download = False
        self.data = None
        self.pageNum = None
        self.pageSize = None
        self.sort = None
        self.order = None
        self.orderBy = None
        self.maximum = None

    # setPath: Sets path of URL
    # param: path used in URL of HTTP request
    def setPath(self, path):
        self.path = path

    # setCallType: Sets call type of HTTP request
    # param: call type
    def setCallType(self, callType):
        self.callType = callType

    # setHeader: Sets header of HTTP request
    # param: header key, header value
    def setHeader(self, headerKey, headerValue):
        headers = {headerKey: headerValue}
        self.headers = headers

    # setData: Sets data for POST calls
    # param: data to send
    def setData(self, data):
        self.data = data

    # setDownload: Sets bool value, true if download call, false if not
    # param: download bool value
    def setDownload(self, downloadable):
        self.download = downloadable

    # setPageNum: Sets page number of search results
    # param: page number
    def setPageNum(self, pageNum):
        pageNum = pageNum or 1
        if type(pageNum) == int:
            pageNum = str(pageNum)
        self.pageNum = 'pageNum=' + pageNum

    # setPageSize: Sets page size of search results
    # param: page size
    def setPageSize(self, pageSize):
        pageSize = pageSize or 5
        if type(pageSize) == int:
            pageSize = str(pageSize)
        self.pageSize = 'pageSize=' + pageSize

    # setSortType: Sets method of sorting search results
    # param: sort type
    def setSortType(self, sort):
        sort = sort or 'DATEADDED'
        self.sort = 'sort=' + sort

    # setOrder: Sets order of search results
    # param: order
    def setOrder(self, order):
        order = order or 'DESC'
        self.order = 'order=' + order

    # setOrderBy: Sets order of results by field
    # param: field
    def setOrderBy(self, orderBy):
        orderBy = orderBy or 'description'
        self.orderBy = 'orderBy=' + orderBy

    # setMax: Sets maximum amount of files to download
    # param: max
    def setMax(self, maximum):
        maximum = maximum or 10
        self.maximum = 'maximum=' + str(maximum)

    # getUrl: Concatenates base URI, path, and parameters and returns final URL
    # param: none
    def getUrl(self):
        url = self.baseUri + self.path
        if self.pageNum is not None:
            url = url + '?' + self.pageNum
        if self.pageSize is not None:
            url = url + '&' + self.pageSize
        if self.sort is not None:
            url = url + '&' + self.sort
        if self.order is not None:
            url = url + '&' + self.order
        if self.orderBy is not None:
            url = url + '&' + self.orderBy
        if self.maximum is not None:
            url = url + '?' + self.maximum

        return url

    # build: Builds and returns Call Object
    # param: none
    def build(self):
        if self.callType == 'POST':
            r = requests.post(self.getUrl(), data=self.data, headers=self.headers)
        if self.callType == 'GET':
            r = requests.get(self.getUrl(), data=self.data, headers=self.headers)
        if self.callType == 'PUT':
            r = requests.put(self.getUrl(), data=self.data, headers=self.headers)
        if self.callType == 'DELETE':
            r = requests.delete(self.getUrl(), data=self.data, headers=self.headers)

        if self.download is False:
            r = r.json()

        self.response = r
