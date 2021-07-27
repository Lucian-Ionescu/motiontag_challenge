from typing import Dict

import pandas as pd
from flask import Flask, request

from motiontag_challenge.filter import filter_waypoints
from motiontag_challenge.tools.timer import elapsed_timer

app = Flask(__name__)

MODEL_PARAM = 'model'
VERBOSE = 'verbose'
DISABLE_FILTER = 'disable_filter'


@app.route('/waypoints', methods=['POST'])
# attributes: latitude longitude time_min accuracy
def predict():
    use_model = MODEL_PARAM in request.args and request.args[MODEL_PARAM] == 'True'
    verbose = VERBOSE in request.args and request.args[VERBOSE] == 'True'
    df = convert_to_df(request.get_json())
    filtered = get_filtered_waypoint_data(
        data=df,
        use_model=use_model,
        verbose=verbose)
    return filtered.to_json()


def convert_to_df(content: Dict):
    df = pd.DataFrame(content)
    df.index = df.index.astype(int)  # use integer index
    return df


def get_filtered_waypoint_data(data: pd.DataFrame, use_model: bool = False,
                               verbose: bool = False):
    if verbose:
        print(f'attributes retrieved: {" ".join(data.columns)}')
    with elapsed_timer(2) as timer:
        nrows_before = len(data)
        invalids = len(data) - data.valid.sum() if 'valid' in data else None
        filtered = filter_waypoints(
            data=data,
            use_model=use_model,
            verbose=verbose)
        nrows_after = len(filtered)
        if verbose:
            print(f'removed {nrows_before - nrows_after}'
                  f'{f"/{invalids}" if invalids is not None else ""}'
                  f' waypoints in {timer()}s')
    return filtered


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10400)
