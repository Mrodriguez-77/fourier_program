# 🚀 GUÍA DE INICIO RÁPIDO - Visualizador de Epiciclos de Fourier# 🚀 INICIO RÁPIDO - Solucionador de Series de Fourier



## ⚡ Instalación en 3 Pasos## ⚡ Instalación Rápida (3 pasos)



### 1️⃣ Instalar Dependencias### 1️⃣ Instalar Dependencias

```powershell```powershell

.\install.bat.\install.bat

``````

O manualmente:O manualmente:

```powershell```powershell

pip install -r requirements.txtpip install -r requirements.txt

``````



### 2️⃣ Ejecutar la Aplicación### 2️⃣ Ejecutar Aplicación

```powershell```powershell

.\run.bat.\run.bat

``````

O manualmente:O manualmente:

```powershell```powershell

python main.pypython main.py

``````



### 3️⃣ (Opcional) Compilar Ejecutable### 2️⃣.5 Probar Nuevas Características (Versión 2.0) ⭐

```powershell```powershell

.\build_exe.batpython test_new_modules.py

``````

Genera `dist/FourierSolver.exe` (ejecutable independiente)Esto probará:

- 📚 Biblioteca de 12 funciones famosas

---- ⚪ Epiciclos (círculos de Fourier)

- 📊 Análisis de convergencia avanzado

## 🎯 Tu Primera Animación de Epiciclos (2 minutos)- 🔄 Comparador de funciones

- 🔢 Series de Fourier complejas

### Paso 1: Abrir la aplicación- 📖 Documentación de casos de uso

- Ejecuta `run.bat` o `python main.py`

- Verás 4 pestañas principales### 3️⃣ (Opcional) Compilar a Ejecutable

```powershell

### Paso 2: Selecciona una función espectacular.\build_exe.bat

1. En el menú desplegable, selecciona: **"Onda cuadrada (Gibbs) | 1 if x > 0 else -1"**```

2. Deja **200 términos** (valor por defecto)

3. Selecciona velocidad: **Normal**---



### Paso 3: Ver los Epiciclos## 🎯 Primera Vez - Tutorial de 2 Minutos

1. Haz clic en **"🎡 Animar Epiciclos"**

2. ¡Observa la magia! Verás:### Paso 1: Abrir la aplicación

   - 🔵 **150 círculos girando** a la izquierda- Ejecuta `run.bat` o `python main.py`

   - 💗 **Línea rosada** trazando la función

   - 📊 **Gráfica formándose** en tiempo real### Paso 2: Calcular tu primera serie

1. Deja la función predeterminada: `sin(x)`

### Paso 4: Controlar la visualización2. Haz clic en **"🔍 Calcular"**

- **Zoom +/-**: Acercar o alejar la vista3. ¡Listo! Verás la gráfica

- **Restablecer**: Volver a vista original

- **Cambiar velocidad**: Prueba "Rápido" o "Detallado"### Paso 3: Explorar

- **📊 Gráfica Estática**: Ver comparación

---- **🎬 Animar**: Ver cómo converge la serie

- **📚 Modo Educativo**: Aprender cómo se calcula

## 🎨 Funciones Recomendadas para Ver- **📋 Coeficientes**: Ver tabla de valores



### ⭐ Top 5 - Las Más Espectaculares---



1. **Onda Cuadrada con Fenómeno de Gibbs**## 📝 Funciones de Ejemplo para Probar

   ```

   1 if x > 0 else -1Copia y pega estas funciones en el campo "Función f(x)":

   ```

   - Muestra sobreimpulsos en discontinuidades### Básicas

   - Necesita muchos términos (150-200)```

sin(x)          # Función seno

2. **Diente de Sierra**cos(x)          # Función coseno

   ```x               # Función rampa

   xx**2            # Parábola

   ``````

   - Patrón visual hipnótico

   - Círculos van todos en la misma dirección### Intermedias

```

3. **Valor Absoluto**abs(x)          # Valor absoluto

   ```sign(x)         # Función signo (onda cuadrada)

   abs(x)sin(x) + cos(2*x)     # Combinación

   ``````

   - Solo círculos pares rotan

   - Simetría perfecta### Avanzadas

