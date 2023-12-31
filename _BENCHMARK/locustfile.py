from locust import HttpUser, task


class RunLoad(HttpUser):
    @task
    def get_all(self):
        self.client.get("/")

    @task
    def create(self):
        self.client.post("/")
