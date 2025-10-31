"""
Módulo solver.py - Cálculo de Series de Fourier
Calcula los coeficientes a₀, aₙ y bₙ de la serie de Fourier
Optimizado para mejor rendimiento
"""

import numpy as np
import sympy as sp
from sympy import symbols, sin, cos, pi, integrate, lambdify
from typing import Dict, List, Tuple, Callable
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import warnings

# Suprimir warnings de SymPy para mejor rendimiento
warnings.filterwarnings('ignore', category=RuntimeWarning)


class FourierSolver:
    """Clase para calcular series de Fourier de funciones periódicas"""
    
    def __init__(self, function_str: str, period: float = 2*np.pi, n_terms: int = 10):
        """
        Inicializa el solucionador de Fourier
        
        Args:
            function_str: Función como string (ej: "sin(x)", "x**2")
            period: Período de la función
            n_terms: Número de términos a calcular
        """
        self.function_str = function_str
        self.period = period
        self.n_terms = n_terms
        self.L = period / 2  # Semi-período
        
        # Cache para evaluaciones de función
        self._eval_cache = {}
        
        # Símbolos de sympy
        self.x = symbols('x', real=True)
        self.n = symbols('n', integer=True, positive=True)
        
        # Preprocesar funciones condicionales comunes
        processed_str, use_numeric = self._preprocess_function(function_str)
        
        # Parsear la función
        try:
            if use_numeric:
                # Para funciones condicionales complejas, usar solo evaluación numérica
                self.f_lambda = self._create_numeric_function(function_str)
                # Para integración simbólica, intentar parsear la versión procesada
                try:
                    self.f_symbolic = sp.sympify(processed_str)
                except:
                    self.f_symbolic = None  # No disponible para integración simbólica
            else:
                # Función normal - parsear con SymPy
                self.f_symbolic = sp.sympify(processed_str)
                self.f_lambda = lambdify(self.x, self.f_symbolic, modules=['numpy'])
        except Exception as e:
            raise ValueError(f"Error al parsear la función: {e}")
        
        # Coeficientes
        self.a0 = None
        self.an_list = []
        self.bn_list = []
        self.an_symbolic = None
        self.bn_symbolic = None
    
    def _preprocess_function(self, func_str: str) -> Tuple[str, bool]:
        """
        Preprocesa funciones con condicionales para convertirlas a forma evaluable
        
        Returns:
            Tupla (función_procesada, usar_numérico)
        """
        # Diccionario de conversiones a SymPy
        conversions = {
            "1 if x > 0 else -1": ("sign(x)", False),
            "1 if x>0 else -1": ("sign(x)", False),
        }
        
        # Buscar conversiones exactas
        if func_str in conversions:
            return conversions[func_str]
        
        # Detectar patrones de condicionales que requieren evaluación numérica
        if " if " in func_str and " else " in func_str:
            # Funciones con condicionales complejos
            return (func_str, True)  # Usar evaluación numérica
        else:
            # Función normal
            return (func_str, False)
    
    def _create_numeric_function(self, expr_str: str) -> Callable:
        """
        Crea una función numérica segura para expresiones condicionales
        
        Args:
            expr_str: Expresión con condicionales de Python (ej: "1 if x > 0 else 0")
            
        Returns:
            Función que evalúa la expresión
        """
        # Namespace seguro con funciones matemáticas
        safe_namespace = {
            'pi': np.pi,
            'e': np.e,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'exp': np.exp,
            'log': np.log,
            'log10': np.log10,
            'sqrt': np.sqrt,
            'abs': np.abs,
            'sign': np.sign,
            'floor': np.floor,
            'ceil': np.ceil,
        }
        
        def safe_eval_function(x_val):
            """Evalúa la expresión de forma segura"""
            if isinstance(x_val, np.ndarray):
                # Para arrays, evaluar elemento por elemento
                result = np.zeros_like(x_val, dtype=float)
                for i, xi in enumerate(x_val):
                    try:
                        # Evaluar con x = xi
                        local_ns = {'x': xi}
                        local_ns.update(safe_namespace)
                        result[i] = eval(expr_str, {"__builtins__": {}}, local_ns)
                    except Exception as e:
                        print(f"⚠️ Error evaluando en x={xi}: {e}")
                        result[i] = 0
                return result
            else:
                # Valor escalar
                try:
                    local_ns = {'x': x_val}
                    local_ns.update(safe_namespace)
                    return float(eval(expr_str, {"__builtins__": {}}, local_ns))
                except Exception as e:
                    print(f"⚠️ Error evaluando en x={x_val}: {e}")
                    return 0.0
        
        return safe_eval_function
        
    def calculate_a0(self) -> float:
        """Calcula el coeficiente a₀"""
        # Usar método numérico si no hay forma simbólica disponible
        if self.f_symbolic is None:
            x_vals = np.linspace(-self.L, self.L, 2000)
            y_vals = self.f_lambda(x_vals)
            self.a0 = np.trapz(y_vals, x_vals) / self.L
            return self.a0
            
        try:
            # a₀ = (1/L) ∫f(x)dx de -L a L
            integral = integrate(self.f_symbolic, (self.x, -self.L, self.L))
            self.a0 = float(integral / self.L)
            return self.a0
        except Exception as e:
            print(f"Error calculando a₀ simbólicamente, usando método numérico: {e}")
            # Método numérico de respaldo
            x_vals = np.linspace(-self.L, self.L, 2000)
            y_vals = self.f_lambda(x_vals)
            self.a0 = np.trapz(y_vals, x_vals) / self.L
            return self.a0
    
    def calculate_an(self, n_value: int) -> float:
        """Calcula el coeficiente aₙ para un n específico"""
        # Usar método numérico si no hay forma simbólica disponible
        if self.f_symbolic is None:
            x_vals = np.linspace(-self.L, self.L, 2000)
            y_vals = self.f_lambda(x_vals) * np.cos(n_value * np.pi * x_vals / self.L)
            return np.trapz(y_vals, x_vals) / self.L
            
        try:
            # aₙ = (1/L) ∫f(x)cos(nπx/L)dx de -L a L
            integrand = self.f_symbolic * cos(n_value * pi * self.x / self.L)
            integral = integrate(integrand, (self.x, -self.L, self.L))
            return float(integral / self.L)
        except Exception as e:
            print(f"Error calculando a_{n_value} simbólicamente, usando método numérico")
            # Método numérico de respaldo
            x_vals = np.linspace(-self.L, self.L, 2000)
            y_vals = self.f_lambda(x_vals) * np.cos(n_value * np.pi * x_vals / self.L)
            return np.trapz(y_vals, x_vals) / self.L
    
    def calculate_bn(self, n_value: int) -> float:
        """Calcula el coeficiente bₙ para un n específico"""
        # Usar método numérico si no hay forma simbólica disponible
        if self.f_symbolic is None:
            x_vals = np.linspace(-self.L, self.L, 2000)
            y_vals = self.f_lambda(x_vals) * np.sin(n_value * np.pi * x_vals / self.L)
            return np.trapz(y_vals, x_vals) / self.L
            
        try:
            # bₙ = (1/L) ∫f(x)sin(nπx/L)dx de -L a L
            integrand = self.f_symbolic * sin(n_value * pi * self.x / self.L)
            integral = integrate(integrand, (self.x, -self.L, self.L))
            return float(integral / self.L)
        except Exception as e:
            print(f"Error calculando b_{n_value} simbólicamente, usando método numérico")
            # Método numérico de respaldo
            x_vals = np.linspace(-self.L, self.L, 2000)
            y_vals = self.f_lambda(x_vals) * np.sin(n_value * np.pi * x_vals / self.L)
            return np.trapz(y_vals, x_vals) / self.L
    
    def calculate_symbolic_coefficients(self):
        """Calcula las fórmulas simbólicas de aₙ y bₙ"""
        try:
            # Fórmula simbólica para aₙ
            integrand_a = self.f_symbolic * cos(self.n * pi * self.x / self.L)
            self.an_symbolic = integrate(integrand_a, (self.x, -self.L, self.L)) / self.L
            
            # Fórmula simbólica para bₙ
            integrand_b = self.f_symbolic * sin(self.n * pi * self.x / self.L)
            self.bn_symbolic = integrate(integrand_b, (self.x, -self.L, self.L)) / self.L
        except Exception as e:
            print(f"No se pudieron calcular fórmulas simbólicas: {e}")
            self.an_symbolic = None
            self.bn_symbolic = None
    
    def detect_symmetry(self) -> str:
        """
        Detecta la simetría de la función para optimizar cálculos
        
        Returns:
            'even' (par), 'odd' (impar), 'half-wave' (simetría de media onda), 'none'
        """
        try:
            # Muestrear puntos simétricos (evitar x=0 para no dividir por cero)
            test_points = np.linspace(0.1, self.L * 0.95, 25)
            
            # Evaluar función en puntos simétricos
            y_positive = self.f_lambda(test_points)
            y_negative = self.f_lambda(-test_points)
            
            # Test función PAR: f(-x) == f(x)
            is_even = np.allclose(y_negative, y_positive, rtol=1e-4, atol=1e-6)
            
            # Test función IMPAR: f(-x) == -f(x)
            is_odd = np.allclose(y_negative, -y_positive, rtol=1e-4, atol=1e-6)
            
            # Test simetría de MEDIA ONDA: f(x + T/2) == -f(x)
            # Solo para puntos en primera mitad del período
            test_half = np.linspace(-self.L * 0.5, 0, 15)
            y_half1 = self.f_lambda(test_half)
            y_half2 = self.f_lambda(test_half + self.L)
            is_half_wave = np.allclose(y_half2, -y_half1, rtol=1e-4, atol=1e-6)
            
            if is_even:
                return 'even'
            elif is_odd:
                return 'odd'
            elif is_half_wave:
                return 'half-wave'
            else:
                return 'none'
        except Exception as e:
            print(f"Error detectando simetría: {e}")
            return 'none'
    
    def use_known_series(self) -> bool:
        """
        Intenta usar series de Fourier conocidas analíticamente
        
        Returns:
            True si se usó una serie conocida, False si hay que calcular
        """
        # Base de datos de series conocidas
        known_series = {
            'sin(x)': {
                'name': 'Función seno',
                'a0': 0,
                'an': lambda n: 0,
                'bn': lambda n: 1 if n == 1 else 0,
                'period_factor': 1  # Debe coincidir con período actual
            },
            'cos(x)': {
                'name': 'Función coseno',
                'a0': 0,
                'an': lambda n: 1 if n == 1 else 0,
                'bn': lambda n: 0,
                'period_factor': 1
            },
            'abs(x)': {
                'name': 'Valor absoluto',
                'a0': self.L / 2,  # pi/2 para período 2π
                'an': lambda n: -4*self.L/(np.pi*n**2) if n % 2 == 1 else 0,
                'bn': lambda n: 0,
                'period_factor': 1
            },
            'x**2': {
                'name': 'Parábola',
                'a0': 2 * self.L**2 / 3,  # pi²/3 para L=π
                'an': lambda n: 4 * self.L**2 * (-1)**n / (np.pi**2 * n**2),
                'bn': lambda n: 0,
                'period_factor': 1
            }
        }
        
        # Normalizar función string
        func_normalized = self.function_str.strip().replace(' ', '')
        
        if func_normalized in known_series:
            series = known_series[func_normalized]
            
            print(f"✅ Usando serie conocida: {series['name']}")
            
            # Calcular a0
            self.a0 = series['a0'] if isinstance(series['a0'], (int, float)) else series['a0']
            
            # Calcular coeficientes
            self.an_list = [series['an'](n) for n in range(1, self.n_terms + 1)]
            self.bn_list = [series['bn'](n) for n in range(1, self.n_terms + 1)]
            
            print(f"   ⚡ Cálculo instantáneo - {self.n_terms} términos")
            return True
        
        return False
    
    def calculate_all_coefficients(self) -> Dict:
        """Calcula todos los coeficientes hasta n_terms - OPTIMIZADO con simetría"""
        print(f"Calculando {self.n_terms} términos...")
        
        # 1. Intentar usar serie conocida (instantáneo)
        if self.use_known_series():
            print(f"✓ Serie conocida detectada - cálculo instantáneo")
            # Calcular fórmulas simbólicas si aplica
            if self.n_terms <= 50:
                self.calculate_symbolic_coefficients()
            else:
                self.an_symbolic = None
                self.bn_symbolic = None
            
            return {
                'a0': self.a0,
                'an': self.an_list,
                'bn': self.bn_list,
                'an_symbolic': self.an_symbolic,
                'bn_symbolic': self.bn_symbolic
            }
        
        # 2. Detectar simetría para optimizar
        symmetry = self.detect_symmetry()
        print(f"Simetría detectada: {symmetry}")
        
        self.calculate_a0()
        self.an_list = []
        self.bn_list = []
        
        # 3. Calcular coeficientes según simetría
        if symmetry == 'even':
            # Función par: solo términos de coseno (bn = 0)
            print("Optimización: función par, solo cosenos")
            if self.n_terms > 20:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    an_futures = [executor.submit(self.calculate_an, n) for n in range(1, self.n_terms + 1)]
                    self.an_list = [future.result() for future in an_futures]
            else:
                for n in range(1, self.n_terms + 1):
                    self.an_list.append(self.calculate_an(n))
            self.bn_list = [0.0] * self.n_terms
            
        elif symmetry == 'odd':
            # Función impar: solo términos de seno (an = 0, a0 = 0)
            print("Optimización: función impar, solo senos")
            self.a0 = 0.0
            self.an_list = [0.0] * self.n_terms
            if self.n_terms > 20:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    bn_futures = [executor.submit(self.calculate_bn, n) for n in range(1, self.n_terms + 1)]
                    self.bn_list = [future.result() for future in bn_futures]
            else:
                for n in range(1, self.n_terms + 1):
                    self.bn_list.append(self.calculate_bn(n))
                    
        elif symmetry == 'half_wave':
            # Simetría de media onda: solo armónicos impares
            print("Optimización: simetría de media onda, solo armónicos impares")
            if self.n_terms > 20:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    an_futures = {n: executor.submit(self.calculate_an, n) for n in range(1, self.n_terms + 1)}
                    bn_futures = {n: executor.submit(self.calculate_bn, n) for n in range(1, self.n_terms + 1)}
                    
                    for n in range(1, self.n_terms + 1):
                        if n % 2 == 0:  # Par
                            self.an_list.append(0.0)
                            self.bn_list.append(0.0)
                        else:  # Impar
                            self.an_list.append(an_futures[n].result())
                            self.bn_list.append(bn_futures[n].result())
            else:
                for n in range(1, self.n_terms + 1):
                    if n % 2 == 0:  # Par
                        self.an_list.append(0.0)
                        self.bn_list.append(0.0)
                    else:  # Impar
                        self.an_list.append(self.calculate_an(n))
                        self.bn_list.append(self.calculate_bn(n))
        else:
            # Sin simetría especial: calcular todo
            if self.n_terms > 20:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    an_futures = [executor.submit(self.calculate_an, n) for n in range(1, self.n_terms + 1)]
                    bn_futures = [executor.submit(self.calculate_bn, n) for n in range(1, self.n_terms + 1)]
                    
                    self.an_list = [future.result() for future in an_futures]
                    self.bn_list = [future.result() for future in bn_futures]
            else:
                for n in range(1, self.n_terms + 1):
                    an = self.calculate_an(n)
                    bn = self.calculate_bn(n)
                    self.an_list.append(an)
                    self.bn_list.append(bn)
        
        print(f"✓ Coeficientes calculados")
        
        # Calcular fórmulas simbólicas (solo si no hay muchos términos)
        if self.n_terms <= 50:
            self.calculate_symbolic_coefficients()
        else:
            self.an_symbolic = None
            self.bn_symbolic = None
        
        return {
            'a0': self.a0,
            'an': self.an_list,
            'bn': self.bn_list,
            'an_symbolic': self.an_symbolic,
            'bn_symbolic': self.bn_symbolic
        }
    
    def evaluate_series(self, x_values: np.ndarray, n_terms: int = None) -> np.ndarray:
        """
        Evalúa la serie de Fourier en puntos específicos - OPTIMIZADO
        Usa vectorización completa de NumPy para máximo rendimiento
        
        Args:
            x_values: Array de valores de x
            n_terms: Número de términos (si None, usa self.n_terms)
        
        Returns:
            Array con los valores de la serie
        """
        if n_terms is None:
            n_terms = self.n_terms
        
        # Limitar a coeficientes disponibles
        n_terms = min(n_terms, len(self.an_list))
        
        # Iniciar con a₀/2
        result = np.full_like(x_values, self.a0 / 2, dtype=np.float64)
        
        # Convertir listas a arrays de NumPy para operaciones vectorizadas
        an_array = np.array(self.an_list[:n_terms])
        bn_array = np.array(self.bn_list[:n_terms])
        
        # Crear array de índices n (1, 2, 3, ..., n_terms)
        n_indices = np.arange(1, n_terms + 1)
        
        # Calcular todos los argumentos (broadcasting)
        # Shape: (n_terms, len(x_values))
        args = np.outer(n_indices * np.pi / self.L, x_values)
        
        # Calcular todas las contribuciones de una vez
        cos_terms = np.cos(args)  # Shape: (n_terms, len(x_values))
        sin_terms = np.sin(args)  # Shape: (n_terms, len(x_values))
        
        # Multiplicar por coeficientes y sumar
        # Broadcasting: (n_terms, 1) * (n_terms, len(x_values))
        result += np.sum(an_array[:, np.newaxis] * cos_terms, axis=0)
        result += np.sum(bn_array[:, np.newaxis] * sin_terms, axis=0)
        
        return result
    
    def get_series_expression(self, n_terms: int = None) -> str:
        """Retorna la expresión de la serie como string"""
        if n_terms is None:
            n_terms = self.n_terms
        
        expr = f"{self.a0/2:.4f}"
        
        for n in range(1, min(n_terms + 1, len(self.an_list) + 1)):
            an = self.an_list[n-1]
            bn = self.bn_list[n-1]
            
            if abs(an) > 1e-10:
                expr += f" + {an:.4f}*cos({n}πx/{self.L:.2f})"
            if abs(bn) > 1e-10:
                expr += f" + {bn:.4f}*sin({n}πx/{self.L:.2f})"
        
        return expr
    
    def calculate_error(self, x_values: np.ndarray) -> np.ndarray:
        """Calcula el error entre f(x) y la serie"""
        original = self.f_lambda(x_values)
        approximation = self.evaluate_series(x_values)
        return original - approximation
    
    def get_coefficients_table(self) -> List[Dict]:
        """Retorna una tabla con todos los coeficientes"""
        table = [{'n': 0, 'an': self.a0, 'bn': 0.0}]
        
        for n in range(1, len(self.an_list) + 1):
            table.append({
                'n': n,
                'an': self.an_list[n-1],
                'bn': self.bn_list[n-1]
            })
        
        return table


def test_solver():
    """Función de prueba"""
    # Probar con sin(x)
    solver = FourierSolver("sin(x)", period=2*np.pi, n_terms=5)
    coeffs = solver.calculate_all_coefficients()
    
    print("Función: sin(x)")
    print(f"a₀ = {coeffs['a0']:.6f}")
    print(f"Coeficientes aₙ: {[f'{a:.6f}' for a in coeffs['an']]}")
    print(f"Coeficientes bₙ: {[f'{b:.6f}' for b in coeffs['bn']]}")
    print(f"\nFórmula simbólica aₙ: {coeffs['an_symbolic']}")
    print(f"Fórmula simbólica bₙ: {coeffs['bn_symbolic']}")
    
    # Evaluar en algunos puntos
    x_test = np.linspace(-np.pi, np.pi, 100)
    y_series = solver.evaluate_series(x_test)
    
    print(f"\nExpresión de la serie:\n{solver.get_series_expression()}")


if __name__ == "__main__":
    test_solver()
