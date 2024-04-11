from typing import Optional, Tuple

from importlib_resources import files

try:
    from PySide6.QtCore import Signal, Slot
except ImportError:
    from PySide2.QtCore import Signal, Slot


from .base import QMapBase

""" GoogleMaps QWebEngineView supporting GoogleMaps, OSM
Google Maps JavaScript API: https://developers.google.com/maps/documentation/javascript/overview
"""


class QGoogleMapsBase(QMapBase):
    map_click = Signal(float, float)
    map_contextmenu = Signal(float, float)
    map_dblclick = Signal(float, float)
    map_move = Signal(float, float)
    map_moveend = Signal(float, float)
    map_movestart = Signal(float, float)
    map_rightclick = Signal(float, float)
    map_zoom = Signal(int)

    marker_move = Signal(str, float, float)
    marker_moveend = Signal(str, float, float)
    marker_movestart = Signal(str, float, float)
    marker_click = Signal(str, float, float)
    marker_dblclick = Signal(str, float, float)
    marker_rightclick = Signal(str, float, float)

    # JavaScript API

    @Slot(float, float)
    def on_click(self, lat: float, lng: float) -> None:
        self.map_click.emit(lat, lng)

    @Slot(float, float)
    def on_contextmenu(self, lat: float, lng: float) -> None:
        self.map_contextmenu.emit(lat, lng)

    @Slot(float, float)
    def on_dblclick(self, lat: float, lng: float) -> None:
        self.map_dblclick.emit(lat, lng)

    @Slot(float, float)
    def on_move(self, lat: float, lng: float) -> None:
        self.map_move.emit(lat, lng)

    @Slot(float, float)
    def on_moveend(self, lat: float, lng: float) -> None:
        self.map_moveend.emit(lat, lng)

    @Slot(float, float)
    def on_movestart(self, lat: float, lng: float) -> None:
        self.map_movestart.emit(lat, lng)

    @Slot(float, float)
    def on_rightclick(self, lat: float, lng: float) -> None:
        self.map_rightclick.emit(lat, lng)

    @Slot(int)
    def on_zoom(self, zoom: int) -> None:
        self.map_zoom.emit(zoom)

    @Slot(str, float, float)
    def on_marker_move(self, key: str, lat: float, lng: float) -> None:
        self.marker_move.emit(key, lat, lng)

    @Slot(str, float, float)
    def on_marker_moveend(self, key: str, lat: float, lng: float) -> None:
        self.marker_moveend.emit(key, lat, lng)

    @Slot(str, float, float)
    def on_marker_movestart(self, key: str, lat: float, lng: float) -> None:
        self.marker_movestart.emit(key, lat, lng)

    @Slot(str, float, float)
    def on_marker_click(self, key: str, lat: float, lng: float) -> None:
        self.marker_click.emit(key, lat, lng)

    @Slot(str, float, float)
    def on_marker_dblclick(self, key: str, lat: float, lng: float) -> None:
        self.marker_dblclick.emit(key, lat, lng)

    @Slot(str, float, float)
    def on_marker_rightclick(self, key: str, lat: float, lng: float) -> None:
        self.marker_rightclick.emit(key, lat, lng)

    # Python API

    def get_center(self) -> Tuple[float, float]:
        lat, lon = self.run_func_sync("get_center")
        return (lat, lon)

    def set_center(self, latitude: float, longitude: float) -> None:
        self.run_func_async("set_center", latitude, longitude)

    def set_zoom(self, zoom: int) -> None:
        self.run_func_async("set_zoom", zoom)

    def move_marker(self, key: str, latitude: float, longitude: float) -> None:
        self.run_func_async("move_marker", key, latitude, longitude)

    def change_marker(
        self,
        key: str,
        clickable: bool = True,
        draggable: bool = False,
        label: Optional[str] = None,
        title: Optional[str] = None,
    ) -> None:
        self.run_func_async("change_marker", key, clickable, draggable, label, title)

    def delete_marker(self, key: str) -> None:
        self.run_func_async("delete_marker", key)

    def add_marker(
        self,
        key: str,
        latitude: float,
        longitude: float,
        clickable: bool = True,
        draggable: bool = False,
        label: Optional[str] = None,
        title: Optional[str] = None,
    ) -> None:
        self.run_func_async("add_marker", key, latitude, longitude, clickable, draggable, label, title)


class QGoogleMapsOSM(QGoogleMapsBase):
    """QWidget (QWebEngineView) which renders OpenStreetMap using GoogleMaps"""

    HTML = files(__package__).joinpath("resources/googlemaps_osm.htm").read_text(encoding="utf-8")

    def __init__(self, latitude: float = 0, longitude: float = 0, zoom: int = 0) -> None:
        super().__init__("qGoogleMaps")

        html = self.HTML
        html = html.replace("'<latitude>'", str(latitude))
        html = html.replace("'<longitude>'", str(longitude))
        html = html.replace("'<zoom>'", str(zoom))
        self.page().setHtml(html)


class QGoogleMapsGoogleMaps(QGoogleMapsBase):
    """QWidget (QWebEngineView) which renders GoogleMaps using GoogleMaps"""

    HTML = files(__package__).joinpath("resources/googlemaps_googlemaps.htm").read_text(encoding="utf-8")

    def __init__(self, api_key: str, latitude: float = 0, longitude: float = 0, zoom: int = 0) -> None:
        super().__init__("qGoogleMaps")

        self.api_key = api_key

        html = self.HTML
        html = html.replace("<YOUR_API_KEY>", api_key)
        html = html.replace("'<latitude>'", str(latitude))
        html = html.replace("'<longitude>'", str(longitude))
        html = html.replace("'<zoom>'", str(zoom))
        self.page().setHtml(html)

    def clean_log_url(self, url: str) -> str:
        return url.replace(self.api_key, "<redacted>")
