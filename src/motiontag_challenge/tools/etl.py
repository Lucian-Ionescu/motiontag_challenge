import os

import geopandas as gpd
import pandas as pd

from constants import DATA_ROOT, FILE, M_TO_KM, MIN_TO_HOUR, CRS_BERLIN
from data_columns import Columns


def load_base_data(include_labels: bool = True):
    data = pd.read_csv(os.path.join(DATA_ROOT, FILE))
    if include_labels:
        data[Columns.label.value] = ~data[Columns.outlier.value]
    data.drop(columns=Columns.outlier.value, inplace=True)
    data.rename(columns={'accuracy (m)': Columns.accuracy.value, 'time (min)': Columns.time.value}, inplace=True)
    return data


def create_geopandas(data: pd.DataFrame = None, crs: str = None):
    if data is None:
        data = load_base_data()

    data = gpd.GeoDataFrame(
        data,
        geometry=gpd.points_from_xy(
            x=data[Columns.lat.value],
            y=data[Columns.lon.value]),
        crs=4326)
    if crs is not None:
        data.to_crs(
            crs=crs,
            inplace=True)
    return data


def get_analysis_data_set():
    data = create_geopandas()

    data = data.merge(
        pd.Series(
            data=get_distance(
                data=data,
                crs=CRS_BERLIN,
                valid_only=True),
            name=Columns.distance.value),
        left_index=True,
        right_index=True,
        how='left')

    data = data.merge(
        pd.Series(
            data=get_distance(
                data=data,
                crs=CRS_BERLIN,
                valid_only=False),
            name=Columns.distance.value + '_all'),
        left_index=True,
        right_index=True,
        how='left')

    data = data.merge(
        pd.Series(
            get_duration(
                data=data,
                valid_only=True),
            name=Columns.duration.value),
        left_index=True,
        right_index=True,
        how='left')

    data = data.merge(
        pd.Series(
            get_duration(
                data=data,
                valid_only=False),
            name=Columns.duration.value + '_all'),
        left_index=True,
        right_index=True,
        how='left')

    # drop first entry
    data = data.loc[1:]

    # compute velocities
    data[Columns.velocity.value] = get_velocity(distance=data.dist, duration=data.duration)
    data[Columns.velocity.value + '_all'] = get_velocity(distance=data.dist_all, duration=data.duration_all)

    return data


def get_velocity(distance: pd.Series(dtype=float), duration: pd.Series(dtype=float)):
    return (distance * M_TO_KM) / (duration * MIN_TO_HOUR)


def get_distance(data: gpd.GeoDataFrame, crs: str = None, valid_only: bool = False):
    if valid_only:
        data = data[data.valid]
    geo = data.geometry
    if crs is not None:
        geo = geo.to_crs(crs)
    return geo.distance(geo.shift())


def get_duration(data: pd.DataFrame, valid_only: bool = False):
    if valid_only:
        return data.loc[data.valid, Columns.time.value] - data.loc[data.valid, Columns.time.value].shift()
    return data[Columns.time.value] - data[Columns.time.value].shift()
