import os, json, requests
from typing import Optional

class ApiClient:
    def __init__(self, config_path: Optional[str] = None):
        cfg_path = config_path or os.path.join(os.path.dirname(__file__), "config.json")
        with open(cfg_path, "r", encoding="utf-8") as f:
            self.cfg = json.load(f)
        self.base = self.cfg["api_base"].rstrip("/")
        self.token: Optional[str] = None

    def _auth(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def healthy(self) -> bool:
        try:
            r = requests.get(f"{self.base}/health", timeout=3)
            return r.ok
        except Exception:
            return False

    # ---------- Auth ----------
    def login(self, email: str, password: str) -> bool:
        try:
            r = requests.post(
                f"{self.base}/auth/login_json",
                json={"email": email, "password": password},
                timeout=10,
            )
        except requests.RequestException:
            return False
        if r.ok:
            self.token = r.json().get("access_token")
            return bool(self.token)
        return False

    def me(self) -> dict:
        r = requests.get(f"{self.base}/auth/me", headers=self._auth(), timeout=10)
        r.raise_for_status()
        return r.json()

    # ---------- Usuário ----------
    def today_offers(self) -> dict:
        r = requests.get(f"{self.base}/offers/today", headers=self._auth(), timeout=10)
        r.raise_for_status()
        return r.json()

    def place_order(self, offer_id: int) -> dict:
        r = requests.post(
            f"{self.base}/orders",
            params={"offer_id": offer_id},
            headers=self._auth(),
            timeout=10,
        )
        if not r.ok:
            try:
                detail = r.json().get("detail")
            except Exception:
                detail = r.text
            raise RuntimeError(detail or "Erro ao registrar pedido")
        return (
            r.json()
            if r.headers.get("content-type", "").startswith("application/json")
            else {"ok": True}
        )

    # ---------- Admin: Ofertas ----------
    def create_offer(self, name: str, description: str | None, active: bool = True) -> dict:
        r = requests.post(
            f"{self.base}/offers",
            json={"name": name, "description": description, "active": active},
            headers=self._auth(),
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    def list_offers(self):
        r = requests.get(f"{self.base}/offers", headers=self._auth(), timeout=10)
        if r.status_code == 404:
            raise RuntimeError("GET /offers não disponível no backend")
        r.raise_for_status()
        return r.json()

    def update_offer(self, offer_id: int, data: dict):
        r = requests.put(
            f"{self.base}/offers/{offer_id}",
            json=data,
            headers=self._auth(),
            timeout=10,
        )
        if r.status_code == 404:
            raise RuntimeError("PUT /offers/{id} não disponível no backend")
        r.raise_for_status()
        return r.json()

    # ---------- Admin: Janela de oferta ----------
    def create_window(
        self,
        offer_id: int,
        start_date: str,
        end_date: str,
        weekdays: list[int],
        cutoff_local_time: str,
    ) -> dict:
        r = requests.post(
            f"{self.base}/offers/window",
            json={
                "offer_id": offer_id,
                "start_date": start_date,
                "end_date": end_date,
                "weekdays": weekdays,
                "cutoff_local_time": cutoff_local_time,
            },
            headers=self._auth(),
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    # ---------- Admin: Relatórios ----------
    def report_summary(self, date_from: str, date_to: str):
        r = requests.post(
            f"{self.base}/reports/summary",
            json={"date_from": date_from, "date_to": date_to},
            headers=self._auth(),
            timeout=20,
        )
        r.raise_for_status()
        return r.json().get("items", [])

    def report_detail(self, date_from: str, date_to: str):
        r = requests.post(
            f"{self.base}/reports/detail",
            json={"date_from": date_from, "date_to": date_to},
            headers=self._auth(),
            timeout=30,
        )
        r.raise_for_status()
        return r.json().get("items", [])
