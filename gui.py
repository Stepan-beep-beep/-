import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from config import *
from database import Database

class HomeInventoryGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        self.db = Database()
        
        self.setup_ui()
        
        self.load_materials()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        self.create_title()
        self.create_input_frame()
        self.create_operation_frame()
        self.create_search_frame()
        self.create_table()
        self.create_info_label()
    
    def create_title(self):
        title_label = tk.Label(
            self.root,
            text=UI_TEXTS['title'],
            font=FONTS['title'],
            fg=COLORS['title']
        )
        title_label.pack(pady=10)
    
    def create_input_frame(self):
        input_frame = tk.LabelFrame(
            self.root,
            text=UI_TEXTS['input_frame'],
            padx=10,
            pady=10,
            font=FONTS['label_bold']
        )
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row1 = tk.Frame(input_frame)
        row1.pack(fill=tk.X, pady=5)
        
        tk.Label(row1, text=UI_TEXTS['name_label'], font=FONTS['label']).pack(
            side=tk.LEFT, padx=5
        )
        self.name_entry = tk.Entry(row1, width=25, font=FONTS['entry'])
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(row1, text=UI_TEXTS['unit_label'], font=FONTS['label']).pack(
            side=tk.LEFT, padx=5
        )
        self.unit_entry = tk.Entry(row1, width=8, font=FONTS['entry'])
        self.unit_entry.pack(side=tk.LEFT, padx=5)
        self.unit_entry.insert(0, DEFAULT_UNIT)
        
        tk.Label(row1, text=UI_TEXTS['quantity_label'], font=FONTS['label']).pack(
            side=tk.LEFT, padx=5
        )
        self.quantity_entry = tk.Entry(row1, width=8, font=FONTS['entry'])
        self.quantity_entry.pack(side=tk.LEFT, padx=5)
        
        # Вторая строка - примечание
        row2 = tk.Frame(input_frame)
        row2.pack(fill=tk.X, pady=5)
        
        tk.Label(row2, text=UI_TEXTS['note_label'], font=FONTS['label']).pack(
            side=tk.LEFT, padx=5
        )
        self.note_entry = tk.Entry(row2, width=60, font=FONTS['entry'])
        self.note_entry.pack(side=tk.LEFT, padx=5)

        self.create_input_buttons(input_frame)
    
    def create_input_buttons(self, parent):
        button_frame = tk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(
            button_frame,
            text=UI_TEXTS['add_btn'],
            command=self.add_material,
            bg=COLORS['add_button'],
            fg="white",
            font=FONTS['button'],
            width=15,
            height=1
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text=UI_TEXTS['update_btn'],
            command=self.update_material,
            bg=COLORS['update_button'],
            fg="white",
            font=FONTS['button'],
            width=15,
            height=1
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text=UI_TEXTS['delete_btn'],
            command=self.delete_material,
            bg=COLORS['delete_button'],
            fg="white",
            font=FONTS['button'],
            width=15,
            height=1
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text=UI_TEXTS['clear_btn'],
            command=self.clear_fields,
            bg=COLORS['clear_button'],
            fg="white",
            font=FONTS['button_small'],
            width=15,
            height=1
        ).pack(side=tk.LEFT, padx=5)
    
    def create_operation_frame(self):
        op_frame = tk.LabelFrame(
            self.root,
            text=UI_TEXTS['operation_frame'],
            padx=10,
            pady=10,
            font=FONTS['label_bold']
        )
        op_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            op_frame,
            text=UI_TEXTS['quantity_label'],
            font=FONTS['label']
        ).pack(side=tk.LEFT, padx=5)
        
        self.op_quantity_entry = tk.Entry(op_frame, width=10, font=FONTS['entry'])
        self.op_quantity_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            op_frame,
            text=UI_TEXTS['income_btn'],
            command=self.add_quantity,
            bg=COLORS['income_button'],
            fg="white",
            font=FONTS['button_small'],
            width=12
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            op_frame,
            text=UI_TEXTS['expense_btn'],
            command=self.remove_quantity,
            bg=COLORS['expense_button'],
            fg="white",
            font=FONTS['button_small'],
            width=12
        ).pack(side=tk.LEFT, padx=10)
    
    def create_search_frame(self):
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            search_frame,
            text=UI_TEXTS['search_label'],
            font=FONTS['label']
        ).pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, width=30, font=FONTS['entry'])
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_materials)
        
        tk.Button(
            search_frame,
            text=UI_TEXTS['refresh_btn'],
            command=self.load_materials,
            font=FONTS['button_small']
        ).pack(side=tk.RIGHT, padx=5)
    
    def create_table(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = tuple(TABLE_COLUMNS.keys())
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=12
        )
        
        for key, text in TABLE_COLUMNS.items():
            self.tree.heading(key, text=text)
        
        self.tree.column('name', width=200)
        self.tree.column('quantity', width=100)
        self.tree.column('unit', width=80)
        self.tree.column('note', width=250)
        
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<ButtonRelease-1>', self.on_select)
    
    def create_info_label(self):
        self.info_label = tk.Label(
            self.root,
            text="",
            font=FONTS['info'],
            fg=COLORS['info_text']
        )
        self.info_label.pack(pady=5)
    
    def add_material(self):
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get()
        unit = self.unit_entry.get().strip()
        note = self.note_entry.get().strip()
        
        if not name:
            messagebox.showerror("Ошибка", ERROR_MESSAGES['empty_name'])
            return
        
        try:
            quantity = int(quantity) if quantity else 0
        except ValueError:
            messagebox.showerror("Ошибка", ERROR_MESSAGES['invalid_quantity'])
            return
        
        if not unit:
            unit = DEFAULT_UNIT
        
        try:
            self.db.add_material(name, quantity, unit, note)
            messagebox.showinfo("Успех", SUCCESS_MESSAGES['added'].format(name))
            self.clear_fields()
            self.load_materials()
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Ошибка",
                ERROR_MESSAGES['already_exists'].format(name)
            )
    
    def update_material(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", ERROR_MESSAGES['select_material'])
            return
        
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get()
        unit = self.unit_entry.get().strip()
        note = self.note_entry.get().strip()
        
        if not name:
            messagebox.showerror("Ошибка", ERROR_MESSAGES['empty_name'])
            return
        
        try:
            quantity = int(quantity) if quantity else 0
        except ValueError:
            messagebox.showerror("Ошибка", ERROR_MESSAGES['invalid_quantity'])
            return
        
        if not unit:
            unit = DEFAULT_UNIT
        
        old_name = self.tree.item(selected[0])['values'][0]
        
        try:
            self.db.update_material(old_name, name, quantity, unit, note)
            messagebox.showinfo("Успех", SUCCESS_MESSAGES['updated'].format(name))
            self.clear_fields()
            self.load_materials()
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Ошибка",
                ERROR_MESSAGES['already_exists'].format(name)
            )
    
    def delete_material(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", ERROR_MESSAGES['select_material'])
            return
        
        name = self.tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno(
            "Подтверждение",
            f"Вы уверены, что хотите удалить '{name}'?"
        ):
            self.db.delete_material(name)
            messagebox.showinfo("Успех", SUCCESS_MESSAGES['deleted'].format(name))
            self.clear_fields()
            self.load_materials()
    
    def add_quantity(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", ERROR_MESSAGES['select_material'])
            return
        
        try:
            quantity = int(self.op_quantity_entry.get())
            if quantity <= 0:
                messagebox.showerror("Ошибка", ERROR_MESSAGES['positive_quantity'])
                return
        except ValueError:
            messagebox.showerror("Ошибка", ERROR_MESSAGES['invalid_quantity'])
            return
        
        name = self.tree.item(selected[0])['values'][0]
        new_qty = self.db.update_quantity(name, quantity)
        
        messagebox.showinfo(
            "Успех",
            SUCCESS_MESSAGES['income'].format(quantity, name)
        )
        self.op_quantity_entry.delete(0, tk.END)
        self.load_materials()
    
    def remove_quantity(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", ERROR_MESSAGES['select_material'])
            return
        
        try:
            quantity = int(self.op_quantity_entry.get())
            if quantity <= 0:
                messagebox.showerror("Ошибка", ERROR_MESSAGES['positive_quantity'])
                return
        except ValueError:
            messagebox.showerror("Ошибка", ERROR_MESSAGES['invalid_quantity'])
            return
        
        name = self.tree.item(selected[0])['values'][0]
        current_qty = self.db.get_current_quantity(name)
        
        if quantity > current_qty:
            messagebox.showerror(
                "Ошибка",
                ERROR_MESSAGES['not_enough'].format(current_qty)
            )
            return
        
        new_qty = self.db.update_quantity(name, -quantity)
        
        messagebox.showinfo(
            "Успех",
            SUCCESS_MESSAGES['expense'].format(quantity, name)
        )
        self.op_quantity_entry.delete(0, tk.END)
        self.load_materials()
        
        if self.db.check_low_stock(name, new_qty):
            messagebox.showwarning(
                "Внимание",
                ERROR_MESSAGES['low_stock'].format(name, new_qty)
            )
    
    def load_materials(self):

        for item in self.tree.get_children():
            self.tree.delete(item)
        
        materials = self.db.get_all_materials()
        
        for material in materials:
            name, quantity, unit, note = material
            self.tree.insert(
                '',
                tk.END,
                values=(name, quantity, unit, note if note else '')
            )
        
        self.update_info_label()
    
    def search_materials(self, event=None):
        search_term = self.search_entry.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if search_term:
            materials = self.db.search_materials(search_term)
        else:
            materials = self.db.get_all_materials()
        
        for material in materials:
            name, quantity, unit, note = material
            self.tree.insert(
                '',
                tk.END,
                values=(name, quantity, unit, note if note else '')
            )
        
        self.update_info_label()
    
    def update_info_label(self):
        total_items, total_quantity = self.db.get_statistics()
        total_items = total_items if total_items else 0
        total_quantity = total_quantity if total_quantity else 0
        
        self.info_label.config(
            text=f"Всего позиций: {total_items} | Общее количество: {total_quantity} ед."
        )
    
    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            
            self.clear_fields()
            self.name_entry.insert(0, values[0])
            self.quantity_entry.insert(0, values[1])
            self.unit_entry.insert(0, values[2])
            if values[3]:
                self.note_entry.insert(0, values[3])
    
    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.unit_entry.delete(0, tk.END)
        self.unit_entry.insert(0, DEFAULT_UNIT)
        self.note_entry.delete(0, tk.END)
        self.op_quantity_entry.delete(0, tk.END)
    
    def on_closing(self):
        self.db.close()
        self.root.destroy()