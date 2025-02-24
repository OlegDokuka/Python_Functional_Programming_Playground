from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any
from typing import Deque
from typing import List


class AdzunaAppCredentials:
    app_id: str
    app_key: str
    requests: deque[datetime]

    def __init__(self, app_id: str, app_key: str, requests: Deque[datetime] = None):
        self.app_id = app_id
        self.app_key = app_key
        self.requests = deque(requests) if requests else deque()

        # Rate limits
        self.limits = {
            'minute': (25, timedelta(minutes=1)),
            'day': (250, timedelta(days=1)),
            'week': (1000, timedelta(weeks=1)),
            'month': (2500, timedelta(days=30)),  # Approximate month duration
        }

    def _cleanup_old_requests(self, requests: Deque[datetime]) -> Deque[datetime]:
        """Removes outdated request timestamps."""
        now = datetime.utcnow()
        return deque(req for req in requests if req >= now - self.limits['month'][1])

    def can_make_request(self) -> bool:
        """Checks if a request can be made without exceeding rate limits."""
        cleaned_requests = self._cleanup_old_requests(self.requests)
        now = datetime.utcnow()

        return all(
            len([req for req in cleaned_requests if req > now - duration]) < max_requests
            for max_requests, duration in self.limits.values()
        )

    def check_limit(self, period: str) -> bool:
        """Checks if the request limit for a specific period is exceeded."""
        if period not in self.limits:
            raise ValueError("Invalid period specified")

        max_requests, duration = self.limits[period]
        now = datetime.utcnow()
        recent_requests = [req for req in self.requests if req > now - duration]

        return len(recent_requests) < max_requests

    def check_minute_limit(self) -> bool:
        return self.check_limit('minute')

    def check_day_limit(self) -> bool:
        return self.check_limit('day')

    def check_week_limit(self) -> bool:
        return self.check_limit('week')

    def check_month_limit(self) -> bool:
        return self.check_limit('month')

    def register_request(self):
        """Returns a new AdzunaAppCredentials instance with the updated request log."""
        if not self.can_make_request():
            raise Exception("Rate limit exceeded")

        new_requests = self._cleanup_old_requests(self.requests)
        new_requests.append(datetime.utcnow())

        return AdzunaAppCredentials(self.app_id, self.app_key, new_requests)


@dataclass
class Category:
    tag: str
    label: str

    @staticmethod
    def from_dict(obj: Any) -> 'Category':
        _tag = str(obj.get("tag"))
        _label = str(obj.get("label"))
        return Category(_tag, _label)


@dataclass
class Company:
    display_name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Company':
        _display_name = str(obj.get("display_name"))
        return Company(_display_name)


@dataclass
class Location:
    area: List[str]
    display_name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        _area = [y for y in obj.get("area")]
        _display_name = str(obj.get("display_name"))
        return Location(_area, _display_name)


@dataclass
class Job:
    country: str
    description: str
    contract_time: str
    longitude: float
    location: Location
    salary_min: int
    created: str
    contract_type: str
    salary_is_predicted: str
    adref: str
    id: str
    latitude: float
    redirect_url: str
    title: str
    salary_max: int
    company: Company
    category: Category

    @staticmethod
    def from_dict(obj: dict, country: str) -> 'Job':
        _description = str(obj.get("description"))
        _contract_time = str(obj.get("contract_time"))
        _longitude = float(obj.get("latitude")) if "latitude" in obj else None
        _location = Location.from_dict(obj.get("location"))
        try:
            _salary_min = int(obj.get("salary_min"))
        except TypeError as e:
            print(e)
        _created = str(obj.get("created"))
        _contract_type = str(obj.get("contract_type"))
        _salary_is_predicted = str(obj.get("salary_is_predicted"))
        _adref = str(obj.get("adref"))
        _id = str(obj.get("id"))
        _latitude = float(obj.get("latitude")) if "latitude" in obj else None
        _redirect_url = str(obj.get("redirect_url"))
        _title = str(obj.get("title"))
        _salary_max = int(obj.get("salary_max")) if "salary_max" in obj else None
        _company = Company.from_dict(obj.get("company"))
        _category = Category.from_dict(obj.get("category"))
        return Job(country, _description, _contract_time, _longitude, _location, _salary_min, _created, _contract_type,
                   _salary_is_predicted, _adref, _id, _latitude, _redirect_url, _title, _salary_max, _company,
                   _category)


@dataclass
class JobSearchResults:
    results: List[Job]
    mean: float
    count: int

    @staticmethod
    def from_dict(obj: Any, country: str) -> 'JobSearchResults':
        _results = [Job.from_dict(y, country) for y in obj.get("results")]
        _mean = float(obj.get("mean"))
        _count = int(obj.get("count"))
        return JobSearchResults(_results, _mean, _count)
