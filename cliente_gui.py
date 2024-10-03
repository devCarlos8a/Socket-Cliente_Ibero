import socket
import tkinter as tk
import threading

# Configuraciones del servidor
direccion_del_Servidor = 'localhost'
puerto_Servidor = 8080

# Variable para almacenar la conexión del cliente
cliente_socket = None

# Función para iniciar la conexión del cliente en un hilo separado
def iniciar_cliente():
    global cliente_socket

    try:
        # Creación del socket
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((direccion_del_Servidor, puerto_Servidor))
        label_estado.config(text="Conectado al servidor.", fg="green")
        boton_conectar.config(state=tk.DISABLED)  # Deshabilitar botón "Conectar"
        boton_desconectar.config(state=tk.NORMAL)  # Habilitar botón "Desconectar"
    except Exception as e:
        label_estado.config(text=f"Error de conexión: {e}", fg="red")
        return

    recibir_respuesta()

# Función para desconectar del servidor
def desconectar_cliente():
    global cliente_socket
    if cliente_socket:
        cliente_socket.sendall("salir".encode('utf-8'))  # Enviar comando "salir" al servidor
        cliente_socket.close()  # Cerrar el socket del cliente
        cliente_socket = None
        label_estado.config(text="Desconectado del servidor.", fg="red")
        boton_conectar.config(state=tk.NORMAL)  # Habilitar botón "Conectar"
        boton_desconectar.config(state=tk.DISABLED)  # Deshabilitar botón "Desconectar"
        entry_mensaje.config(state=tk.DISABLED)  # Deshabilitar envío de mensajes

# Función para enviar el documento al servidor
def enviar_documento():
    documento = entry_documento.get()
    if cliente_socket:
        cliente_socket.sendall(documento.encode('utf-8'))
        entry_documento.delete(0, tk.END)  # Limpiar el campo de entrada

# Función para recibir respuesta del servidor
def recibir_respuesta():
    while True:
        try:
            respuesta = cliente_socket.recv(1024).decode('utf-8')
            if respuesta:
                actualizar_respuesta_servidor(f"Servidor: {respuesta}")

                # Si la respuesta indica que el acceso fue concedido, habilitar el campo de mensaje
                if "Sesión abierta" in respuesta:
                    habilitar_envio_mensajes()

            if "Sesión cerrada" in respuesta or not respuesta:
                actualizar_respuesta_servidor("Conexión cerrada.")
                cliente_socket.close()
                break
        except:
            actualizar_respuesta_servidor("Error en la conexión.")
            break

# Función para enviar un mensaje al servidor
def enviar_mensaje():
    mensaje = entry_mensaje.get()
    if cliente_socket:
        cliente_socket.sendall(mensaje.encode('utf-8'))  # Enviar el mensaje al servidor
        entry_mensaje.delete(0, tk.END)  # Limpiar el campo de entrada

# Función para actualizar la etiqueta con la respuesta del servidor
def actualizar_respuesta_servidor(mensaje):
    label_respuesta.config(text=mensaje)

# Función para habilitar el envío de mensajes después de la validación del documento
def habilitar_envio_mensajes():
    entry_mensaje.config(state=tk.NORMAL)  # Habilitar el campo de mensaje
    boton_enviar_mensaje.config(state=tk.NORMAL)  # Habilitar el botón de enviar mensaje
    actualizar_respuesta_servidor("Acceso autorizado. Ahora puedes enviar mensajes.")

# Función para iniciar el cliente en un hilo para no bloquear la GUI
def iniciar_cliente_en_hilo():
    hilo_cliente = threading.Thread(target=iniciar_cliente)
    hilo_cliente.start()

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Cliente GUI")
root.geometry("400x350")

# Etiqueta para el estado de la conexión
label_estado = tk.Label(root, text="Desconectado", fg="red")
label_estado.pack(pady=10)

# Entrada para el documento
entry_documento = tk.Entry(root, width=50)
entry_documento.pack(pady=10)

# Botón para enviar el documento
boton_enviar_documento = tk.Button(root, text="Enviar ID de Acceso", command=enviar_documento)
boton_enviar_documento.pack(pady=10)

# Entrada para enviar mensajes (inicialmente deshabilitada)
entry_mensaje = tk.Entry(root, width=50, state=tk.DISABLED)
entry_mensaje.pack(pady=10)

# Botón para enviar mensaje (inicialmente deshabilitado)
boton_enviar_mensaje = tk.Button(root, text="Enviar Mensaje", command=enviar_mensaje, state=tk.DISABLED)
boton_enviar_mensaje.pack(pady=10)

# Etiqueta para mostrar la respuesta del servidor
label_respuesta = tk.Label(root, text="Respuesta del servidor aparecerá aquí")
label_respuesta.pack(pady=10)

# Botón para conectar al servidor
boton_conectar = tk.Button(root, text="Conectar al Servidor", command=iniciar_cliente_en_hilo)
boton_conectar.pack(pady=10)

# Botón para desconectar del servidor (inicialmente deshabilitado)
boton_desconectar = tk.Button(root, text="Desconectar del Servidor", command=desconectar_cliente, state=tk.DISABLED)
boton_desconectar.pack(pady=10)

# Iniciar la interfaz gráfica
root.mainloop()



