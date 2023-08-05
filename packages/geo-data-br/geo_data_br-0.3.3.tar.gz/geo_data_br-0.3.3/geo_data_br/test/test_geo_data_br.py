import pytest
import geo_data_br.points

class TestGeoDataBr:
    def test_geo_data_br(self):
        points = [(-59.23352, -3.35030), (-60.17875, -3.27442)]
        df = geo_data_br.points.data_on_points(points)
        assert df.shape[0] == len(points)

        points = [(-60.17875, -3.27442)]
        df = geo_data_br.points.data_on_points(points)
        points = [(-59.23352, -3.35030)]
        df = geo_data_br.points.data_on_points(points)

    def test_empty(self):
        points = []
        df = geo_data_br.points.data_on_points(points)
        assert df.empty
