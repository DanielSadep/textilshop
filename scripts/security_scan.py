#!/usr/bin/env python3
import time
import json
import requests
from zapv2 import ZAPv2


class TextilShopSecurityScanner:
    def __init__(self):
        # ZAP API en 127.0.0.1
        self.zap = ZAPv2(proxies={
            'http': 'http://127.0.0.1:8080',
            'https': 'http://127.0.0.1:8080'
        })
        self.target_url = 'http://localhost:8000'

        # Validar conexión antes de arrancar
        try:
            requests.get("http://127.0.0.1:8080")
        except requests.exceptions.ConnectionError:
            print("❌ No se pudo conectar con ZAP. Asegúrate de correrlo con:")
            print('   zap.bat -daemon -port 8080 -host 127.0.0.1 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true')
            exit(1)

    def start_scan(self):
        print("=== INICIANDO AUDITORÍA DE SEGURIDAD TEXTILSHOP ===")
        self.spider_scan()
        self.passive_scan()
        self.active_scan()
        self.generate_reports()

    def spider_scan(self):
        context_name = 'TextilShop'
        print("1. Ejecutando Spider...")

        # Crear contexto de manera segura
        try:
            self.zap.context.new_context(context_name)
        except Exception:
            print(f"⚠️ El contexto '{context_name}' ya existe. Continuando...")

        self.zap.context.include_in_context(context_name, f'{self.target_url}.*')

        spider_id = self.zap.spider.scan(self.target_url)

        while int(self.zap.spider.status(spider_id)) < 100:
            print(f"Spider progress: {self.zap.spider.status(spider_id)}%")
            time.sleep(5)

        print("Spider completado!")
        print(f"URLs encontradas: {len(self.zap.core.urls())}")

    def passive_scan(self):
        print("2. Ejecutando Passive Scan...")
        while int(self.zap.pscan.records_to_scan) > 0:
            print(f"Pending: {self.zap.pscan.records_to_scan}")
            time.sleep(5)
        print("Passive Scan completado!")

    def active_scan(self):
        print("3. Ejecutando Active Scan...")
        urls = [
            f'{self.target_url}/admin/',
            f'{self.target_url}/api/products/',
            f'{self.target_url}/cart/',
            f'{self.target_url}/checkout/'
        ]

        for url in urls:
            print(f"Escaneando: {url}")
            scan_id = self.zap.ascan.scan(url)
            while int(self.zap.ascan.status(scan_id)) < 100:
                print(f"Active scan {url}: {self.zap.ascan.status(scan_id)}%")
                time.sleep(10)
        print("Active Scan completado!")

    def generate_reports(self):
        print("4. Generando reportes...")
        alerts = self.zap.core.alerts()
        report = {
            "high": [a for a in alerts if a['risk'] == 'High'],
            "medium": [a for a in alerts if a['risk'] == 'Medium'],
            "low": [a for a in alerts if a['risk'] == 'Low'],
        }
        print(f"Alto riesgo: {len(report['high'])}")
        print(f"Medio riesgo: {len(report['medium'])}")
        print(f"Bajo riesgo: {len(report['low'])}")

        with open('security_report.json', 'w') as f:
            json.dump(report, f, indent=2)

        with open('security_report.html', 'w') as f:
            f.write(self.zap.core.htmlreport())

        print("Reportes guardados: security_report.json, security_report.html")


if __name__ == "__main__":
    scanner = TextilShopSecurityScanner()
    scanner.start_scan()
