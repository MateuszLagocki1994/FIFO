import tkinter as tk
from tkinter import messagebox

class WarehouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Magazyn Towarów - FIFO")

        # Inicjalizacja danych magazynu
        self.stock = []  # Lista przechowująca partie dostaw (FIFO)
        self.documents_pz = []  # Lista dokumentów PZ
        self.documents_wz = []  # Lista dokumentów WZ

        # Elementy GUI
        tk.Label(root, text="Magazyn Towarów", font=("Helvetica", 16)).pack(pady=10)

        # Dodawanie dostawy
        tk.Label(root, text="Dodaj dostawę").pack(anchor="w", padx=10)
        tk.Label(root, text="Nazwa produktu:").pack(anchor="w", padx=20)
        self.product_name_entry = tk.Entry(root, width=30)
        self.product_name_entry.pack(padx=20, pady=5)

        tk.Label(root, text="Ilość:").pack(anchor="w", padx=20)
        self.quantity_entry = tk.Entry(root, width=30)
        self.quantity_entry.pack(padx=20, pady=5)

        tk.Label(root, text="Cena zakupu:").pack(anchor="w", padx=20)
        self.price_entry = tk.Entry(root, width=30)
        self.price_entry.pack(padx=20, pady=5)

        tk.Button(root, text="Dodaj dostawę", command=self.add_delivery).pack(pady=10)

        # Wydawanie towaru
        tk.Label(root, text="Wydaj towar").pack(anchor="w", padx=10)
        tk.Label(root, text="Nazwa produktu:").pack(anchor="w", padx=20)
        self.issue_product_name_entry = tk.Entry(root, width=30)
        self.issue_product_name_entry.pack(padx=20, pady=5)

        tk.Label(root, text="Ilość:").pack(anchor="w", padx=20)
        self.issue_quantity_entry = tk.Entry(root, width=30)
        self.issue_quantity_entry.pack(padx=20, pady=5)

        tk.Button(root, text="Wydaj towar", command=self.issue_goods).pack(pady=10)

        # Wyświetlanie stanu magazynu
        tk.Button(root, text="Pokaż stan magazynu", command=self.current_stock).pack(pady=10)
        tk.Button(root, text="Pokaż wartość magazynu", command=self.stock_value).pack(pady=10)

        # Pole tekstowe na wyniki
        self.output_text = tk.Text(root, height=15, width=60)
        self.output_text.pack(pady=10)

    def add_delivery(self):
        """Dodanie nowej partii dostawy (PZ)."""
        product_name = self.product_name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        if not product_name or not quantity or not price:
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Błąd", "Ilość i cena muszą być liczbami.")
            return

        self.stock.append({
            'product_name': product_name,
            'quantity': quantity,
            'purchase_price': price
        })
        self.documents_pz.append({
            'product_name': product_name,
            'quantity': quantity,
            'purchase_price': price
        })

        self.output_text.insert(tk.END, f"Dodano dostawę: {product_name}, ilość: {quantity}, cena: {price}\n")
        self.clear_entries()

    def issue_goods(self):
        """Wydanie towaru zgodnie z zasadą FIFO (WZ)."""
        product_name = self.issue_product_name_entry.get().strip()
        quantity = self.issue_quantity_entry.get().strip()

        if not product_name or not quantity:
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Błąd", "Ilość musi być liczbą.")
            return

        issued_quantity = 0
        total_value = 0
        issued_batches = []

        for batch in self.stock:
            if batch['product_name'] == product_name and quantity > 0:
                if batch['quantity'] <= quantity:
                    issued_quantity += batch['quantity']
                    total_value += batch['quantity'] * batch['purchase_price']
                    issued_batches.append(batch)
                    quantity -= batch['quantity']
                else:
                    issued_quantity += quantity
                    total_value += quantity * batch['purchase_price']
                    batch['quantity'] -= quantity
                    issued_batches.append({
                        'product_name': product_name,
                        'quantity': quantity,
                        'purchase_price': batch['purchase_price']
                    })
                    quantity = 0

        for batch in issued_batches:
            if batch in self.stock:
                self.stock.remove(batch)

        if issued_quantity > 0:
            self.documents_wz.append({
                'product_name': product_name,
                'quantity': issued_quantity,
                'total_value': total_value
            })
            self.output_text.insert(tk.END, f"Wydano towar: {product_name}, ilość: {issued_quantity}, wartość: {total_value}\n")
        else:
            self.output_text.insert(tk.END, "Brak wystarczającej ilości towaru w magazynie.\n")

        self.clear_entries()

    def current_stock(self):
        """Wyświetlenie bieżącego stanu magazynu."""
        self.output_text.insert(tk.END, "Bieżący stan magazynu:\n")
        for batch in self.stock:
            self.output_text.insert(tk.END, f"Produkt: {batch['product_name']}, Ilość: {batch['quantity']}, Cena zakupu: {batch['purchase_price']}\n")

    def stock_value(self):
        """Obliczenie łącznej wartości magazynu."""
        total_value = sum(batch['quantity'] * batch['purchase_price'] for batch in self.stock)
        self.output_text.insert(tk.END, f"Łączna wartość magazynu: {total_value}\n")

    def clear_entries(self):
        """Czyszczenie pól wejściowych."""
        self.product_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.issue_product_name_entry.delete(0, tk.END)
        self.issue_quantity_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()
