#!/bin/bash
# Configuración
BASE_URL="http://localhost:8000/api"
CONTENT_TYPE="Content-Type: application/json"

echo "=== TESTING TEXTILSHOP API CON cURL ==="

# 1. Listar productos
echo "1. Listando productos..."
curl -X GET "$BASE_URL/products/" \
 -H "$CONTENT_TYPE" \
 | python -m json.tool

# 2. Crear nueva categoría
echo "2. Creando categoría..."
CATEGORY_RESPONSE=$(curl -s -X POST "$BASE_URL/categories/" \
 -H "$CONTENT_TYPE" \
 -d '{
 "name": "Camisetas",
 "description": "Camisetas de algodón premium"
 }')
echo $CATEGORY_RESPONSE | python -m json.tool

# Extraer ID de categoría
CATEGORY_ID=$(echo $CATEGORY_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

# 3. Crear producto
echo "3. Creando producto..."
PRODUCT_RESPONSE=$(curl -s -X POST "$BASE_URL/products/" \
 -H "$CONTENT_TYPE" \
 -d "{
 \"name\": \"Camiseta Básica\",
 \"description\": \"Camiseta de algodón 100%\",
 \"price\": \"29.99\",
 \"category_id\": $CATEGORY_ID,
 \"sizes\": [\"S\", \"M\", \"L\", \"XL\"],
 \"colors\": [\"Blanco\", \"Negro\", \"Azul\"],
 \"stock\": 50
 }")
echo $PRODUCT_RESPONSE | python -m json.tool

# Extraer ID de producto
PRODUCT_ID=$(echo $PRODUCT_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

# 4. Buscar productos
echo "4. Buscando productos..."
curl -X GET "$BASE_URL/products/?search=camiseta" \
 -H "$CONTENT_TYPE" \
 | python -m json.tool

# 5. Filtrar por categoría
echo "5. Filtrando por categoría..."
curl -X GET "$BASE_URL/products/?category=$CATEGORY_ID" \
 -H "$CONTENT_TYPE" \
 | python -m json.tool

# 6. Actualizar stock
echo "6. Actualizando stock..."
curl -X POST "$BASE_URL/products/$PRODUCT_ID/update_stock/" \
 -H "$CONTENT_TYPE" \
 -d '{"stock": 25}' \
 | python -m json.tool

# 7. Obtener productos destacados
echo "7. Productos destacados..."
curl -X GET "$BASE_URL/products/featured/" \
 -H "$CONTENT_TYPE" \
 | python -m json.tool

echo "=== TESTING COMPLETADO ==="
