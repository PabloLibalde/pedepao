import os, sys, datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QScrollArea, QGridLayout, QFrame
)
from PySide6.QtCore import Qt, Signal
from scheduler import get_tz

def _log_path():
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, "pedido.dll")

def _audit_log(line: str):
    try:
        with open(_log_path(), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

class Card(QFrame):
    clicked = Signal(int, str)
    def __init__(self, offer_id: int, name: str):
        super().__init__()
        self.offer_id = offer_id
        self.name = name
        self.setObjectName("card")
        self.setFrameShape(QFrame.StyledPanel)
        self.setProperty("selected", False)
        self.setStyleSheet("""
            QFrame#card {
                border: 2px solid #444;
                border-radius: 8px;
                padding: 10px;
            }
            QFrame#card[selected="true"] {
                border: 3px solid #2a82da;
                background: #1f2630;
            }
        """)
        lbl = QLabel(name); lbl.setWordWrap(True)
        lay = QVBoxLayout(self); lay.addWidget(lbl)

    def mousePressEvent(self, e):
        self.clicked.emit(self.offer_id, self.name)

    def set_selected(self, val: bool):
        self.setProperty("selected", "true" if val else "false")
        self.style().unpolish(self); self.style().polish(self); self.update()

class OrderBlocks(QWidget):
    def __init__(self, api, me: dict, cfg: dict):
        super().__init__()
        self.api = api; self.me = me; self.cfg = cfg
        self.tz = get_tz(cfg.get("tz","UTC"))
        self.setWindowTitle("PedePao - Meu pedido")

        self.info = QLabel("Carregando ofertas ...")
        self.grid = QGridLayout(); self.grid.setSpacing(10)
        wrap = QWidget(); wrap.setLayout(self.grid)

        sc = QScrollArea(); sc.setWidgetResizable(True); sc.setWidget(wrap)

        self.btn = QPushButton("Fazer/Alterar pedido")
        self.btn.clicked.connect(self._confirm_current)

        lay = QVBoxLayout(self); lay.addWidget(self.info); lay.addWidget(sc); lay.addWidget(self.btn)

        self.cards = []
        self.selected_id = None
        self.cutoff_hhmm = "13:00"
        self.refresh()

    def _is_after_cutoff(self):
        try:
            hh, mm = map(int, (self.cutoff_hhmm or "13:00").split(":"))
            now = datetime.datetime.now(self.tz)
            limit = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
            return now > limit
        except Exception:
            return False

    def _update_cutoff_state(self):
        if self._is_after_cutoff():
            self.btn.setEnabled(False)
            self.info.setText(f"Pedidos até {self.cutoff_hhmm} — prazo encerrado.")
        else:
            self.btn.setEnabled(True)
            self.info.setText(f"Pedidos até {self.cutoff_hhmm}")

    def refresh(self):
        data = self.api.today_offers()
        items = data.get("items", [])
        # cutoff
        co = None
        for it in items: co = it.get("cutoff") or co
        self.cutoff_hhmm = co or "13:00"
        self._update_cutoff_state()

        # limpar grade
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w: w.setParent(None)
        self.cards = []; self.selected_id = None

        if not items:
            self.info.setText("Sem ofertas ativas hoje.")
            self.btn.setEnabled(False)
            return
        col_max = 3
        r = c = 0
        for it in items:
            oid = int(it["offer_id"])
            name = it["name"]
            card = Card(oid, name)
            card.clicked.connect(self._select)
            self.grid.addWidget(card, r, c)
            self.cards.append(card)
            c += 1
            if c >= col_max:
                c = 0; r += 1

    def _select(self, offer_id: int, name: str):
        self.selected_id = offer_id
        for card in self.cards:
            card.set_selected(card.offer_id == offer_id)

    def _confirm_current(self):
        if self._is_after_cutoff():
            QMessageBox.warning(self, "Prazo encerrado", f"O prazo terminou às {self.cutoff_hhmm}.")
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _audit_log(f"{ts}; user={self.me.get('email','')}; action=blocked_after_cutoff; cutoff={self.cutoff_hhmm}")
            return
        if not self.selected_id:
            QMessageBox.warning(self, "Atenção", "Selecione um item.")
            return
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.api.place_order(self.selected_id)
            _audit_log(f"{ts}; user={self.me.get('email','')}; action=select; item_id={self.selected_id}; result=ok")
            QMessageBox.information(self, "OK", "Pedido registrado/atualizado!")
        except Exception as e:
            _audit_log(f"{ts}; user={self.me.get('email','')}; action=select; item_id={self.selected_id}; result={str(e)}")
            QMessageBox.critical(self, "Erro", str(e))
