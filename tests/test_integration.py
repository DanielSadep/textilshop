import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.test import override_settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from apps.products.models import Product, Category


@override_settings(DEBUG=True)
class TextilShopIntegrationTest(StaticLiveServerTestCase):
    """Pruebas de integración de TextilShop"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Configuración del navegador (headless para CI/CD)
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')

        cls.selenium = webdriver.Chrome(options=chrome_options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Crear datos de prueba
        self.category = Category.objects.create(
            name="Camisetas",
            description="Camisetas de algodón"
        )
        self.product = Product.objects.create(
            name="Camiseta Básica",
            description="Camiseta de algodón 100%",
            price=29.99,
            category=self.category,
            sizes=["S", "M", "L", "XL"],
            colors=["Blanco", "Negro"],
            stock=10
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@textilshop.com',
            password='admin123'
        )

    def test_catalogo_productos(self):
        """El catálogo carga y muestra productos"""
        self.selenium.get(f'{self.live_server_url}/products/')

        # Verificar que se muestra el nombre del producto
        product = self.selenium.find_element(By.TAG_NAME, "body").text
        self.assertIn("Camiseta Básica", product)

        # Verificar que el precio aparece en pantalla
        self.assertIn("29.99", product)

    def test_flujo_carrito(self):
        """Agregar un producto al carrito"""
        url = f'{self.live_server_url}/products/{self.product.id}/'
        self.selenium.get(url)

        # Seleccionar talla (si existe el selector)
        try:
            size_select = self.selenium.find_element(By.NAME, 'size')
            size_select.click()
            size_select.find_elements(By.TAG_NAME, "option")[1].click()
        except:
            print("⚠️ Selector de talla no encontrado")

        # Seleccionar color (si existe)
        try:
            color_select = self.selenium.find_element(By.NAME, 'color')
            color_select.click()
            color_select.find_elements(By.TAG_NAME, "option")[1].click()
        except:
            print("⚠️ Selector de color no encontrado")

        # Intentar encontrar el botón de agregar
        try:
            add_btn = self.selenium.find_element(By.CSS_SELECTOR, "form button, form input[type='submit']")
        except:
            # Si no se encuentra, mostramos el HTML para depurar
            print("❌ No se encontró el botón de agregar al carrito")
            print(self.selenium.page_source[:1000])  # imprime los primeros 1000 caracteres del HTML
            self.fail("No se encontró el botón de agregar al carrito")

        # Esperar a que sea clickeable y hacer click
        WebDriverWait(self.selenium, 10).until(EC.element_to_be_clickable(add_btn))
        add_btn.click()

        # Ir al carrito
        self.selenium.get(f'{self.live_server_url}/cart/')
        cart = self.selenium.find_element(By.TAG_NAME, "body").text
        self.assertIn("Camiseta Básica", cart)

    def test_admin_login(self):
        """El admin carga y muestra la lista de productos"""
        self.selenium.get(f'{self.live_server_url}/admin/')

        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")

        username_input.send_keys("admin")
        password_input.send_keys("admin123")

        self.selenium.find_element(By.XPATH, "//input[@type='submit']").click()

        # Esperar a que cargue el dashboard
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Products"))
        )

        products_link = self.selenium.find_element(By.LINK_TEXT, "Products")
        self.assertTrue(products_link.is_displayed())