```

4. **Parábola Invertida**exp(-x**2/10)   # Gaussiana

   ```x**3            # Cúbica

   -x**2 + pi**2/3sin(x)*cos(x)   # Producto

   ``````

   - Círculos decrecientes rápidamente

   - Convergencia suave---



5. **Tren de Pulsos**## 🎓 Ejemplos Educativos

   ```

   1 if abs(x) < 1 else 0### Ejemplo 1: Función Seno (Fácil)

   ``````

   - Oscilaciones complejasFunción: sin(x)

   - Fenómeno de Gibbs extremoPeríodo: 6.283185307179586  (2π)

Términos: 10

---```

**Resultado**: Solo b₁ = 1, todos los demás = 0

## 🎓 Modo Educativo - Aprender Paso a Paso

---

### Ejemplo 1: Función Seno (Principiante)

```### Ejemplo 2: Onda Cuadrada (Medio)

Función: sin(x)```

Términos: 10Función: sign(x)

```Período: 6.283185307179586

1. Calcula la serie → Solo verás **1 círculo grande** girandoTérminos: 20

2. Ve a "Modo Educativo" → Lee por qué solo b₁ ≠ 0```

3. Observa: El círculo único traza perfectamente el seno**Resultado**: Solo términos impares, fenómeno de Gibbs



**Concepto**: Funciones simples = Pocos círculos---



---### Ejemplo 3: Parábola (Medio)

```

### Ejemplo 2: Onda Cuadrada (Intermedio)Función: x**2

```Período: 6.283185307179586

Función: 1 if x > 0 else -1Términos: 15

Términos: 100```

```**Resultado**: Solo términos coseno (función par)

1. Anima epiciclos → Verás **muchos círculos pequeños**

2. Observa el "overshoot" en los saltos → **Fenómeno de Gibbs**---

3. Ve al "Espectro" → Solo armónicos impares (1, 3, 5, 7...)

## ⚙️ Configuración Típica

**Concepto**: Discontinuidades requieren infinitos términos

| Parámetro | Valor Típico | Descripción |

---|-----------|--------------|-------------|

| Período | `2*pi` | Para funciones estándar |

### Ejemplo 3: Parábola (Avanzado)| Términos | `10-50` | ⚡ Balance velocidad/precisión |

```|          | `50-100` | 🎯 Alta precisión |

Función: x**2|          | `100-200` | 📈 Análisis muy detallado |

Términos: 50|          | `200-500` | 🔬 Máxima precisión (~8s) |

```

1. Mira la pestaña "Términos" → Círculos decrecen rápido---

2. Compara con "Espectro" → Magnitudes decaen como 1/n²

3. Anima con 10 términos → Ya es muy preciso## 🛠️ Solución Rápida de Problemas



**Concepto**: Funciones suaves convergen rápidamente### ❌ "Python no está instalado"

→ Instala Python 3.8+ desde https://python.org

---

### ❌ "No se puede parsear la función"

## ⚙️ Configuración Recomendada→ Usa sintaxis correcta:

- Potencias: `x**2` no `x^2`

### Para Aprendizaje Interactivo- Multiplicación: `2*x` no `2x`

| Parámetro | Valor | Por qué |

|-----------|-------|---------|### ❌ "La aproximación es mala"

| Términos | **50-100** | Balance visual/velocidad |→ Aumenta el número de términos

| Velocidad | **Normal** | Tiempo para observar detalles |

| Función | Ondas cuadradas | Efectos visuales claros |### ❌ "La app se congela"

→ Reduce el número de términos o simplifica la función

### Para Máxima Precisión

| Parámetro | Valor | Por qué |---

|-----------|-------|---------|

| Términos | **200-500** | Máxima aproximación |## 📚 Documentación Completa

| Velocidad | **Lenta** | Observar cada detalle |

| Función | Discontinuas | Muestran limitaciones |- **README.md**: Documentación general

- **docs/manual.md**: Manual completo de usuario

