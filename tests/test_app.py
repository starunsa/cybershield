import os
import unittest
from unittest.mock import patch

os.environ["FLASK_ENV"] = "testing"

from app import create_app
from src.models import db


class CyberShieldAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def register_user(self, username="alice", email="alice@example.com", password="password123"):
        return self.client.post(
            "/api/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password,
                "full_name": "Alice Example",
            },
        )

    def login_user(self, username="alice", password="password123"):
        return self.client.post(
            "/api/auth/login",
            json={"username": username, "password": password},
        )

    def auth_headers(self):
        self.register_user()
        response = self.login_user()
        token = response.get_json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_register_login_and_validate_token(self):
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 201)

        login_response = self.login_user()
        self.assertEqual(login_response.status_code, 200)
        token = login_response.get_json()["access_token"]
        self.assertTrue(token)

        validate_response = self.client.get(
            "/api/auth/validate",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(validate_response.status_code, 200)
        self.assertTrue(validate_response.get_json()["valid"])

    def test_dashboard_contains_logout_fallback(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('id="logoutBtn"', html)
        self.assertIn('onclick="logout(event)"', html)
        self.assertIn('dashboard.js?v=20260529-5', html)

    def test_chat_greeting_send_history_and_sessions(self):
        headers = self.auth_headers()

        greeting_response = self.client.post("/api/chat/greeting", headers=headers)
        self.assertEqual(greeting_response.status_code, 200)
        self.assertIn("CyberGuard", greeting_response.get_json()["greeting"])

        chat_response = self.client.post(
            "/api/chat/send",
            headers=headers,
            json={"message": "Analyze my API security"},
        )
        self.assertEqual(chat_response.status_code, 200)
        chat_data = chat_response.get_json()
        self.assertIn("API security", chat_data["bot_response"])
        self.assertIsNotNone(chat_data["session_id"])

        history_response = self.client.get(
            f"/api/chat/history/{chat_data['session_id']}",
            headers=headers,
        )
        self.assertEqual(history_response.status_code, 200)
        self.assertEqual(len(history_response.get_json()["messages"]), 2)

        sessions_response = self.client.get("/api/chat/sessions", headers=headers)
        self.assertEqual(sessions_response.status_code, 200)
        self.assertEqual(len(sessions_response.get_json()["sessions"]), 1)

    def test_chat_recovers_from_stale_session_id(self):
        headers = self.auth_headers()

        chat_response = self.client.post(
            "/api/chat/send",
            headers=headers,
            json={"message": "hi", "session_id": 9999},
        )

        self.assertEqual(chat_response.status_code, 200)
        self.assertIn("bot_response", chat_response.get_json())
        self.assertIsNotNone(chat_response.get_json()["session_id"])

    def test_chat_gives_specific_image_examples_when_requested(self):
        headers = self.auth_headers()

        for message in ["give me image to scan", "give me image name"]:
            chat_response = self.client.post(
                "/api/chat/send",
                headers=headers,
                json={"message": message},
            )

            self.assertEqual(chat_response.status_code, 200)
            bot_response = chat_response.get_json()["bot_response"]
            self.assertIn("nginx:latest", bot_response)
            self.assertIn("alpine:latest", bot_response)
            self.assertNotIn("Container image scanning checks:", bot_response)

    def test_chat_recognizes_container_image_target(self):
        headers = self.auth_headers()

        chat_response = self.client.post(
            "/api/chat/send",
            headers=headers,
            json={"message": "nginx:latest"},
        )

        self.assertEqual(chat_response.status_code, 200)
        bot_response = chat_response.get_json()["bot_response"]
        self.assertIn("valid container image target", bot_response)
        self.assertIn("Image Scanning", bot_response)

    def test_chat_gives_specific_website_examples_when_requested(self):
        headers = self.auth_headers()

        chat_response = self.client.post(
            "/api/chat/send",
            headers=headers,
            json={"message": "suggest a website which I can scan"},
        )

        self.assertEqual(chat_response.status_code, 200)
        bot_response = chat_response.get_json()["bot_response"]
        self.assertIn("https://example.com", bot_response)
        self.assertIn("https://owasp.org", bot_response)

    def test_invalid_token_response_has_error_for_cached_clients(self):
        response = self.client.post(
            "/api/chat/send",
            headers={"Authorization": "Bearer invalid-token"},
            json={"message": "hi"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("error", response.get_json())

    def test_delete_chat_session_removes_history(self):
        headers = self.auth_headers()
        chat_response = self.client.post(
            "/api/chat/send",
            headers=headers,
            json={"message": "hi"},
        )
        session_id = chat_response.get_json()["session_id"]

        delete_response = self.client.delete(
            f"/api/chat/session/{session_id}",
            headers=headers,
        )
        self.assertEqual(delete_response.status_code, 200)

        sessions_response = self.client.get("/api/chat/sessions", headers=headers)
        self.assertEqual(sessions_response.status_code, 200)
        self.assertEqual(sessions_response.get_json()["sessions"], [])

        history_response = self.client.get(
            f"/api/chat/history/{session_id}",
            headers=headers,
        )
        self.assertEqual(history_response.status_code, 403)

    def test_profile_update_and_password_change(self):
        headers = self.auth_headers()

        profile_response = self.client.put(
            "/api/user/profile",
            headers=headers,
            json={"full_name": "Alice Updated", "email": "alice.updated@example.com"},
        )
        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(profile_response.get_json()["user"]["full_name"], "Alice Updated")

        password_response = self.client.post(
            "/api/user/change-password",
            headers=headers,
            json={"old_password": "password123", "new_password": "newpassword123"},
        )
        self.assertEqual(password_response.status_code, 200)

        login_response = self.login_user(password="newpassword123")
        self.assertEqual(login_response.status_code, 200)

    @patch("src.routes.security_agent.analyze_api")
    @patch("src.routes.security_agent.analyze_image")
    @patch("src.routes.web_scanner.scan_website")
    def test_security_analysis_endpoints(self, mock_scan_website, mock_analyze_image, mock_analyze_api):
        headers = self.auth_headers()
        mock_analyze_api.return_value = {
            "url": "https://api.example.com/health",
            "method": "GET",
            "risks": [],
            "resolutions": [],
            "status_code": 200,
        }
        mock_analyze_image.return_value = {
            "image": "nginx:latest",
            "vulnerabilities": [],
            "risks": [],
            "resolutions": [],
        }
        mock_scan_website.return_value = {
            "url": "https://example.com",
            "overall_score": 90,
            "risks": [],
            "recommendations": [],
            "ssl_check": {"status": "PASS"},
            "headers_check": {"missing_headers": []},
        }

        api_response = self.client.post(
            "/api/security/analyze-api",
            headers=headers,
            json={"url": "https://api.example.com/health", "method": "GET"},
        )
        self.assertEqual(api_response.status_code, 200)
        self.assertTrue(api_response.get_json()["success"])

        image_response = self.client.post(
            "/api/security/scan-image",
            headers=headers,
            json={"image": "nginx:latest"},
        )
        self.assertEqual(image_response.status_code, 200)
        self.assertTrue(image_response.get_json()["success"])

        website_response = self.client.post(
            "/api/security/scan-website",
            headers=headers,
            json={"url": "https://example.com"},
        )
        self.assertEqual(website_response.status_code, 200)
        self.assertTrue(website_response.get_json()["success"])

        report_response = self.client.post(
            "/api/security/report",
            headers=headers,
            json={
                "api_urls": ["https://api.example.com/health"],
                "images": ["nginx:latest"],
                "websites": ["https://example.com"],
            },
        )
        self.assertEqual(report_response.status_code, 200)
        self.assertTrue(report_response.get_json()["success"])
        self.assertIn("Website Analysis", report_response.get_json()["report"])

    @patch("src.routes.security_agent.analyze_api")
    @patch("src.routes.security_agent.analyze_image")
    @patch("src.routes.web_scanner.scan_website")
    def test_end_to_end_user_security_workflow(self, mock_scan_website, mock_analyze_image, mock_analyze_api):
        mock_analyze_api.return_value = {
            "url": "https://api.example.com/health",
            "method": "GET",
            "risks": ["Missing X-Frame-Options header"],
            "resolutions": ["Add X-Frame-Options header"],
            "status_code": 200,
        }
        mock_analyze_image.return_value = {
            "image": "nginx:latest",
            "vulnerabilities": [],
            "risks": [],
            "resolutions": [],
        }
        mock_scan_website.return_value = {
            "url": "https://example.com",
            "overall_score": 90,
            "risks": [],
            "recommendations": ["Keep software and dependencies updated"],
            "ssl_check": {"status": "PASS"},
            "headers_check": {"missing_headers": []},
        }

        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.register_user(username="e2e", email="e2e@example.com").status_code, 201)
        login_response = self.login_user(username="e2e")
        self.assertEqual(login_response.status_code, 200)

        headers = {"Authorization": f"Bearer {login_response.get_json()['access_token']}"}
        self.assertEqual(self.client.get("/dashboard").status_code, 200)
        self.assertEqual(self.client.get("/api/user/profile", headers=headers).status_code, 200)

        chat_response = self.client.post(
            "/api/chat/send",
            headers=headers,
            json={"message": "hi"},
        )
        self.assertEqual(chat_response.status_code, 200)
        self.assertIn("CyberGuard", chat_response.get_json()["bot_name"])

        api_response = self.client.post(
            "/api/security/analyze-api",
            headers=headers,
            json={"url": "https://api.example.com/health", "method": "GET"},
        )
        self.assertEqual(api_response.status_code, 200)

        image_response = self.client.post(
            "/api/security/scan-image",
            headers=headers,
            json={"image": "nginx:latest"},
        )
        self.assertEqual(image_response.status_code, 200)

        website_response = self.client.post(
            "/api/security/scan-website",
            headers=headers,
            json={"url": "https://example.com"},
        )
        self.assertEqual(website_response.status_code, 200)

        report_response = self.client.post(
            "/api/security/report",
            headers=headers,
            json={
                "api_urls": ["https://api.example.com/health"],
                "images": ["nginx:latest"],
                "websites": ["https://example.com"],
            },
        )
        self.assertEqual(report_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
