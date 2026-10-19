import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path
import json
import sys

if getattr(sys, "frozen", False):
    CARPETA_BASE = Path(sys.executable).resolve().parent
else:
    CARPETA_BASE = Path(__file__).resolve().parent
ARCHIVO_TAREAS = CARPETA_BASE / "tareas.json"

#Listas de tareas pendientes y completadas
pendientes = []
completadas = []

def cargar_tareas():
    """Cargar las tareas de la última ejecución desde un archivo."""
    if not ARCHIVO_TAREAS.exists():
        return [], []
    try:
        with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return datos.get("pendientes", []), datos.get("completadas", [])        
    except (json.JSONDecodeError, IOError):
        messagebox.showwarning("Error", "No se pudo cargar la lista de tareas. Se inicia con las listas vacía", parent=ventana)
        return [], []

def guardar_tareas():
    """Guardar las tareas en un archivo."""
    datos = {"pendientes": pendientes, "completadas": completadas}
    with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def agregar_tarea():
    """Agregar una nueva tarea a la lista."""
    texto = simpledialog.askstring("Agregar tarea", "Ingrese la nueva tarea:", parent=ventana)

    if texto is None:
        return

    texto = texto.strip()
    if texto == "":
        messagebox.showwarning("Campo vaciío", "Debes ingresar una tarea", parent=ventana)
        return

    pendientes.append(texto)
    guardar_tareas()
    refrescar_listas()    

def eliminar_tarea():
    """Eliminar una tarea seleccionada de una de las listas."""
    i = indice_seleccionado.get()
    lista_datos = pendientes if origen_actual.get() == "pendientes" else completadas
    if messagebox.askyesno("Borrar", f"Borrar '{lista_datos[i]}'?", parent=ventana):
        del lista_datos[i]
        guardar_tareas()
        refrescar_listas()

def reactivar_tarea():
    """Reactivar una tarea completada y moverla a la lista de pendientes."""
    i = indice_seleccionado.get()
    texto = completadas.pop(i)
    pendientes.append(texto)
    guardar_tareas()
    refrescar_listas()

def refrescar_listas():
    """Refrescar las listas en la interfaz."""
    lista_pendientes.delete(0, tk.END)
    for texto in pendientes:
        lista_pendientes.insert(tk.END, texto)

    lista_completadas.delete(0, tk.END)
    for texto in completadas:
        lista_completadas.insert(tk.END, texto) 

def limpiar_completadas():
    """Eliminar todas las tareas completadas."""
    if messagebox.askyesno("Limpiar lista de completadas", "Limpiar tareas completadas?", parent=ventana):
        completadas.clear()
        guardar_tareas()
        refrescar_listas()  

def editar_tarea():
    """Editar una tarea existente. Ya sea una completada o una pendiente"""
    i = indice_seleccionado.get()
    lista_datos = pendientes if origen_actual.get() == "pendientes" else completadas
    nuevo = simpledialog.askstring(
        "Editar tarea", "Ingrese la nueva descripción de la tarea:",
        initialvalue=lista_datos[i], parent=ventana
    )
    if nuevo is None:
        return
    if nuevo == "":
        messagebox.showwarning("Campo vacío", "Debes ingresar una tarea", parent=ventana)
        return
    lista_datos[i] = nuevo
    guardar_tareas()
    refrescar_listas()

def marcar_como_completada():
    """Marcar una tarea como completada."""
    i = indice_seleccionado.get()
    texto = pendientes.pop(i)
    completadas.append(texto)
    guardar_tareas()
    refrescar_listas()

def mostrar_menu(event, lista_origen):
    """Mostrar el menu al hacer click derecho sobre una tarea"""
    indice = lista_origen.nearest(event.y)
    if indice < 0 or indice >= lista_origen.size():
        return

    lista_origen.selection_clear(0, tk.END)
    lista_origen.selection_set(indice)

    origen_actual.set("pendientes" if lista_origen is lista_pendientes else "completadas")
    indice_seleccionado.set(indice)

    menu_pendiente.tk_popup(event.x_root, event.y_root) if lista_origen is lista_pendientes \
        else menu_completada.tk_popup(event.x_root, event.y_root)

#Creamos la ventana
ventana = tk.Tk()
ventana.title("Task manager")
ventana.geometry("400x500")

indice_seleccionado = tk.IntVar(value=-1)
origen_actual = tk.StringVar(value="")

#Cabecera de las tareas pendientes y el boton para agregar tareas
cabecera_pendientes = tk.Frame(ventana, padx=10, pady=10, bg="blue")
cabecera_pendientes.pack(side="top", fill="x")

boton_agregar = tk.Button(cabecera_pendientes, text="Agregar tarea", font=("Arial", 12), command=agregar_tarea)
boton_agregar.pack(side="right")

# Cuerpo de la lista de tareas pendientes
cuerpo_pendientes = tk.Frame(ventana, padx=10, pady=5, bg="red")
cuerpo_pendientes.pack(side="top", fill="both", expand=True)

tk.Label(cuerpo_pendientes, text="Tareas pendientes", font=("Arial", 12, "bold")).pack(anchor="w")
lista_pendientes = tk.Listbox(cuerpo_pendientes, font=("Arial", 14))
lista_pendientes.pack(fill="both", expand=True)
lista_pendientes.bind("<Button-3>", lambda event: mostrar_menu(event, lista_pendientes))

# Cuerpo y cabecera de la lista de tareas completadas
cuerpo_completadas = tk.Frame(ventana, padx=10, pady=5, bg="green")
cuerpo_completadas.pack(side="top", fill="both", expand=True)

cabecera_completadas = tk.Frame(cuerpo_completadas)
cabecera_completadas.pack(fill="x")
tk.Label(cabecera_completadas, text="Completadas", font=("Arial", 14, "bold")).pack(side="left")
tk.Button(cabecera_completadas, text="Limpiar completadas", command=limpiar_completadas).pack(side="right")

lista_completadas = tk.Listbox(cuerpo_completadas, font=("Arial", 14))
lista_completadas.pack(fill="both", expand=True)
lista_completadas.bind("<Button-3>", lambda event: mostrar_menu(event, lista_completadas))

# Menú contextual para tareas pendientes y otro para tareas completadas
menu_pendiente = tk.Menu(ventana, tearoff=0)
menu_pendiente.add_command(label="Marcar como completada", command=marcar_como_completada)
menu_pendiente.add_command(label="Editar tarea", command=editar_tarea)
menu_pendiente.add_separator()
menu_pendiente.add_command(label="Eliminar", command=eliminar_tarea)

menu_completada = tk.Menu(ventana, tearoff=0)
menu_completada.add_command(label="Volver a pendientes", command=reactivar_tarea)
menu_completada.add_command(label="Editar tarea", command=editar_tarea)
menu_completada.add_separator()
menu_completada.add_command(label="Eliminar", command=eliminar_tarea)

#Carga inicial
pendientes, completadas = cargar_tareas()
refrescar_listas()

ventana.mainloop()