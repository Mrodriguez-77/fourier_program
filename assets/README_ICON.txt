# Nota sobre el ícono

Para generar un ícono personalizado para tu aplicación, puedes:

1. **Usar un generador online**:
   - Visita https://www.icoconverter.com/
   - Sube una imagen PNG (preferiblemente 256x256 px)
   - Descarga el archivo .ico generado
   - Guárdalo como `icon.ico` en esta carpeta

2. **Usar Pillow (Python)**:
   ```python
   from PIL import Image
   img = Image.open('tu_imagen.png')
   img.save('icon.ico', format='ICO', sizes=[(256,256)])
   ```

3. **Usar un ícono de biblioteca gratuita**:
   - https://icons8.com/
   - https://www.flaticon.com/
   - https://fontawesome.com/

Por ahora, el build_exe.bat funcionará sin ícono (PyInstaller usará uno por defecto).
Si quieres usar un ícono personalizado, simplemente colócalo aquí como `icon.ico`.

## Ícono Sugerido

Un diseño que represente:
- Una onda sinusoidal
- Símbolo matemático (π, Σ)
- Gráfico de frecuencias
- Colores: Azul/Verde (matemáticas/ciencia)
