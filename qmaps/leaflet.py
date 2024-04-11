import json
from typing import Optional, Sequence, Tuple, Union

from importlib_resources import files

try:
    from PySide6 import QtCore
except ImportError:
    from PySide2 import QtCore

from .base import QMapBase

""" Leaflet QWebEngineView supporting OSM
"""

CoordsT = Sequence[Tuple[float, float]]
NumberT = Union[int, float]

DEFAULT_MARKER_TITLE: str = ""
DEFAULT_MARKER_OPACITY: NumberT = 1.0
DEFAULT_PATH_COLOR: str = "#3388ff"
DEFAULT_PATH_WEIGHT: NumberT = 3
DEFAULT_PATH_FILL_COLOR: str = "*"
DEFAULT_PATH_FILL_OPACITY: NumberT = 0.2
DEFAULT_PATH_OPACITY: NumberT = 1.0
DEFAULT_IMAGEOVERLAY_OPACITY: NumberT = 1.0
DEFAULT_IMAGEOVERLAY_INTERACTIVE: bool = False


class QLeafletOSM(QMapBase):
    """QWidget (QWebEngineView) which renders OpenStreetMap using Leaflet"""

    HTML = files(__package__).joinpath("resources/leaflet_osm.htm").read_text(encoding="utf-8")

    map_move = QtCore.Signal(float, float)
    map_moveend = QtCore.Signal(float, float)
    map_movestart = QtCore.Signal(float, float)
    map_click = QtCore.Signal(float, float)
    map_contextmenu = QtCore.Signal(float, float)
    map_dblclick = QtCore.Signal(float, float)
    map_zoom = QtCore.Signal(float, float, int)

    def __init__(self, latitude: float = 0, longitude: float = 0, zoom: int = 0) -> None:
        super().__init__("qOSM")

        html = self.HTML
        html = html.replace("'<latitude>'", str(latitude))
        html = html.replace("'<longitude>'", str(longitude))
        html = html.replace("'<zoom>'", str(zoom))
        self.page().setHtml(html)

    # JavaScript API

    @QtCore.Slot(float, float)
    def on_move(self, lat: float, lng: float) -> None:
        self.map_move.emit(lat, lng)

    @QtCore.Slot(float, float)
    def on_moveend(self, lat: float, lng: float) -> None:
        self.map_moveend.emit(lat, lng)

    @QtCore.Slot(float, float)
    def on_movestart(self, lat: float, lng: float) -> None:
        self.map_movestart.emit(lat, lng)

    @QtCore.Slot(float, float)
    def on_click(self, lat: float, lng: float) -> None:
        self.map_click.emit(lat, lng)

    @QtCore.Slot(float, float)
    def on_contextmenu(self, lat: float, lng: float) -> None:
        self.map_contextmenu.emit(lat, lng)

    @QtCore.Slot(float, float)
    def on_dblclick(self, lat: float, lng: float) -> None:
        self.map_dblclick.emit(lat, lng)

    @QtCore.Slot(float, float, int)
    def on_zoom(self, lat: float, lng: float, zoom: int) -> None:
        self.map_zoom.emit(lat, lng, zoom)

    # Sync Python API

    def get_center(self) -> dict:
        return self.run_func_sync("get_center")

    def get_zoom(self) -> int:
        return self.run_func_sync("get_zoom")

    def get_bounds(self) -> Tuple[dict, dict]:
        a, b = self.run_func_sync("get_bounds")
        return a, b

    # Async Python API

    def set_view(self, lat: float, lng: float, zoom: int) -> None:
        self.run_func_async("set_view", lat, lng, zoom)

    def set_zoom(self, zoom: int) -> None:
        self.run_func_async("set_zoom", zoom)

    def fit_bounds(self, lat1: float, lng1: float, lat2: float, lng2: float) -> None:
        self.run_func_async("fit_bounds", lat1, lng1, lat2, lng2)

    def pan_to(self, lat: float, lng: float) -> None:
        self.run_func_async("pan_to", lat, lng)

    def add_marker(
        self,
        key: str,
        lat: float,
        lng: float,
        title: str = DEFAULT_MARKER_TITLE,
        opacity: NumberT = DEFAULT_MARKER_OPACITY,
        popup: Optional[str] = None,
    ) -> None:
        self.run_func_async("add_marker", key, lat, lng, title, opacity, popup)

    def add_circle(
        self,
        key: str,
        lat: float,
        lng: float,
        radius: int,
        color: str = DEFAULT_PATH_COLOR,
        fill_color: str = DEFAULT_PATH_FILL_COLOR,
        fill_opacity: NumberT = DEFAULT_PATH_FILL_OPACITY,
        popup: Optional[str] = None,
    ) -> None:
        self.run_func_async("add_circle", key, lat, lng, radius, color, fill_color, fill_opacity, popup)

    def add_polygon(
        self,
        key: str,
        latlngs: Union[CoordsT, Sequence[CoordsT], Sequence[Sequence[CoordsT]]],
        smooth_factor: NumberT = 1.0,
        color: str = DEFAULT_PATH_COLOR,
        weight: NumberT = DEFAULT_PATH_WEIGHT,
        popup: Optional[str] = None,
    ) -> None:
        latlng_list = json.dumps(latlngs)
        self.run_func_async("add_polygon", key, latlng_list, smooth_factor, color, weight, popup)

    def add_polyline(
        self,
        key: str,
        latlngs: Union[CoordsT, Sequence[CoordsT]],
        smooth_factor: NumberT = 1.0,
        color: str = DEFAULT_PATH_COLOR,
        weight: NumberT = DEFAULT_PATH_WEIGHT,
        popup: Optional[str] = None,
    ) -> None:
        latlng_list = json.dumps(latlngs)
        self.run_func_async("add_polyline", key, latlng_list, smooth_factor, color, weight, popup)

    def add_image_url(
        self,
        key: str,
        image_url: str,
        lat1: float,
        lng1: float,
        lat2: float,
        lng2: float,
        opacity: NumberT = DEFAULT_IMAGEOVERLAY_OPACITY,
        interactive: bool = DEFAULT_IMAGEOVERLAY_INTERACTIVE,
    ) -> None:
        self.run_func_async("add_image_url", key, image_url, lat1, lng1, lat2, lng2, opacity, interactive)

    def remove_layer(self, key: str) -> None:
        self.run_func_async("remove_layer", key)

    def open_popup(self, key: str) -> None:
        self.run_func_async("open_popup", key)
