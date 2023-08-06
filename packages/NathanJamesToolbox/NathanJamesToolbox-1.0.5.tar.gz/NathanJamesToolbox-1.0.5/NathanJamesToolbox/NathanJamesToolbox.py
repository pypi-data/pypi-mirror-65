import requests
from slacker import Slacker
import datetime as dt
from google.cloud import storage
import pymysql


class airtableToolbox:
    def __init__(self, base, apiKey):
        self.base = base
        self.apiKey = apiKey
        self.airtableURL = 'https://api.airtable.com/v0/{}'.format(base)
        self.airtableHeaders = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(apiKey)}

    def create_dictionary(self, url, baseName, reverse=False, *args):
        _dict = {}
        _dict_reverse = {}
        atURL = url

        while True:
            print(atURL)
            r = requests.get(atURL, headers=self.airtableHeaders).json()
            if len(r) != 0:
                for rec in r['records']:
                    try:
                        _items = []
                        _name = str(rec['fields'][baseName]).strip()
                        _items.append(rec['id'])
                        for a in args:
                            try:
                                _items.append(str(rec['fields'][a]).strip())
                            except:
                                _items.append('N/A')
                        _dict[_name] = _items
                        if reverse:
                            _dict_reverse[rec['id']] = _name
                    except KeyError:
                        pass

                try:
                    offset = r['offset']
                    if '?' in url:
                        atURL = '{}&offset={}'.format(url, offset)
                    else:
                        atURL = '{}?offset={}'.format(url, offset)
                except KeyError:
                    break
                except Exception:
                    break
            else:
                if reverse:
                    _dict_reverse = {}
                else:
                    _dict = {}
                break

        if reverse:
            return _dict_reverse
        else:
            return _dict

    def clean_list_string(self, str):
        str = str.replace('[', '').replace("'", '').replace(']', '')
        return str

    def push_data(self, url, payload, patch=True):
        try:
            if patch:
                r = requests.patch(url, payload, headers=self.airtableHeaders)
            else:
                r = requests.post(url, payload, headers=self.airtableHeaders)
            statCode = r.status_code
        except requests.exceptions.HTTPError as e:
            return e
        return statCode

    def table_duplicate_check(self, url, baseName):
        _list = []
        _dup_list = []
        atURL = url

        while True:
            print(atURL)
            r = requests.get(atURL, headers=self.airtableHeaders).json()
            if len(r) != 0:
                for rec in r['records']:
                    try:
                        _item = str(rec['fields'][baseName]).strip()
                        if _item not in _list:
                            _list.append(_item)
                        else:
                            _dup_list.append(_item)
                    except KeyError:
                        pass

                try:
                    offset = r['offset']
                    if '?' in url:
                        atURL = '{}&offset={}'.format(url, offset)
                    else:
                        atURL = '{}?offset={}'.format(url, offset)
                except KeyError:
                    break
                except Exception:
                    break
        if len(_dup_list) == 0:
            return 'No duplicates found on\n----table: {}\n----column: {}'.format(url, baseName)
        else:
            return 'The following duplicates found on\n----table: {}\n----column: {}'.format(url, _dup_list)

    def create_list(self, url, _column):
        airtableURL = url
        _list = []

        while True:
            print(airtableURL)
            r = requests.get(airtableURL, headers=self.airtableHeaders).json()
            if len(r) != 0:
                for rec in r['records']:
                    try:
                        _list.append(rec['fields'][_column])
                    except KeyError:
                        pass

                try:
                    offset = r['offset']
                    if '?' in url:
                        airtableURL = '{}&offset={}'.format(url, offset)
                    else:
                        airtableURL = '{}?offset={}'.format(url, offset)
                except KeyError:
                    break
                except Exception:
                    break
        return _list

    def get_json(self, url):
        airtableURL = url
        _list_json = []

        while True:
            print(airtableURL)
            r = requests.get(airtableURL, headers=self.airtableHeaders).json()
            for rec in r['records']:
                _list_json.append(rec)

            try:
                offset = r['offset']
                if '?' in url:
                    airtableURL = '{}&offset={}'.format(url, offset)
                else:
                    airtableURL = '{}?offset={}'.format(url, offset)
            except KeyError:
                break
            except Exception:
                break
        return _list_json

    def create_url(self, url_base):
        return '{}/{}'.format(self.airtableURL, url_base)


