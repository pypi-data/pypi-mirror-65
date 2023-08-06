"""A place to keep standard geometries an associated functions."""

import shapely.geometry
import shapely.wkt

from geospin.utilities.data.wkt import germany_coarse, germany_fine


class Germany(object):
    """
    Contains methods to determine if a point is located within Germany.

    Coarse and fine boundaries were generated according to:
    https://gis.stackexchange.com/questions/183248/getting-polygon-boundaries-
    of-city-in-json-from-google-maps-api/192298#192298
    """

    def __init__(self, coarse=True):
        """
        Initialize the boundary of Germany.

        :param bool coarse: Whether to use the coarse boundary of Germany.
        """
        if coarse:
            self.boundary = shapely.wkt.loads(germany_coarse)
        else:
            self.boundary = shapely.wkt.loads(germany_fine)

    def contains(self, lat, lon):
        """
        Determine if a point is located within Germany.

        :param float lat: Latitude of the location.
        :param float lon: Longitude of the location.
        :return: Whether the point is contained within Germany or not.
        :rtype: bool
        """
        point = shapely.geometry.Point(lon, lat)

        for polygon in self.boundary:
            if polygon.contains(point):
                return True
        return False
