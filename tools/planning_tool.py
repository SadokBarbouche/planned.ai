from langchain.tools import BaseTool
from math import sin, cos, sqrt, atan2, radians
from typing import Union, Any


class FetchGeoLocationTool(BaseTool):
    name = "Fetch GeoLocation Tool"
    description = "use this tool when you need to get the geolocation of a specific place"

    def _run(self,):
        pass

    def _arun(self):
        raise NotImplementedError("This tool does not support async")


class PlanningTool(BaseTool):
    name = "Planning Tool"
    description = "use this tool when you need to choose the best destination from a location to another."

    def _run(self, lat1: Union[int, float], lon1: Union[int, float], city: str, category: str):
        # Adjacency list
        pass

    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")