class slackToolbox:
    def __init__(self, _key, _channel):
        self._key = _key
        self._channel = _channel

    def send_message(self, funcName, errorDesc):
        _message = 'Python File: {}\n' \
                   'Function Name: {}\n' \
                   'Error Description: {}'.format(__file__, funcName, errorDesc)
        slack = Slacker(self._key)
        slack.chat.post_message(self._channel, _message)


class pdfFillerToolbox:
    def __init__(self, baseURL, downloadPath):
        self.baseURL = baseURL
        self.downloadPath = downloadPath
        self.postHeaders = {'content-type': 'application/json',
                            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjgwNThiOTFhYTE5MDViZGJhNmNmZ'
                                             'TIwZTI0ZmFiYjBlNTc5MDNlYjE4MWM4N2UzNGEzYjVhOTc4ZGJkM2E4YTg2YjUwM2EwNTkwNzk3ZWZkIn0.'
                                             'eyJhdWQiOiIwIiwianRpIjoiODA1OGI5MWFhMTkwNWJkYmE2Y2ZlMjBlMjRmYWJiMGU1NzkwM2ViMTgxYzg'
                                             '3ZTM0YTNiNWE5NzhkYmQzYThhODZiNTAzYTA1OTA3OTdlZmQiLCJpYXQiOjE1NzM1MzY0NDMsIm5iZiI6MT'
                                             'U3MzUzNjQ0MywiZXhwIjoxNjA1MTU4ODQzLCJzdWIiOiIyMDYxMjU0MjUiLCJzY29wZXMiOltdfQ.ffahz4f'
                                             '-INxOYoKqoBMcfLQDmTRRE8s9pTY_PWLiU7A5BnmlZI0fz6ch6bfnENlB00BXO7XLaVRZiMmSp2HmHP_X0u'
                                             'bl76horv8eGrnYwB21Sldr9M4YL0as-fg6fa65Za9jS2iXfkQyhnMXKmoC4_bbEbGT3wtFGl9sFhaJJ_'
                                             'tAbkS9lOkBCxwKFiR61girhocWYEAAlnJDqwYUk3E-L4k3QfVBZphLb9FVEWm_woWzixrmHBeVI6h1ymjHd'
                                             'MndV5ctDMU5CCBvISodcr9aMaDzIukHWxHqDNb1DTtYqtO7yPXkjvlfuvPABeD4xHyH5KPOxFqt0tSOaJmU'
                                             'J5xGh0vh_SV_FwtLDVizg4ALrnWGu5BNoVWnmo7sy9YKgU3LEm0mzr--j6mW4TC_Aw8y6eXE5uAc1p5wiZP'
                                             '1OnfGYG3a8ZEaY-F7ZopR_KXJyf-oHWoZh9--8BHZgffiGz1_cuVcq8leMhf5R3etLlwrPDbt-kYcVkXFFb'
                                             'npM2fxQqYxPPUhas2U9q9A9q3x8KXSRdm7efurFVIe_gWCrqL1_DQ52FzphyRzANxqzoCvM4EsAU-t1B0Dd'
                                             'VZ6ybtQ3h3aneZaNnFdG3zv3Zm7BQqAY_IGhM7Wlq2GkM9nbz2A-Sc6K6cwIskXdvqF2acXNyXWXGXlSD3L'
                                             'YI-FicJ0RoM8DtU'}
        self.downloadHeaders = {'content-type': 'application/json',
                                'Authorization': 'Bearer fXVIj4MZeHAahieugwzygN9dKkRXEklAwH98AfD8'}

    def postJSON(self, templateID, pl):
        data = requests.post('{}{}'.format(self.baseURL, templateID), pl, headers=self.postHeaders).json()
        return data

    def pdf_download(self, docID, docName):

        url = 'https://api.pdffiller.com/v1/document/' + str(docID) + '/download/'
        r = requests.get(url, headers=self.downloadHeaders)
        fName = '{}{}.pdf'.format(self.downloadPath, docName)
        with open(fName, 'wb') as f:
            f.write(r.content)
        print('Documnet downloaded from PDFfiller. Local path =', fName)

    def checkAvail_Format(self, _json, _data, _type):
        try:
            _data = _json['fields'][_data]
            if type(_data) is list:
                _data = _data[0]
        except KeyError:
            return ''

        if _type == 'date':
            try:
                _data = dt.datetime.strptime(_data, '%Y-%m-%d')
                _data = dt.datetime.strftime(_data, '%m/%d/%Y')
            except KeyError:
                _data = ''
        elif _type == 'str':
            try:
                _data = _data
            except KeyError:
                _data = ''
            except TypeError:
                _data = ''
        elif _type == 'float':
            try:
                _data = round(_data, 3)
                _data = '{:,.2f}'.format(_data)
            except KeyError:
                _data = ''
        elif _type == 'int':
            try:
                _data = int(_data)
                _data = '{:,}'.format(_data)
            except KeyError:
                _data = ''
        else:
            print('invalid _type')
        return _data


