import folium
import geopandas as gpd

from data_columns import Columns


def show_map(data: gpd.GeoDataFrame,
             show_points: bool = False, show_lines: bool = False,
             valid_only: bool = False):
    m = folium.Map()
    bounding_box = data.total_bounds
    m.fit_bounds([(bounding_box[0], bounding_box[1]),
                  (bounding_box[2], bounding_box[3])])

    # extract data
    valid_col = Columns.valid.value
    aux = (
        data.loc[data[Columns.label.value], Columns.geometry.value] if valid_only and 'valid' in data.columns else data[
            Columns.geometry.value])

    if show_points:
        for point in aux:
            folium.Marker(
                location=point.coords[0],
                popup=point).add_to(m)

    if show_lines:
        folium.PolyLine([p.coords[0] for p in aux]).add_to(m)

    return m
