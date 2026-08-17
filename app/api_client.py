from __future__ import annotations

from typing import Any

import httpx

from app.config import API_BASE_URL, API_TIMEOUT_SECONDS


class ApiError(RuntimeError):
    """A user-safe API failure."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class ApiClient:
    def __init__(
        self,
        base_url: str = API_BASE_URL,
        timeout: float = API_TIMEOUT_SECONDS,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.access_token: str | None = None
        self.user: dict[str, Any] | None = None
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            transport=transport,
        )

    @property
    def is_authenticated(self) -> bool:
        return bool(self.access_token)

    def close(self) -> None:
        self._client.close()

    def logout(self) -> None:
        self.access_token = None
        self.user = None

    def _headers(self) -> dict[str, str]:
        if not self.access_token:
            return {}
        return {"Authorization": f"Bearer {self.access_token}"}

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        headers = dict(kwargs.pop("headers", {}))
        headers.update(self._headers())
        try:
            response = self._client.request(method, path, headers=headers, **kwargs)
        except httpx.TimeoutException as exc:
            raise ApiError("The server took too long to respond. Please try again.") from exc
        except httpx.RequestError as exc:
            raise ApiError(
                "Cannot connect to the MedicalAssist server. Start the backend and try again."
            ) from exc

        if response.is_error:
            try:
                payload = response.json()
                message = payload.get("detail") or payload.get("message")
            except (ValueError, AttributeError):
                message = None
            if not message:
                message = f"The server returned an error ({response.status_code})."
            raise ApiError(str(message), response.status_code)

        if not response.content:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise ApiError("The server returned an invalid response.") from exc

    def health(self) -> dict[str, Any]:
        return self._request("GET", "/health")

    def login(self, username: str, password: str) -> dict[str, Any]:
        data = self._request(
            "POST",
            "/login",
            data={"username": username, "password": password},
        )
        if not isinstance(data, dict):
            raise ApiError("The server returned an invalid login response.")

        access_token = data.get("access_token")
        role = str(data.get("role", "")).lower()
        if not access_token or role not in {"cadet", "doctor"}:
            raise ApiError("The server returned an incomplete login response.")

        data["role"] = role
        self.access_token = str(access_token)
        self.user = data
        return data

    def get_profile(self) -> dict[str, Any]:
        if not self.user:
            raise ApiError("You are not logged in.")
        return self._request("GET", f"/users/{self.user['user_id']}")

    def get_cases(self) -> list[dict[str, Any]]:
        return self._request("GET", "/cases")

    def create_case(self, symptoms: str) -> dict[str, Any]:
        return self._request("POST", "/cases", json={"symptoms": symptoms})

    def get_case(self, case_id: int) -> dict[str, Any]:
        return self._request("GET", f"/cases/{case_id}")

    def get_case_response(self, case_id: int) -> dict[str, Any]:
        return self._request("GET", f"/cases/{case_id}/response")

    def get_messages(self, case_id: int) -> list[dict[str, Any]]:
        return self._request("GET", f"/cases/{case_id}/messages")

    def ask_assistant(self, case_id: int, message: str) -> dict[str, Any]:
        return self._request(
            "POST", f"/cases/{case_id}/assistant", json={"message": message}
        )

    def get_doctor_cases(self) -> list[dict[str, Any]]:
        return self._request("GET", "/doctor/cases")

    def get_doctor_case(self, case_id: int) -> dict[str, Any]:
        return self._request("GET", f"/doctor/cases/{case_id}")

    def submit_doctor_decision(
        self, case_id: int, decision: str, response: str
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/doctor/cases/{case_id}/decision",
            json={"decision": decision, "response": response},
        )

    def get_notifications(self) -> list[dict[str, Any]]:
        return self._request("GET", "/notifications")
