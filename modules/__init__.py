"""
Paquete modules - Solucionador Educativo de Series de Fourier
Contiene los módulos principales de la aplicación
"""

from .solver import FourierSolver
from .explanations import FourierExplanation
from .visualization import FourierVisualizer
from .epicycles import FourierEpicycles

__all__ = ['FourierSolver', 'FourierExplanation', 'FourierVisualizer', 'FourierEpicycles']

