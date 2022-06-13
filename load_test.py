import json
import logging
from locust import FastHttpUser, constant, task
from uuid import uuid4

from string import ascii_letters
from random import sample
from typing import TypedDict


log = logging.getLogger()


class Payload(TypedDict):
    email: str
    uuid: str


def payload_generate() -> Payload:
    """
    generate valid mail and uuid
    """
    return Payload(
        email=f"{''.join(sample(ascii_letters, 7))}@{''.join(sample(ascii_letters,4))}.{''.join(sample(ascii_letters,3))}",
        uuid=str(uuid4()),
    )


class LocustClient(FastHttpUser):

    host = "http://fastapi.localhost:8008"
    wait_time = constant(0)

    def __init__(self, environment):

        super().__init__(environment)

    def on_start(self):
        """on_start is called when a Locust start before any task is scheduled"""
        pass

    def on_stop(self):
        """on_stop is called when the TaskSet is stopping"""
        pass

    @task
    def load_rest_api_based_service(self):
        """This method contains all the APIs that needs to be load tested for a service."""

        try:

            path = "/save_mail"
            headers = {"accept": "application/json", "Content-Type": "application/json"}
            generated_payload = payload_generate()
            api_payload = json.dumps(generated_payload)

            with self.client.post(
                path, catch_response=True, data=api_payload, headers=headers
            ) as resp_of_api:

                if resp_of_api.status_code == 201:

                    resp_body_of_api = resp_of_api.json()

                    assert (
                        resp_body_of_api["data"].get("email").lower()
                        == generated_payload["email"].lower()
                    )
                    assert (
                        resp_body_of_api["data"].get("uuid")
                        == generated_payload["uuid"]
                    )
                    resp_of_api.success()

        except Exception as ex:
            log.error(f"catch {ex}")
