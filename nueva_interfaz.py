import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox
from mysql.connector import Error


def connect_to_realestatedb():
    """Conectar a la base de datos RealEstateDB"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='RealEstateDB',
            user='root',  # Cambia por tu usuario
            password='password'  # Cambia por tu contraseña
        )
        print("✅ Conectado a RealEstateDB")
        return connection
    except Error as e:
        print(f"❌ Error conectando a RealEstateDB: {e}")
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
        return None


# FUNCIONES PARA PROPIEDADES (Tab 1)
def insert_property():
    """Insertar nueva propiedad"""
    direccion = adress.get().strip()
    precio_str = price.get().strip()

    # Validaciones
    if not direccion:
        messagebox.showwarning("Campo vacío", "Por favor ingresa la dirección de la propiedad")
        return
    if not precio_str:
        messagebox.showwarning("Campo vacío", "Por favor ingresa el precio de la propiedad")
        return

    try:
        precio = float(precio_str)
    except ValueError:
        messagebox.showwarning("Precio inválido", "Por favor ingresa un precio válido")
        return

    connection = connect_to_realestatedb()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Properties (Address, Price) VALUES (%s, %s)"
            cursor.execute(query, (direccion, precio))
            connection.commit()
            messagebox.showinfo("Éxito", f"Propiedad insertada correctamente con ID: {cursor.lastrowid}")
            limpiar_campos_propiedades()
            refresh_properties_table()
        except Error as e:
            messagebox.showerror("Error", f"No se pudo insertar la propiedad: {e}")
        finally:
            cursor.close()
            connection.close()


def update_property():
    """Actualizar propiedad existente"""
    property_id = propertyID.get().strip()
    direccion = adress.get().strip()
    precio_str = price.get().strip()

    if not property_id:
        messagebox.showwarning("Campo vacío", "Por favor ingresa el PropertyID para actualizar")
        return

    try:
        property_id_int = int(property_id)
        precio = float(precio_str) if precio_str else None
    except ValueError:
        messagebox.showwarning("ID inválido", "Por favor ingresa un PropertyID válido")
        return

    connection = connect_to_realestatedb()
    if connection:
        try:
            cursor = connection.cursor()

            # Construir query dinámicamente basado en los campos llenados
            updates = []
            params = []

            if direccion:
                updates.append("Address = %s")
                params.append(direccion)
            if precio_str:
                updates.append("Price = %s")
                params.append(precio)

            if not updates:
                messagebox.showwarning("Sin cambios", "No hay campos para actualizar")
                return

            params.append(property_id_int)
            query = f"UPDATE Properties SET {', '.join(updates)} WHERE PropertyID = %s"

            cursor.execute(query, params)
            connection.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Propiedad actualizada correctamente")
                limpiar_campos_propiedades()
                refresh_properties_table()
            else:
                messagebox.showwarning("No encontrado", "No se encontró ninguna propiedad con ese ID")

        except Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar la propiedad: {e}")
        finally:
            cursor.close()
            connection.close()


def delete_property():
    """Eliminar propiedad"""
    property_id = propertyID.get().strip()

    if not property_id:
        messagebox.showwarning("Campo vacío", "Por favor ingresa el PropertyID para eliminar")
        return

    try:
        property_id_int = int(property_id)
    except ValueError:
        messagebox.showwarning("ID inválido", "Por favor ingresa un PropertyID válido")
        return

    # Confirmar eliminación
    respuesta = messagebox.askyesno("Confirmar eliminación",
                                    f"¿Estás seguro de que quieres eliminar la propiedad con ID {property_id}?")
    if not respuesta:
        return

    connection = connect_to_realestatedb()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM Properties WHERE PropertyID = %s"
            cursor.execute(query, (property_id_int,))
            connection.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Propiedad eliminada correctamente")
                limpiar_campos_propiedades()
                refresh_properties_table()
            else:
                messagebox.showwarning("No encontrado", "No se encontró ninguna propiedad con ese ID")

        except Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar la propiedad: {e}")
        finally:
            cursor.close()
            connection.close()


def search_property():
    """Buscar propiedad por ID"""
    property_id = propertyID.get().strip()

    if not property_id:
        messagebox.showwarning("Campo vacío", "Por favor ingresa el PropertyID para buscar")
        return

    try:
        property_id_int = int(property_id)
    except ValueError:
        messagebox.showwarning("ID inválido", "Por favor ingresa un PropertyID válido")
        return

    connection = connect_to_realestatedb()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM Properties WHERE PropertyID = %s"
            cursor.execute(query, (property_id_int,))
            propiedad = cursor.fetchone()

            if propiedad:
                # Llenar los campos con los datos encontrados
                adress.delete(0, tk.END)
                adress.insert(0, propiedad[1])
                price.delete(0, tk.END)
                price.insert(0, str(propiedad[2]))
                messagebox.showinfo("Encontrado", "Propiedad encontrada y cargada en el formulario")
            else:
                messagebox.showwarning("No encontrado", "No se encontró ninguna propiedad con ese ID")

        except Error as e:
            messagebox.showerror("Error", f"No se pudo buscar la propiedad: {e}")
        finally:
            cursor.close()
            connection.close()


def limpiar_campos_propiedades():
    """Limpiar campos de propiedades"""
    propertyID.delete(0, tk.END)
    adress.delete(0, tk.END)
    price.delete(0, tk.END)


def refresh_properties_table():
    """Actualizar tabla de propiedades"""
    connection = connect_to_realestatedb()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT PropertyID, Address, Price FROM Properties")
            propiedades = cursor.fetchall()

            # Limpiar tabla
            for item in properties_tree.get_children():
                properties_tree.delete(item)

            # Insertar nuevos datos
            for propiedad in propiedades:
                properties_tree.insert("", tk.END, values=propiedad)

        except Error as e:
            print(f"Error al refrescar tabla: {e}")
        finally:
            cursor.close()
            connection.close()


# FUNCIONES SIMILARES PARA LAS OTRAS TABLAS (debes implementarlas)
def insert_agent():
    """Insertar nuevo agente"""
    nombre = agent_name.get().strip()
    telefono = agent_phone.get().strip()

    if not nombre or not telefono:
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos")
        return

    connection = connect_to_realestatedb()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Agents (Name, Phone) VALUES (%s, %s)"
            cursor.execute(query, (nombre, telefono))
            connection.commit()
            messagebox.showinfo("Éxito", f"Agente insertado correctamente con ID: {cursor.lastrowid}")
            limpiar_campos_agentes()
            refresh_agents_table()
        except Error as e:
            messagebox.showerror("Error", f"No se pudo insertar el agente: {e}")
        finally:
            cursor.close()
            connection.close()


# ... Implementa funciones similares para update_agent, delete_agent, search_agent, etc.

def limpiar_campos_agentes():
    """Limpiar campos de agentes"""
    agent_id.delete(0, tk.END)
    agent_name.delete(0, tk.END)
    agent_phone.delete(0, tk.END)


def refresh_agents_table():
    """Actualizar tabla de agentes"""
    connection = connect_to_realestatedb()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT AgentID, Name, Phone FROM Agents")
            agentes = cursor.fetchall()

            for item in agents_tree.get_children():
                agents_tree.delete(item)

            for agente in agentes:
                agents_tree.insert("", tk.END, values=agente)

        except Error as e:
            print(f"Error al refrescar tabla agentes: {e}")
        finally:
            cursor.close()
            connection.close()


# Configuración de la ventana principal
root = tk.Tk()
root.geometry('1000x700')
root.title("Sistema de Gestión Inmobiliaria")

# Crear el widget Notebook (pestañas)
notebook = ttk.Notebook(root)

# Crear los frames que irán dentro de las pestañas
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab5 = ttk.Frame(notebook)

# Añadir las pestañas al Notebook
notebook.add(tab1, text="Propiedades")
notebook.add(tab2, text="Agentes")
notebook.add(tab3, text="Clientes")
notebook.add(tab4, text="Ventas")
notebook.add(tab5, text="Oficinas")

notebook.pack(expand=True, fill="both")

# CONTENIDO DE LA PESTAÑA 1 (PROPIEDADES)
titulo = tk.Label(tab1, text="Gestión de Propiedades", font=("Times New Roman", 16, "bold"), fg="black")
titulo.pack(pady=10)

# Frame para contener el formulario y la tabla
main_frame = tk.Frame(tab1)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Frame para el formulario
form_frame = tk.LabelFrame(main_frame, text="Formulario de Propiedades", font=("Arial", 12))
form_frame.pack(fill="x", pady=(0, 10))

# Fila 1: PropertyID
tk.Label(form_frame, text="PropertyID:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)
propertyID = tk.Entry(form_frame, width=20, font=("Arial", 10))
propertyID.grid(row=0, column=1, sticky="w", pady=5, padx=(0, 10))

# Fila 2: Address
tk.Label(form_frame, text="Address:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
adress = tk.Entry(form_frame, width=50, font=("Arial", 10))
adress.grid(row=1, column=1, sticky="w", pady=5, padx=(0, 10), columnspan=3)

# Fila 3: Price
tk.Label(form_frame, text="Price:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=(10, 5), pady=5)
price = tk.Entry(form_frame, width=20, font=("Arial", 10))
price.grid(row=2, column=1, sticky="w", pady=5, padx=(0, 10))

# Frame para botones de propiedades
button_frame = tk.Frame(form_frame)
button_frame.grid(row=3, column=0, columnspan=4, pady=10)

# Botones de acción para propiedades
btn_search = tk.Button(button_frame, text="Buscar", font=("Arial", 10), bg="#FFC107", width=10, command=search_property)
btn_search.pack(side=tk.LEFT, padx=2)

btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10,
                     command=insert_property)
btn_save.pack(side=tk.LEFT, padx=2)

btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10,
                       command=update_property)
btn_update.pack(side=tk.LEFT, padx=2)

btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10,
                       command=delete_property)
btn_delete.pack(side=tk.LEFT, padx=2)

btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 10), bg="#FF9800", fg="white", width=10,
                      command=limpiar_campos_propiedades)
btn_clear.pack(side=tk.LEFT, padx=2)

# Frame para la tabla de propiedades
table_frame = tk.LabelFrame(main_frame, text="Lista de Propiedades", font=("Arial", 12))
table_frame.pack(fill="both", expand=True)

# Treeview para mostrar propiedades
columns = ("ID", "Dirección", "Precio")
properties_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

# Configurar columnas
properties_tree.heading("ID", text="ID")
properties_tree.heading("Dirección", text="Dirección")
properties_tree.heading("Precio", text="Precio")

properties_tree.column("ID", width=80)
properties_tree.column("Dirección", width=400)
properties_tree.column("Precio", width=100)

# Scrollbar para la tabla
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=properties_tree.yview)
properties_tree.configure(yscrollcommand=scrollbar.set)

properties_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
scrollbar.pack(side="right", fill="y", pady=10)

# CONTENIDO DE LA PESTAÑA 2 (AGENTES) - Similar estructura
titulo2 = tk.Label(tab2, text="Gestión de Agentes", font=("Arial", 16, "bold"), fg="green")
titulo2.pack(pady=10)

main_frame2 = tk.Frame(tab2)
main_frame2.pack(fill="both", expand=True, padx=20, pady=10)

form_frame2 = tk.LabelFrame(main_frame2, text="Formulario de Agentes", font=("Arial", 12))
form_frame2.pack(fill="x", pady=(0, 10))

# Campos para agentes
tk.Label(form_frame2, text="AgentID:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)
agent_id = tk.Entry(form_frame2, width=20, font=("Arial", 10))
agent_id.grid(row=0, column=1, sticky="w", pady=5, padx=(0, 10))

tk.Label(form_frame2, text="Name:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
agent_name = tk.Entry(form_frame2, width=30, font=("Arial", 10))
agent_name.grid(row=1, column=1, sticky="w", pady=5, padx=(0, 10))

tk.Label(form_frame2, text="Phone:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=(10, 5), pady=5)
agent_phone = tk.Entry(form_frame2, width=20, font=("Arial", 10))
agent_phone.grid(row=2, column=1, sticky="w", pady=5, padx=(0, 10))

# Botones para agentes (debes conectar las funciones)
button_frame2 = tk.Frame(form_frame2)
button_frame2.grid(row=3, column=0, columnspan=4, pady=10)

btn_search2 = tk.Button(button_frame2, text="Buscar", font=("Arial", 10), bg="#FFC107", width=10)
btn_search2.pack(side=tk.LEFT, padx=2)

btn_save2 = tk.Button(button_frame2, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10,
                      command=insert_agent)
btn_save2.pack(side=tk.LEFT, padx=2)

btn_update2 = tk.Button(button_frame2, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
btn_update2.pack(side=tk.LEFT, padx=2)

btn_delete2 = tk.Button(button_frame2, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
btn_delete2.pack(side=tk.LEFT, padx=2)

btn_clear2 = tk.Button(button_frame2, text="Limpiar", font=("Arial", 10), bg="#FF9800", fg="white", width=10,
                       command=limpiar_campos_agentes)
btn_clear2.pack(side=tk.LEFT, padx=2)

# Tabla para agentes
table_frame2 = tk.LabelFrame(main_frame2, text="Lista de Agentes", font=("Arial", 12))
table_frame2.pack(fill="both", expand=True)

columns2 = ("ID", "Nombre", "Teléfono")
agents_tree = ttk.Treeview(table_frame2, columns=columns2, show="headings", height=12)

agents_tree.heading("ID", text="ID")
agents_tree.heading("Nombre", text="Nombre")
agents_tree.heading("Teléfono", text="Teléfono")

agents_tree.column("ID", width=80)
agents_tree.column("Nombre", width=200)
agents_tree.column("Teléfono", width=150)

scrollbar2 = ttk.Scrollbar(table_frame2, orient="vertical", command=agents_tree.yview)
agents_tree.configure(yscrollcommand=scrollbar2.set)

agents_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
scrollbar2.pack(side="right", fill="y", pady=10)

# ... Continúa con las demás pestañas (Clientes, Ventas, Oficinas) con estructura similar

# Cargar datos iniciales
root.after(100, refresh_properties_table)
root.after(100, refresh_agents_table)

root.mainloop()