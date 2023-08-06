import requests
import pandas as pd
from functools import wraps
from typing import Dict


class HTTPError(Exception):
    pass


def authenticated(func):
    """
    Decorator to check if token has expired.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.token_expiration_time <= pd.Timestamp.utcnow().timestamp():
            self.login()
        return func(*args, **kwargs)

    return wrapper


class Client:
    base_url = 'https://eu5.fusionsolar.huawei.com/thirdData'

    def __init__(self, user_name: str, system_code: str):
        self.user_name = user_name
        self.system_code = system_code

        self.session = requests.session()
        self.session.headers.update({'Connection': 'keep-alive', 'Content-Type': 'application/json'})

        self.token_expiration_time = 0

    def login(self):
        url = f'{self.base_url}/login'
        body = {
            'userName': self.user_name,
            'systemCode': self.system_code
        }
        self.session.cookies.clear()
        r = self.session.post(url=url, json=body)
        self._validate_response(response=r)
        self.session.headers.update({'XSRF-TOKEN': r.cookies.get(name='XSRF-TOKEN')})
        self.token_expiration_time = pd.Timestamp.utcnow().timestamp() + 30

    @staticmethod
    def _validate_response(response: requests.Response) -> bool:
        response.raise_for_status()
        body = response.json()
        success = body.get('success', False)
        if not success:
            raise HTTPError(body)
        else:
            return True

    @authenticated
    def get_stations(self) -> Dict:
        url = f'{self.base_url}/getStationList'
        r = self.session.post(url=url, json={})
        self._validate_response(r)
        return r.json()

    @authenticated
    def get_kpi_day(self, station_code: str, date: pd.Timestamp) -> Dict:
        url = f'{self.base_url}/getKpiStationDay'
        time = int(date.timestamp()) * 1000
        body = {
            'stationCodes': station_code,
            'collectTime': time
        }
        r = self.session.post(url=url, json=body)
        self._validate_response(r)
        return r.json()


class PandasClient(Client):
    def get_kpi_day(self, station_code: str, date: pd.Timestamp) -> pd.DataFrame:
        data = super(PandasClient, self).get_kpi_day(station_code=station_code, date=date)

        def flatten_data(j):
            for point in j['data']:
                line = {'collectTime': point['collectTime']}
                line.update(point['dataItemMap'])
                yield line

        df = pd.DataFrame(flatten_data(data))
        df['collectTime'] = pd.to_datetime(df['collectTime'], unit='ms', utc=True)
        df.set_index('collectTime', inplace=True)
        df = df.astype(float)
        return df
