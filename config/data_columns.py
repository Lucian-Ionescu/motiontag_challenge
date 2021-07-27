from enum import Enum


class Columns(Enum):
    lat = 'latitude'
    lon = 'longitude'
    geometry = 'geometry'
    duration = 'duration'
    distance = 'dist'
    velocity = 'velocity'
    accuracy = 'accuracy'
    time = 'time_min'
    outlier = 'outlier'
    valid = 'keep'
    label = 'valid'
