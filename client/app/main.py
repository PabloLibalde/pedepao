import sys, os, json
from PySide6.QtWidgets import QApplication, QWidget, QStackedLayout, QTabWidget, QVBoxLayout
from api_client import ApiClient
from ui_login import LoginWidget
from ui_blocks import OrderBlocks
from ui_settings import SettingsTab
from scheduler import DailyTrigger
import autostart_windows

def bring_to_front(win):
    win.show(); win.raise_(); win.activateWindow()
    try:
        import win32gui, win32con
        hwnd = int(win.winId())
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        pass

def main():
    app = QApplication(sys.argv)

    cfg_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    hh, mm = map(int, cfg["bring_to_front_time"].split(":"))

    api = ApiClient()

    root = QWidget()
    stack = QStackedLayout(root)

    def on_login(email: str, pw: str):
        if not api.login(email, pw):
            login.set_error("Falha no login")
            return
        me = api.me()

        tabs = QTabWidget()
        tabs.addTab(OrderBlocks(api, me, cfg), "Meu pedido")
        if me.get("is_admin"):
            tabs.addTab(SettingsTab(api), "Configurações")

        wrapper = QWidget()
        lay = QVBoxLayout(wrapper); lay.addWidget(tabs)

        stack.addWidget(wrapper)
        stack.setCurrentWidget(wrapper)
        wrapper.show(); root.show()

    login = LoginWidget(on_login)
    stack.addWidget(login); stack.setCurrentWidget(login)

    def daily_focus():
        if api.healthy():
            bring_to_front(root)

    DailyTrigger(hh, mm, cfg["tz"], daily_focus)

    root.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
