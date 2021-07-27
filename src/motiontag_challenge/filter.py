import pickle

import pandas as pd

from constants import CRS_BERLIN, M_TO_KM, MIN_TO_HOUR, ACCURACY_VALID_BELOW, VELOCITY_VALID_BELOW, USE_MODEL
from data_columns import Columns
from motiontag_challenge.tools.etl import create_geopandas
from motiontag_challenge.tools.ml_evaluation import print_evaluation

TARGET_COLUMNS = [Columns.lat.value,
                  Columns.lon.value,
                  Columns.time.value,
                  Columns.accuracy.value]


def compute_velocity(distance: float, duration: float):
    return (distance * M_TO_KM) / (duration * MIN_TO_HOUR)


def get_valid_predecessor(df: pd.DataFrame, idx: int):
    pred = df.loc[(df[Columns.valid.value]) & (df.index < idx)]  # get all valid predecessor waypoints
    if not pred.empty:
        return pred.iloc[-1]
    return None


def ml_prediction(model, accuracy: float, velocity: float):
    pred = model.predict([[accuracy, velocity]])[0]
    return pred


def heuristic_validation(accuracy: float, velocity: float):
    pred = (accuracy < ACCURACY_VALID_BELOW) & (velocity < VELOCITY_VALID_BELOW)
    return pred


# design question: remove waypoints that we can't decide on?
def filter_waypoints(data: pd.DataFrame, use_model: bool = USE_MODEL,
                     verbose: bool = False):
    # load model (if needed)
    model = pickle.load(open('./data/model.mdl', 'rb')) if use_model else None

    # create geo dataframe – since we do not need WGS84 anymore here, apply projection
    gdf = create_geopandas(data, crs=CRS_BERLIN)
    # initially assume invalidity for all waypoints
    gdf[Columns.valid.value] = False

    # ...though, (technically) assume first waypoint as valid
    last_valid_idx = gdf.index[0]
    for idx in gdf.iloc[1:].index:
        current_waypoint = gdf.loc[idx]
        if last_valid_idx >= 0:
            pred_waypoint = gdf.loc[last_valid_idx]
        else:
            continue  # if there is no predecessor, waypoint won't be considered as valid

        if determine_waypoint_validity(
                current_waypoint=current_waypoint,
                pred_waypoint=pred_waypoint,
                model=model,
                use_model=use_model,
                verbose=verbose):
            last_valid_idx = idx
            gdf.loc[idx, Columns.valid.value] = True

    if verbose and Columns.label.value in gdf:
        print_evaluation(
            y_true=gdf[Columns.label.value],
            y_pred=gdf[Columns.valid.value])

    mask = gdf[Columns.valid.value]
    return pd.DataFrame(gdf.loc[mask, TARGET_COLUMNS])


def determine_waypoint_validity(current_waypoint, pred_waypoint, model,
                                use_model: bool,
                                verbose: bool = False):
    label = get_label(current_waypoint)
    accuracy = current_waypoint[Columns.accuracy.value]
    duration = current_waypoint[Columns.time.value] - pred_waypoint[Columns.time.value]
    distance = current_waypoint[Columns.geometry.value].distance(pred_waypoint[Columns.geometry.value])
    velocity = compute_velocity(
        distance=distance,
        duration=duration)
    is_valid = predict_validity(
        accuracy=accuracy,
        velocity=velocity,
        model=model,
        use_model=use_model)
    if verbose:
        print(accuracy, velocity, label, is_valid)
    return is_valid


def get_label(current_waypoint):
    return current_waypoint[Columns.label.value] if Columns.label.value in current_waypoint else None


def predict_validity(accuracy: float, velocity: float,
                     model, use_model: bool):
    if use_model:
        is_valid = ml_prediction(
            model=model,
            accuracy=accuracy,
            velocity=velocity)
    else:
        is_valid = heuristic_validation(
            accuracy=accuracy,
            velocity=velocity)
    return is_valid
