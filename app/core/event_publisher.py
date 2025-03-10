import logging
from typing import Any, Dict, List

import requests
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed

from app.core.config import settings


class BaseEventPublisher:
    """
    Abstract base class for publishing events.
    Subclasses should implement specific event publishing methods.
    """

    def publish_user_deleted_event(self, id: str) -> None:
        raise NotImplementedError(
            "Subclasses must implement publish_user_deleted_event"
        )

    def publish_user_created_event(self, id: str) -> None:
        raise NotImplementedError(
            "Subclasses must implement publish_user_created_event"
        )


class HTTPEventPublisher(BaseEventPublisher):
    """
    An event publisher that sends HTTP POST requests to target service endpoints.
    It uses tenacity to retry sending the request until a successful response is received,
    or until the maximum number of attempts is reached.

    Expected configuration in settings:
      - EVENTS_ENABLED: Boolean flag to enable event publishing.
      - EVENT_TARGETS: dict mapping event names (e.g., "user_created", "user_deleted") to a list of target URLs.
      - EVENT_MAX_ATTEMPTS: int for maximum retry attempts (default: 5).
      - EVENT_RETRY_DELAY: int for delay in seconds between retry attempts (default: 1).
    """

    def __init__(self) -> None:
        self.services: Dict[str, List[str]] = getattr(settings, "EVENT_TARGETS", {})
        self.max_attempts: int = getattr(settings, "EVENT_MAX_ATTEMPTS", 5)
        self.retry_delay: int = getattr(settings, "EVENT_RETRY_DELAY", 1)
        self.logger = logging.getLogger(__name__)

    @retry(
        stop=stop_after_attempt(getattr(settings, "EVENT_MAX_ATTEMPTS", 5)),
        wait=wait_fixed(getattr(settings, "EVENT_RETRY_DELAY", 1)),
        retry=retry_if_result(lambda r: r is None or r.status_code != 200),
        reraise=True,
    )
    def _send_request(
        self, url: str, payload: Dict[str, Any], method: str = "POST"
    ) -> requests.Response:
        """
        Sends an HTTP request with the given payload to the specified URL.
        Automatically retries the request if the response status code is not 200.

        Args:
            url: The target URL
            payload: The JSON payload to send
            method: HTTP method to use (default: "POST")
        """
        self.logger.debug(f"Sending {method} request to {url} with payload: {payload}")
        if method.upper() == "DELETE":
            user_id = str(payload.get("id", ""))
            params = {"id": user_id}
            response = requests.delete(url, params=params, timeout=5)
        else:
            response = requests.post(url, json=payload, timeout=5)
        if response.status_code != 200:
            self.logger.error(f"Received status code {response.status_code} from {url}")
        return response

    def _publish_event(self, event: str, payload: Dict[str, Any]) -> None:
        """
        Iterates over all target URLs for the given event and sends the payload.
        Logs an error if the event could not be delivered after retrying.
        """
        targets: List[str] = self.services.get(event, [])
        if not targets:
            self.logger.warning(f"No target services configured for event '{event}'.")
        for url in targets:
            try:
                method = "DELETE" if event == "user_deleted" else "POST"
                response = self._send_request(url, payload, method)
                self.logger.info(
                    f"Event '{event}' delivered to {url} with status {response.status_code}"
                )
            except Exception as e:
                self.logger.error(
                    f"Failed to deliver event '{event}' to {url} after {self.max_attempts} attempts: {e}"
                )

    def publish_user_deleted_event(self, id: str) -> None:
        """
        Publishes a user deletion event by assembling the payload and sending it to the target endpoints.
        """
        payload = {"event": "user_deleted", "id": id}
        self._publish_event("user_deleted", payload)

    def publish_user_created_event(self, id: str) -> None:
        """
        Publishes a user creation event by assembling the payload and sending it to the target endpoints.
        """
        payload = {"event": "user_created", "id": id}
        self._publish_event("user_created", payload)


class NullEventPublisher(BaseEventPublisher):
    """
    A null implementation that logs events instead of sending them.
    Useful for local or small projects where event publishing is not enabled.
    """

    def publish_user_deleted_event(self, id: str) -> None:
        logging.info(
            f"[NullEventPublisher] Would publish user_deleted event for user_id: {id}"
        )

    def publish_user_created_event(self, id: str) -> None:
        logging.info(
            f"[NullEventPublisher] Would publish user_created event for user_id: {id}"
        )


def get_event_publisher() -> BaseEventPublisher:
    """
    Factory function to retrieve an instance of an event publisher.
    If EVENTS_ENABLED is True in the settings, it returns an HTTPEventPublisher,
    otherwise it returns a NullEventPublisher.
    """
    if getattr(settings, "EVENTS_ENABLED", False):
        return HTTPEventPublisher()
    else:
        return NullEventPublisher()
