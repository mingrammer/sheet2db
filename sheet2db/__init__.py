import pymysql
from apiclient.discovery import build


__version__ = '0.0.1'
__author__ = 'mingrammer'
__license__ = 'MIT'


class Sheet2db(object):

    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    def __init__(self, api_key):
        """
        Args:
            api_key: Google API key which is accessible to spreadsheet API
        """
        self.api_key = api_key
        self.cols = tuple()
        self.rows = list(tuple())

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
        service = build('sheets', 'v4', developerKey=self.api_key)
        range_name = u"'{}'!{}".format(tab, range)
        result = service.spreadsheets().values().get(
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

    def _quote(self, a_tuple):
        return tuple('\'{}\''.format(e) for e in a_tuple)

    def _back_quote(self, a_tuple):
        return tuple('`{}`'.format(e) for e in a_tuple)
