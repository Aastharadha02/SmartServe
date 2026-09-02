import unittest
from fastapi.testclient import TestClient
from app.main import app


class TestProviderDomain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_get_my_provider_profile(self):
        response = self.client.get("/api/v1/providers/me")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("user_id", data)
        self.assertIn("reliability_score", data)

    def test_update_my_provider_profile(self):
        update_payload = {
            "full_name": "Pushkar Kanjani",
            "category": "Plumbing & Smart Home",
            "skills": "Pipe fitting, Leak detection, Water heaters",
            "experience_years": 5,
            "base_price": "75.00",
            "service_area": "Delhi NCR & Noida",
        }
        response = self.client.patch("/api/v1/providers/me", json=update_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["full_name"], "Pushkar Kanjani")
        self.assertEqual(data["category"], "Plumbing & Smart Home")
        self.assertEqual(float(data["base_price"]), 75.0)

    def test_availability_workflow(self):
        slot_payload = {
            "slot_date": "2026-08-20",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
        }
        # Create slot
        post_res = self.client.post("/api/v1/providers/me/availability", json=slot_payload)
        self.assertEqual(post_res.status_code, 201)
        slot_data = post_res.json()
        slot_id = slot_data["id"]
        provider_id = slot_data["provider_id"]

        # List slots
        get_res = self.client.get(f"/api/v1/providers/{provider_id}/availability")
        self.assertEqual(get_res.status_code, 200)
        slots = get_res.json()
        self.assertTrue(any(s["id"] == slot_id for s in slots))

        # Delete slot
        del_res = self.client.delete(f"/api/v1/providers/me/availability/{slot_id}")
        self.assertEqual(del_res.status_code, 204)

    def test_certificates_workflow(self):
        cert_payload = {
            "document_url": "https://storage.smartserve.dev/certs/pushkar_master_plumber.pdf",
            "certificate_type": "Government Trade License",
        }
        # Upload certificate
        post_res = self.client.post("/api/v1/certificates", json=cert_payload)
        self.assertEqual(post_res.status_code, 201)
        cert_data = post_res.json()
        self.assertEqual(cert_data["verification_status"], "PENDING")

        # List my certificates
        get_res = self.client.get("/api/v1/certificates")
        self.assertEqual(get_res.status_code, 200)
        certs = get_res.json()
        self.assertGreaterEqual(len(certs), 1)


if __name__ == "__main__":
    unittest.main()