### Para Presentaciones- **modules/**: Código fuente comentado

| Parámetro | Valor | Por qué |

|-----------|-------|---------|---

| Términos | **100-150** | Espectacular pero fluido |

| Velocidad | **Rápida** | Dinámica visual |## ✅ Verificar Instalación

| Función | Valor absoluto, parábolas | Simétricos y claros |

Ejecuta las pruebas:

---```powershell

python test_application.py

## 🔧 Todas las Funcionalidades```



### 🎡 Pestaña Epiciclos (Principal)Si todas las pruebas pasan: ✅ Todo listo!

- **Animar Epiciclos**: Visualización de círculos rotatorios

- **Zoom**: Controles para acercar/alejar---

- **Velocidad**: 4 presets (Rápido, Normal, Detallado, Lento)

- **Info en pantalla**: N términos, círculos visibles, posición actual## 🆘 Ayuda



### 📊 Pestaña Visualización### Recursos

- **Gráfica Estática**: Compara función original vs aproximación- Lee el manual: `docs/manual.md`

- **Espectro de Frecuencias**: Magnitud de cada armónico- Ejecuta pruebas: `test_application.py`

- **Términos Individuales**: Ve cada componente por separado- Revisa ejemplos en el código



### 🎓 Pestaña Modo Educativo### Contacto

- **Teoría**: Fundamentos de Series de Fourier- Abre un issue en GitHub

- **Explicación**: Cálculo paso a paso de coeficientes- Revisa la documentación incluida

- **Resumen**: Tabla completa de valores

---

### 📋 Pestaña Coeficientes

- **Tabla completa**: Todos los valores calculados**¡Disfruta aprendiendo series de Fourier! 📐✨**

- **Exportar**: Guarda en TXT o CSV

---

## 🛠️ Solución de Problemas

### ❌ "No veo los círculos girando"
→ Asegúrate de dar clic en **"🎡 Animar Epiciclos"**  
→ Espera unos segundos mientras calcula (200 términos ~3-5s)

### ❌ "Los círculos son muy pequeños"
→ Usa el botón **"Acercar +"**  
→ O reduce el número de términos a 50-100

### ❌ "La animación va muy lenta"
→ Cambia velocidad a **"Rápida"**  
→ Reduce términos a 100 o menos

### ❌ "Error al parsear función condicional"
→ Usa formato exacto: `1 if x > 0 else -1`  
→ Espacios son importantes

### ❌ "La función no se ve bien aproximada"
→ Aumenta número de términos (150-200)  
→ Algunas funciones necesitan infinitos términos

---

## 📚 Próximos Pasos

1. **Experimenta con las 21 funciones** del menú desplegable
2. **Observa el espectro** de cada función
3. **Compara velocidades** de convergencia
4. **Lee el modo educativo** para entender la teoría
5. **Crea tus propias funciones** en el campo de texto

---

## 💡 Tips para Mejores Visualizaciones

### Para Ver Detalles
- Usa **"Velocidad: Lenta"**
- Activa **zoom +** antes de animar
- Reduce términos a 50-100

### Para Impresionar
- Usa funciones discontinuas (ondas cuadradas)
- Configura **200 términos**
- Velocidad **Normal** o **Rápida**

### Para Aprender
- Empieza con funciones simples (`sin(x)`, `cos(x)`)
- Lee el **Modo Educativo** primero
- Ve el **Espectro** para entender armónicos

---

## 📖 Recursos Adicionales

- **README.md**: Documentación completa del proyecto
- **modules/**: Código fuente con comentarios explicativos
- **21 funciones predefinidas**: Menú desplegable con descripciones

---

## ✅ Verificación de Instalación

Prueba rápida para verificar que todo funciona:

```powershell
python main.py
```

1. Selecciona "sin(x)" del menú
2. Clic en "Calcular"
3. Clic en "Animar Epiciclos"

Si ves un círculo grande girando y trazando una onda → ✅ **¡Todo funciona!**

---

**¡Disfruta explorando las Series de Fourier visualmente! 🎡📐✨**
