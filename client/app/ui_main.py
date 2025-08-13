from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QCheckBox,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QGridLayout, QGroupBox, QDialog, QDialogButtonBox
)

class OffersTab(QWidget):
    def __init__(self, api):
        super().__init__()
        self.api = api

        # -------- lista à esquerda --------
        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self._edit_selected)

        btn_reload = QPushButton("Atualizar lista")
        btn_reload.clicked.connect(self._reload)

        left = QVBoxLayout()
        left.addWidget(QLabel("Ofertas cadastradas"))
        left.addWidget(self.list)
        left.addWidget(btn_reload)

        # -------- criar nova oferta (direita) --------
        self.name = QLineEdit()
        self.desc = QTextEdit()
        self.active = QCheckBox("Ativa"); self.active.setChecked(True)
        btn_create = QPushButton("Cadastrar oferta")
        btn_create.clicked.connect(self.create_offer)

        form = QGridLayout()
        form.addWidget(QLabel("Nome"), 0,0); form.addWidget(self.name,0,1)
        form.addWidget(QLabel("Descrição"),1,0); form.addWidget(self.desc,1,1)
        form.addWidget(self.active,2,1)
        form.addWidget(btn_create,3,1)

        box = QGroupBox("Nova oferta")
        box.setLayout(form)

        right = QVBoxLayout()
        right.addWidget(box)
        right.addStretch(1)

        root = QHBoxLayout(self)
        root.addLayout(left, 3)
        root.addLayout(right, 5)

        self._reload()

    def _reload(self):
        try:
            data = self.api.list_offers()
            self.list.clear()
            for row in data:
                item = QListWidgetItem(f"{row.get('id')} - {row.get('name')}")
                item.setData(32, row)  # guarda o dict
                self.list.addItem(item)
        except Exception as e:
            self.list.clear()
            self.list.addItem(f"(Falha ao carregar: {e})")

    def _edit_selected(self, item: QListWidgetItem):
        row = item.data(32) or {}
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Editar oferta #{row.get('id')}")
        nm = QLineEdit(row.get("name",""))
        ds = QTextEdit(); ds.setPlainText(row.get("description") or "")
        ac = QCheckBox("Ativa"); ac.setChecked(bool(row.get("active")))
        frm = QGridLayout()
        frm.addWidget(QLabel("Nome"),0,0); frm.addWidget(nm,0,1)
        frm.addWidget(QLabel("Descrição"),1,0); frm.addWidget(ds,1,1)
        frm.addWidget(ac,2,1)
        btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        frm.addWidget(btns,3,1)
        dlg.setLayout(frm)

        def do_save():
            try:
                self.api.update_offer(
                    int(row["id"]),
                    {"name": nm.text().strip(), "description": ds.toPlainText().strip(), "active": ac.isChecked()}
                )
                QMessageBox.information(self,"OK","Oferta atualizada.")
                dlg.accept()
                self._reload()
            except Exception as e:
                QMessageBox.critical(self,"Erro",str(e))

        btns.accepted.connect(do_save)
        btns.rejected.connect(dlg.reject)
        dlg.exec()

    def create_offer(self):
        try:
            resp = self.api.create_offer(
                self.name.text().strip(),
                self.desc.toPlainText().strip(),
                self.active.isChecked()
            )
            QMessageBox.information(self, "OK", f"Oferta criada (id={resp.get('id','?')})")
            self.name.clear(); self.desc.clear(); self.active.setChecked(True)
            self._reload()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
