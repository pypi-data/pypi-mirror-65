try:
    import h3

    h3.k_ring('841e265ffffffff', 4)
except AttributeError:
    from h3 import h3

import pyproj
import shapely
import shapely.wkt


def get_geojson_dict_of_hex_id_boundary(hex_id):
    """
    :param str hex_id:
        A hex ID
    :return dict:
        geoJSON-like dictionary
    """
    geojson_dict = {
        "type": "Polygon",
        "coordinates":
            [
                h3.h3_to_geo_boundary(
                    h3_address=str(hex_id),
                    geo_json=True)
            ]
    }
    return geojson_dict


def extract_bbox_polygon(polygon):
    """
    Return the bounding box of the provided polygon as new polygon object

    :param shapely.geometry.Polygon polygon: Shapely geometry polygon object
    :return: Shapely geometry Polygon object
    """
    min_lon, min_lat, max_lon, max_lat = polygon.bounds
    polygon_bbox_geom = shapely.geometry.box(min_lon, min_lat, max_lon, max_lat)
    return polygon_bbox_geom


def buffer_polygon(polygon, buffer_size,
                   source_crs='epsg:4326',
                   buffering_crs='epsg:3035'):
    """
    Create a buffer around the given polygon and return it.

    :param shapely.geometry.Polygon polygon: A polygon
    :param int buffer_size: Size of the buffer in meters
    :param str source_crs: Source CRS of the polygon
    :param str buffering_crs: CRS used to calculate the buffer. Must
        be metric, measured in meter. Will not be checked!
    :return shapely.geometry.Polygon poly:
        The buffered polygon
    """
    # transform to metric crs
    # https://gis.stackexchange.com/questions/127427/transforming-shapely
    # -polygon-and-multipolygon-objects
    projection = pyproj.Transformer.from_proj(
        pyproj.Proj(init=source_crs),
        pyproj.Proj(init=buffering_crs)
    )
    polygon_metric = shapely.ops.transform(projection.transform, polygon)
    # add buffer
    # https://gis.stackexchange.com/questions/97963/how-to-surround-a-polygon
    # -object-with-a-corridor-of-specified-width/97964
    polygon_metric = polygon_metric.buffer(distance=buffer_size)
    # transform back to origin crs
    projection = pyproj.Transformer.from_proj(
        pyproj.Proj(init=buffering_crs),
        pyproj.Proj(init=source_crs)
    )
    poly = shapely.ops.transform(projection.transform, polygon_metric)
    return poly


class PolyFiller:
    """
    Fill polygons and multipolygons with H3 hexagons.

    This extends upon H3's ``polyfill`` function in the following ways:
    * Geometries can be specified in different formats
    * Multipolygons are supported
    * Whether or not hexagons at the geometry boundaries are included or
    excluded can be specified

    .. note::
        If geometry is a single polygon in GeoJSON format and no buffering is
        desired one can use `polyfill` from H3 directly (more efficient,
        because no shape transformation is required).
    """

    def __init__(self,
                 resolution=9,
                 add_hex_id_if='intersected',
                 source_crs='epsg:4326',
                 buffer_crs='epsg:3035'):
        """
        :param int resolution:
            Resolution of H3 hexagons that should fill the polygon
        :param str add_hex_id_if:
            Choose one of 'center_contained', 'intersected'
        :param str source_crs:
            Coordinate reference system of `geometry`. Not needed,
            if `geometry` is a GeoJson dictionary
        :param str buffering_crs:
            Coordinate reference system used for buffering. The default is
            accurate in Europe.
        """
        self.resolution = resolution
        self.add_hex_id_if = add_hex_id_if
        self.source_crs = source_crs
        self.buffer_crs = buffer_crs

    def fill(self, geometry):
        """
        Return list of hex IDs that are inside `geometry`.

        :param geometry:
            Representation of a polygon or a multipolygon. This can either be a
            GeoJson dictionary, a WKT string or a shapely geometry.
        :type geometry:
            dict or str or shapely.geometry.Polygon or
            shapely.geometry.MultiPolygon
        :return list: List of H3 hex IDs.
        """
        hex_ids = []
        polygons = self._get_list_of_polygons_in_geometry(geometry)
        for polygon in polygons:
            hex_ids.extend(self._fill_polygon(polygon))
        return hex_ids

    def _fill_polygon(self, polygon):
        """
        :param shapely.geometry.Polygon polygon:
        :return list:
            List of hex IDs inside ``polygon``
        """
        # 'center-contained' does not require buffering
        if self.add_hex_id_if == 'center_contained':
            polygon_ = polygon
        else:
            polygon_ = self._buffer_polygon(polygon)

        # Convert shapely object to geojson
        geo_json = shapely.geometry.mapping(polygon_)
        hex_ids = h3.polyfill(geo_json, res=self.resolution,
                              geo_json_conformant=True)
        return hex_ids

    def _buffer_polygon(self, polygon):
        """
        Apply different buffering schemes specified by `self.add_hex_id_if`.

        :param shapely.geometry.Polygon polygon:
        :return shapely.geometry.Polygon buffered_polygon:
            A buffered polygon
        """
        if self.add_hex_id_if == 'intersected':
            buffer_size = h3.edge_length(self.resolution, 'm')
            buffered_polygon = buffer_polygon(
                polygon, buffer_size, source_crs=self.source_crs,
                buffering_crs=self.buffer_crs)
        elif self.add_hex_id_if == 'contained':
            raise NotImplementedError
        else:
            raise ValueError('Buffering scheme not known.')

        return buffered_polygon

    @staticmethod
    def _convert_geometry_to_shape(geometry):
        """
        :return shape.geometry.base.BaseGeometry:
            Shapely geometry based on representation specified in `geometry`.
            See `fill()` for details.
        """
        if isinstance(geometry, str):
            shape = shapely.wkt.loads(geometry)
        elif isinstance(geometry, dict):
            shape = shapely.geometry.asShape(geometry)
        elif isinstance(geometry, shapely.geometry.base.BaseGeometry):
            # No conversion for shapely geometries
            shape = geometry
        else:
            raise ValueError('Geometry is in invalid format.')
        return shape

    @staticmethod
    def _get_list_of_polygons_in_geometry(geometry):
        """
        :return list: List of shapely Polygons that comprise `geometry`
        """
        shape = PolyFiller._convert_geometry_to_shape(geometry)
        if isinstance(shape, shapely.geometry.Polygon):
            polygons = [shape]
        elif isinstance(shape, shapely.geometry.MultiPolygon):
            polygons = shape
        else:
            raise ValueError('shape must be Polygon or MultiPolygon')
        return polygons
