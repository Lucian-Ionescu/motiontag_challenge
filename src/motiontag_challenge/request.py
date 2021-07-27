import pandas as pd
import requests

from motiontag_challenge.filter import TARGET_COLUMNS
from data_columns import Columns
from motiontag_challenge.tools.etl import load_base_data
from motiontag_challenge.main import VERBOSE, MODEL_PARAM, DISABLE_FILTER


url = 'http://127.0.0.1'
port = 10400
endpoint = 'waypoints'
request_str = ''.join([url, ':', str(port), '/', endpoint])


def send_request(data: pd.DataFrame = None, use_model: bool = False,
                 include_labels: bool = False, disable_filter: bool = False,
                 verbose: bool = False):
    data = prepare_df(
        data=data,
        include_labels=include_labels)

    payload = data.to_json()
    headers = {'Content-Type': 'application/json'}
    params = {MODEL_PARAM: use_model, DISABLE_FILTER: disable_filter, VERBOSE: verbose}

    response = requests.post(
        url=request_str,
        params=params,
        data=payload,
        headers=headers)
    return response.json()


def prepare_df(data: pd.DataFrame, include_labels: bool = False):
    cols_to_send = TARGET_COLUMNS.copy()
    if data is None:
        data = load_base_data()
    if not include_labels:
        data.drop(
            columns=[Columns.label.value],
            inplace=True)
    else:
        cols_to_send.append(Columns.label.value)
    return data[cols_to_send]
