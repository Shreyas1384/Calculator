"""
Integration and API tests for Shrey's Calc Flask server.
"""

import unittest
import json
from app import app


class TestShreysCalcAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "shreys-calc")

    def test_scientific_expression_api(self):
        response = self.client.post(
            "/api/calculate",
            data=json.dumps({
                "expression": "sin(30) + 0.5",
                "angle_mode": "DEG"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["result"], 1)

    def test_single_scientific_operation_api(self):
        # Factorial of 5
        res = self.client.post(
            "/api/calculate",
            data=json.dumps({"operation": "factorial", "a": 5}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["result"], 120)

        # Tan of 45 in degrees
        res_tan = self.client.post(
            "/api/calculate",
            data=json.dumps({"operation": "tan", "a": 45, "angle_mode": "DEG"}),
            content_type="application/json"
        )
        self.assertEqual(res_tan.status_code, 200)
        self.assertEqual(json.loads(res_tan.data)["result"], 1)

        # Log10 of 1000
        res_log = self.client.post(
            "/api/calculate",
            data=json.dumps({"operation": "log10", "a": 1000}),
            content_type="application/json"
        )
        self.assertEqual(res_log.status_code, 200)
        self.assertEqual(json.loads(res_log.data)["result"], 3)

    def test_history_api(self):
        self.client.post(
            "/api/calculate",
            data=json.dumps({"expression": "9 * 9"}),
            content_type="application/json"
        )
        res = self.client.get("/api/history")
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["history"][0]["result"], 81)


if __name__ == "__main__":
    unittest.main()
