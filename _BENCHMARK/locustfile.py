from locust import HttpUser, task


class RunLoad(HttpUser):
    @task
    def filter_random(self):
        self.client.get("/benchmark/filter")

    @task
    def create_random(self):
        self.client.post("/benchmark/create")