class googleCloudStrorageToolbox:
    def __init__(self, keyFile, downloadPath):
        self.keyFile = keyFile
        self.downloadPath = downloadPath

    def upload_to_bucket(self, blob_name, path_to_file, bucket_name):
        """ Upload data to a bucket"""
        storage_client = storage.Client.from_service_account_json(self.keyFile)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(path_to_file)
        return blob.public_url

    def list_blobs(self, bucket_name):
        """Lists all the blobs in the bucket."""
        # bucket_name = "your-bucket-name"

        # storage_client = storage.Client()
        storage_client = storage.Client.from_service_account_json(self.keyFile)

        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = storage_client.list_blobs(bucket_name)
        gcpFileList = []

        for blob in blobs:
            # print(blob.name)
            gcpFileList.append(blob.name)

        return gcpFileList

    def upload_file(self, gcpFilename, gcpBucketName):
        # Upload file to GCP
        print('Uploading to Google Cloud Storage...')
        filePath = '{}{}'.format(self.downloadPath, gcpFilename)
        uploadURL = self.upload_to_bucket(gcpFilename, filePath, gcpBucketName)
        return uploadURL


class mySQLToolbox:
    def __init__(self, sqlPath, host, user, password, db):
        self.sqlPath = sqlPath
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def readQuery(self, qry, _type):
        if _type == 'f':
            with open('{}{}'.format(self.sqlPath, qry), 'r') as f:
                fString = f.read()
        elif _type == 'q':
            fString = qry
        else:
            raise Exception('Invalid readFile type.')

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        cursor.execute(fString)
        data = cursor.fetchall()
        db.close()

        return data

    def runQuery(self, qry):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()

        try:
            # Execute the SQL command
            cursor.execute(qry)
            db.commit()
            return 'Passed'
        except Exception as e:
            db.rollback()
            return 'Failed', e
        finally:
            db.close()


class FlexportToolbox:
    def __init__(self, token):
        self.base_url = 'https://api.flexport.com/'
        self.token = token
        self.headers = {'Accept': 'application/vnd.flexport.v1',
                        'Flexport-Version': '2',
                        'content-type': 'application/json; charset=utf-8',
                        'Authorization': 'Token token="%s"' % token}

    def get_json(self, endpoint, *args):
        url = '{}{}'.format(self.base_url, endpoint)
        if len(args) != 0:
            url += '?'
            for arg in args:
                url += arg + '&'
        url = url[:-1]
        return requests.get(url, headers=self.headers).json()


class Cin7Toolbox:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.baseURL = 'https://api.cin7.com/api/v1/'

    def get_json(self, endpoint):
        jsonURL = '{}{}'.format(self.baseURL, endpoint)
        if 'page=' in jsonURL:
            return requests.get(jsonURL, auth=(self.username, self.password)).json()
        else:
            # loop all pages
            jsonAll = []
            pg = 0
            while True:
                pg += 1
                print(jsonURL + '&page={}'.format(pg))
                data = requests.get(jsonURL + '&page={}'.format(pg), auth=(self.username, self.password)).json()
                if len(data) != 0:
                    for r in data:
                        jsonAll.append(r)
                else:
                    break
            return jsonAll


class FreshdeskToolbox:
    def __init__(self, key):
        self.base_url = 'https://bluefyn.freshdesk.com/api/v2/'
        self.key = key
        self.auth_ = (self.key, '')

    def create_list(self, endpoint, *args):
        pg = 0

        url = 'https://bluefyn.freshdesk.com/api/v2/{}'.format(endpoint)

        _list_generic = []
        totalData = 0
        while True:
            if 'page=' in url:
                reqURL = url
            else:
                pg += 1
                reqURL = '{}?page={}'.format(url, pg) if '?' not in url else '{}&page={}'.format(url, pg)

            print(reqURL)
            data = requests.get(reqURL, auth=self.auth_).json()
            totalData += len(data)

            if len(data) == 0:
                break

            for r in data:
                _list_arg = []
                for arg in args:
                    _list_arg.append(r[arg])
                _list_generic.append(_list_arg)
            if 'page=' in url:
                break
        return _list_generic

    def get_json(self, endpoint):
        url = '{}{}'.format(self.base_url, endpoint)
        return requests.get(url, auth=self.auth_).json()
