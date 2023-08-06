from rescape_python_helpers import ewkt_from_feature
from rescape_python_helpers.geospatial.geometry_helpers import ewkt_from_feature_collection


def geos_feature_geometry_default():
    """
    The default geometry is a polygon of the earth's extent
    :return:
    """
    return ewkt_from_feature(
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon", "coordinates": [[[-85, -180], [85, -180], [85, 180], [-85, 180], [-85, -180]]]
            }
        }
    )


def geos_feature_collection_geometry_default():
    """
        Default FeatureCollection as ewkt representing the entire world
    :return:
    """
    return ewkt_from_feature_collection(
        feature_collection_default()
    )


def feature_collection_default():
    return {
        'type': 'FeatureCollection',
        'features': [{
            "type": "Feature",
            "geometry": {
                "type": "Polygon", "coordinates": [[[-85, -180], [85, -180], [85, 180], [-85, 180], [-85, -180]]]
            }
        }]
    }


def region_data_default():
    return dict(locations=dict(params=[dict(
        country="ENTER A COUNTRY OR REMOVE THIS KEY/VALUE",
        state="ENTER A STATE/PROVINCE ABBREVIATION OR REMOVE THIS KEY/VALUE",
        city="ENTER A CITY OR REMOVE THIS KEY/VALUE",
        neighborhood="ENTER A NEIGHBORHOOD OR REMOVE THIS KEY/VALUE",
        blockname="ENTER A BLOCKNAME OR REMOVE THIS KEY/VALUE"
    )]))


def project_data_default():
    return dict()


def user_state_data_default():
    return dict(
        userRegions=[]
    )


def group_state_data_default():
    return dict()
