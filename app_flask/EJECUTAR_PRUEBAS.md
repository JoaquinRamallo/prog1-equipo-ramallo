# CÓMO EJECUTAR LAS PRUEBAS UNITARIAS

## ✅ Resumen rápido

Todos los tests pasaron correctamente:
- **19 pruebas ejecutadas**
- **0 errores**
- **Tiempo: 0.028 segundos**

---

## 📋 Comandos para ejecutar pruebas

### 1. Ejecutar TODAS las pruebas (verbose)
```powershell
cd "c:\Users\Usuario\Desktop\APLICACION-FINANZAS-modificado\app_flask"
python -m unittest test_app.py -v
```

### 2. Ejecutar TODAS las pruebas (sin verbose)
```powershell
python -m unittest test_app.py
```

### 3. Ejecutar una clase de pruebas específica
```powershell
# Solo validaciones
python -m unittest test_app.TestValidaciones -v

# Solo transacciones
python -m unittest test_app.TestTransacciones -v

# Solo categorías
python -m unittest test_app.TestCategorias -v
```

### 4. Ejecutar una prueba individual
```powershell
# Solo test de email válido
python -m unittest test_app.TestValidaciones.test_email_valido -v

# Solo test de interés compuesto
python -m unittest test_app.TestRecursividad.test_interes_compuesto_basico -v
```

### 5. Ejecutar el archivo directamente
```powershell
python test_app.py
```

---

## 🧪 Desglose de las 19 pruebas

### TestValidaciones (4 pruebas)
```
✓ test_email_valido - Verifica emails correctos
✓ test_email_invalido - Verifica rechazo de emails malos
✓ test_password_valido - Verifica contraseñas fuertes
✓ test_password_invalido - Verifica rechazo de contraseñas débiles
```

### TestTransacciones (3 pruebas)
```
✓ test_procesar_transacciones_numeros - Lambda, filter, map, reduce
✓ test_resumen_transacciones_dicts - Procesar diccionarios
✓ test_resumen_transacciones_vacia - Manejar lista vacía
```

### TestLogs (1 prueba)
```
✓ test_crear_log_tuple - Tuplas con (usuario, accion, fecha)
```

### TestCategorias (2 pruebas)
```
✓ test_categorias_unicas - Extraer categorías únicas (sets)
✓ test_categorias_vacia - Manejo de descripciones vacías/None
```

### TestRecursividad (3 pruebas)
```
✓ test_interes_compuesto_basico - Cálculo de interés compuesto
✓ test_interes_sin_años - Caso cuando años = 0
✓ test_interes_negativo - Caso cuando años < 0
```

### TestMatrices (2 pruebas)
```
✓ test_matriz_historial - Convertir transacciones a matriz
✓ test_matriz_vacia - Manejo de lista vacía
```

### TestEjemploTodo (1 prueba)
```
✓ test_ejemplo_todo - Función que ejecuta todos los ejemplos
```

### TestFlaskApp (3 pruebas)
```
✓ test_login_get - GET en ruta /
✓ test_crear_cuenta_get - GET en /crear_cuenta
✓ test_olvide_contra_get - GET en /olvide_contra
```

---

## 📊 Salida esperada

```
test_categorias_unicas ... ok
test_categorias_vacia ... ok
test_ejemplo_todo ... ok
test_crear_cuenta_get ... ok
test_login_get ... ok
test_olvide_contra_get ... ok
test_crear_log_tuple ... ok
test_matriz_historial ... ok
test_matriz_vacia ... ok
test_interes_compuesto_basico ... ok
test_interes_negativo ... ok
test_interes_sin_años ... ok
test_procesar_transacciones_numeros ... ok
test_resumen_transacciones_dicts ... ok
test_resumen_transacciones_vacia ... ok
test_email_invalido ... ok
test_email_valido ... ok
test_password_invalido ... ok
test_password_valido ... ok

------------------------------------------------------
Ran 19 tests in 0.028s

OK
```

---

## 🔧 Si algo falla

### Error: ModuleNotFoundError: No module named 'flask'
```powershell
pip install flask
```

### Error: No such file or directory
```powershell
# Verifica que estés en el directorio correcto
cd "c:\Users\Usuario\Desktop\APLICACION-FINANZAS-modificado\app_flask"
# Y que los archivos existan
dir test_app.py
dir app.py
```

### Error: Templates no encontrados (en pruebas Flask)
Esto es normal. Las pruebas Flask usan `TESTING = True`, así que solo verifican que las rutas respondan sin procesar templates.

---

## 📈 Metricas de cobertura (opcional)

Para ver qué porcentaje del código está cubierto por pruebas:

```powershell
# Instalar coverage
pip install coverage

# Ejecutar con coverage
coverage run -m unittest test_app.py

# Ver reporte
coverage report
coverage html
```

---

## 💡 Conceptos probados

| Concepto | Función | Test |
|----------|---------|------|
| REGEX | `validar_email()`, `validar_password()` | TestValidaciones |
| LAMBDA | `procesar_transacciones_numeros()` | TestTransacciones |
| FILTER | `procesar_transacciones_numeros()` | TestTransacciones |
| MAP | `procesar_transacciones_numeros()` | TestTransacciones |
| REDUCE | `procesar_transacciones_numeros()` | TestTransacciones |
| TUPLAS | `crear_log_tuple()` | TestLogs |
| SETS | `categorias_unicas()` | TestCategorias |
| RECURSIVIDAD | `interes_compuesto_recursivo()` | TestRecursividad |
| MATRICES | `matriz_historial()` | TestMatrices |
| INTEGRACIÓN | `ejemplo_todo()` | TestEjemploTodo |

---

## 📝 Notas

- ✅ Todas las pruebas **pasan correctamente**
- 🚀 Las pruebas son **rápidas** (28ms totales)
- 📚 El archivo `GUIA_PRUEBAS.md` tiene información detallada
- 🔍 Para agregar nuevas pruebas, sigue el patrón en `test_app.py`
