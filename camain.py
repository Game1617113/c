import tkinter as tk
from tkinter import messagebox
import re 

current_expression = ""
notes_window = None
notes_content = ""

def clear_display():
    """ล้างช่องแสดงผลและรีเซ็ตนิพจน์."""
    global current_expression
    current_expression = ""
    display_entry.delete(0, tk.END)

def backspace():
    """ลบตัวอักษรสุดท้ายออกจากนิพจน์."""
    global current_expression
    if current_expression:
        current_expression = current_expression[:-1]
        display_entry.delete(0, tk.END)
        display_entry.insert(0, current_expression)

def button_click(item):
    """เพิ่มตัวเลขหรือตัวดำเนินการที่คลิกเข้าไปในนิพจน์ปัจจุบัน."""
    global current_expression
    
    if str(item) not in ['+', '-', '*', '/'] and current_expression in ['Error: Div/0', 'Error']:
        current_expression = ""
        
    operators = ['+', '-', '*', '/']
    if str(item) in operators and current_expression and current_expression[-1] in operators:
        current_expression = current_expression[:-1] + str(item)
    else:
        current_expression += str(item)

    if len(current_expression) > 20:
        current_expression = current_expression[:20] 

    display_entry.delete(0, tk.END)
    display_entry.insert(0, current_expression)

def clean_expression_for_eval(expression):
    """
    ใช้ Regular Expression ลบศูนย์นำหน้าออกจากตัวเลขในนิพจน์ (เช่น 01 -> 1, 5+007 -> 5+7)
    """
    
    return re.sub(r'(\b|\D)0+(\d+)', r'\g<1>\g<2>', expression)

def calculate():
    """คำนวณผลลัพธ์ของนิพจน์ที่อยู่ในช่องแสดงผล."""
    global current_expression
    
    expression_to_eval = clean_expression_for_eval(current_expression)
    
    try:
        result = str(eval(expression_to_eval))
        
        display_entry.delete(0, tk.END)
        display_entry.insert(0, result)
        
        current_expression = result
        
    except ZeroDivisionError:
        messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถหารด้วยศูนย์ได้!")
        current_expression = "Error: Div/0"
        display_entry.delete(0, tk.END)
        display_entry.insert(0, current_expression)
    except Exception:
        messagebox.showerror("ข้อผิดพลาด", "นิพจน์ไม่ถูกต้อง!")
        current_expression = "Error"
        display_entry.delete(0, tk.END)
        display_entry.insert(0, current_expression)

def open_notes():
    """เปิดหน้าต่างสำหรับจดบันทึก (Notes) ที่ข้อมูลจะอยู่แค่ในหน่วยความจำ (RAM)."""
    global notes_window, notes_content

    if notes_window is None or not notes_window.winfo_exists():
        notes_window = tk.Toplevel(root)
        notes_window.title("Notes")
        notes_window.geometry("400x300")
        
        scrollbar = tk.Scrollbar(notes_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 
        
        notes_text = tk.Text(
            notes_window, 
            wrap=tk.WORD, 
            font=('Arial', 12),
            padx=5, 
            pady=5,
            yscrollcommand=scrollbar.set
            )
        notes_text.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        notes_text.insert(tk.END, notes_content)

        scrollbar.config(command=notes_text.yview)
        
        def close_notes_and_store():
            nonlocal notes_text
            global notes_content
            notes_content = notes_text.get("1.0", tk.END)
            notes_window.destroy()
        
        notes_window.protocol("WM_DELETE_WINDOW", close_notes_and_store)
        
def disable_keyboard_input(event):
    """ฟังก์ชันดักจับการกดแป้นพิมพ์และยกเลิกการทำงานเพื่อป้องกันการพิมพ์ลง Entry."""
    return "break"

root = tk.Tk()
root.title("Calculator")
root.geometry("250x400")
bg="#4B4B4B"
root.configure(bg=bg)

display_entry = tk.Entry(
    root, 
    width=120, 
    font=('Arial', 20), 
    bd=5, 
    relief=tk.SUNKEN, 
    justify='right'
)
display_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
display_entry.bind('<Key>', disable_keyboard_input)

buttons_layout = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 3) 
]

for (text, row, col) in buttons_layout:
    tk.Button(
        root, 
        text=text, 
        padx=15, 
        pady=10,
        font=('Arial', 14, 'bold' ,),
        command=lambda t=text: button_click(t),
        fg="#FFFFFF",
        bg="#202020"
    ).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

tk.Button(
    root, 
    text='<-', 
    padx=15, 
    pady=10,
    font=('Arial', 14, 'bold'),
    bg="#202020",
    fg="#FFFFFF",
    command=backspace
).grid(row=4, column=2, sticky="nsew", padx=2, pady=2)

tk.Button(
    root, 
    text='C', 
    padx=15, 
    pady=10,
    font=('Arial', 14, 'bold'),
    bg="#4B4B4B",
    fg="#FF2020",
    command=clear_display
).grid(row=5, column=0, sticky="nsew", padx=2, pady=2)

tk.Button(
    root, 
    text='=', 
    padx=15, 
    pady=10,
    font=('Arial', 14, 'bold'),
    bg="#20CA2F",
    fg="#FFFFFF",
    command=calculate
).grid(row=5, column=1, columnspan=3, sticky="nsew", padx=2, pady=2)

tk.Button(
    root, 
    text='Notes', 
    padx=15, 
    pady=10,
    font=('Arial', 12),
    bg="#F7F71E",
    fg="#000000",
    command=open_notes
).grid(row=6, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)

for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)


root.mainloop()
