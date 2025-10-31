"""
Módulo function_library.py - Biblioteca de Funciones Famosas
Colección de funciones periódicas clásicas con sus propiedades
"""

import numpy as np


class FunctionLibrary:
    """Biblioteca de funciones periódicas famosas"""
    
    def __init__(self):
        """Inicializa la biblioteca"""
        self.functions = self._create_library()
    
    def _create_library(self):
        """Crea la biblioteca de funciones"""
        return {
            # ONDAS BÁSICAS
            'square_wave': {
                'name': 'Onda Cuadrada',
                'function': 'sign(x)',
                'period': 2 * np.pi,
                'description': 'Onda cuadrada clásica. Alterna entre +1 y -1.',
                'properties': [
                    'Solo términos impares de seno',
                    'bₙ = 4/(nπ) para n impar',
                    'Convergencia lenta (1/n)',
                    'Muestra fenómeno de Gibbs en discontinuidades'
                ],
                'applications': 'Electrónica digital, relojes, PWM',
                'terms_recommended': 50,
                'difficulty': 'Medio'
            },
            
            'triangular_wave': {
                'name': 'Onda Triangular',
                'function': '(2/pi)*arcsin(sin(x))',
                'function_alt': 'abs(x) - pi/2',  # Aproximación
                'period': 2 * np.pi,
                'description': 'Onda triangular simétrica.',
                'properties': [
                    'Solo términos impares de coseno',
                    'Convergencia rápida (1/n²)',
                    'Función continua',
                    'Derivada es onda cuadrada'
                ],
                'applications': 'Síntesis de audio, generadores de señal',
                'terms_recommended': 20,
                'difficulty': 'Medio'
            },
            
            'sawtooth_wave': {
                'name': 'Diente de Sierra',
                'function': 'x',
                'period': 2 * np.pi,
                'description': 'Función lineal periódica (rampa).',
                'properties': [
                    'Todos los términos de seno',
                    'bₙ = (-1)^(n+1) * 2/n',
                    'Convergencia moderada (1/n)',
                    'Rica en armónicos'
                ],
                'applications': 'Síntesis de sonido, osciladores',
                'terms_recommended': 30,
                'difficulty': 'Fácil'
            },
            
            # PULSOS
            'pulse_train': {
                'name': 'Tren de Pulsos',
                'function': '1 if abs(x) < pi/4 else 0',
                'function_code': 'np.where(np.abs(x) < np.pi/4, 1, 0)',
                'period': 2 * np.pi,
                'description': 'Secuencia de pulsos rectangulares.',
                'properties': [
                    'Función sinc en frecuencia',
                    'Todos los armónicos presentes',
                    'Fenómeno de Gibbs pronunciado'
                ],
                'applications': 'Comunicaciones digitales, muestreo',
                'terms_recommended': 40,
                'difficulty': 'Medio'
            },
            
            # FUNCIONES SUAVES
            'parabola': {
                'name': 'Parábola',
                'function': 'x**2',
                'period': 2 * np.pi,
                'description': 'Función cuadrática periódica.',
                'properties': [
                    'Función par: solo cosenos',
                    'Convergencia muy rápida',
                    'Suave y continua',
                    'Derivada es lineal'
                ],
                'applications': 'Trayectorias, física',
                'terms_recommended': 10,
                'difficulty': 'Fácil'
            },
            
            'gaussian': {
                'name': 'Gaussiana Periódica',
                'function': 'exp(-x**2/4)',
                'period': 2 * np.pi,
                'description': 'Campana de Gauss periódica.',
                'properties': [
                    'Función par: solo cosenos',
                    'Muy suave',
                    'Convergencia excelente',
                    'Espectro gaussiano'
                ],
                'applications': 'Probabilidad, procesamiento de señales',
                'terms_recommended': 15,
                'difficulty': 'Medio'
            },
            
            # FUNCIONES COMBINADAS
            'am_signal': {
                'name': 'Señal AM (Modulada en Amplitud)',
                'function': '(1 + 0.5*cos(x))*cos(5*x)',
                'period': 2 * np.pi,
                'description': 'Señal modulada en amplitud.',
                'properties': [
                    'Portadora más bandas laterales',
                    'Espectro con 3 picos principales',
                    'Demodulación por envolvente'
                ],
                'applications': 'Radio AM, telecomunicaciones',
                'terms_recommended': 25,
                'difficulty': 'Avanzado'
            },
            
            'beat_signal': {
                'name': 'Batimiento',
                'function': 'cos(9*x) + cos(11*x)',
                'period': 2 * np.pi,
                'description': 'Suma de dos frecuencias cercanas.',
                'properties': [
                    'Envolvente de baja frecuencia',
                    'Solo 2 componentes espectrales',
                    'Patrón de batimiento audible'
                ],
                'applications': 'Acústica, afinación de instrumentos',
                'terms_recommended': 15,
                'difficulty': 'Medio'
            },
            
            # FUNCIONES ESPECIALES
            'rectified_sine': {
                'name': 'Seno Rectificado',
                'function': 'abs(sin(x))',
                'period': np.pi,
                'description': 'Valor absoluto de seno (rectificación).',
                'properties': [
                    'Solo términos pares de coseno',
                    'Período es π, no 2π',
                    'Aplicación en rectificadores'
                ],
                'applications': 'Fuentes de alimentación, rectificadores',
                'terms_recommended': 20,
                'difficulty': 'Medio'
            },
            
            'chirp': {
                'name': 'Chirp Lineal',
                'function': 'sin(x**2/2)',
                'period': 2 * np.pi,
                'description': 'Frecuencia variable (chirp).',
                'properties': [
                    'Frecuencia instantánea variable',
                    'Espectro distribuido',
                    'No armónico'
                ],
                'applications': 'Radar, sonar, análisis tiempo-frecuencia',
                'terms_recommended': 50,
                'difficulty': 'Avanzado'
            },
            
            # FUNCIONES CLÁSICAS
            'abs_x': {
                'name': 'Valor Absoluto',
                'function': 'abs(x)',
                'period': 2 * np.pi,
                'description': 'Función valor absoluto periódica.',
                'properties': [
                    'Función par: solo cosenos',
                    'Continua pero no derivable en 0',
                    'Convergencia buena'
                ],
                'applications': 'Rectificadores, distorsión',
                'terms_recommended': 25,
                'difficulty': 'Fácil'
            },
            
            'cubic': {
                'name': 'Cúbica',
                'function': 'x**3',
                'period': 2 * np.pi,
                'description': 'Función cúbica periódica.',
                'properties': [
                    'Función impar: solo senos',
                    'Convergencia muy rápida',
                    'Suave'
                ],
                'applications': 'Matemáticas, modelado',
                'terms_recommended': 12,
                'difficulty': 'Fácil'
            }
        }
    
    def get_function(self, key):
        """
        Obtiene una función de la biblioteca
        
        Args:
            key: Clave de la función
            
        Returns:
            Diccionario con información de la función
        """
        return self.functions.get(key, None)
    
    def get_all_names(self):
        """Retorna lista de nombres de todas las funciones"""
        return [info['name'] for info in self.functions.values()]
    
    def get_all_keys(self):
        """Retorna lista de todas las claves"""
        return list(self.functions.keys())
    
    def get_by_difficulty(self, difficulty):
        """
        Filtra funciones por dificultad
        
        Args:
            difficulty: 'Fácil', 'Medio', o 'Avanzado'
            
        Returns:
            Lista de claves de funciones
        """
        return [key for key, info in self.functions.items() 
                if info['difficulty'] == difficulty]
    
    def get_categories(self):
        """Retorna funciones organizadas por categoría"""
        return {
            'Ondas Básicas': ['square_wave', 'triangular_wave', 'sawtooth_wave'],
            'Pulsos': ['pulse_train'],
            'Funciones Suaves': ['parabola', 'gaussian'],
            'Señales Moduladas': ['am_signal', 'beat_signal'],
            'Funciones Especiales': ['rectified_sine', 'chirp'],
            'Clásicas': ['abs_x', 'cubic']
        }
    
    def get_info_text(self, key):
        """
        Genera texto informativo sobre una función
        
        Args:
            key: Clave de la función
            
        Returns:
            String con información formateada
        """
        func = self.functions.get(key)
        if not func:
            return "Función no encontrada"
        
        text = f"""
╔══════════════════════════════════════════════════════════════╗
║  {func['name'].upper().center(58)}  ║
╚══════════════════════════════════════════════════════════════╝

Función: {func['function']}
Período: {func['period']:.4f}

Descripción:
{func['description']}

Propiedades de la Serie de Fourier:
"""
        for prop in func['properties']:
            text += f"  • {prop}\n"
        
        text += f"""
Aplicaciones:
{func['applications']}

Términos Recomendados: {func['terms_recommended']}
Dificultad: {func['difficulty']}

══════════════════════════════════════════════════════════════
"""
        return text


def test_library():
    """Función de prueba"""
    lib = FunctionLibrary()
    
    print("FUNCIONES DISPONIBLES:")
    print("=" * 60)
    for key, info in lib.functions.items():
        print(f"{info['name']:30s} - {info['difficulty']:10s} - {info['function']}")
    
    print("\n" + "=" * 60)
    print(lib.get_info_text('square_wave'))


if __name__ == "__main__":
    test_library()
