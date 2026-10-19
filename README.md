# Lista de tareas

Aplicación de escritorio para gestionar tareas pendientes y completadas, hecha en Python con `tkinter`.

## Características

- Agregar tareas con el botón **Agregar tarea**
- Clic derecho sobre una tarea para:
  - Marcarla como completada (pasa a la lista de completadas)
  - Editar su nombre
  - Borrarla (con confirmación)
- Clic derecho sobre una tarea completada para volver a pendientes
- Botón **Limpiar completadas** para vaciar esa lista (con confirmación)
- Las tareas se guardan automáticamente en `tareas.json` y se conservan al cerrar el programa

## Descargar el ejecutable

Para Windows no necesitas tener Python instalado. Descarga `lista_tareas.exe` desde la sección [Releases](https://github.com/elaptopsito/lista-tareas/releases) y ábrelo con doble clic.

El archivo `tareas.json` se crea en la misma carpeta donde está el ejecutable.

## Ejecutar desde el código fuente

Requisitos: Python 3.10 o superior.

```bash
git clone https://github.com/elaptopsito/lista-tareas.git
cd lista-tareas
python lista_tareas.py
```

`tkinter` viene incluido con Python, así que no hace falta instalar nada más.

## Generar el ejecutable

```bash
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed lista_tareas.py
```

El resultado queda en `dist/lista_tareas.exe`.

## Aviso de seguridad

Windows Defender o SmartScreen pueden advertir sobre el ejecutable porque no tiene firma digital. Es un falso positivo común en programas generados con PyInstaller.

## Autor

elaptopsito