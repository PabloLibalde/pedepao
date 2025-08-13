import httpx

class ApiClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self._client = httpx.Client(timeout=10)

    def list_products(self):
        r = self._client.get(f"{self.base_url}/products")
        r.raise_for_status()
        return r.json()

    def create_order(self, user_id: str, product_id: int):
        r = self._client.post(f"{self.base_url}/orders", json={"user_id": user_id, "product_id": product_id})
        r.raise_for_status()
        return r.json()


    def list_offers(self):
        r = self._client.get(f"{self.base_url}/offers")
        r.raise_for_status()
        return r.json()
