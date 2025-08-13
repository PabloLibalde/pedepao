from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel

class LoginWidget(QWidget):
    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.setWindowTitle("PedePao - Login")

        self.email = QLineEdit(placeholderText="Email")
        self.pw = QLineEdit(placeholderText="Senha"); self.pw.setEchoMode(QLineEdit.Password)
        self.msg = QLabel("")

        btn = QPushButton("Entrar")
        btn.clicked.connect(self._do_login)

        lay = QVBoxLayout(self); lay.addWidget(self.email); lay.addWidget(self.pw); lay.addWidget(btn); lay.addWidget(self.msg)

    def _do_login(self):
        e = self.email.text().strip()
        p = self.pw.text()
        if not e or not p:
            self.msg.setText("Informe e-mail e senha")
            return
        self.on_login(e, p)

    def set_error(self, text: str):
        self.msg.setText(text)
