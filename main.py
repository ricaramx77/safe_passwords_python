# Generador de contraseñas seguras con interfaz tkinter
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

def generar_contraseña(longitud, usar_simbolos, usar_mayusculas):
    caracteres = string.ascii_lowercase
    if usar_mayusculas:
        caracteres += string.ascii_uppercase
    caracteres += string.digits
    if usar_simbolos:
        caracteres += string.punctuation
    if not caracteres:
        return ''
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def copiar_al_portapapeles(texto):
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()

def generar_y_mostrar():
    try:
        longitud = int(longitud_var.get())
        if longitud < 4:
            messagebox.showwarning('Advertencia', 'La longitud mínima es 4.')
            return
    except ValueError:
        messagebox.showerror('Error', 'Introduce un número válido para la longitud.')
        return
    usar_simbolos = simbolos_var.get()
    usar_mayusculas = mayusculas_var.get()
    contraseña = generar_contraseña(longitud, usar_simbolos, usar_mayusculas)
    resultado_var.set(contraseña)

def copiar_contraseña():
    contraseña = resultado_var.get()
    if contraseña:
        copiar_al_portapapeles(contraseña)
        messagebox.showinfo('Copiado', '¡Contraseña copiada al portapapeles!')
    else:
        messagebox.showwarning('Advertencia', 'No hay contraseña para copiar.')

# Interfaz gráfica
root = tk.Tk()
root.title('Generador de Contraseñas Seguras')
root.geometry('400x250')
root.resizable(False, False)

mainframe = ttk.Frame(root, padding='15')
mainframe.pack(fill='both', expand=True)

ttk.Label(mainframe, text='Longitud de la contraseña:').grid(column=0, row=0, sticky='w')
longitud_var = tk.StringVar(value='12')
longitud_entry = ttk.Entry(mainframe, textvariable=longitud_var, width=5)
longitud_entry.grid(column=1, row=0, sticky='w')

simbolos_var = tk.BooleanVar(value=True)
simbolos_check = ttk.Checkbutton(mainframe, text='Incluir símbolos', variable=simbolos_var)
simbolos_check.grid(column=0, row=1, columnspan=2, sticky='w')

mayusculas_var = tk.BooleanVar(value=True)
mayusculas_check = ttk.Checkbutton(mainframe, text='Incluir mayúsculas', variable=mayusculas_var)
mayusculas_check.grid(column=0, row=2, columnspan=2, sticky='w')

generar_btn = ttk.Button(mainframe, text='Generar contraseña', command=generar_y_mostrar)
generar_btn.grid(column=0, row=3, columnspan=2, pady=10)

resultado_var = tk.StringVar()
resultado_entry = ttk.Entry(mainframe, textvariable=resultado_var, width=30, font=('Consolas', 12))
resultado_entry.grid(column=0, row=4, columnspan=2, pady=5)

copiar_btn = ttk.Button(mainframe, text='Copiar', command=copiar_contraseña)
copiar_btn.grid(column=0, row=5, columnspan=2)

root.mainloop()

