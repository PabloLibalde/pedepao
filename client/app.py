import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox
from PySide6.QtCore import QTimer

from services.api import ApiClient

TZ = "America/Sao_Paulo"
CUTOFF = "13:00"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.api = ApiClient()
        self.setWindowTitle("PedePao")
        self.layout = QVBoxLayout(self)

        self.info = QLabel("Selecione uma oferta e envie seu pedido (1 por dia).")
        self.timer_label = QLabel("")
        self.listw = QListWidget()
        self.btn = QPushButton("Enviar pedido")
        self.btn.clicked.connect(self.enviar)

        self.layout.addWidget(self.info)
        self.layout.addWidget(self.timer_label)
        self.layout.addWidget(self.listw)
        self.layout.addWidget(self.btn)

        self.load_offers()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cutoff_state)
        self.timer.start(1000)
        self.update_cutoff_state()

    def load_offers(self):
        try:
            for o in self.api.list_offers():
                if o["is_active"]:
                    self.listw.addItem(f'{o["id"]} - {o["product_name"]}')
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar produtos: {e}")

    def cutoff_passed(self) -> bool:
        now = datetime.now(ZoneInfo(TZ)).strftime("%H:%M")
        return now >= CUTOFF

    def update_cutoff_state(self):
        now = datetime.now(ZoneInfo(TZ))
        cutoff_h, cutoff_m = map(int, CUTOFF.split(":"))
        cutoff_dt = now.replace(hour=cutoff_h, minute=cutoff_m, second=0, microsecond=0)
        remaining = (cutoff_dt - now).total_seconds()
        if remaining <= 0:
            self.timer_label.setText("Após o cutoff das 13:00 — pedidos bloqueados.")
            self.btn.setEnabled(False)
        else:
            self.timer_label.setText(f"Faltam {int(remaining)} segundos para o cutoff ({CUTOFF}).")
            self.btn.setEnabled(True)

    def enviar(self):
        if self.cutoff_passed():
            QMessageBox.warning(self, "Atenção", "Pedido após o cutoff não é permitido.")
            return
        item = self.listw.currentItem()
        if not item:
            QMessageBox.information(self, "Info", "Selecione uma oferta.")
            return
        offer_id = int(item.text().split(" - ")[0])
        try:
            # Encontrar a oferta selecionada para obter o product_id
            offers = self.api.list_offers()
            selected = next((o for o in offers if o["id"] == offer_id), None)
            if not selected:
                raise Exception("Oferta não encontrada")
            prod_id = selected["product_id"]
            # user_id fixo apenas para demo. Integre com login conforme necessário.
            resp = self.api.create_order(user_id="demo-user", product_id=prod_id)
            QMessageBox.information(self, "Sucesso", f"Pedido criado: {resp}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao criar pedido: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(480, 600)
    w.show()
    sys.exit(app.exec())
