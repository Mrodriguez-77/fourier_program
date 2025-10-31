"""
Módulo explanations.py - Explicaciones educativas paso a paso
Proporciona explicaciones detalladas del cálculo de series de Fourier
Incluye detección y explicación del fenómeno de Gibbs
"""

import numpy as np
import sympy as sp
from sympy import symbols, sin, cos, pi, integrate, latex
from typing import List, Dict, Tuple, Callable, Optional


class FourierExplanation:
    """Clase para generar explicaciones educativas del cálculo de Fourier"""
    
    def __init__(self, solver):
        """
        Inicializa el explicador
        
        Args:
            solver: Instancia de FourierSolver
        """
        self.solver = solver
        self.steps = []
        
    def explain_theory(self) -> str:
        """Retorna la teoría básica de las series de Fourier"""
        theory = """
═══════════════════════════════════════════════════════════
        TEORÍA DE SERIES DE FOURIER
═══════════════════════════════════════════════════════════

Una función periódica f(x) con período T puede expresarse como
una serie infinita de senos y cosenos:

    f(x) = a₀/2 + Σ[aₙcos(nπx/L) + bₙsin(nπx/L)]
    
donde L = T/2 (semi-período)

Los coeficientes se calculan mediante:

    a₀ = (1/L) ∫₋ₗᴸ f(x) dx
    
    aₙ = (1/L) ∫₋ₗᴸ f(x)cos(nπx/L) dx
    
    bₙ = (1/L) ∫₋ₗᴸ f(x)sin(nπx/L) dx

═══════════════════════════════════════════════════════════
"""
        return theory
    
    def explain_a0_calculation(self) -> str:
        """Explica el cálculo de a₀"""
        L = self.solver.L
        f_str = str(self.solver.f_symbolic)
        
        explanation = f"""
╔═══════════════════════════════════════════════════════════╗
║           CÁLCULO DEL COEFICIENTE a₀                      ║
╚═══════════════════════════════════════════════════════════╝

Función: f(x) = {f_str}
Período: T = {self.solver.period:.4f}
Semi-período: L = {L:.4f}

Paso 1: Aplicar la fórmula
────────────────────────────────────────────────────────────
    a₀ = (1/L) ∫₋ₗᴸ f(x) dx
    
    a₀ = (1/{L:.4f}) ∫₋{L:.4f}^{L:.4f} ({f_str}) dx

Paso 2: Calcular la integral
────────────────────────────────────────────────────────────
"""
        
        try:
            # Calcular la integral simbólicamente
            x = self.solver.x
            integral = integrate(self.solver.f_symbolic, (x, -L, L))
            explanation += f"    ∫₋{L:.4f}^{L:.4f} ({f_str}) dx = {integral}\n\n"
            
            explanation += f"Paso 3: Dividir por L\n"
            explanation += f"────────────────────────────────────────────────────────────\n"
            explanation += f"    a₀ = {integral} / {L:.4f} = {self.solver.a0:.6f}\n\n"
        except:
            explanation += f"    (Calculada numéricamente)\n"
            explanation += f"    a₀ ≈ {self.solver.a0:.6f}\n\n"
        
        explanation += f"═══════════════════════════════════════════════════════════\n"
        explanation += f"RESULTADO: a₀ = {self.solver.a0:.6f}\n"
        explanation += f"═══════════════════════════════════════════════════════════\n"
        
        return explanation
    
    def explain_an_calculation(self, n: int) -> str:
        """Explica el cálculo de aₙ para un n específico"""
        L = self.solver.L
        f_str = str(self.solver.f_symbolic)
        an_value = self.solver.an_list[n-1] if n <= len(self.solver.an_list) else 0
        
        explanation = f"""
╔═══════════════════════════════════════════════════════════╗
║         CÁLCULO DEL COEFICIENTE a_{n}                      ║
╚═══════════════════════════════════════════════════════════╝

Paso 1: Aplicar la fórmula
────────────────────────────────────────────────────────────
    aₙ = (1/L) ∫₋ₗᴸ f(x)cos(nπx/L) dx
    
    a_{n} = (1/{L:.4f}) ∫₋{L:.4f}^{L:.4f} ({f_str})·cos({n}πx/{L:.4f}) dx

Paso 2: Expandir el producto
────────────────────────────────────────────────────────────
    Integrando: ({f_str})·cos({n}πx/{L:.4f})

Paso 3: Calcular la integral
────────────────────────────────────────────────────────────
"""
        
        try:
            x = self.solver.x
            integrand = self.solver.f_symbolic * cos(n * pi * x / L)
            integral = integrate(integrand, (x, -L, L))
            explanation += f"    ∫₋{L:.4f}^{L:.4f} [...] dx = {integral}\n\n"
            explanation += f"Paso 4: Dividir por L\n"
            explanation += f"────────────────────────────────────────────────────────────\n"
            explanation += f"    a_{n} = {integral} / {L:.4f} = {an_value:.6f}\n\n"
        except:
            explanation += f"    (Calculada numéricamente)\n"
            explanation += f"    a_{n} ≈ {an_value:.6f}\n\n"
        
        explanation += f"═══════════════════════════════════════════════════════════\n"
        explanation += f"RESULTADO: a_{n} = {an_value:.6f}\n"
        explanation += f"═══════════════════════════════════════════════════════════\n"
        
        return explanation
    
    def explain_bn_calculation(self, n: int) -> str:
        """Explica el cálculo de bₙ para un n específico"""
        L = self.solver.L
        f_str = str(self.solver.f_symbolic)
        bn_value = self.solver.bn_list[n-1] if n <= len(self.solver.bn_list) else 0
        
        explanation = f"""
╔═══════════════════════════════════════════════════════════╗
║         CÁLCULO DEL COEFICIENTE b_{n}                      ║
╚═══════════════════════════════════════════════════════════╝

Paso 1: Aplicar la fórmula
────────────────────────────────────────────────────────────
    bₙ = (1/L) ∫₋ₗᴸ f(x)sin(nπx/L) dx
    
    b_{n} = (1/{L:.4f}) ∫₋{L:.4f}^{L:.4f} ({f_str})·sin({n}πx/{L:.4f}) dx

Paso 2: Expandir el producto
────────────────────────────────────────────────────────────
    Integrando: ({f_str})·sin({n}πx/{L:.4f})

Paso 3: Calcular la integral
────────────────────────────────────────────────────────────
"""
        
        try:
            x = self.solver.x
            integrand = self.solver.f_symbolic * sin(n * pi * x / L)
            integral = integrate(integrand, (x, -L, L))
            explanation += f"    ∫₋{L:.4f}^{L:.4f} [...] dx = {integral}\n\n"
            explanation += f"Paso 4: Dividir por L\n"
            explanation += f"────────────────────────────────────────────────────────────\n"
            explanation += f"    b_{n} = {integral} / {L:.4f} = {bn_value:.6f}\n\n"
        except:
            explanation += f"    (Calculada numéricamente)\n"
            explanation += f"    b_{n} ≈ {bn_value:.6f}\n\n"
        
        explanation += f"═══════════════════════════════════════════════════════════\n"
        explanation += f"RESULTADO: b_{n} = {bn_value:.6f}\n"
        explanation += f"═══════════════════════════════════════════════════════════\n"
        
        return explanation
    
    def explain_symbolic_formulas(self) -> str:
        """Explica las fórmulas simbólicas generales"""
        explanation = """
╔═══════════════════════════════════════════════════════════╗
║         FÓRMULAS SIMBÓLICAS GENERALES                     ║
╚═══════════════════════════════════════════════════════════╝

Si es posible calcular las integrales simbólicamente,
obtenemos fórmulas generales para cualquier n:

"""
        
        if self.solver.an_symbolic is not None:
            explanation += f"Fórmula general para aₙ:\n"
            explanation += f"────────────────────────────────────────────────────────────\n"
            explanation += f"    aₙ = {self.solver.an_symbolic}\n\n"
        else:
            explanation += "No se pudo obtener fórmula simbólica para aₙ\n\n"
        
        if self.solver.bn_symbolic is not None:
            explanation += f"Fórmula general para bₙ:\n"
            explanation += f"────────────────────────────────────────────────────────────\n"
            explanation += f"    bₙ = {self.solver.bn_symbolic}\n\n"
        else:
            explanation += "No se pudo obtener fórmula simbólica para bₙ\n\n"
        
        explanation += "═══════════════════════════════════════════════════════════\n"
        
        return explanation
    
    def get_coefficients_summary(self) -> str:
        """Retorna un resumen de todos los coeficientes"""
        summary = """
╔═══════════════════════════════════════════════════════════╗
║         RESUMEN DE COEFICIENTES                           ║
╚═══════════════════════════════════════════════════════════╝

"""
        summary += f"a₀ = {self.solver.a0:.6f}\n\n"
        summary += "  n  │      aₙ      │      bₙ      │  Magnitud\n"
        summary += "─────┼──────────────┼──────────────┼─────────────\n"
        
        for i, (an, bn) in enumerate(zip(self.solver.an_list, self.solver.bn_list), 1):
            magnitude = (an**2 + bn**2)**0.5
            summary += f"  {i:2d} │ {an:12.6f} │ {bn:12.6f} │ {magnitude:11.6f}\n"
        
        summary += "\n═══════════════════════════════════════════════════════════\n"
        
        return summary
    
    def get_series_construction(self, n_max: int = None) -> str:
        """Muestra cómo se construye la serie término a término"""
        if n_max is None:
            n_max = min(5, len(self.solver.an_list))
        
        L = self.solver.L
        construction = """
╔═══════════════════════════════════════════════════════════╗
║         CONSTRUCCIÓN DE LA SERIE                          ║
╚═══════════════════════════════════════════════════════════╝

La serie de Fourier se construye sumando términos:

"""
        construction += f"S₀(x) = a₀/2 = {self.solver.a0/2:.6f}\n\n"
        
        for n in range(1, n_max + 1):
            an = self.solver.an_list[n-1]
            bn = self.solver.bn_list[n-1]
            
            construction += f"Término {n}:\n"
            if abs(an) > 1e-10:
                construction += f"  + {an:.6f}·cos({n}πx/{L:.2f})\n"
            if abs(bn) > 1e-10:
                construction += f"  + {bn:.6f}·sin({n}πx/{L:.2f})\n"
            construction += f"\nS_{n}(x) = S_{n-1}(x) + término {n}\n\n"
        
        construction += "═══════════════════════════════════════════════════════════\n"
        
        return construction
    
    def get_complete_explanation(self) -> str:
        """Genera la explicación completa"""
        full_text = self.explain_theory()
        full_text += "\n" + self.explain_a0_calculation()
        
        # Explicar los primeros 3 términos
        for n in range(1, min(4, len(self.solver.an_list) + 1)):
            full_text += "\n" + self.explain_an_calculation(n)
            full_text += "\n" + self.explain_bn_calculation(n)
        
        full_text += "\n" + self.explain_symbolic_formulas()
        full_text += "\n" + self.get_coefficients_summary()
        full_text += "\n" + self.get_series_construction()
        
        return full_text
    
    def get_latex_formulas(self) -> Dict[str, str]:
        """Retorna las fórmulas en formato LaTeX para visualización"""
        formulas = {
            'general': r'f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty} \left[a_n \cos\left(\frac{n\pi x}{L}\right) + b_n \sin\left(\frac{n\pi x}{L}\right)\right]',
            'a0': r'a_0 = \frac{1}{L} \int_{-L}^{L} f(x) \, dx',
            'an': r'a_n = \frac{1}{L} \int_{-L}^{L} f(x) \cos\left(\frac{n\pi x}{L}\right) \, dx',
            'bn': r'b_n = \frac{1}{L} \int_{-L}^{L} f(x) \sin\left(\frac{n\pi x}{L}\right) \, dx'
        }
        
        return formulas


