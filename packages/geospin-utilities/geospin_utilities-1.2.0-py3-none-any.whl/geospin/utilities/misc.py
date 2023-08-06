import fiona  # Needs to be imported after shapely!
import geopandas as gpd
import numpy
import requests
import shapely
import shapely.ops
import shapely.wkt


def rectangular_cells(bounds, n, m):
    """
    Creates an iterator that returns the specified number of rectangular grid
    cell centers in each dimension within the provided bounds.
    :param tuple(tuple) bounds: The bounds used as border for the returned grid
        cells given as (xmin, ymin, xmax, ymax).
    :param int n: Number of grid cells in x dimension.
    :param int m: Number of grid cells in y dimension.
    :return: Iterator that yields grid cell centers.
    :rtype: Iterator(shapely.geometry.Point)
    """
    xmin, ymin, xmax, ymax = bounds
    radius_x = (xmax - xmin) / (2 * n)
    radius_y = (ymax - ymin) / (2 * m)
    for y in numpy.linspace(ymin + radius_y, ymax - radius_y, m):
        for x in numpy.linspace(xmin + radius_x, xmax - radius_x, n):
            center = shapely.geometry.Point(x, y)
            yield center


def create_grid(polygon, n=10, m=10, wkt=True):
    """
    Creates an iterator that yields rectangular grid cells at the specified
    number in each dimension and within the provided rectangular bounds of the
    given polygon.

    .. note:: The `polygon` can not be a MULTIPOLYGON (because holes are not
    supported).

    :param str polygon: Polygon in WKT format containing the area of interest
        (without holes) from which the bounds are computed.
    :param int n: Number of grid cell centers in the x dimension of the bounds.
    :param int m: Number of grid cell centers in the y dimension of the bounds.
    :param bool wkt: Should the final output be returned as a WKT formatted
        point? If False, returns a shapely.geometry.Point object, else a string.
    :return: Grid cell centers in the specified format.
    :rtype: Iterator(shapely.geometry.Point or str)
    """
    bounds = shapely.wkt.loads(polygon).bounds

    for center in rectangular_cells(bounds, n, m):
        if wkt:
            center = str(center)
        yield center


def fetch_latest_zip_code_areas(
        url="https://www.suche-postleitzahl.org/download_files/public/plz"
            "-gebiete.shp.zip"
        # noqa
):
    """Fetch the latest zip code areas for Germany.

    The latest release of zip code areas is downloaded and converted
    into a standardized format. The resulting data consists of two columns:
    'zip_code' and 'wkt'.

    .. note:: All polygons of an identical zip code will be merged to a
        union.

    :param str url: URL of the zipped shapefile containing zip code areas.
    :return: DataFrame containing columns `zip_code` and `wkt`.
    :rtype: geopandas.GeoDataFrame
    """
    resp = requests.get(url, stream=True)
    resp.raise_for_status()

    with fiona.io.ZipMemoryFile(resp.content) as zip_memory_file:
        with zip_memory_file.open('plz-gebiete.shp') as collection:
            gdf = gpd.GeoDataFrame.from_features(collection, crs=collection.crs)

    gdf = gdf[['plz', 'geometry']]
    gdf = gdf.dissolve(by='plz')

    gdf = gdf.reset_index()
    gdf = gdf.rename(columns={"plz": "zip_code", "geometry": "wkt"})

    return gdf
