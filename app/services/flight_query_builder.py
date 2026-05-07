from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

@dataclass
class FlightQueryBuilder:
    airline_name: str
    _where: List[str] = field(default_factory=list)
    _params: List[object] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Base query + required airline filter
        self._base_sql = """
            SELECT f.*, a1.airport_city as departure_city,
                   a2.airport_city as arrival_city
            FROM flight f
            JOIN airport a1 ON f.departure_airport = a1.airport_name
            JOIN airport a2 ON f.arrival_airport = a2.airport_name
            WHERE f.airline_name = %s
        """
        self._params.append(self.airline_name)

    def with_start_date(self, start_date: Optional[str]) -> "FlightQueryBuilder":
        if start_date:
            self._where.append("f.departure_time >= %s")
            self._params.append(start_date)
        return self

    def with_end_date(self, end_date: Optional[str]) -> "FlightQueryBuilder":
        if end_date:
            self._where.append("f.departure_time <= %s")
            self._params.append(end_date)
        return self

    def with_source(self, source: Optional[str]) -> "FlightQueryBuilder":
        if source:
            self._where.append("(a1.airport_name LIKE %s OR a1.airport_city LIKE %s)")
            search = f"%{source}%"
            self._params.extend([search, search])
        return self

    def with_destination(self, destination: Optional[str]) -> "FlightQueryBuilder":
        if destination:
            self._where.append("(a2.airport_name LIKE %s OR a2.airport_city LIKE %s)")
            search = f"%{destination}%"
            self._params.extend([search, search])
        return self

    def build(self) -> Tuple[str, List[object]]:
        sql = self._base_sql
        if self._where:
            sql += " AND " + " AND ".join(self._where)
        return sql, self._params