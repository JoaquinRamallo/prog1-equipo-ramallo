# test_app.py
# Pruebas unitarias para app.py usando unittest

import unittest
import json
import os
import tempfile
from datetime import datetime

# Importar las funciones del app
from app import (
    validar_email,
    validar_password,
    procesar_transacciones_numeros,
    resumen_transacciones_dicts,
    crear_log_tuple,
    categorias_unicas,
    interes_compuesto_recursivo,
    matriz_historial,
    ejemplo_todo,
    app
)


class TestValidaciones(unittest.TestCase):
    """Pruebas para validar email y contraseña con regex"""
    
    def test_email_valido(self):
        """Email válido debe retornar True"""
        self.assertTrue(validar_email('user@example.com'))
        self.assertTrue(validar_email('juan.perez@gmail.com'))
        self.assertTrue(validar_email('test_user@domain.co.uk'))
    
    def test_email_invalido(self):
        """Email inválido debe retornar False"""
        self.assertFalse(validar_email('bad-email'))
        self.assertFalse(validar_email('user@'))
        self.assertFalse(validar_email('@example.com'))
        self.assertFalse(validar_email('user@.com'))
    
    def test_password_valido(self):
        """Contraseña válida (mayúscula + número + 6+ caracteres)"""
        self.assertTrue(validar_password('Password1'))
        self.assertTrue(validar_password('Secure123'))
        self.assertTrue(validar_password('MyPass9'))
    
    def test_password_invalido(self):
        """Contraseña inválida (sin mayúscula o sin número)"""
        self.assertFalse(validar_password('password123'))  # Sin mayúscula
        self.assertFalse(validar_password('PASSWORD'))  # Sin número
        self.assertFalse(validar_password('Pass1'))  # Menos de 6 caracteres
        self.assertFalse(validar_password('pass'))  # Muy corta


class TestTransacciones(unittest.TestCase):
    """Pruebas para procesar transacciones"""
    
    def test_procesar_transacciones_numeros(self):
        """Prueba filtro (positivos), map (impuesto) y reduce (suma)"""
        lista = [100, -50, 200, -30]
        positivos, con_impuesto, total = procesar_transacciones_numeros(lista)
        
        # Positivos: [100, 200]
        self.assertEqual(positivos, [100, 200])
        
        # Con impuesto 10%: [110, 220]
        self.assertEqual(con_impuesto, [110.0, 220.0])
        
        # Total: 330
        self.assertEqual(total, 330.0)
    
    def test_resumen_transacciones_dicts(self):
        """Prueba procesar diccionarios de transacciones"""
        transacciones = [
            {'monto': 100, 'descripcion': 'Sueldo'},
            {'monto': -50, 'descripcion': 'Gasto'},
            {'monto': 200, 'descripcion': 'Bonus'}
        ]
        positivos, con_impuesto, total = resumen_transacciones_dicts(transacciones)
        
        self.assertEqual(positivos, [100, 200])
        self.assertEqual(con_impuesto, [110.0, 220.0])
        self.assertEqual(total, 330.0)
    
    def test_resumen_transacciones_vacia(self):
        """Prueba con lista de transacciones vacía"""
        transacciones = []
        positivos, con_impuesto, total = resumen_transacciones_dicts(transacciones)
        
        self.assertEqual(positivos, [])
        self.assertEqual(con_impuesto, [])
        self.assertEqual(total, 0)


class TestLogs(unittest.TestCase):
    """Pruebas para crear logs con tuplas"""
    
    def test_crear_log_tuple(self):
        """Prueba creación de tupla de log"""
        log = crear_log_tuple('usuario1', 'login')
        
        # Verificar que es una tupla
        self.assertIsInstance(log, tuple)
        
        # Verificar estructura: (usuario, accion, fecha)
        self.assertEqual(log[0], 'usuario1')
        self.assertEqual(log[1], 'login')
        
        # Verificar que tiene fecha en formato ISO
        try:
            datetime.fromisoformat(log[2])
            es_fecha_valida = True
        except ValueError:
            es_fecha_valida = False
        
        self.assertTrue(es_fecha_valida)


