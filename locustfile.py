from locust import HttpUser, task, between


class FinanceUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def home(self):
        self.client.get("/")

    @task(2)
    def transactions(self):
        self.client.get("/transactions")

    @task(1)
    def dashboard(self):
        self.client.get("/dashboard")

    @task(1)
    def api(self):
        self.client.get("/api/v1/transactions")
        