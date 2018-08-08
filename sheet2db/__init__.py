import pymysql
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import client
from oauth2client import file as oauth_file
from oauth2client import tools


__version__ = '1.0.0'
__author__ = 'mingrammer'
__license__ = 'MIT'


class Sheet2db(object):

    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    def __init__(self, api_key=None, creds_path='credentials.json', token_path='token.json'):
        """
        Args:
            api_key: Google API key which is accessible to spreadsheet API.
                     Service will be built with api key if and only if this value has set.
            credentials_path: File path where Google API credentials is stored.
            token_storage_path: File path to store the credential in.
        """
        if api_key:
            self.service = self._build_with_api_key(api_key)
        else:
            self.service = self._build_with_oauth_token(creds_path, token_path)
        self.cols = tuple()
        self.rows = list(tuple())

    def _build_with_api_key(self, api_key):
        service = build('sheets', 'v4', developerKey=api_key)
        return service

    def _build_with_oauth_token(self, credentials_path, token_storage_path):
        store = oauth_file.Storage(token_storage_path)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                credentials_path, self.SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        return service

    def _quote(self, a_tuple):
        return tuple('\'{}\''.format(e) for e in a_tuple)

    def _back_quote(self, a_tuple):
        return tuple('`{}`'.format(e) for e in a_tuple)

    def fetch(self, sheet, tab, range):
        """
        Fetch and store data from Google spreadsheet.

        Args:
            sheet: Sheet id to fetch from.
            tab: Tab name to fetch from.
            range: Cell range to fetch.
                   Range must include a row will be used as database cols.

        Returns:
            None.
        """
        range_name = u"'{}'!{}".format(tab, range)
        result = self.service.spreadsheets().values().get(
            spreadsheetId=sheet, range=range_name).execute()
        values = result.get('values', [])
        if len(values) > 1:
            self.cols = tuple(values[0])
            self.rows = [tuple(row) for row in values[1:]]

    def sync(self, host, port, user, password, db, table):
        """
        Sync to database.

        Args:
            host: DB host.
            port: DB port.
            user: DB username.
            password: DB password.
            db: Target db sync to.
            table: Target table sync to.

        Returns:
            None.
        """
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=db,
            charset='utf8',
            use_unicode=True)
        with conn.cursor() as cur:
            back_quoted_cols = self._back_quote(self.cols)
            for row in self.rows:
                quoted_row = self._quote(row)
                query = u'REPLACE INTO {}({}) VALUES ({})'.format(
                    table,
                    ','.join(back_quoted_cols),
                    ','.join(quoted_row))
                cur.execute(query)
            conn.commit()
