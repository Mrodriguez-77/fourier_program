"""
Módulo epicycles.py - Visualización de Círculos de Fourier (Epicíclos)
Muestra cómo cada término de Fourier es un círculo rotando
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import matplotlib
matplotlib.use('TkAgg')


class FourierEpicycles:
    """Clase para visualizar círculos de Fourier (epicíclos)"""
    
    def __init__(self, solver):
        """
        Inicializa el visualizador de epicíclos
        
        Args:
            solver: Instancia de FourierSolver
        """
        self.solver = solver
        
    def create_epicycles_animation(self, n_terms=None, speed_preset='normal'):
        """
        Crea una animación de círculos de Fourier - ULTRA OPTIMIZADO
        
        Args:
            n_terms: Número de términos a mostrar (None = usar todos disponibles)
            speed_preset: 'fast' (200 fps), 'normal' (120 fps), 'detailed' (80 fps), 'slow' (50 fps)
            
        Returns:
            Tupla (fig, animation)
        """
        # PRESETS DE VELOCIDAD - Dinámicos según cantidad de términos
        speed_configs = {
            'fast': {'base_frames': 60, 'base_interval': 16},      # ~60 FPS, 1 segundo
            'normal': {'base_frames': 100, 'base_interval': 25},   # ~40 FPS, 2.5 segundos
            'detailed': {'base_frames': 150, 'base_interval': 40}, # ~25 FPS, 6 segundos
            'slow': {'base_frames': 200, 'base_interval': 50}      # ~20 FPS, 10 segundos
        }
        
        if n_terms is None:
            n_terms = self.solver.n_terms  # Usar TODOS los términos disponibles
        
        # Limitar a los coeficientes calculados
        n_terms = min(n_terms, len(self.solver.an_list))
        
        # NUEVO: Sistema inteligente de selección de círculos visibles
        # Para muchos términos, mostrar los más significativos (mayores amplitudes)
        if n_terms <= 50:
            visual_terms = n_terms  # Mostrar todos
        elif n_terms <= 150:
            visual_terms = min(100, n_terms)  # Hasta 100 círculos
        else:
            # Para 150+ términos, mostrar los 150 más grandes
            visual_terms = min(150, n_terms)
        
        # OPTIMIZACIÓN: Precalcular arrays de coeficientes
        an_array = np.array(self.solver.an_list[:n_terms])
        bn_array = np.array(self.solver.bn_list[:n_terms])
        radii = np.sqrt(an_array**2 + bn_array**2)
        phases = np.arctan2(bn_array, an_array)
        
        # Si hay muchos términos, seleccionar los más significativos para visualizar
        if n_terms > visual_terms:
            # Ordenar por magnitud y tomar los más grandes
            indices_sorted = np.argsort(radii)[::-1]  # De mayor a menor
            visual_indices = sorted(indices_sorted[:visual_terms])  # Mantener orden original
            
            print(f"⚠️ Mostrando los {visual_terms} círculos más grandes de {n_terms} términos totales")
            print(f"   Amplitud mínima mostrada: {radii[visual_indices[-1]]:.6f}")
        else:
            visual_indices = list(range(n_terms))
        
        # CREAR FIGURA ADAPTABLE - Se ajusta al espacio disponible
        # El tamaño real lo determina el canvas de Tkinter, no matplotlib
        # Proporción compacta que se adapta bien a ventanas modernas
        fig, ax = plt.subplots(1, 1, figsize=(10, 3.8))
        fig.patch.set_facecolor('#f8f9fa')
        
        # Reducir márgenes para aprovechar espacio
        fig.subplots_adjust(left=0.08, right=0.98, top=0.93, bottom=0.12)
        
        # Calcular límites de la función PRIMERO
        x_vals = np.linspace(-self.solver.L, self.solver.L, 500)
        y_original = self.solver.f_lambda(x_vals)
        y_range = y_original.max() - y_original.min()
        y_margin = y_range * 0.15
        y_min = y_original.min() - y_margin
        y_max = y_original.max() + y_margin
        
        # Calcular espacio para círculos de forma DINÁMICA
        # El espacio se adapta a la suma de radios de los círculos más grandes
        total_radius = np.sum(radii[:min(10, len(radii))])  # Suma de los 10 más grandes
        
        # REDUCIR tamaño de círculos si son muy grandes (escala de visualización)
        # Esto permite que los círculos grandes no dominen todo el espacio
        scale_factor = 0.75  # Reducir círculos al 75% de su tamaño
        radii_visual = radii * scale_factor
        
        # Espacio compacto proporcional - MÁS PEQUEÑO para zoom alejado por defecto
        circle_space_ratio = 0.18  # Solo 18% del ancho para círculos (antes 28%)
        circle_space = min(total_radius * scale_factor * 1.5, self.solver.L * circle_space_ratio)
        
        # ASEGURAR ESPACIO MÍNIMO para funciones con pocos/pequeños círculos (ej. sin(x))
        min_circle_space = self.solver.L * 0.15  # Al menos 15% del período
        circle_space = max(circle_space, min_circle_space)
        
        # LÍMITES ADAPTATIVOS: Vista alejada por defecto (como zoom out 4x)
        # Expandir límites para mostrar todo el contexto
        view_expansion = 1.5  # Factor de expansión para vista alejada
        left_margin = circle_space * 0.4  # Margen proporcional al espacio de círculos
        right_margin = self.solver.L * 0.3  # Margen derecho generoso
        
        ax.set_xlim(-circle_space * view_expansion - left_margin, 
                    self.solver.L + right_margin)
        ax.set_ylim(y_min * 1.2, y_max * 1.2)  # También expandir verticalmente
        
        # Configurar panel - SIN aspect equal para aprovechar espacio
        ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
        ax.set_title('Epiciclos de Fourier', fontsize=10, fontweight='bold', pad=4)
        ax.set_xlabel('x', fontsize=8)
        ax.set_ylabel('f(x)', fontsize=8)
        ax.tick_params(labelsize=7)  # Etiquetas de ejes más pequeñas
        ax.axhline(0, color='gray', linewidth=0.5, alpha=0.4)
        ax.axvline(0, color='gray', linewidth=0.5, alpha=0.4)
        
        # Dibujar función original MUY SUTIL (para no distraer)
        ax.plot(x_vals, y_original, color='#88AAFF', linewidth=1.5, 
                alpha=0.3, linestyle=':', zorder=1)
        
        # Elementos a animar
        circles = []
        lines = []
        
        # Crear círculos y líneas con colores del arcoíris
        colors = plt.cm.rainbow(np.linspace(0, 1, len(visual_indices)))
        
        # Crear círculos ULTRA DELGADOS - Estilo GIF con escala reducida
        for idx, i in enumerate(visual_indices):
            # Usar el radio VISUAL (escalado) para círculos más pequeños
            radius_visual = radii_visual[i]
            
            # Círculo muy delgado y sutil
            circle = Circle((0, 0), radius_visual, fill=False, 
                          color=colors[idx], linewidth=1.2, alpha=0.5)
            ax.add_patch(circle)
            circles.append(circle)
            
            # Línea del radio ultra delgada
            line, = ax.plot([], [], color=colors[idx], linewidth=1, alpha=0.4)
            lines.append(line)
        
        # Punto final pequeño pero visible
        point, = ax.plot([], [], 'o', color='#FF3366', markersize=7, 
                         markeredgecolor='#FFFF00', markeredgewidth=1.5, zorder=100)
        
        # Línea conectora VISIBLE - mismo color que la función para continuidad visual
        connector_line, = ax.plot([], [], color='#FF1493', linewidth=2, 
                                   alpha=0.6, linestyle='-', zorder=50)
        
        # LÍNEA DE LA FUNCIÓN - DESTACADA (como en el GIF)
        trail_function, = ax.plot([], [], color='#FF1493', linewidth=2.5, 
                                   alpha=0.9, zorder=10)
        
        # Punto actual MUY PEQUEÑO
        current_point, = ax.plot([], [], 'o', color='#FF0000', markersize=5,
                                 markeredgecolor='white', markeredgewidth=1, zorder=100)
        
        # Texto informativo MINI - Esquina superior derecha, ultra compacto
        info_text = ax.text(0.98, 0.97, '', transform=ax.transAxes,
                            fontsize=7, verticalalignment='top', horizontalalignment='right',
                            fontweight='normal',
                            bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                                    edgecolor='#CCCCCC', alpha=0.85, linewidth=0.5))
        
        def init():
            point.set_data([], [])
            current_point.set_data([], [])
            connector_line.set_data([], [])
            trail_function.set_data([], [])
            for line in lines:
                line.set_data([], [])
            return circles + lines + [point, current_point, connector_line, trail_function, info_text]
        
        def update(frame):
            # x avanza de -L a L
            x_pos = -self.solver.L + (frame / 100) * (2 * self.solver.L)
            
            # OPTIMIZACIÓN: Usar arrays precalculados y vectorización
            # Frecuencias angulares (precalculadas una sola vez fuera sería mejor)
            n_indices = np.arange(1, n_terms + 1)
            omegas = n_indices * np.pi / self.solver.L
            
            # Calcular TODAS las contribuciones con vectorización
            angles = omegas * x_pos + phases
            contributions = an_array * np.cos(omegas * x_pos) + bn_array * np.sin(omegas * x_pos)
            
            # Valor de la función
            y_func = self.solver.a0 / 2 + np.sum(contributions)
            
            # CÍRCULOS: Posición adaptativa - MÁS A LA IZQUIERDA
            # Colocar círculos bien a la izquierda para aprovechar el espacio
            # Para funciones simples (pocos círculos), posicionar más cerca del centro
            if len(visual_indices) <= 3:
                # Funciones simples: más cercanas al centro para mejor visibilidad
                circle_start_x = -circle_space * 0.8
            else:
                # Funciones complejas: más a la izquierda (como antes)
                circle_start_x = -circle_space * 1.3
            
            circle_x = circle_start_x
            circle_y = self.solver.a0 / 2
            
            # IMPORTANTE: Apilar círculos en orden correcto usando visual_indices
            # Usar radios VISUALES (escalados) para mantener tamaño reducido
            for idx, i in enumerate(visual_indices):
                # Centro del círculo en la posición actual acumulada
                circles[idx].center = (circle_x, circle_y)
                
                # Ángulo de rotación de este término
                angle_i = angles[i]
                
                # Vector del radio usando RADIO VISUAL (escalado)
                dx = radii_visual[i] * np.cos(angle_i)
                dy = radii_visual[i] * np.sin(angle_i)
                
                # Dibujar línea del radio
                lines[idx].set_data([circle_x, circle_x + dx], [circle_y, circle_y + dy])
                
                # Actualizar posición para el siguiente círculo
                circle_y += dy
                circle_x += dx
            
            # Punto final en los círculos (tip del último círculo visualizado)
            final_x = circle_x
            final_y = circle_y
            
            # Si hay términos no mostrados, agregar su contribución (con radios escalados)
            if n_terms > len(visual_indices):
                # Términos no visualizados pero que contribuyen al resultado
                hidden_indices = [i for i in range(n_terms) if i not in visual_indices]
                for i in hidden_indices:
                    angle_i = angles[i]
                    dx = radii_visual[i] * np.cos(angle_i)
                    dy = radii_visual[i] * np.sin(angle_i)
                    final_x += dx
                    final_y += dy
            
            # Punto final (debe coincidir con y_func)
            point.set_data([final_x], [final_y])
            
            # Línea conectora: desde el punto final de los círculos hasta el punto actual en la gráfica
            # Esta línea DEBE ir desde donde terminan los círculos hasta donde se está dibujando
            connector_line.set_data([final_x, x_pos], [final_y, y_func])
            
            # DIBUJAR LA FUNCIÓN: Solo la parte desde -L hasta x_pos (como en GIF)
            if frame > 0:
                # Calcular puntos desde -L hasta posición actual
                num_points = min(frame * 3, 300)
                x_range = np.linspace(-self.solver.L, x_pos, num_points)
                
                # Evaluar serie
                y_range = self.solver.evaluate_series(x_range, n_terms)
                
                trail_function.set_data(x_range, y_range)
            else:
                trail_function.set_data([], [])
            
            # Punto actual en la función
            current_point.set_data([x_pos], [y_func])
            
            # Texto COMPACTO - Solo lo esencial
            if n_terms > len(visual_indices):
                info_text.set_text(f'N={n_terms}\nVis={len(visual_indices)}\nx={x_pos:.1f}')
            else:
                info_text.set_text(f'N={n_terms}\nx={x_pos:.1f}\nf={y_func:.2f}')
            
            return circles + lines + [point, current_point, connector_line, trail_function, info_text]
        
        # OPTIMIZACIÓN DINÁMICA: Ajustar frames e interval según preset y complejidad
        config = speed_configs[speed_preset]
        
        # Ajustar según cantidad de términos (más términos = menos frames para mantener velocidad)
        if n_terms <= 50:
            n_frames = config['base_frames']
            interval_adjusted = config['base_interval']
        elif n_terms <= 200:
            n_frames = int(config['base_frames'] * 0.75)  # 25% menos frames
            interval_adjusted = config['base_interval']
        else:  # 200+ términos
            n_frames = int(config['base_frames'] * 0.5)  # 50% menos frames
            interval_adjusted = config['base_interval']
        
        print(f"📊 Animación: {n_frames} frames, {interval_adjusted}ms/frame, preset={speed_preset}, términos={n_terms}")
        
        anim = FuncAnimation(fig, update, init_func=init,
                           frames=n_frames, interval=interval_adjusted,
                           blit=False, repeat=True)
        
        # Tight layout para aprovechar máximo el espacio disponible
        plt.tight_layout(pad=0.5)
        
        return fig, anim
    
    def create_rotating_phasors(self, n_terms=None):
        """
        Crea un diagrama de fasores rotantes
        
        Args:
            n_terms: Número de términos
            
        Returns:
            Figure de matplotlib
        """
        if n_terms is None:
            n_terms = min(12, self.solver.n_terms)
        
        # Crear grid de subplots
        n_cols = 4
        n_rows = (n_terms + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 3 * n_rows),
                                subplot_kw=dict(projection='polar'))
        fig.patch.set_facecolor('#f8f9fa')
        axes = axes.flatten() if n_terms > 1 else [axes]
        
        for i in range(n_terms):
            ax = axes[i]
            n = i + 1
            
            an = self.solver.an_list[i]
            bn = self.solver.bn_list[i]
            
            magnitude = np.sqrt(an**2 + bn**2)
            phase = np.arctan2(bn, an)
            
            # Dibujar fasor
            ax.arrow(0, 0, phase, magnitude, head_width=0.3, head_length=0.1,
                    fc='#2E86AB', ec='#2E86AB', linewidth=2, alpha=0.8)
            
            ax.set_ylim(0, max(magnitude * 1.2, 0.1))
            ax.set_title(f'n={n}\n|c|={magnitude:.3f}, φ={np.degrees(phase):.1f}°',
                        fontsize=9, fontweight='bold')
            ax.grid(True, alpha=0.3)
        
        # Ocultar subplots no usados
        for i in range(n_terms, len(axes)):
            axes[i].set_visible(False)
        
        plt.suptitle('Fasores de Fourier (Representación Polar)', 
                    fontsize=15, fontweight='bold', y=0.995)
        plt.tight_layout()
        
        return fig


def test_epicycles():
    """Función de prueba básica"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from solver import FourierSolver
    
    print("Probando módulo de epiciclos...")
    print("Creando solver con función rampa: f(x) = x")
    
    # Crear solver con función simple
    solver = FourierSolver("x", -np.pi, np.pi)
    
    print("Calculando coeficientes...")
    a0 = solver.calculate_a0()
    print(f"  a₀ = {a0}")
    
    for n in range(1, 4):
        an = solver.calculate_an(n)
        bn = solver.calculate_bn(n)
        print(f"  a_{n} = {an:.4f}, b_{n} = {bn:.4f}")
    
    print("\n✅ Módulo de epiciclos funciona correctamente")
    print("Nota: Para ver la animación, integrar en main.py")


if __name__ == "__main__":
    test_epicycles()