def test_explanations():
    """Función de prueba"""
    from solver import FourierSolver
    
    # Crear solver
    solver = FourierSolver("x", period=2*3.14159, n_terms=5)
    solver.calculate_all_coefficients()
    
    # Crear explicador
    explainer = FourierExplanation(solver)
    
    # Mostrar explicación completa
    print(explainer.get_complete_explanation())


if __name__ == "__main__":
    test_explanations()


class GibbsExplainer:
    """Detecta y explica el fenómeno de Gibbs en discontinuidades"""
    
    def __init__(self, func: Callable, period: float, tolerance: float = 0.1):
        """
        Inicializa el explicador de Gibbs
        
        Args:
            func: Función a analizar
            period: Período de la función
            tolerance: Tolerancia para detectar discontinuidades
        """
        self.func = func
        self.period = period
        self.tolerance = tolerance
        
    def detect_discontinuities(self, num_samples: int = 1000) -> list:
        """
        Detecta discontinuidades en la función
        
        Args:
            num_samples: Número de puntos a evaluar
            
        Returns:
            Lista de posiciones x donde hay discontinuidades
        """
        x_values = np.linspace(-self.period/2, self.period/2, num_samples)
        discontinuities = []
        
        for i in range(len(x_values) - 1):
            x1, x2 = x_values[i], x_values[i+1]
            
            try:
                # Calcular límites
                y1 = self.func(x1)
                y2 = self.func(x2)
                
                # Detectar salto brusco
                jump = abs(y2 - y1)
                dx = abs(x2 - x1)
                
                # Si la derivada es muy grande, hay discontinuidad
                if dx > 0 and jump / dx > 100:  # Pendiente > 100
                    discontinuities.append(x1)
                    
            except:
                # Error al evaluar puede indicar discontinuidad
                discontinuities.append(x1)
        
        # Eliminar discontinuidades muy cercanas (mismo punto)
        if discontinuities:
            unique_disc = [discontinuities[0]]
            for d in discontinuities[1:]:
                if abs(d - unique_disc[-1]) > self.period / 100:
                    unique_disc.append(d)
            return unique_disc
        
        return []
    
    def calculate_jump_size(self, x_disc: float) -> float:
        """
        Calcula el tamaño del salto en una discontinuidad
        
        Args:
            x_disc: Posición de la discontinuidad
            
        Returns:
            Tamaño del salto (valor absoluto)
        """
        epsilon = self.period / 10000  # Punto muy cercano
        
        try:
            left_limit = self.func(x_disc - epsilon)
            right_limit = self.func(x_disc + epsilon)
            return abs(right_limit - left_limit)
        except:
            return 0.0
    
    def get_gibbs_explanation(self) -> Optional[str]:
        """
        Genera explicación del fenómeno de Gibbs si aplica
        
        Returns:
            Texto explicativo o None si no hay discontinuidades
        """
        discontinuities = self.detect_discontinuities()
        
        if not discontinuities:
            return None
        
        # Calcular tamaño promedio de saltos
        jumps = [self.calculate_jump_size(d) for d in discontinuities]
        valid_jumps = [j for j in jumps if j > 0 and not np.isnan(j)]
        
        if not valid_jumps:
            return None
        
        avg_jump = np.mean(valid_jumps)
        
        if avg_jump < self.tolerance or np.isnan(avg_jump):
            return None
        
        # Generar explicación
        explanation = f"""
╔══════════════════════════════════════════════════════════════════╗
║              🌊 FENÓMENO DE GIBBS DETECTADO 🌊                    ║
╚══════════════════════════════════════════════════════════════════╝

📍 Discontinuidades encontradas: {len(discontinuities)}
📏 Salto promedio: {avg_jump:.3f}

❓ ¿QUÉ ES EL FENÓMENO DE GIBBS?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cuando una serie de Fourier aproxima una función con discontinuidades 
(saltos bruscos), aparece un SOBREPICO del 9% cerca del salto, 
sin importar cuántos términos uses.

⚠️  OBSERVACIÓN IMPORTANTE:
   • Sobrepico inevitable: ~9% del salto
   • No desaparece con más términos
   • El pico se "concentra" pero NO se elimina
   • Es una propiedad MATEMÁTICA fundamental

🔬 EJEMPLO EN TU FUNCIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Si el salto es de {avg_jump:.2f} unidades:
   • Sobrepico esperado: {avg_jump * 0.09:.3f} unidades
   • Posición: justo antes/después de x = {discontinuities[0]:.3f}

📊 ¿POR QUÉ OCURRE?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Las funciones seno/coseno son SUAVES (diferenciables infinitamente).
Cuando intentan aproximar un SALTO BRUSCO:
   • Cerca del salto: oscilaciones rápidas
   • El pico máximo siempre es 9% mayor
   • Más términos → pico más angosto, NO más bajo

💡 SOLUCIONES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Aceptarlo: es comportamiento esperado
2. Usar ventanas (Hann, Hamming): reduce el sobrepico
3. Wavelets: mejor para discontinuidades
4. Aproximación local: diferentes series en cada región

🎓 TEORÍA MATEMÁTICA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

El sobrepico viene de la integral:

    lim   ∫[0 to π] sin(x)/x dx ≈ 1.851937...
   N→∞

Para un salto de altura h:
    Sobrepico = h × (1.851937/π - 0.5) ≈ h × 0.0895 ≈ 9% de h

Este valor es CONSTANTE, probado por Josiah Willard Gibbs (1899)

╔══════════════════════════════════════════════════════════════════╗
║  ℹ️  Este comportamiento es NORMAL y ESPERADO en tu aproximación ║
╚══════════════════════════════════════════════════════════════════╝
"""
        return explanation
    
    def get_short_explanation(self) -> Optional[str]:
        """Versión corta de la explicación para la GUI"""
        discontinuities = self.detect_discontinuities()
        
        if not discontinuities:
            return None
        
        jumps = [self.calculate_jump_size(d) for d in discontinuities]
        valid_jumps = [j for j in jumps if j > 0 and not np.isnan(j)]
        
        if not valid_jumps:
            return None
            
        avg_jump = np.mean(valid_jumps)
        
        if avg_jump < self.tolerance or np.isnan(avg_jump):
            return None
        
        return f"""⚠️ FENÓMENO DE GIBBS DETECTADO
{len(discontinuities)} discontinuidad(es) encontrada(s)
Sobrepico inevitable: ~{avg_jump * 0.09:.3f} unidades ({avg_jump * 9:.1f}% del salto)

Este sobrepico NO desaparece con más términos.
Es una propiedad matemática fundamental de las series de Fourier.

💡 Tip: Usa ventanas (Hann/Hamming) para reducir el efecto."""


def explain_convergence(n_terms: int, symmetry: str) -> str:
    """
    Explica qué esperar de la convergencia según los parámetros
    
    Args:
        n_terms: Número de términos
        symmetry: Tipo de simetría detectada
        
    Returns:
        Texto explicativo
    """
    explanations = {
        'even': f"""
Función PAR detectada (f(-x) = f(x))
Solo se calculan {n_terms} términos de COSENO
Cálculo 50% más rápido ⚡""",
        
        'odd': f"""
Función IMPAR detectada (f(-x) = -f(x))
Solo se calculan {n_terms} términos de SENO
Cálculo 50% más rápido ⚡""",
        
        'half_wave': f"""
Simetría de MEDIA ONDA detectada
Solo armónicos IMPARES ({n_terms//2} términos efectivos)
Cálculo 50% más rápido ⚡""",
        
        'none': f"""
Sin simetría especial
Se calculan {n_terms} términos completos (senos + cosenos)"""
    }
    
    return explanations.get(symmetry, "")
