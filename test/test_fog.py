"""Module containing the tests of the Fog object."""

import pytest

from src.fog import Fog

polygons = [
    [(-200, 100), (50, 100), (50, 200), (-200, 200)],
    [(-100, 50), (25, 50), (25, 100), (-100, 100)],
    [(-50, 25), (12.5, 25), (12.5, 50), (-50, 50)],
    [(200, 200), (250, 250), (300, 200)],
    [(180, 180), (225, 225), (270, 180)],
    [(162, 162), (202.5, 202.5), (243, 162)],
    [(145.8, 145.8), (182.25, 182.25), (218.7, 145.8)],
]

centroids = [
    (-75, 150),
    (-37.5, 75),
    (-18.75, 37.5),
    (250, 216.67),
    (225, 195),
    (202.5, 175.5),
    (182.25, 157.95),
]

polygons_order = [
    [0, 1, 2],
    [1, 2, 0],
    [2, 0, 1],
    [0, 1, 2],
    [3, 4, 5, 6],
    [4, 5, 6, 3],
    [5, 6, 3, 4],
    [6, 3, 4, 5],
]


@pytest.fixture(params=polygons_order)
def param_polygon(request):
    """Fixture for polygon centroid tests."""
    return (
        polygons,
        centroids,
        request.param,
    )


def test_get_polygon_centroid(param_polygon):
    """Test the fog method to compute the centroid of a polygon."""
    fog = Fog()
    polygon_order = param_polygon[2]

    for polygon_pos in polygon_order:
        polygon = param_polygon[0][polygon_pos]
        expected_centroid = param_polygon[1][polygon_pos]

        # Compute centroid and check that is as expected (within 1 pixel tolerance)
        computed_centroid = fog.get_polygon_centroid(polygon)
        assert (
            expected_centroid[0] - 1 < computed_centroid[0] < expected_centroid[0] + 1
        )
        assert (
            expected_centroid[1] - 1 < computed_centroid[1] < expected_centroid[1] + 1
        )


def test_center_polygons(param_polygon):
    """Test the fog method to center polygons with respect to a reference polygon."""
    fog = Fog()

    # Get the first polygon as reference and center the others
    # All polygons should have now the same centroid than the first one
    polygon_ref = param_polygon[0][0]
    polygons_list = param_polygon[0][1:]
    centered_polygons = fog.center_polygons(polygon_ref, polygons_list)

    for polygon in centered_polygons:
        # Check that the computed value is in expected range (+- 1 because of the pixel resolution)
        centroid_ref = fog.get_polygon_centroid(polygon_ref)
        centroid = fog.get_polygon_centroid(polygon)
        assert centroid[0] - 1 < centroid_ref[0] < centroid[0] + 1
        assert centroid[1] - 1 < centroid_ref[1] < centroid[1] + 1


def test_get_scaled_polygons():
    """Test fog method to get scaled polygons."""
    fog = Fog()
    i_ref_polygon = 0
    ref_polygon = polygons[i_ref_polygon]
    scale_factor = 0.5
    num_polygons = 3
    scaled_polygons = fog.get_scaled_polygons(ref_polygon, scale_factor, num_polygons)
    assert len(scaled_polygons) == num_polygons
    num_vertices = len(polygons[i_ref_polygon])
    for i_polygon in range(num_polygons - 1):
        ref_polygon = polygons[i_ref_polygon + i_polygon + 1]
        scaled_polygon = scaled_polygons[i_polygon + 1]
        for i_vertex in range(num_vertices):
            for i_coord in range(2):
                assert (
                    scaled_polygon[i_vertex][i_coord] - 1
                    < ref_polygon[i_vertex][i_coord]
                    < scaled_polygon[i_vertex][i_coord] + 1
                )

    i_ref_polygon = 3
    polygon = polygons[i_ref_polygon]
    scale_factor = 0.9
    num_polygons = 4
    scaled_polygons = fog.get_scaled_polygons(polygon, scale_factor, num_polygons)
    assert len(scaled_polygons) == num_polygons
    num_vertices = len(polygons[i_ref_polygon])
    for i_polygon in range(num_polygons - 1):
        ref_polygon = polygons[i_ref_polygon + i_polygon + 1]
        scaled_polygon = scaled_polygons[i_polygon + 1]
        for i_vertex in range(num_vertices):
            for i_coord in range(2):
                assert (
                    scaled_polygon[i_vertex][i_coord] - 1
                    < ref_polygon[i_vertex][i_coord]
                    < scaled_polygon[i_vertex][i_coord] + 1
                )