class TestCategorias(unittest.TestCase):
    """Pruebas para extraer categorías únicas con sets"""
    
    def test_categorias_unicas(self):
        """Prueba extracción de categorías de transacciones"""
        transacciones = [
            {'descripcion': 'Comida almuerzo', 'monto': -50},
            {'descripcion': 'Comida cena', 'monto': -30},
            {'descripcion': 'Sueldo mensual', 'monto': 1000},
            {'descripcion': 'Transporte colectivo', 'monto': -20}
        ]
        
        categorias = categorias_unicas(transacciones)
        
        # Debe ser un set
        self.assertIsInstance(categorias, set)
        
        # Debe contener las categorías correctas
        self.assertIn('comida', categorias)
        self.assertIn('sueldo', categorias)
        self.assertIn('transporte', categorias)
        
        # No debe haber duplicados (set)
        self.assertEqual(len(categorias), 3)
    
    def test_categorias_vacia(self):
        """Prueba con transacciones sin descripción o descripción None"""
        transacciones = [
            {'descripcion': '', 'monto': -50},
            {'descripcion': None, 'monto': 100},
            {'monto': 200}  # Sin clave 'descripcion'
        ]
        
        categorias = categorias_unicas(transacciones)
        
        # Debe retornar set vacío
        self.assertEqual(categorias, set())


class TestRecursividad(unittest.TestCase):
    """Pruebas para interés compuesto recursivo"""
    
    def test_interes_compuesto_basico(self):
        """Prueba cálculo de interés compuesto"""
        # Capital: 100, Tasa: 10%, Años: 2
        # Año 0: 100
        # Año 1: 100 * 1.1 = 110
        # Año 2: 110 * 1.1 = 121
        resultado = interes_compuesto_recursivo(100, 0.1, 2)
        
        self.assertEqual(round(resultado, 2), 121.0)
    
    def test_interes_sin_años(self):
        """Prueba cuando años es 0"""
        resultado = interes_compuesto_recursivo(100, 0.1, 0)
        
        self.assertEqual(resultado, 100)
    
    def test_interes_negativo(self):
        """Prueba cuando años es negativo"""
        resultado = interes_compuesto_recursivo(100, 0.1, -1)
        
        self.assertEqual(resultado, 100)


class TestMatrices(unittest.TestCase):
    """Pruebas para convertir transacciones en matriz"""
    
    def test_matriz_historial(self):
        """Prueba conversión de transacciones a matriz"""
        transacciones = [
            {'descripcion': 'Gasto 1', 'monto': -50},
            {'descripcion': 'Ingreso 1', 'monto': 100},
            {'descripcion': 'Gasto 2', 'monto': -30}
        ]
        
        matriz = matriz_historial(transacciones)
        
        # Debe ser una lista
        self.assertIsInstance(matriz, list)
        
        # Debe tener 3 filas
        self.assertEqual(len(matriz), 3)
        
        # Cada fila debe tener [descripcion, monto]
        self.assertEqual(matriz[0], ['Gasto 1', -50])
        self.assertEqual(matriz[1], ['Ingreso 1', 100])
        self.assertEqual(matriz[2], ['Gasto 2', -30])
    
    def test_matriz_vacia(self):
        """Prueba con transacciones vacías"""
        matriz = matriz_historial([])
        
        self.assertEqual(matriz, [])


class TestEjemploTodo(unittest.TestCase):
    """Pruebas para la función de demostración"""
    
    def test_ejemplo_todo(self):
        """Prueba función que ejecuta todos los ejemplos"""
        transacciones = [
            {'descripcion': 'Comida almuerzo', 'monto': -50},
            {'descripcion': 'Sueldo', 'monto': 500},
            {'descripcion': 'Comida cena', 'monto': -30}
        ]
        
        resultado = ejemplo_todo(transacciones)
        
        # Verificar que retorna un diccionario
        self.assertIsInstance(resultado, dict)
        
        # Verificar que tiene todas las claves esperadas
        claves_esperadas = ['positivos', 'con_impuesto', 'total', 
                            'categorias', 'matriz', 'log_guardado_en']
        
        for clave in claves_esperadas:
            self.assertIn(clave, resultado)


class TestFlaskApp(unittest.TestCase):
    """Pruebas para rutas Flask"""
    
    def setUp(self):
        """Configurar cliente de prueba"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_login_get(self):
        """Prueba GET en ruta de login"""
        response = self.client.get('/')
        
        # Debe retornar 200 OK
        self.assertEqual(response.status_code, 200)
    
    def test_crear_cuenta_get(self):
        """Prueba GET en ruta crear_cuenta"""
        response = self.client.get('/crear_cuenta')
        
        # Debe retornar 200 OK
        self.assertEqual(response.status_code, 200)
    
    def test_olvide_contra_get(self):
        """Prueba GET en ruta olvide_contra"""
        response = self.client.get('/olvide_contra')
        
        # Debe retornar 200 OK
        self.assertEqual(response.status_code, 200)


# ============================================================
# Comando para ejecutar las pruebas
# ============================================================
# python -m unittest test_app.py -v
# o
# python -m unittest test_app.TestValidaciones -v
# ============================================================

if __name__ == '__main__':
    unittest.main()
