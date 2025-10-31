"""
Módulo recommender.py - Recomendador inteligente de parámetros
Analiza la función y sugiere parámetros óptimos para la aproximación
"""

import numpy as np
from typing import Callable, Dict, Tuple


class SmartRecommender:
    """Recomendador inteligente de parámetros para series de Fourier"""
    
    def __init__(self, func: Callable, period: float):
        """
        Inicializa el recomendador
        
        Args:
            func: Función a analizar
            period: Período de la función
        """
        self.func = func
        self.period = period
        self.L = period / 2
        
    def analyze_function(self, num_samples: int = 2000) -> Dict:
        """
        Analiza la complejidad de la función
        
        Args:
            num_samples: Número de puntos para análisis
            
        Returns:
            Diccionario con métricas de complejidad
        """
        x = np.linspace(-self.L, self.L, num_samples)
        
        try:
            y = np.array([self.func(xi) for xi in x])
        except:
            # Si hay errores, usar evaluación vectorizada
            try:
                y = self.func(x)
            except:
                # Función muy problemática
                return {
                    'complexity': 'extreme',
                    'discontinuities': -1,
                    'high_frequency_content': 1.0,
                    'smoothness': 0.0
                }
        
        # 1. Detectar discontinuidades
        discontinuities = self._detect_discontinuities(x, y)
        
        # 2. Analizar contenido de altas frecuencias
        high_freq_content = self._analyze_frequency_content(y)
        
        # 3. Medir suavidad (derivadas)
        smoothness = self._measure_smoothness(x, y)
        
        # 4. Clasificar complejidad
        complexity = self._classify_complexity(
            len(discontinuities), 
            high_freq_content, 
            smoothness
        )
        
        return {
            'complexity': complexity,
            'discontinuities': len(discontinuities),
            'high_frequency_content': high_freq_content,
            'smoothness': smoothness,
            'discontinuity_positions': discontinuities
        }
    
    def _detect_discontinuities(self, x: np.ndarray, y: np.ndarray) -> list:
        """Detecta discontinuidades en la función"""
        discontinuities = []
        
        # Calcular diferencias
        dy = np.diff(y)
        dx = np.diff(x)
        
        # Detectar saltos grandes
        derivatives = np.abs(dy / (dx + 1e-10))
        threshold = np.mean(derivatives) + 5 * np.std(derivatives)
        
        disc_indices = np.where(derivatives > threshold)[0]
        
        for idx in disc_indices:
            if idx < len(x) - 1:
                discontinuities.append(x[idx])
        
        # Eliminar duplicados muy cercanos
        if discontinuities:
            unique_disc = [discontinuities[0]]
            for d in discontinuities[1:]:
                if abs(d - unique_disc[-1]) > self.period / 100:
                    unique_disc.append(d)
            return unique_disc
        
        return []
    
    def _analyze_frequency_content(self, y: np.ndarray) -> float:
        """
        Analiza el contenido de altas frecuencias usando FFT
        
        Returns:
            Proporción de energía en altas frecuencias (0-1)
        """
        # FFT de la señal
        Y = np.fft.fft(y)
        power = np.abs(Y)**2
        
        # Dividir espectro en mitades
        mid = len(power) // 2
        low_freq_power = np.sum(power[:mid//2])
        high_freq_power = np.sum(power[mid//2:mid])
        
        total_power = low_freq_power + high_freq_power
        
        if total_power < 1e-10:
            return 0.0
        
        return high_freq_power / total_power
    
    def _measure_smoothness(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Mide la suavidad de la función
        
        Returns:
            Métrica de suavidad (0 = muy irregular, 1 = muy suave)
        """
        # Calcular segunda derivada aproximada
        if len(y) < 3:
            return 1.0
        
        d2y = np.diff(np.diff(y))
        
        # Variación de la segunda derivada (curvatura)
        curvature_variation = np.std(d2y)
        
        # Normalizar (valores típicos: 0.1-100)
        # Valores bajos = suave, valores altos = irregular
        smoothness = 1.0 / (1.0 + curvature_variation / 10)
        
        return smoothness
    
    def _classify_complexity(self, n_disc: int, high_freq: float, smoothness: float) -> str:
        """
        Clasifica la complejidad de la función
        
        Args:
            n_disc: Número de discontinuidades
            high_freq: Contenido de altas frecuencias
            smoothness: Métrica de suavidad
            
        Returns:
            'simple', 'medium', 'high', 'extreme'
        """
        # Sistema de puntuación
        score = 0
        
        # Discontinuidades
        if n_disc == 0:
            score += 0
        elif n_disc <= 2:
            score += 2
        elif n_disc <= 5:
            score += 4
        else:
            score += 6
        
        # Contenido de altas frecuencias
        if high_freq < 0.1:
            score += 0
        elif high_freq < 0.3:
            score += 1
        elif high_freq < 0.5:
            score += 2
        else:
            score += 3
        
        # Suavidad
        if smoothness > 0.8:
            score += 0
        elif smoothness > 0.5:
            score += 1
        elif smoothness > 0.3:
            score += 2
        else:
            score += 3
        
        # Clasificar según puntuación
        if score <= 2:
            return 'simple'
        elif score <= 5:
            return 'medium'
        elif score <= 8:
            return 'high'
        else:
            return 'extreme'
    
    def recommend_n_terms(self, analysis: Dict = None) -> int:
        """
        Recomienda número de términos basado en el análisis
        
        Args:
            analysis: Resultado de analyze_function (opcional)
            
        Returns:
            Número recomendado de términos
        """
        if analysis is None:
            analysis = self.analyze_function()
        
        complexity = analysis['complexity']
        n_disc = analysis['discontinuities']
        high_freq = analysis['high_frequency_content']
        
        # Base según complejidad
        base_terms = {
            'simple': 20,
            'medium': 50,
            'high': 100,
            'extreme': 200
        }
        
        recommended = base_terms.get(complexity, 50)
        
        # Ajustar por discontinuidades
        recommended += n_disc * 15
        
        # Ajustar por altas frecuencias
        if high_freq > 0.5:
            recommended += 30
        elif high_freq > 0.3:
            recommended += 15
        
        # Limitar a rangos razonables
        recommended = max(10, min(300, recommended))
        
        return recommended
    
    def recommend_speed(self, n_terms: int) -> str:
        """
        Recomienda velocidad de animación según número de términos
        
        Args:
            n_terms: Número de términos a usar
            
        Returns:
            'Muy Lenta', 'Lenta', 'Normal', 'Rápida'
        """
        if n_terms < 20:
            return 'Lenta'
        elif n_terms < 50:
            return 'Normal'
        elif n_terms < 100:
            return 'Rápida'
        else:
            return 'Muy Rápida'
    
    def recommend_window(self, analysis: Dict = None) -> str:
        """
        Recomienda tipo de ventana según características
        
        Args:
            analysis: Resultado de analyze_function (opcional)
            
        Returns:
            'Rectangular', 'Hann', 'Hamming'
        """
        if analysis is None:
            analysis = self.analyze_function()
        
        n_disc = analysis['discontinuities']
        
        if n_disc == 0:
            return 'Rectangular'  # Sin discontinuidades, no hace falta ventana
        elif n_disc <= 2:
            return 'Hann'  # Pocas discontinuidades, Hann es buena opción
        else:
            return 'Hamming'  # Muchas discontinuidades, Hamming reduce mejor Gibbs
    
    def get_full_recommendation(self) -> Dict:
        """
        Genera recomendación completa con análisis y sugerencias
        
        Returns:
            Diccionario con análisis y recomendaciones
        """
        # Analizar función
        analysis = self.analyze_function()
        
        # Generar recomendaciones
        n_terms = self.recommend_n_terms(analysis)
        speed = self.recommend_speed(n_terms)
        window = self.recommend_window(analysis)
        
        # Explicar razones
        reasons = self._explain_recommendations(analysis, n_terms, speed, window)
        
        return {
            'analysis': analysis,
            'recommended_n_terms': n_terms,
            'recommended_speed': speed,
            'recommended_window': window,
            'reasons': reasons
        }
    
    def _explain_recommendations(self, analysis: Dict, n_terms: int, 
                                 speed: str, window: str) -> str:
        """Genera explicación de las recomendaciones"""
        
        complexity_names = {
            'simple': 'SIMPLE',
            'medium': 'MODERADA',
            'high': 'ALTA',
            'extreme': 'MUY ALTA'
        }
        
        explanation = f"""
╔═══════════════════════════════════════════════════════════════╗
║           🎯 RECOMENDACIÓN INTELIGENTE DE PARÁMETROS           ║
╚═══════════════════════════════════════════════════════════════╝

📊 ANÁLISIS DE LA FUNCIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Complejidad: {complexity_names[analysis['complexity']]}
Discontinuidades: {analysis['discontinuities']}
Contenido de altas frecuencias: {analysis['high_frequency_content']:.1%}
Suavidad: {analysis['smoothness']:.1%}

💡 RECOMENDACIONES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Número de términos: {n_terms}
✓ Velocidad de animación: {speed}
✓ Tipo de ventana: {window}

📝 JUSTIFICACIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Explicar términos
        if analysis['complexity'] == 'simple':
            explanation += f"• {n_terms} términos son SUFICIENTES para esta función suave\n"
            explanation += "  Más términos NO mejorarán significativamente la aproximación\n\n"
        elif analysis['complexity'] == 'medium':
            explanation += f"• {n_terms} términos logran buen balance precisión/velocidad\n"
            explanation += "  La función tiene complejidad moderada\n\n"
        elif analysis['complexity'] == 'high':
            explanation += f"• {n_terms} términos son NECESARIOS para capturar los detalles\n"
            explanation += "  La función tiene alta complejidad y/o discontinuidades\n\n"
        else:
            explanation += f"• {n_terms} términos son el MÍNIMO para aproximación razonable\n"
            explanation += "  ⚠️ Función muy compleja, considera simplificarla\n\n"
        
        # Explicar ventana
        if window == 'Rectangular':
            explanation += "• Ventana RECTANGULAR: sin discontinuidades, no es necesaria\n"
        elif window == 'Hann':
            explanation += "• Ventana HANN: reduce el fenómeno de Gibbs suavemente\n"
        else:
            explanation += "• Ventana HAMMING: mejor reducción de Gibbs para múltiples discontinuidades\n"
        
        # Advertencias especiales
        if analysis['discontinuities'] > 0:
            explanation += f"\n⚠️  FENÓMENO DE GIBBS ESPERADO\n"
            explanation += f"   {analysis['discontinuities']} discontinuidad(es) causarán sobrepicos del 9%\n"
        
        if analysis['high_frequency_content'] > 0.5:
            explanation += f"\n🔊 ALTO CONTENIDO DE FRECUENCIAS\n"
            explanation += f"   La función cambia rápidamente, necesita muchos términos\n"
        
        explanation += """
╔═══════════════════════════════════════════════════════════════╗
║  💡 Sugerencia: Acepta estas recomendaciones para resultados   ║
║     óptimos, o ajusta manualmente según tus necesidades        ║
╚═══════════════════════════════════════════════════════════════╝
"""
        
        return explanation
    
    def get_compact_recommendation(self) -> str:
        """Versión compacta para mostrar en GUI"""
        rec = self.get_full_recommendation()
        
        return f"""🎯 Recomendación: {rec['recommended_n_terms']} términos | Velocidad: {rec['recommended_speed']} | Ventana: {rec['recommended_window']}
Complejidad: {rec['analysis']['complexity'].upper()} | Discontinuidades: {rec['analysis']['discontinuities']}"""


def test_recommender():
    """Función de prueba"""
    import numpy as np
    
    # Función simple (seno)
    def f_simple(x):
        return np.sin(x)
    
    # Función compleja (onda cuadrada)
    def f_complex(x):
        return 1 if x % (2*np.pi) < np.pi else -1
    
    print("=" * 70)
    print("PRUEBA 1: Función simple (seno)")
    print("=" * 70)
    rec1 = SmartRecommender(f_simple, 2*np.pi)
    print(rec1.get_full_recommendation()['reasons'])
    
    print("\n" + "=" * 70)
    print("PRUEBA 2: Función compleja (onda cuadrada)")
    print("=" * 70)
    rec2 = SmartRecommender(f_complex, 2*np.pi)
    print(rec2.get_full_recommendation()['reasons'])


if __name__ == "__main__":
    test_recommender()
