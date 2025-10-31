"""
Módulo visualization.py - Gráficos estáticos de Series de Fourier
(Reemplazo simplificado del módulo animations.py eliminado)
"""

import numpy as np
import matplotlib.pyplot as plt


class FourierVisualizer:
    """Clase para crear visualizaciones estáticas de Series de Fourier"""
    
    def __init__(self, solver):
        """
        Inicializa el visualizador
        
        Args:
            solver: Instancia de FourierSolver
        """
        self.solver = solver
        
    def create_static_plot(self, show_error=True, n_points=500):
        """
        Crea un gráfico estático comparando f(x) original y la aproximación
        
        Args:
            show_error: Si True, muestra panel de error
            n_points: Número de puntos para graficar
            
        Returns:
            Figure de matplotlib
        """
        if show_error:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        else:
            fig, ax1 = plt.subplots(1, 1, figsize=(12, 6))
        
        fig.patch.set_facecolor('#f8f9fa')
        
        # Puntos para evaluación
        x_vals = np.linspace(-self.solver.L, self.solver.L, n_points)
        
        # Evaluar función original
        y_original = self.solver.f_lambda(x_vals)
        
        # Evaluar serie de Fourier
        y_fourier = self.solver.evaluate_series(x_vals, self.solver.n_terms)
        
        # Panel 1: Comparación
        ax1.plot(x_vals, y_original, 'b-', linewidth=2.5, label='f(x) original', alpha=0.7)
        ax1.plot(x_vals, y_fourier, 'r--', linewidth=2, label=f'Serie Fourier (N={self.solver.n_terms})', alpha=0.8)
        ax1.axhline(0, color='black', linewidth=0.5, alpha=0.3)
        ax1.axvline(0, color='black', linewidth=0.5, alpha=0.3)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_xlabel('x', fontsize=11, fontweight='bold')
        ax1.set_ylabel('f(x)', fontsize=11, fontweight='bold')
        ax1.set_title(f'Serie de Fourier: f(x) vs Aproximación ({self.solver.n_terms} términos)', 
                     fontsize=13, fontweight='bold', pad=15)
        ax1.legend(loc='best', framealpha=0.9, fontsize=10)
        
        if show_error:
            # Panel 2: Error
            error = y_original - y_fourier
            ax2.plot(x_vals, error, 'g-', linewidth=2, label='Error', alpha=0.7)
            ax2.axhline(0, color='black', linewidth=0.5, alpha=0.3)
            ax2.fill_between(x_vals, 0, error, alpha=0.3, color='green')
            ax2.grid(True, alpha=0.3, linestyle='--')
            ax2.set_xlabel('x', fontsize=11, fontweight='bold')
            ax2.set_ylabel('Error', fontsize=11, fontweight='bold')
            ax2.set_title('Error de Aproximación: f(x) - Serie', 
                         fontsize=12, fontweight='bold', pad=10)
            ax2.legend(loc='best', framealpha=0.9, fontsize=10)
            
            # Calcular métricas de error
            mse = np.mean(error**2)
            mae = np.mean(np.abs(error))
            max_error = np.max(np.abs(error))
            
            error_text = f'MSE: {mse:.6f} | MAE: {mae:.6f} | Max: {max_error:.6f}'
            ax2.text(0.5, 0.95, error_text, transform=ax2.transAxes,
                    fontsize=9, verticalalignment='top', horizontalalignment='center',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff3cd', 
                             edgecolor='#ffc107', alpha=0.9))
        
        plt.tight_layout()
        return fig
    
    def create_spectrum_plot(self):
        """
        Crea gráfico del espectro de frecuencias (amplitudes)
        
        Returns:
            Figure de matplotlib
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.patch.set_facecolor('#f8f9fa')
        
        ns = np.arange(1, self.solver.n_terms + 1)
        
        # Calcular amplitudes
        amplitudes = np.sqrt(np.array(self.solver.an_list)**2 + 
                           np.array(self.solver.bn_list)**2)
        
        # Panel 1: Espectro de amplitudes
        ax1.stem(ns, amplitudes, basefmt=' ', linefmt='C0-', markerfmt='C0o')
        ax1.axhline(0, color='black', linewidth=0.5, alpha=0.3)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_xlabel('n (Armónico)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Amplitud |cn|', fontsize=11, fontweight='bold')
        ax1.set_title('Espectro de Amplitudes de Fourier', 
                     fontsize=13, fontweight='bold', pad=15)
        
        # Panel 2: Coeficientes an y bn
        ax2.stem(ns, self.solver.an_list, basefmt=' ', linefmt='C0-', 
                markerfmt='C0o', label='an (coseno)')
        ax2.stem(ns, self.solver.bn_list, basefmt=' ', linefmt='C1-', 
                markerfmt='C1s', label='bn (seno)')
        ax2.axhline(0, color='black', linewidth=0.5, alpha=0.3)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.set_xlabel('n (Armónico)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Coeficiente', fontsize=11, fontweight='bold')
        ax2.set_title('Coeficientes de Fourier (an, bn)', 
                     fontsize=13, fontweight='bold', pad=15)
        ax2.legend(loc='best', framealpha=0.9, fontsize=10)
        
        plt.tight_layout()
        return fig
    
    def create_term_by_term_plot(self, max_terms=6):
        """
        Muestra términos individuales de la serie
        
        Args:
            max_terms: Número máximo de términos a mostrar
            
        Returns:
            Figure de matplotlib
        """
        actual_terms = min(max_terms, self.solver.n_terms)
        
        fig, axes = plt.subplots(actual_terms, 1, figsize=(12, 2.5 * actual_terms))
        fig.patch.set_facecolor('#f8f9fa')
        
        if actual_terms == 1:
            axes = [axes]
        
        x_vals = np.linspace(-self.solver.L, self.solver.L, 500)
        
        for i, ax in enumerate(axes):
            n = i + 1
            an = self.solver.an_list[i]
            bn = self.solver.bn_list[i]
            
            # Evaluar término individual
            omega = n * np.pi / self.solver.L
            term = an * np.cos(omega * x_vals) + bn * np.sin(omega * x_vals)
            
            # Graficar
            ax.plot(x_vals, term, linewidth=2, label=f'n={n}')
            ax.axhline(0, color='black', linewidth=0.5, alpha=0.3)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_ylabel(f'Término {n}', fontsize=10, fontweight='bold')
            ax.legend(loc='upper right', framealpha=0.9, fontsize=9)
            
            # Mostrar coeficientes
            coef_text = f'an={an:.4f}, bn={bn:.4f}'
            ax.text(0.02, 0.95, coef_text, transform=ax.transAxes,
                   fontsize=8, verticalalignment='top',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                            alpha=0.8, edgecolor='gray'))
        
        axes[-1].set_xlabel('x', fontsize=11, fontweight='bold')
        fig.suptitle('Términos Individuales de la Serie de Fourier', 
                    fontsize=14, fontweight='bold', y=0.995)
        
        plt.tight_layout()
        return fig
