from shapely.geometry import Point, MultiPoint, LineString, MultiPolygon, Polygon, MultiLineString, LinearRing


def _geometry_coordinates(geom):
    """
    :param geom:
    :type geom:
    :return:
    :rtype:
    """
    return [list(c)[:2] for c in geom.coords]


def _create_geojson(geometry, type):
    return {'type': 'Feature',
            'geometry': {
                'type': type.__name__,
                'coordinates': geometry
            },
            'properties': {}}


def _transform_multipoint(multipoint):
    points = list(multipoint.geoms)
    coordinates = []
    for point in points:
        coordinates.append(_transform_point(point))
    return coordinates


def _transform_point(point):
    coordinates = _geometry_coordinates(point)[0]
    return coordinates


def _transform_line_string(line_string):
    coordinates = _geometry_coordinates(line_string)
    return coordinates


def _transform_line_ring(line_ring):
    coordinates = _geometry_coordinates(line_ring)
    return coordinates


def _transform_multi_line_string(multi_linestring):
    coordinates = []
    for line_string in list(multi_linestring.geoms):
        coordinates.append(_transform_line_string(line_string))
    return coordinates


def _transform_polygon(polygon):
    exterior_ring = _geometry_coordinates(polygon.exterior)
    internal_holes = []
    for hole in list(polygon.interiors):
        internal_holes.append(_geometry_coordinates(hole))
    coordinates = [exterior_ring]
    coordinates.extend(internal_holes)
    return coordinates


def _transform_multipolygon(multipolygon):
    polygons = list(multipolygon.geoms)
    coordinates = []
    for polygon in polygons:
        coordinates.append(_transform_polygon(polygon))
    return coordinates


SWITCHER = {
    Point: _transform_point,
    MultiPoint: _transform_multipoint,
    LineString: _transform_line_string,
    MultiLineString: _transform_multi_line_string,
    LinearRing: _transform_line_ring,
    Polygon: _transform_polygon,
    MultiPolygon: _transform_multipolygon,
}


def transform(geometry):
    """
    This function only returns the transformed coordinates from shapely to geojson
    :param geometry:
    :return:
    """
    geometry_type = type(geometry)
    get_coordinates = SWITCHER.get(geometry_type)
    return get_coordinates(geometry)


def get_feature(geometry):
    """
    This is the main function which returns geojson feature from shapely feature
    :param geometry:
    :return:
    """
    coordinates = transform(geometry)
    return _create_geojson(coordinates, type(geometry))
