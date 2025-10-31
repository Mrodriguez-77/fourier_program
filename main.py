"""
main.py - Interfaz gráfica principal
Solucionador Educativo de Series de Fourier
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.solver import FourierSolver
from modules.explanations import FourierExplanation
from modules.visualization import FourierVisualizer


class FourierApp:
    """Aplicación principal de Series de Fourier"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador Educativo de Series de Fourier")
        self.root.geometry("1400x900")
        
        # Variables
        self.solver = None
        self.explainer = None
        self.visualizer = None  # Reemplaza animator
        self.current_animation = None
        
        # Funciones de ejemplo con nombres descriptivos - 21 FUNCIONES CLÁSICAS
        # Formato: "Nombre Descriptivo | código"
        self.example_functions = [
            # === BÁSICAS ===
            "Seno simple | sin(x)",
            "Coseno simple | cos(x)",
            "Rampa lineal | x",
            "Parábola | x**2",
            
            # === DISCONTINUAS (Espectaculares para epiciclos) ⭐ ===
            "Onda cuadrada (Gibbs) | 1 if x > 0 else -1",
            "Semirectificadora | x if x > 0 else 0",
            "Pulso rectangular | 1 if abs(x) < pi/2 else 0",
            "Tren de pulsos | 1 if (x % (2*pi/3)) < pi/3 else -1",
            
            # === ONDAS PERIÓDICAS CLÁSICAS ===
            "Onda triangular | abs(x) - pi/2",
            "Diente de sierra | x if x > 0 else x + 2*pi",
            "Sierra periódica | (x % pi) - pi/2",
            "Rectificador completo | abs(sin(x))",
            "Rectificador media onda | sin(x) if sin(x) > 0 else 0",
            
            # === COMBINACIONES ARMÓNICAS ===
            "Aprox. cuadrada (4 sen θ)/π | sin(x) + 0.5*sin(3*x) + 0.25*sin(5*x)",
            "Serie armónica | sin(x) + sin(2*x)/2 + sin(3*x)/3",
            "Armónicos impares | cos(x) - cos(3*x)/9 + cos(5*x)/25",
            
            # === SUAVES (Convergencia rápida) ===
            "Gaussiana | exp(-x**2/10)",
            "Lorentziana | 1/(1 + x**2)",
            "Cúbica centrada | x**3 - pi**2 * x",
            
            # === EXÓTICAS ===
            "Valor absoluto |x| | abs(x)",
        ]
        
        # Tema
        self.theme = "light"
        self.colors = {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "button_bg": "#4CAF50",
            "button_fg": "#ffffff"
        }
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
    def setup_styles(self):
        """Configura estilos de ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TButton', background=self.colors['button_bg'], 
                       foreground=self.colors['button_fg'])
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        style.configure('SubHeader.TLabel', font=('Arial', 12, 'bold'))
        
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== Panel superior: Entrada de datos =====
        input_frame = ttk.LabelFrame(main_frame, text="Configuración", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Fila 1: Función
        row1 = ttk.Frame(input_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="Función f(x):").pack(side=tk.LEFT, padx=5)
        self.function_entry = ttk.Entry(row1, width=30, font=('Courier', 10))
        self.function_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.function_entry.insert(0, "sin(x)")
        
        # Menú de ejemplos con más ancho para mostrar nombres descriptivos
        ttk.Label(row1, text="Ejemplos:").pack(side=tk.LEFT, padx=(20, 5))
        self.example_combo = ttk.Combobox(row1, values=self.example_functions, 
                                         width=35, state='readonly', font=('Arial', 9))
        self.example_combo.pack(side=tk.LEFT, padx=5)
        self.example_combo.bind('<<ComboboxSelected>>', self.load_example)
        
        # Fila 2: Período y términos
        row2 = ttk.Frame(input_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="Período (T):").pack(side=tk.LEFT, padx=5)
        self.period_entry = ttk.Entry(row2, width=15)
        self.period_entry.pack(side=tk.LEFT, padx=5)
        self.period_entry.insert(0, str(2*np.pi))
        
        ttk.Label(row2, text="Número de términos (N):").pack(side=tk.LEFT, padx=(20, 5))
        self.nterms_spinbox = ttk.Spinbox(row2, from_=1, to=1000, width=10)
        self.nterms_spinbox.pack(side=tk.LEFT, padx=5)
        self.nterms_spinbox.set(10)
        
        # Fila 3: Velocidad de animación (para epiciclos)
        row3 = ttk.Frame(input_frame)
        row3.pack(fill=tk.X, pady=5)
        
        ttk.Label(row3, text="🎬 Velocidad de Epiciclos:").pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.StringVar(value='normal')
        speed_frame = ttk.Frame(row3)
        speed_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(speed_frame, text="⚡ Rápido", variable=self.speed_var, 
                       value='fast').pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(speed_frame, text="▶️ Normal", variable=self.speed_var, 
                       value='normal').pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(speed_frame, text="🔍 Detallado", variable=self.speed_var, 
                       value='detailed').pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(speed_frame, text="🐌 Lento", variable=self.speed_var, 
                       value='slow').pack(side=tk.LEFT, padx=2)
        
        # Botones de acción
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="🔍 Calcular", 
                  command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 Gráfica Estática", 
                  command=self.show_static_plot).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⚪ Epiciclos (Animación)", 
                  command=self.show_epicycles).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📈 Espectro", 
                  command=self.show_spectrum).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🧮 Términos", 
                  command=self.show_terms).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Exportar", 
                  command=self.export_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Limpiar", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # ===== Panel central: Notebook con pestañas =====
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña 1: Visualización
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="📊 Visualización")
        
        # Canvas con scrollbars para matplotlib
        # Frame contenedor con scrollbars
        self.canvas_container = ttk.Frame(self.viz_frame)
        self.canvas_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear canvas con scrollbars
        self.viz_canvas = tk.Canvas(self.canvas_container, bg='white')
        self.viz_scrollbar_y = ttk.Scrollbar(self.canvas_container, orient=tk.VERTICAL, 
                                             command=self.viz_canvas.yview)
        self.viz_scrollbar_x = ttk.Scrollbar(self.canvas_container, orient=tk.HORIZONTAL, 
                                             command=self.viz_canvas.xview)
        
        self.viz_canvas.configure(yscrollcommand=self.viz_scrollbar_y.set,
                                 xscrollcommand=self.viz_scrollbar_x.set)
        
        # Empaquetar scrollbars y canvas
        self.viz_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.viz_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.viz_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame interno para los gráficos
        self.canvas_frame = ttk.Frame(self.viz_canvas)
        self.canvas_window = self.viz_canvas.create_window((0, 0), window=self.canvas_frame, 
                                                            anchor='nw')
        
        # Configurar el scroll region cuando el frame cambie de tamaño
        self.canvas_frame.bind('<Configure>', self.on_canvas_configure)
        
        # Habilitar scroll con la rueda del mouse
        self.viz_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.viz_canvas.bind_all("<Shift-MouseWheel>", self.on_shift_mousewheel)
        
        # Pestaña 2: Explicación Educativa
        self.edu_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.edu_frame, text="📚 Modo Educativo")
        
        # Botones de explicación
        edu_buttons = ttk.Frame(self.edu_frame)
        edu_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(edu_buttons, text="Ver Teoría", 
                  command=self.show_theory).pack(side=tk.LEFT, padx=5)
        ttk.Button(edu_buttons, text="Explicar a₀", 
                  command=self.explain_a0).pack(side=tk.LEFT, padx=5)
        ttk.Button(edu_buttons, text="Explicar aₙ y bₙ", 
                  command=self.explain_coefficients).pack(side=tk.LEFT, padx=5)
        ttk.Button(edu_buttons, text="Ver Resumen", 
                  command=self.show_summary).pack(side=tk.LEFT, padx=5)
        ttk.Button(edu_buttons, text="Explicación Completa", 
                  command=self.show_complete_explanation).pack(side=tk.LEFT, padx=5)
        
        # Área de texto para explicaciones
        self.explanation_text = scrolledtext.ScrolledText(
            self.edu_frame, wrap=tk.WORD, font=('Courier', 10),
            width=100, height=35
        )
        self.explanation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña 3: Coeficientes
        self.coeff_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.coeff_frame, text="📋 Coeficientes")
        
        # Crear Treeview para mostrar coeficientes
        columns = ('n', 'an', 'bn', 'magnitude')
        self.coeff_tree = ttk.Treeview(self.coeff_frame, columns=columns, 
                                       show='headings', height=20)
        
        self.coeff_tree.heading('n', text='n')
        self.coeff_tree.heading('an', text='aₙ (coseno)')
        self.coeff_tree.heading('bn', text='bₙ (seno)')
        self.coeff_tree.heading('magnitude', text='Magnitud |cₙ|')
        
        self.coeff_tree.column('n', width=80, anchor='center')
        self.coeff_tree.column('an', width=150, anchor='center')
        self.coeff_tree.column('bn', width=150, anchor='center')
        self.coeff_tree.column('magnitude', width=150, anchor='center')
        
        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(self.coeff_frame, orient=tk.VERTICAL, 
                                 command=self.coeff_tree.yview)
        self.coeff_tree.configure(yscrollcommand=scrollbar.set)
        
        self.coeff_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ===== Barra de estado =====
        self.status_bar = ttk.Label(main_frame, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
    
    def on_canvas_configure(self, event=None):
        """Actualiza el scroll region cuando el canvas cambia de tamaño"""
        self.viz_canvas.configure(scrollregion=self.viz_canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Scroll vertical con la rueda del mouse"""
        self.viz_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def on_shift_mousewheel(self, event):
        """Scroll horizontal con Shift + rueda del mouse"""
        self.viz_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def load_example(self, event=None):
        """Carga una función de ejemplo del menú desplegable"""
        selected = self.example_combo.get()
        if selected:
            # Extraer el código después del separador "|"
            if " | " in selected:
                # Formato: "Nombre descriptivo | código"
                _, code = selected.split(" | ", 1)
            else:
                # Formato antiguo (retrocompatibilidad)
                code = selected
            
            self.function_entry.delete(0, tk.END)
            self.function_entry.insert(0, code)
    
    def update_status(self, message):
        """Actualiza la barra de estado"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def calculate(self):
        """Calcula la serie de Fourier"""
        try:
            self.update_status("Calculando...")
            
            # Obtener parámetros
            function_str = self.function_entry.get().strip()
            if not function_str:
                messagebox.showerror("Error", "Por favor ingrese una función")
                return
            
            period = float(eval(self.period_entry.get()))
            n_terms = int(self.nterms_spinbox.get())
            
            # Crear solver
            self.solver = FourierSolver(function_str, period, n_terms)
            
            # Calcular coeficientes
            coeffs = self.solver.calculate_all_coefficients()
            
            # Crear objetos auxiliares
            self.explainer = FourierExplanation(self.solver)
            self.visualizer = FourierVisualizer(self.solver)
            
            # Actualizar tabla de coeficientes
            self.update_coefficients_table()
            
            # Mostrar gráfica automáticamente
            self.show_static_plot()
            
            self.update_status(f"Cálculo completado: {n_terms} términos calculados")
            messagebox.showinfo("Éxito", "Serie de Fourier calculada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")
            self.update_status("Error en el cálculo")
    
    def update_coefficients_table(self):
        """Actualiza la tabla de coeficientes"""
        # Limpiar tabla
        for item in self.coeff_tree.get_children():
            self.coeff_tree.delete(item)
        
        # Agregar a₀
        self.coeff_tree.insert('', 'end', values=(0, f"{self.solver.a0:.8f}", "0.00000000", 
                                                  f"{abs(self.solver.a0):.8f}"))
        
        # Agregar términos
        for i, (an, bn) in enumerate(zip(self.solver.an_list, self.solver.bn_list), 1):
            magnitude = np.sqrt(an**2 + bn**2)
            self.coeff_tree.insert('', 'end', values=(
                i, f"{an:.8f}", f"{bn:.8f}", f"{magnitude:.8f}"
            ))
    
    def show_static_plot(self):
        """Muestra el gráfico estático"""
        if self.solver is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular la serie")
            return
        
        try:
            self.update_status("Generando gráfico...")
            
            # Limpiar canvas anterior
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            # Crear gráfico
            fig = self.visualizer.create_static_plot(show_error=True)
            
            # Integrar con Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Agregar toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.canvas_frame)
            toolbar.update()
            
            self.notebook.select(self.viz_frame)
            self.update_status("Gráfico mostrado")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")
    
    def show_epicycles(self):
        """Muestra la animación de epiciclos (círculos de Fourier)"""
        if self.solver is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular la serie")
            return
        
        try:
            self.update_status("Generando epiciclos...")
            
            # Limpiar canvas anterior
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            # Crear animación de epiciclos con preset de velocidad
            from modules.epicycles import FourierEpicycles
            epicycles = FourierEpicycles(self.solver)
            
            # Obtener preset de velocidad del GUI
            speed_preset = self.speed_var.get()
            
            # Usar todos los términos disponibles con preset de velocidad
            fig, anim = epicycles.create_epicycles_animation(
                n_terms=self.solver.n_terms,
                speed_preset=speed_preset
            )
            self.current_animation = anim  # Guardar referencia
            
            # Integrar con Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
            
            # Frame para controles de zoom
            zoom_frame = ttk.Frame(self.canvas_frame)
            zoom_frame.pack(fill=tk.X, pady=5)
            
            # Botones de zoom
            ttk.Button(zoom_frame, text="🔍+ Acercar", 
                      command=lambda: self.zoom_plot(fig, canvas, 0.8)).pack(side=tk.LEFT, padx=5)
            ttk.Button(zoom_frame, text="🔍- Alejar", 
                      command=lambda: self.zoom_plot(fig, canvas, 1.2)).pack(side=tk.LEFT, padx=5)
            ttk.Button(zoom_frame, text="↺ Restablecer Vista", 
                      command=lambda: self.reset_zoom(fig, canvas)).pack(side=tk.LEFT, padx=5)
            
            # Guardar límites originales para reset
            ax = fig.axes[0]
            self.original_xlim = ax.get_xlim()
            self.original_ylim = ax.get_ylim()
            
            # Agregar toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.canvas_frame)
            toolbar.update()
            
            self.notebook.select(self.viz_frame)
            self.update_status("Epiciclos en reproducción - Círculos de Fourier")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar epiciclos: {str(e)}")
    
    def show_spectrum(self):
        """Muestra el espectro de frecuencias"""
        if self.solver is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular la serie")
            return
        
        try:
            self.update_status("Generando espectro...")
            
            # Limpiar canvas anterior
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            # Crear gráfico
            # Crear gráfico de espectro
            fig = self.visualizer.create_spectrum_plot()
            
            # Integrar con Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Agregar toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.canvas_frame)
            toolbar.update()
            
            self.notebook.select(self.viz_frame)
            self.update_status("Espectro mostrado")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar espectro: {str(e)}")
    
    def show_terms(self):
        """Muestra gráfico de términos individuales"""
        if self.solver is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular la serie")
            return
        
        try:
            self.update_status("Generando gráfico de términos...")
            
            # Limpiar canvas anterior
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            # Crear gráfico
            # Crear gráfico término por término
            fig = self.visualizer.create_term_by_term_plot(max_terms=6)
            
            # Integrar con Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Agregar toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.canvas_frame)
            toolbar.update()
            
            self.notebook.select(self.viz_frame)
            self.update_status("Términos mostrados")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar términos: {str(e)}")
    
    def show_theory(self):
        """Muestra la teoría básica"""
        if self.explainer is None:
            # Crear explicador genérico
            dummy_solver = FourierSolver("sin(x)", 2*np.pi, 5)
            self.explainer = FourierExplanation(dummy_solver)
        
        theory = self.explainer.explain_theory()
        self.explanation_text.delete('1.0', tk.END)
        self.explanation_text.insert('1.0', theory)
        self.notebook.select(self.edu_frame)
        self.update_status("Teoría mostrada")
    
    def explain_a0(self):
        """Explica el cálculo de a₀"""
        if self.explainer is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular la serie")
            return
        
        explanation = self.explainer.explain_a0_calculation()
        self.explanation_text.delete('1.0', tk.END)
        self.explanation_text.insert('1.0', explanation)
        self.notebook.select(self.edu_frame)
        self.update_status("Explicación de a₀ mostrada")
    
    def explain_coefficients(self):
        """Explica el cálculo de aₙ y bₙ"""
        if self.explainer is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular la serie")
            return
        
        explanation = ""
        # Mostrar los primeros 3 términos
        for n in range(1, min(4, len(self.solver.an_list) + 1)):
            explanation += self.explainer.explain_an_calculation(n) + "\n"
            explanation += self.explainer.explain_bn_calculation(n) + "\n"
        
        explanation += self.explainer.explain_symbolic_formulas()
        
        self.explanation_text.delete('1.0', tk.END)
        self.explanation_text.insert('1.0', explanation)
        self.notebook.select(self.edu_frame)
        self.update_status("Explicación de coeficientes mostrada")
    
    def show_summary(self):
        """Muestra el resumen de coeficientes"""
        if self.explainer is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular la serie")
            return
        
        summary = self.explainer.get_coefficients_summary()
        summary += "\n" + self.explainer.get_series_construction()
        
        self.explanation_text.delete('1.0', tk.END)
        self.explanation_text.insert('1.0', summary)
        self.notebook.select(self.edu_frame)
        self.update_status("Resumen mostrado")
    
    def show_complete_explanation(self):
        """Muestra la explicación completa"""
        if self.explainer is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular la serie")
            return
        
        self.update_status("Generando explicación completa...")
        explanation = self.explainer.get_complete_explanation()
        self.explanation_text.delete('1.0', tk.END)
        self.explanation_text.insert('1.0', explanation)
        self.notebook.select(self.edu_frame)
        self.update_status("Explicación completa mostrada")
    
    def export_data(self):
        """Exporta los coeficientes a un archivo"""
        if self.solver is None:
            messagebox.showwarning("Advertencia", "Primero debe calcular la serie")
            return
        
        try:
            # Pedir nombre de archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivo de texto", "*.txt"), 
                          ("CSV", "*.csv"),
                          ("Todos los archivos", "*.*")]
            )
            
            if not filename:
                return
            
            # Determinar formato
            if filename.endswith('.csv'):
                self.export_csv(filename)
            else:
                self.export_txt(filename)
            
            messagebox.showinfo("Éxito", f"Datos exportados a:\n{filename}")
            self.update_status(f"Datos exportados")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def export_txt(self, filename):
        """Exporta a archivo de texto"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("SERIE DE FOURIER - COEFICIENTES\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Función: f(x) = {self.solver.function_str}\n")
            f.write(f"Período: T = {self.solver.period}\n")
            f.write(f"Semi-período: L = {self.solver.L}\n")
            f.write(f"Términos calculados: N = {self.solver.n_terms}\n\n")
            f.write(f"a₀ = {self.solver.a0}\n\n")
            f.write("-" * 60 + "\n")
            f.write(f"{'n':>5} {'aₙ':>20} {'bₙ':>20} {'|cₙ|':>20}\n")
            f.write("-" * 60 + "\n")
            
            for i, (an, bn) in enumerate(zip(self.solver.an_list, self.solver.bn_list), 1):
                magnitude = np.sqrt(an**2 + bn**2)
                f.write(f"{i:>5} {an:>20.10f} {bn:>20.10f} {magnitude:>20.10f}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"Expresión de la serie:\n{self.solver.get_series_expression()}\n")
    
    def export_csv(self, filename):
        """Exporta a archivo CSV"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("n,an,bn,magnitude\n")
            f.write(f"0,{self.solver.a0},0.0,{abs(self.solver.a0)}\n")
            
            for i, (an, bn) in enumerate(zip(self.solver.an_list, self.solver.bn_list), 1):
                magnitude = np.sqrt(an**2 + bn**2)
                f.write(f"{i},{an},{bn},{magnitude}\n")
    
    def clear_all(self):
        """Limpia todos los datos"""
        # Limpiar canvas
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # Limpiar tabla
        for item in self.coeff_tree.get_children():
            self.coeff_tree.delete(item)
        
        # Limpiar explicación
        self.explanation_text.delete('1.0', tk.END)
        
        # Resetear objetos
        self.solver = None
        self.explainer = None
        self.visualizer = None
        self.current_animation = None
        
        self.update_status("Datos limpiados")
    
    def zoom_plot(self, fig, canvas, factor):
        """
        Aplica zoom al gráfico
        
        Args:
            fig: Figura de matplotlib
            canvas: Canvas de Tkinter
            factor: Factor de zoom (< 1 = acercar, > 1 = alejar)
        """
        ax = fig.axes[0]
        
        # Obtener límites actuales
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # Calcular centros
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        
        # Calcular nuevos rangos
        x_range = (xlim[1] - xlim[0]) * factor / 2
        y_range = (ylim[1] - ylim[0]) * factor / 2
        
        # Aplicar nuevos límites
        ax.set_xlim(x_center - x_range, x_center + x_range)
        ax.set_ylim(y_center - y_range, y_center + y_range)
        
        # Redibujar
        canvas.draw()
        self.update_status(f"Zoom aplicado: {100/factor:.0f}%")
    
    def reset_zoom(self, fig, canvas):
        """
        Restablece el zoom a la vista original
        
        Args:
            fig: Figura de matplotlib
            canvas: Canvas de Tkinter
        """
        if hasattr(self, 'original_xlim') and hasattr(self, 'original_ylim'):
            ax = fig.axes[0]
            ax.set_xlim(self.original_xlim)
            ax.set_ylim(self.original_ylim)
            canvas.draw()
            self.update_status("Vista restablecida")
        else:
            messagebox.showwarning("Advertencia", "No hay vista original guardada")


def main():
    """Función principal"""
    root = tk.Tk()
    app = FourierApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
