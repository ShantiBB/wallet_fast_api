from locust import HttpUser, between, SequentialTaskSet, task
import random


class ApiTest(SequentialTaskSet):

    @task(1)
    def create_item(self):
        data = {
            'operation_type': 'deposit',
            'amount': random.randint(10, 100)
        }
        wallet_id = '38e4b5c1-626c-4273-a4c0-531d416ee6bc'
        absolute_url = f'/api/v1/wallets/{wallet_id}/operation/'
        self.client.post(absolute_url, json=data)

    @task(2)
    def get_items(self):
        absolute_url = '/api/v1/wallets/'
        self.client.get(absolute_url)

    @task(3)
    def get_item(self):
        wallet_id = '38e4b5c1-626c-4273-a4c0-531d416ee6bc'
        absolute_url = f'/api/v1/wallets/{wallet_id}/'
        self.client.get(absolute_url)


class UserBehavior(HttpUser):
    tasks = [ApiTest]
    wait_time = between(0.9, 1)
