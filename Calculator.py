import tkinter as tk
import math
from tkinter import messagebox

def tambah(x: float, y: float) -> float:
    """Menjumlahkan dua angka."""
    return x + y

def kurang(x: float, y: float) -> float:
    """Mengurangi dua angka."""
    return x - y

def kali(x: float, y: float) -> float:
    """Mengalikan dua angka."""
    return x * y

def bagi(x: float, y: float) -> float:
    """Membagi dua angka. Menangani pembagian dengan nol."""
    if y == 0:
        raise ValueError("Kesalahan: Tidak dapat membagi dengan nol!")
    return x / y

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Python")
        self.root.geometry("550x550")
        self.root.resizable(False, False)

        self.result_var = tk.StringVar()
        
        # Layar Tampilan
        entry = tk.Entry(root, textvariable=self.result_var, font=('Arial', 20), bd=10, insertwidth=4, width=14, borderwidth=4, justify='right')
        entry.grid(row=0, column=0, columnspan=4, pady=20)

        # Panel Riwayat
        tk.Label(root, text="Riwayat Perhitungan", font=('Arial', 10, 'bold')).grid(row=0, column=4, padx=10)
        self.history_listbox = tk.Listbox(root, font=('Arial', 10), width=30, height=22)
        self.history_listbox.grid(row=1, column=4, rowspan=6, padx=10, pady=5, sticky='nsew')
        self.history_listbox.bind('<Double-1>', self.on_history_double_click)

        # Definisi Tombol
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
            '^', 'sqrt', 'pi', '.',
            'sin', 'cos', 'tan', 'log'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            action = lambda x=button: self.on_button_click(x)
            tk.Button(root, text=button, width=5, height=2, font=('Arial', 14), command=action).grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def on_button_click(self, char):
        current_text = self.result_var.get()

        if char == 'C':
            self.result_var.set("")
        elif char == 'pi':
            self.result_var.set(str(math.pi))
        elif char in ('sqrt', 'sin', 'cos', 'tan', 'log'):
            try:
                val = float(current_text)
                if char == 'sqrt': res = math.sqrt(val)
                elif char == 'sin': res = math.sin(math.radians(val))
                elif char == 'cos': res = math.cos(math.radians(val))
                elif char == 'tan': res = math.tan(math.radians(val))
                elif char == 'log': res = math.log10(val)
                
                self.result_var.set(res)
                # Tambahkan ke riwayat
                self.history_listbox.insert(tk.END, f"{char}({val}) = {res}")
                self.history_listbox.see(tk.END)
            except Exception:
                messagebox.showerror("Error", "Input tidak valid")
                self.result_var.set("")
        elif char == '=':
            try:
                # Menggunakan fungsi helper yang sudah ada dengan parsing sederhana
                # Untuk kemudahan di GUI, kita bisa menggunakan eval() dengan pengamanan
                # atau memanggil fungsi tambah/kurang/kali/bagi yang sudah didefinisikan.
                result = self.calculate_expression(current_text)
                self.result_var.set(result)
                # Tambahkan ke riwayat
                self.history_listbox.insert(tk.END, f"{current_text} = {result}")
                self.history_listbox.see(tk.END)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.result_var.set("")
        else:
            self.result_var.set(current_text + str(char))

    def calculate_expression(self, expression):
        # Logika sederhana untuk memproses ekspresi menggunakan fungsi yang ada
        try:
            # Mencari operator dalam ekspresi
            for op in ['^', '+', '-', '*', '/']:
                if op in expression:
                    parts = expression.split(op)
                    if len(parts) != 2: continue
                    
                    num1 = float(parts[0])
                    num2 = float(parts[1])

                    if op == '+': return tambah(num1, num2)
                    if op == '-': return kurang(num1, num2)
                    if op == '*': return kali(num1, num2)
                    if op == '/': return bagi(num1, num2)
                    if op == '^': return math.pow(num1, num2)
            
            # Jika hanya angka saja
            return float(expression)
        except ValueError:
            raise ValueError("Input tidak valid")
        except ZeroDivisionError:
            raise ValueError("Tidak dapat membagi dengan nol")

    def on_history_double_click(self, event):
        """Mengambil kembali hasil perhitungan dari riwayat saat didouble-klik."""
        selection = self.history_listbox.curselection()
        if selection:
            item = self.history_listbox.get(selection[0])
            result_part = item.split('=')[-1].strip()
            self.result_var.set(result_part)

def main():
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
