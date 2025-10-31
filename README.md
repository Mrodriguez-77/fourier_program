# 📐 Visualizador de Series de Fourier con Epiciclos

Aplicación educativa de escritorio para visualizar y comprender las Series de Fourier a través de epiciclos rotatorios y análisis matemático interactivo.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 ¿Qué hace este programa?

Este programa permite **visualizar geométricamente** cómo las Series de Fourier descomponen funciones periódicas en sumas de senos y cosenos. La característica principal es la visualización mediante **epiciclos**: círculos rotatorios cuya suma vectorial reconstruye la función original.

### ✨ Características Principales

1. **🎡 Visualización de Epiciclos Animados**
   - Cada término de la serie se representa como un círculo rotatorio
   - Los círculos giran a velocidades que son múltiplos de la frecuencia fundamental
   - La suma vectorial de todos los círculos traza la función en tiempo real
   - Hasta 150 círculos simultáneos visualizables

2. **📊 Cálculo Matemático**
   - Calcula automáticamente los coeficientes de Fourier (a₀, aₙ, bₙ)
   - Detección automática de simetría (par/impar/media onda) para optimización
   - Base de datos de series conocidas con fórmulas exactas
   - Soporte para funciones condicionales: `1 if x > 0 else -1`

3. **📈 Análisis y Visualización**
   - Gráfica comparativa entre función original y aproximación
   - Espectro de frecuencias mostrando magnitud de cada armónico
   - Análisis de convergencia y términos individuales
   - Visualización del fenómeno de Gibbs en discontinuidades

4. **🎓 Modo Educativo**
   - Explicaciones paso a paso del cálculo de coeficientes
   - Teoría matemática de series de Fourier
   - Detección y explicación del fenómeno de Gibbs
   - Recomendador inteligente de parámetros según complejidad

## 🔬 Fundamentos Matemáticos

### Teorema de Fourier

Cualquier función periódica f(x) con período T puede descomponerse en una suma infinita de senos y cosenos:

```
f(x) = a₀/2 + Σ[aₙcos(nπx/L) + bₙsin(nπx/L)]
```

donde `L = T/2` (semi-período)

### Coeficientes de Fourier

Los coeficientes se calculan mediante las integrales:

```
a₀ = (1/L) ∫₋ₗᴸ f(x) dx                    [Valor promedio]

aₙ = (1/L) ∫₋ₗᴸ f(x)·cos(nπx/L) dx        [Componentes coseno]

bₙ = (1/L) ∫₋ₗᴸ f(x)·sin(nπx/L) dx        [Componentes seno]
```

### Interpretación Geométrica (Epiciclos)

- **Círculo n-ésimo**: Radio = √(aₙ² + bₙ²), Frecuencia angular = nω
- **Fase inicial**: θₙ = arctan(bₙ/aₙ)
- **Suma vectorial**: La punta del último círculo traza f(x)

**Matemáticamente:**
```
Posición del círculo n:
  x(t) = rₙ·cos(nωt + θₙ)
  y(t) = rₙ·sin(nωt + θₙ)

Suma de todos los círculos = f(t)
```

### Optimizaciones Matemáticas Implementadas

1. **Detección de Simetría**
   - **Función PAR**: f(-x) = f(x) → Solo términos coseno (bₙ = 0)
   - **Función IMPAR**: f(-x) = -f(x) → Solo términos seno (aₙ = 0)
   - **Media onda**: f(x + T/2) = -f(x) → Solo armónicos impares

2. **Series Conocidas**
   - sin(x), cos(x), abs(x), x² → Fórmulas analíticas exactas

3. **Fenómeno de Gibbs**
   - Sobrepico inevitable del ~9% cerca de discontinuidades
   - No desaparece con más términos, solo se concentra

## 📝 Ejemplos de Funciones

| Función | Tipo | Coeficientes Dominantes | Fenómeno Notable |
|---------|------|------------------------|------------------|
| `sin(x)` | Impar | b₁ = 1, resto = 0 | Serie exacta |
| `cos(x)` | Par | a₁ = 1, resto = 0 | Serie exacta |
| `abs(x)` | Par | Solo aₙ pares | Convergencia rápida |
| `1 if x > 0 else -1` | Impar | Solo bₙ impares | Fenómeno de Gibbs |
| `x` | Impar | bₙ = (-1)ⁿ⁺¹·2/n | Diente de sierra |
| `x**2` | Par | Solo aₙ | Parábola periódica |

## � Aplicaciones Educativas

- **Física**: Análisis de ondas, vibraciones y oscilaciones
- **Ingeniería**: Procesamiento de señales y análisis de frecuencias
- **Matemáticas**: Comprensión visual de series trigonométricas
- **Música**: Análisis de armónicos en sonidos
- **Procesamiento de imágenes**: Compresión y filtrado de frecuencias

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

---

Ver **[QUICKSTART.md](QUICKSTART.md)** para guía de instalación y uso.

**¡Explora el fascinante mundo de las Series de Fourier! 📐✨**
