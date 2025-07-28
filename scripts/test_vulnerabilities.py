#!/usr/bin/env python3
import requests
import json

class VulnerabilityTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def test_sql_injection(self):
        """Prueba SQL Injection en endpoints"""
        print("=== TESTING SQL INJECTION ===")

        payloads = [
            "' OR '1'='1",
            "'; DROP TABLE products; --",
            "' UNION SELECT * FROM auth_user --",
            "1' AND (SELECT COUNT(*) FROM auth_user) > 0 --"
        ]

        endpoints = [
            "/api/products/",
            "/products/search/",
            "/"
        ]

        vulnerabilities = []

        for endpoint in endpoints:
            for payload in payloads:
                try:
                    response = self.session.get(
                        f"{self.base_url}{endpoint}",
                        params={"q": payload}
                    )

                    if self.detect_sql_error(response):
                        vulnerabilities.append({
                            'type': 'SQL Injection',
                            'endpoint': endpoint,
                            'payload': payload,
                            'method': 'GET'
                        })

                except Exception as e:
                    print(f"Error testing {endpoint}: {e}")

        return vulnerabilities

    def test_xss(self):
        """Prueba Cross-Site Scripting"""
        print("=== TESTING XSS ===")

        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//"
        ]

        vulnerabilities = []
        for payload in xss_payloads:
            response = self.session.get(
                f"{self.base_url}/products/search/",
                params={"q": payload}
            )

            if payload in response.text:
                vulnerabilities.append({
                    'type': 'XSS',
                    'endpoint': '/products/search/',
                    'payload': payload
                })

        return vulnerabilities

    def test_csrf(self):
        """Prueba CSRF en formularios críticos"""
        print("=== TESTING CSRF ===")

        csrf_tests = []

        product_data = {
            'name': 'Test Product',
            'price': '29.99',
            'description': 'Test description'
        }

        response = self.session.post(
            f"{self.base_url}/admin/products/product/add/",
            data=product_data
        )

        if response.status_code != 403:
            csrf_tests.append({
                'type': 'CSRF',
                'endpoint': '/admin/products/product/add/',
                'status': 'VULNERABLE'
            })

        return csrf_tests

    def detect_sql_error(self, response):
        """Detecta errores SQL en la respuesta"""
        sql_errors = [
            "syntax error",
            "mysql_fetch",
            "ORA-",
            "PostgreSQL",
            "sqlite3.OperationalError"
        ]

        response_text = response.text.lower()
        return any(error in response_text for error in sql_errors)


if __name__ == "__main__":
    tester = VulnerabilityTester()

    all_vulnerabilities = []
    all_vulnerabilities.extend(tester.test_sql_injection())
    all_vulnerabilities.extend(tester.test_xss())
    all_vulnerabilities.extend(tester.test_csrf())

    print(f"\n=== REPORTE FINAL ===")
    print(f"Vulnerabilidades encontradas: {len(all_vulnerabilities)}")

    for vuln in all_vulnerabilities:
        print(f"- {vuln['type']} en {vuln['endpoint']}")

    # Guardar reporte en JSON
    with open('vulnerability_report.json', 'w') as f:
        json.dump(all_vulnerabilities, f, indent=2)
    print("\nReporte guardado en vulnerability_report.json")
