# Explorador del Índice de Innovación Pública 🏛️

Este repositorio contiene la documentación para la aplicación svelte diseñada para explorar, entender y puntuar las respuestas de las entidades del sector público al **Índice de Innovación Pública**. La aplicación permite al equipo de evaluación analizar y comparar la información reportada por las entidades, así como sus respuestas a las preguntas principales y las preguntas detalladas del índice.

## Desarrollado por
1. @SpanishHans

## Funcionalidades principales 🚀

1. **Selección de entidades y preguntas**
   - El usuario puede seleccionar una o varias entidades públicas y una pregunta específica para analizar cómo respondieron.
   - La información incluye:
     - Preguntas raíz y preguntas detalladas.
     - Datos disponibles para cada medición del índice gracias al sistema de selección por año.

   ### Ejemplo de pregunta raíz:
   ¿Su entidad encontró retos de innovación entre 2023 y 2024?
   Si la respuesta es "Sí", ¿cuáles?

Para cada reto identificado, se recopilan datos como:
- Nombre corto del reto.
- Descripción detallada.
- Canal por el cual fue identificado.
- Actores involucrados.

2. **Exploración de resultados**
- Permite visualizar las respuestas y puntuaciones para cualquier entidad del sector público.
- Incluye análisis por índice, entidad, y periodo de medición.

3. **Histórico de mediciones**
- Navegación y consulta de datos a través de los distintos años en los que se ha realizado el índice.

## Cómo usar la aplicación 📋

1. **Configuración inicial**
- Clonar este repositorio:
  ```bash
  git clone https://github.com/usuario/explorador-indice-innovacion.git
  cd explorador-indice-innovacion
  ```
- Instalar las dependencias requeridas:
  ```bash
  pip install -r requirements.txt
  ```

2. **Ejecutar la aplicación**
- Ejecutar el servidor local:
  ```bash
  python app.py
  ```
- Abrir el navegador en `http://127.0.0.1:8050/`.

3. **Navegación en la app**
- Selecciona el año del índice en la parte superior.
- Filtra por entidad(es) pública(s).
- Explora las preguntas raíz y sus respuestas detalladas.
- Visualiza y analiza resultados históricos.

## Estructura del proyecto 🗂️

```plaintext
├── app.py                  # Archivo principal para ejecutar la aplicación Dash.
├── assets/                 # Archivos estáticos (CSS, imágenes, etc.).
├── data/                   # Datos del índice (en formato CSV, JSON, etc.).
├── components/             # Componentes Dash personalizados.
├── requirements.txt        # Dependencias de Python.
└── README.md               # Documentación del proyecto.

# Contribución 🤝

¡Siempre estamos abiertos a mejoras!
Si encuentras algún problema o tienes una idea, por favor abre un issue o envía un pull request.

# Licencia 📜

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
# Visualizador-HUB
