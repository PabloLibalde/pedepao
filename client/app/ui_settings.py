from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QCheckBox,
    QPushButton, QDateEdit, QGroupBox, QGridLayout, QMessageBox, QListWidget, QListWidgetItem, QDialog, QFormLayout
)
from PySide6.QtCore import QDate

class OfferEditDialog(QDialog):
    def __init__(self, offer: dict, on_save):
        super().__init__()
        self.offer = dict(offer)
        self.on_save = on_save
        self.setWindowTitle(f"Editar oferta #{offer.get('id','?')}")
        self.name = QLineEdit(self.offer.get("name",""))
        self.desc = QTextEdit(self.offer.get("description","") or "")
        self.active = QCheckBox("Ativa"); self.active.setChecked(self.offer.get("active", True))

        form = QFormLayout(self)
        form.addRow("Nome", self.name)
        form.addRow("Descrição", self.desc)
        form.addRow("", self.active)
        btn = QPushButton("Salvar"); form.addRow(btn)
        btn.clicked.connect(self._save)

    def _save(self):
        data = {
            "name": self.name.text().strip(),
            "description": self.desc.toPlainText().strip(),
            "active": self.active.isChecked()
        }
        self.on_save(self.offer["id"], data)
        self.accept()

class SettingsTab(QWidget):
    """
    Configurações (Admin): lista e edita ofertas + cadastra novas ofertas e janelas.
    """
    def __init__(self, api):
        super().__init__()
        self.api = api

        # Lista de ofertas com 2 cliques para editar
        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self._edit_selected)
        btn_refresh = QPushButton("Atualizar lista")
        btn_refresh.clicked.connect(self._load_offers)

        # --- Nova Oferta ---
        self.off_name = QLineEdit()
        self.off_desc = QTextEdit()
        self.off_active = QCheckBox("Ativa"); self.off_active.setChecked(True)
        btn_offer = QPushButton("Cadastrar oferta")
        btn_offer.clicked.connect(self._create_offer)

        g1 = QGridLayout()
        g1.addWidget(QLabel("Nome"),0,0); g1.addWidget(self.off_name,0,1)
        g1.addWidget(QLabel("Descrição"),1,0); g1.addWidget(self.off_desc,1,1)
        g1.addWidget(self.off_active,2,1)
        g1.addWidget(btn_offer,3,1)

        gb1 = QGroupBox("Nova oferta"); gb1.setLayout(g1)

        # --- Janela ---
        self.win_offer_id = QLineEdit()
        self.win_start = QDateEdit(); self.win_start.setCalendarPopup(True); self.win_start.setDate(QDate.currentDate())
        self.win_end = QDateEdit(); self.win_end.setCalendarPopup(True); self.win_end.setDate(QDate.currentDate().addMonths(1))
        self.ck = { "Seg": QCheckBox("Seg"),
                    "Ter": QCheckBox("Ter"),
                    "Qua": QCheckBox("Qua"),
                    "Qui": QCheckBox("Qui"),
                    "Sex": QCheckBox("Sex"),
                    "Sáb": QCheckBox("Sáb"),
                    "Dom": QCheckBox("Dom") }
        self.cutoff = QLineEdit(); self.cutoff.setPlaceholderText("13:00")
        btn_window = QPushButton("Criar janela")
        btn_window.clicked.connect(self._create_window)

        g2 = QGridLayout()
        g2.addWidget(QLabel("Offer ID"),0,0); g2.addWidget(self.win_offer_id,0,1)
        g2.addWidget(QLabel("Início"),1,0); g2.addWidget(self.win_start,1,1)
        g2.addWidget(QLabel("Fim"),2,0); g2.addWidget(self.win_end,2,1)
        g2.addWidget(QLabel("Dias da semana"),3,0)
        row = QHBoxLayout()
        for k in ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]:
            row.addWidget(self.ck[k])
        g2.addLayout(row,3,1)
        g2.addWidget(QLabel("Cutoff (HH:MM)"),4,0); g2.addWidget(self.cutoff,4,1)
        g2.addWidget(btn_window,5,1)

        gb2 = QGroupBox("Janela (Oferta ativa em período e dias)"); gb2.setLayout(g2)

        left = QVBoxLayout(); left.addWidget(QLabel("Ofertas cadastradas")); left.addWidget(self.list); left.addWidget(btn_refresh)
        right = QVBoxLayout(); right.addWidget(gb1); right.addWidget(gb2); right.addStretch(1)
        root = QHBoxLayout(self); 
        root.addLayout(left,1); root.addLayout(right,2)

        self._load_offers()

    def _load_offers(self):
        self.list.clear()
        try:
            data = self.api.list_offers()
            # aceita lista bruta ou {"items":[...]}
            items = data if isinstance(data, list) else data.get("items", [])
            for of in items:
                it = QListWidgetItem(f"#{of.get('id','?')} - {of.get('name','')}  [{'Ativa' if of.get('active') else 'Inativa'}]")
                it.setData(32, of)  # Qt.UserRole
                self.list.addItem(it)
        except Exception as e:
            self.list.addItem(f"(Falha ao carregar ofertas: {e})")

    def _edit_selected(self, item: QListWidgetItem):
        of = item.data(32)
        if not isinstance(of, dict): return
        def do_save(offer_id, data):
            try:
                self.api.update_offer(offer_id, data)
                self._load_offers()
            except Exception as e:
                QMessageBox.critical(self, "Erro", str(e))
        dlg = OfferEditDialog(of, do_save); dlg.exec()

    def _create_offer(self):
        try:
            r = self.api.create_offer(self.off_name.text().strip(), self.off_desc.toPlainText().strip(), self.off_active.isChecked())
            self._load_offers()
            QMessageBox.information(self,"OK",f"Oferta criada (id={r.get('id','?')})")
        except Exception as e:
            QMessageBox.critical(self,"Erro",str(e))

    def _create_window(self):
        try:
            wdmap = {"Seg":1,"Ter":2,"Qua":3,"Qui":4,"Sex":5,"Sáb":6,"Dom":7}
            wdays = [wdmap[k] for k,cb in self.ck.items() if cb.isChecked()]
            if not wdays:
                raise RuntimeError("Selecione ao menos um dia.")
            s = self.win_start.date().toString("yyyy-MM-dd")
            e = self.win_end.date().toString("yyyy-MM-dd")
            co = self.cutoff.text().strip() or "13:00"
            oid = int(self.win_offer_id.text().strip())
            self.api.create_window(oid, s, e, wdays, co)
            QMessageBox.information(self,"OK","Janela criada.")
        except Exception as e:
            QMessageBox.critical(self,"Erro",str(e))
