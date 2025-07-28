from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time


class FormIntegrationTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        cls.selenium = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_crear_producto_desde_formulario(self):
        """Verifica que se puede crear un producto desde el formulario"""
        self.selenium.get(f'{self.live_server_url}/products/create/')

        # Llenar el nombre
        name_input = self.selenium.find_element(By.NAME, "name")
        name_input.send_keys("Producto Test")

        # Llenar el precio
        price_input = self.selenium.find_element(By.NAME, "price")
        price_input.clear()
        price_input.send_keys("19.99")

        # Stock
        stock_input = self.selenium.find_element(By.NAME, "stock")
        stock_input.clear()
        stock_input.send_keys("5")

        # Verificar si existe el campo category (en algunos formularios puede estar oculto)
        try:
            category_select = Select(self.selenium.find_element(By.NAME, "category"))
            category_select.select_by_index(0)  # Selecciona la primera categoría disponible
        except:
            print("⚠️ Campo 'category' no encontrado, continuando sin seleccionar categoría...")

        # Guardar
        submit_btn = self.selenium.find_element(By.XPATH, "//button[contains(text(),'Guardar')]")
        submit_btn.click()

        time.sleep(2)

        # Verificar que se redirigió a la lista y aparece el producto
        body_text = self.selenium.find_element(By.TAG_NAME, "body").text
        self.assertIn("Producto Test", body_text)
