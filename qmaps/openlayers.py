from typing import List

from importlib_resources import files
from PySide2 import QtCore

from .base import QMapBase

""" OpenLayers QWebEngineView supporting OSM
"""


class QOpenLayersOSM(QMapBase):
    """QWidget (QWebEngineView) which renders OpenStreetMap using OpenLayers"""

    HTML = files(__package__).joinpath("resources/openlayers_osm.htm").read_text(encoding="utf-8")

    map_click = QtCore.Signal(float, float)
    map_dblclick = QtCore.Signal(float, float)
    map_error = QtCore.Signal()
    map_loadend = QtCore.Signal()
    map_loadstart = QtCore.Signal()
    map_moveend = QtCore.Signal(float, float, float, float)
    map_movestart = QtCore.Signal(float, float, float, float)
    map_pointerdrag = QtCore.Signal()
    map_pointermove = QtCore.Signal()
    map_postcompose = QtCore.Signal()
    map_postrender = QtCore.Signal()
    map_precompose = QtCore.Signal()
    map_rendercomplete = QtCore.Signal()
    map_singleclick = QtCore.Signal(float, float)

    def __init__(self, latitude: float = 0, longitude: float = 0, zoom: int = 0) -> None:
        super().__init__("qOSM")

        html = self.HTML
        html = html.replace("'<latitude>'", str(latitude))
        html = html.replace("'<longitude>'", str(longitude))
        html = html.replace("'<zoom>'", str(zoom))
        self.page().setHtml(html)

    # JavaScript API

    @QtCore.Slot(float, float)
    def on_click(self, lat, lng) -> None:
        self.map_click.emit(lat, lng)

    @QtCore.Slot(float, float)
    def on_dblclick(self, lat, lng) -> None:
        self.map_dblclick.emit(lat, lng)

    @QtCore.Slot()
    def on_error(self) -> None:
        self.map_error.emit()

    @QtCore.Slot()
    def on_loadend(self) -> None:
        self.map_loadend.emit()

    @QtCore.Slot()
    def on_loadstart(self) -> None:
        self.map_loadstart.emit()

    @QtCore.Slot(float, float, float, float)
    def on_moveend(self, minlat: float, minlon: float, maxlat: float, maxlon: float) -> None:
        self.map_moveend.emit(minlat, minlon, maxlat, maxlon)

    @QtCore.Slot(float, float, float, float)
    def on_movestart(self, minlat: float, minlon: float, maxlat: float, maxlon: float) -> None:
        self.map_movestart.emit(minlat, minlon, maxlat, maxlon)

    @QtCore.Slot()
    def on_pointerdrag(self) -> None:
        self.map_pointerdrag.emit()

    @QtCore.Slot()
    def on_pointermove(self) -> None:
        self.map_pointermove.emit()

    @QtCore.Slot()
    def on_postcompose(self) -> None:
        self.map_postcompose.emit()

    @QtCore.Slot()
    def on_postrender(self) -> None:
        self.map_postrender.emit()

    @QtCore.Slot()
    def on_precompose(self) -> None:
        self.map_precompose.emit()

    @QtCore.Slot()
    def on_rendercomplete(self) -> None:
        self.map_rendercomplete.emit()

    @QtCore.Slot(float, float)
    def on_singleclick(self, lat, lng) -> None:
        self.map_singleclick.emit(lat, lng)

    # Python API

    def get_center(self) -> List[float]:
        return self.run_func_sync("get_center")

    def get_zoom(self) -> float:
        return self.run_func_sync("get_zoom")

    def add_layer_point(self, latitude: float, longitude: float) -> None:
        self.run_func_async("add_layer_point", latitude, longitude)

    def add_overlay_text(self, latitude: float, longitude: float, text: str) -> None:
        self.run_func_async("add_overlay_text", latitude, longitude, text)

    # def pan_to(self, lat: float, lng: float) -> None:
    #    self.run_func_async("centerOn", coordinate, size, position)
