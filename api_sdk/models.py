import math
from datetime import datetime


class PointDataUpdate(object):
    """Model for bulk-updating a point's data value and timestamp"""
    __slots__ = ['point_id', 'value', 'last_updated']

    def __init__(self, point_id, value, last_updated):
        errors = []
        if not isinstance(point_id, int):
            errors.append(f"point id must be an integer, saw {point_id}")
        self.point_id = point_id
        self.value = value
        if not isinstance(last_updated, datetime):
            errors.append(f"last updated must be a datetime, saw {last_updated}")
        self.last_updated = last_updated
        if errors:
            raise ValueError(f"Invalid PointDataUpdate: {', '.join(errors)}")

    def json(self):
        return {'id': self.point_id,
                'value': self.value,
                'last_updated': self.last_updated.timestamp() * 1000}


class IngestStats(object):
    def __init__(self):
        self._points = []
        self._building = {}

    def summary(self, info):
        # infos, errors, num_points, sample_points, etc
        for k, v in info.items():
            if k == 'elapsed':
                self.elapsed(v)
            else:
                self._building[k] = v

    def add_points(self, points):
        self._points += points

    def elapsed(self, elapsed):
        self.building['processing_time_ms'] = math.floor(elapsed.microseconds / 100)

    def json(self):
        return {
            'building': self._building,
            'points': self._points,
        }