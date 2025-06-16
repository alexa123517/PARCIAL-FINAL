import tkinter as tk
from tkinter import ttk, messagebox

class SistemaRestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Restaurante")
        self.root.geometry("850x650")
        
        self.productos = [
            {"id": 1, "nombre": "Hamburguesa", "precio": 8.99, "cantidad": 50},
            {"id": 2, "nombre": "Pizza", "precio": 10.99, "cantidad": 30},
            {"id": 3, "nombre": "Perro Caliente", "precio": 6.50, "cantidad": 25}
        ]
        
        self.comandas = []
        self.ventas = []  # Aquí guardamos cada venta como {"nombre": "Pizza", "precio": 10.99}

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.tab_pos = ttk.Frame(self.notebook)
        self.tab_comandas = ttk.Frame(self.notebook)
        self.tab_inventario = ttk.Frame(self.notebook)
        self.tab_reporte = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_pos, text="POS")
        self.notebook.add(self.tab_comandas, text="Comandas")
        self.notebook.add(self.tab_inventario, text="Inventario")
        self.notebook.add(self.tab_reporte, text="Reporte de Ventas")

        self.crear_interfaz_pos()
        self.crear_interfaz_comandas()
        self.crear_interfaz_inventario()
        self.crear_interfaz_reporte()

    def crear_interfaz_pos(self):
        self.tree_productos = ttk.Treeview(self.tab_pos, columns=('nombre', 'precio'), show='headings')
        self.tree_productos.heading('nombre', text='Producto')
        self.tree_productos.heading('precio', text='Precio')
        self.tree_productos.pack(fill='both', expand=True, padx=10, pady=10)
        
        btn_agregar = tk.Button(self.tab_pos, text="Agregar a Comanda", command=self.agregar_a_comanda)
        btn_agregar.pack(pady=5)
        
        self.actualizar_lista_productos()

    def crear_interfaz_comandas(self):
        self.tree_comandas = ttk.Treeview(self.tab_comandas, columns=('mesa', 'items'), show='headings')
        self.tree_comandas.heading('mesa', text='Mesa')
        self.tree_comandas.heading('items', text='Items')
        self.tree_comandas.pack(fill='both', expand=True, padx=10, pady=10)
        
        btn_completar = tk.Button(self.tab_comandas, text="Marcar como Completado", command=self.marcar_completado)
        btn_completar.pack(pady=5)

    def crear_interfaz_inventario(self):
        self.tree_inventario = ttk.Treeview(self.tab_inventario, columns=('nombre', 'cantidad'), show='headings')
        self.tree_inventario.heading('nombre', text='Producto')
        self.tree_inventario.heading('cantidad', text='Cantidad')
        self.tree_inventario.pack(fill='both', expand=True, padx=10, pady=10)
        self.actualizar_inventario()

    def crear_interfaz_reporte(self):
        self.tree_reporte = ttk.Treeview(self.tab_reporte, columns=('producto', 'cantidad', 'total'), show='headings')
        self.tree_reporte.heading('producto', text='Producto')
        self.tree_reporte.heading('cantidad', text='Unidades Vendidas')
        self.tree_reporte.heading('total', text='Total Vendido ($)')
        self.tree_reporte.pack(fill='both', expand=True, padx=10, pady=10)

        btn_generar = tk.Button(self.tab_reporte, text="Generar Reporte", command=self.generar_reporte_ventas)
        btn_generar.pack(pady=5)

    def actualizar_lista_productos(self):
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        for producto in self.productos:
            self.tree_productos.insert('', 'end', values=(producto['nombre'], f"${producto['precio']:.2f}"))

    def agregar_a_comanda(self):
        seleccionado = self.tree_productos.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un producto primero")
            return

        producto_info = self.tree_productos.item(seleccionado)['values']
        nombre_producto = producto_info[0]

        for producto in self.productos:
            if producto["nombre"] == nombre_producto:
                if producto["cantidad"] <= 0:
                    messagebox.showerror("Sin stock", f"No hay unidades disponibles de {nombre_producto}")
                    return

                producto["cantidad"] -= 1
                venta = {"nombre": producto["nombre"], "precio": producto["precio"]}
                self.ventas.append(venta)  # Guardar venta
                nueva_comanda = {
                    "mesa": 1,
                    "items": [venta]
                }
                self.comandas.append(nueva_comanda)
                messagebox.showinfo("Éxito", f"Producto {producto['nombre']} agregado a comanda")

                self.actualizar_comandas()
                self.actualizar_inventario()
                return

    def actualizar_comandas(self):
        for item in self.tree_comandas.get_children():
            self.tree_comandas.delete(item)
        for comanda in self.comandas:
            items = ", ".join([item['nombre'] for item in comanda['items']])
            self.tree_comandas.insert('', 'end', values=(comanda['mesa'], items))

    def marcar_completado(self):
        seleccionado = self.tree_comandas.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona una comanda primero")
            return

        comanda = self.tree_comandas.item(seleccionado)['values']
        self.comandas = [c for c in self.comandas if c['mesa'] != comanda[0]]
        messagebox.showinfo("Éxito", f"Comanda de mesa {comanda[0]} completada")
        self.actualizar_comandas()

    def actualizar_inventario(self):
        for item in self.tree_inventario.get_children():
            self.tree_inventario.delete(item)
        for producto in self.productos:
            self.tree_inventario.insert('', 'end', values=(producto['nombre'], producto['cantidad']))

    def generar_reporte_ventas(self):
        resumen = {}
        for venta in self.ventas:
            nombre = venta['nombre']
            precio = venta['precio']
            if nombre not in resumen:
                resumen[nombre] = {'cantidad': 0, 'total': 0.0}
            resumen[nombre]['cantidad'] += 1
            resumen[nombre]['total'] += precio

        for item in self.tree_reporte.get_children():
            self.tree_reporte.delete(item)
        for nombre, datos in resumen.items():
            self.tree_reporte.insert('', 'end', values=(nombre, datos['cantidad'], f"${datos['total']:.2f}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaRestauranteApp(root)
    root.mainloop()

