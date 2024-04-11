import json
import logging
import webbrowser
from typing import Any, Optional, Sequence

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from PySide6.QtWebChannel import QWebChannel
    from PySide6.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets
    from PySide2.QtWebChannel import QWebChannel
    from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView


logmap = {
    QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel: logging.INFO,
    QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel: logging.WARNING,
    QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel: logging.ERROR,
}

jslog = logging.getLogger("javascript")


def jsrepr(obj: Any) -> str:
    if obj is None:
        return "null"
    elif isinstance(obj, str):
        return repr(obj)
    elif isinstance(obj, bool):  # handle bool before int, since a bool is a int
        return "true" if obj else "false"
    elif isinstance(obj, (int, float)):
        return str(obj)
    else:
        raise TypeError(f"Unhandled type: {type(obj)}")


def js_func_call(name: str, args: Sequence[Any]) -> str:
    args = ", ".join(map(jsrepr, args))
    return f"{name}({args});"


class QMapBasePage(QWebEnginePage):
    accept_language = "en-US,en;q=0.9"

    def __init__(
        self, channel: QWebChannel, cache_dir: str, persistent_dir: str, parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        QWebEnginePage.__init__(self, parent)

        self.profile().setCachePath(cache_dir)
        self.profile().setPersistentStoragePath(persistent_dir)
        self.profile().setHttpAcceptLanguage(self.accept_language)  # important! otherwise OSM requests are blocked

        self.setWebChannel(channel)

    def acceptNavigationRequest(self, url: QtCore.QUrl, type: QWebEnginePage.NavigationType, isMainFrame: bool) -> bool:
        scheme = url.scheme()
        if type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked and scheme in ("http", "https"):
            urlstr = url.toEncoded()
            logging.warning("Open <%s> in browser", urlstr)
            webbrowser.open(urlstr)
            return False
        return True

    def javaScriptConsoleMessage(
        self, level: QWebEnginePage.JavaScriptConsoleMessageLevel, message: str, lineNumber: int, sourceID: str
    ) -> None:
        sourceID = self.parent().clean_log_url(sourceID)

        if sourceID.startswith("data:"):
            sourceID = sourceID[:20] + "..."

        extra = {"sourceID": sourceID, "lineNumber": lineNumber}
        jslog.log(logmap[level], message, extra=extra)

    def run_script_async(self, script: str) -> None:
        self.runJavaScript(script)

    def run_script_sync(self, script: str) -> Any:
        loop = QtCore.QEventLoop()
        result: Optional[str] = None

        def callback(arg: Optional[str]) -> None:
            nonlocal result
            result = arg
            loop.quit()

        self.runJavaScript(script, 0, callback)
        loop.exec_()
        if isinstance(result, str):
            return json.loads(result)
        else:
            return None


class QMapBase(QWebEngineView):
    def __init__(
        self,
        channel_name: str,
        cache_dir: str = "cache",
        persistent_dir: str = "persistent",
    ) -> None:
        QWebEngineView.__init__(self)
        self.initialized = False

        channel = QWebChannel(self)
        page = QMapBasePage(channel, cache_dir, persistent_dir, self)
        self.setPage(page)
        self.loadFinished.connect(self.on_load_finished)

        channel.registerObject(channel_name, self)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:  # disable default QWebEngineView context menu
        pass

    def clean_log_url(self, url: str) -> str:
        return url

    def wait_until_ready(self) -> None:
        if not self.initialized:
            loop = QtCore.QEventLoop()
            self.loadFinished.connect(loop.quit)
            loop.exec_()

    @QtCore.Slot(bool)
    def on_load_finished(self, ok: bool) -> None:
        if not ok:
            raise RuntimeError("Could not initialize map")

        self.initialized = True

    def run_func_async(self, name: str, *args) -> None:
        script = js_func_call(name, args)
        self.page().run_script_async(script)

    def run_func_sync(self, name: str, *args) -> Any:
        script = js_func_call(name, args)
        return self.page().run_script_sync(script)
