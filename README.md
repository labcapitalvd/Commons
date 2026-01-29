# Repo de Commons
Este repo contiene el sistema de autenticación así como algunas utilidades prácticas para proyectos de python. A continuación se describe su estructura:

- Sistema de autenticación basado en Fastapi
- Utilidades de db como conectores asíncronos a Postgres y unidades de trabajo para SQLAlchemy.
- Modelos a manera de abstracciones de tablas de cara a ORM.
- Esquemas a manera de abstracciones para la API.
- Utilidades de:
    - Encriptación
    - Almacenamiento de archivos
    - Hashing y validación de único
    - Logging
    - Limpieza de texto
    - Tokens y JWT.

Se recomienda el uso de algunas herramientas para facilitar el correcto funcionamiento de las herramientas.

- Crear un .venv en la raiz del proyecto.
- Contar con una herramienta de instalación de paquetes que soporte proyectos y no solo requirements.txt.
- Contar con direnv instalado en la máquina para gestión segura de secretos y con un keyring para su almacenamiento encriptado.
- No cambiar las rutas raiz de las utilidades.

