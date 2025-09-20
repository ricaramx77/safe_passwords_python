# --- Conversor de monedas y unidades físicas ---
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import requests

# API gratuita para tasas de cambio (ejemplo: exchangerate-api.com)
API_URL = 'https://open.er-api.com/v6/latest/'

UNIDADES_FISICAS = {
    'Longitud': {
        'Metro': 1.0,
        'Centímetro': 0.01,
        'Milímetro': 0.001,
        'Kilómetro': 1000.0,
        'Pulgada': 0.0254,
        'Pie': 0.3048,
        'Yarda': 0.9144,
        'Milla': 1609.34
    },
    'Masa': {
        'Kilogramo': 1.0,
        'Gramo': 0.001,
        'Miligramo': 0.000001,
        'Libra': 0.453592,
        'Onza': 0.0283495,
        'Tonelada': 1000.0
    }
}

def obtener_tasas(moneda_base):
    try:
        resp = requests.get(API_URL + moneda_base, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if data.get('result') == 'success':
            return data['rates']
        else:
            raise Exception('Respuesta inválida de la API')
    except Exception as e:
        return {'error': str(e)}

def convertir_moneda(cantidad, moneda_origen, moneda_destino):
    tasas = obtener_tasas(moneda_origen)
    if 'error' in tasas:
        return None, tasas['error']
    if moneda_destino not in tasas:
        return None, f'Tasa para {moneda_destino} no disponible.'
    try:
        resultado = cantidad * tasas[moneda_destino]
        return resultado, None
    except Exception as e:
        return None, str(e)

def convertir_unidad(cantidad, tipo, unidad_origen, unidad_destino):
    try:
        base = cantidad * UNIDADES_FISICAS[tipo][unidad_origen]
        resultado = base / UNIDADES_FISICAS[tipo][unidad_destino]
        return resultado, None
    except Exception as e:
        return None, str(e)

def mostrar_conversor():
    conv = tk.Toplevel(root)
    conv.title('Conversor de Unidades y Monedas')
    conv.geometry('430x350')
    conv.resizable(False, False)

    tab_control = ttk.Notebook(conv)
    tab_monedas = ttk.Frame(tab_control)
    tab_unidades = ttk.Frame(tab_control)
    tab_control.add(tab_monedas, text='Monedas')
    tab_control.add(tab_unidades, text='Unidades Físicas')
    tab_control.pack(expand=1, fill='both')

    # --- Tab de monedas ---
    ttk.Label(tab_monedas, text='Cantidad:').grid(column=0, row=0, sticky='w', padx=5, pady=5)
    cantidad_m_var = tk.StringVar(value='1')
    ttk.Entry(tab_monedas, textvariable=cantidad_m_var, width=10).grid(column=1, row=0, sticky='w')

    ttk.Label(tab_monedas, text='De:').grid(column=0, row=1, sticky='w', padx=5)
    moneda_origen_var = tk.StringVar(value='USD')
    ttk.Entry(tab_monedas, textvariable=moneda_origen_var, width=6).grid(column=1, row=1, sticky='w')

    ttk.Label(tab_monedas, text='A:').grid(column=0, row=2, sticky='w', padx=5)
    moneda_destino_var = tk.StringVar(value='MXN')
    ttk.Entry(tab_monedas, textvariable=moneda_destino_var, width=6).grid(column=1, row=2, sticky='w')

    resultado_m_var = tk.StringVar()
    ttk.Label(tab_monedas, text='Resultado:').grid(column=0, row=3, sticky='w', padx=5, pady=5)
    ttk.Entry(tab_monedas, textvariable=resultado_m_var, width=20, font=('Consolas', 12)).grid(column=1, row=3, sticky='w')

    def convertir_monedas_cmd():
        try:
            cantidad = float(cantidad_m_var.get())
        except ValueError:
            messagebox.showerror('Error', 'Cantidad inválida.')
            return
        origen = moneda_origen_var.get().upper()
        destino = moneda_destino_var.get().upper()
        resultado, error = convertir_moneda(cantidad, origen, destino)
        if error:
            messagebox.showerror('Error', error)
            resultado_m_var.set('')
        else:
            resultado_m_var.set(f'{resultado:.4f}')

    ttk.Button(tab_monedas, text='Convertir', command=convertir_monedas_cmd).grid(column=0, row=4, columnspan=2, pady=10)

    # --- Tab de unidades físicas ---
    ttk.Label(tab_unidades, text='Tipo:').grid(column=0, row=0, sticky='w', padx=5, pady=5)
    tipo_var = tk.StringVar(value='Longitud')
    tipo_menu = ttk.Combobox(tab_unidades, textvariable=tipo_var, values=list(UNIDADES_FISICAS.keys()), state='readonly')
    tipo_menu.grid(column=1, row=0, sticky='w')

    ttk.Label(tab_unidades, text='Cantidad:').grid(column=0, row=1, sticky='w', padx=5)
    cantidad_u_var = tk.StringVar(value='1')
    ttk.Entry(tab_unidades, textvariable=cantidad_u_var, width=10).grid(column=1, row=1, sticky='w')

    ttk.Label(tab_unidades, text='De:').grid(column=0, row=2, sticky='w', padx=5)
    unidad_origen_var = tk.StringVar()
    unidad_origen_menu = ttk.Combobox(tab_unidades, textvariable=unidad_origen_var, state='readonly')
    unidad_origen_menu.grid(column=1, row=2, sticky='w')

    ttk.Label(tab_unidades, text='A:').grid(column=0, row=3, sticky='w', padx=5)
    unidad_destino_var = tk.StringVar()
    unidad_destino_menu = ttk.Combobox(tab_unidades, textvariable=unidad_destino_var, state='readonly')
    unidad_destino_menu.grid(column=1, row=3, sticky='w')

    resultado_u_var = tk.StringVar()
    ttk.Label(tab_unidades, text='Resultado:').grid(column=0, row=4, sticky='w', padx=5, pady=5)
    ttk.Entry(tab_unidades, textvariable=resultado_u_var, width=20, font=('Consolas', 12)).grid(column=1, row=4, sticky='w')

    def actualizar_unidades(*args):
        tipo = tipo_var.get()
        unidades = list(UNIDADES_FISICAS[tipo].keys())
        unidad_origen_menu['values'] = unidades
        unidad_destino_menu['values'] = unidades
        if unidades:
            unidad_origen_var.set(unidades[0])
            unidad_destino_var.set(unidades[1] if len(unidades) > 1 else unidades[0])

    tipo_var.trace('w', actualizar_unidades)
    actualizar_unidades()

    def convertir_unidades_cmd():
        try:
            cantidad = float(cantidad_u_var.get())
        except ValueError:
            messagebox.showerror('Error', 'Cantidad inválida.')
            return
        tipo = tipo_var.get()
        origen = unidad_origen_var.get()
        destino = unidad_destino_var.get()
        resultado, error = convertir_unidad(cantidad, tipo, origen, destino)
        if error:
            messagebox.showerror('Error', error)
            resultado_u_var.set('')
        else:
            resultado_u_var.set(f'{resultado:.4f}')

    ttk.Button(tab_unidades, text='Convertir', command=convertir_unidades_cmd).grid(column=0, row=5, columnspan=2, pady=10)

# --- Botón para abrir el conversor en la ventana principal ---
def main():
    global root, mainframe
    root = tk.Tk()
    root.title('Generador de Contraseñas Seguras')
    root.geometry('400x250')
    root.resizable(False, False)

    mainframe = ttk.Frame(root, padding='15')
    mainframe.pack(fill='both', expand=True)

    # --- Widgets del generador de contraseñas ---
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

    resultado_var = tk.StringVar()

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

    generar_btn = ttk.Button(mainframe, text='Generar contraseña', command=generar_y_mostrar)
    generar_btn.grid(column=0, row=3, columnspan=2, pady=10)

    resultado_entry = ttk.Entry(mainframe, textvariable=resultado_var, width=30, font=('Consolas', 12))
    resultado_entry.grid(column=0, row=4, columnspan=2, pady=5)

    copiar_btn = ttk.Button(mainframe, text='Copiar', command=copiar_contraseña)
    copiar_btn.grid(column=0, row=5, columnspan=2)

    # --- Botón para abrir el conversor en la ventana principal ---
    ttk.Button(mainframe, text='Conversor de Unidades/Monedas', command=mostrar_conversor).grid(column=0, row=6, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
