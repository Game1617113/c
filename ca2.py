import tkinter as tk
from tkinter import messagebox

# ----------------------------------------------------
# ตัวแปรและฟังก์ชันหลัก
# ----------------------------------------------------

# ตัวแปรสำหรับเก็บค่าที่แสดงในช่องแสดงผล
current_expression = ""
# ตัวแปรสำหรับเก็บหน้าต่างโน้ต เพื่อป้องกันการเปิดหลายหน้าต่าง
notes_window = None

def clear_display():
    """ล้างช่องแสดงผลและรีเซ็ตนิพจน์."""
    global current_expression
    current_expression = ""
    display_entry.delete(0, tk.END)

def backspace():
    """ลบตัวอักษรสุดท้ายออกจากนิพจน์."""
    global current_expression
    if current_expression:
        current_expression = current_expression[:-1] # ตัดตัวอักษรสุดท้ายออก
        display_entry.delete(0, tk.END)
        display_entry.insert(0, current_expression)

def button_click(item):
    """เพิ่มตัวเลขหรือตัวดำเนินการที่คลิกเข้าไปในนิพจน์ปัจจุบัน."""
    global current_expression
    
    # อนุญาตให้กดตัวดำเนินการต่อท้ายได้ทันทีหลังจากคำนวณเสร็จ
    if str(item) not in ['+', '-', '*', '/'] and current_expression in ['Error: Div/0', 'Error']:
        current_expression = ""
        
    # ป้องกันการใส่ตัวดำเนินการซ้ำซ้อน
    operators = ['+', '-', '*', '/']
    if str(item) in operators and current_expression and current_expression[-1] in operators:
        # แทนที่ตัวดำเนินการตัวสุดท้ายด้วยตัวใหม่
        current_expression = current_expression[:-1] + str(item)
    else:
        current_expression += str(item)

    # ตรวจสอบความยาวเพื่อป้องกันจอแสดงผลล้น
    if len(current_expression) > 20:
        current_expression = current_expression[:20] 

    display_entry.delete(0, tk.END)
    display_entry.insert(0, current_expression)

def calculate():
    """คำนวณผลลัพธ์ของนิพจน์ที่อยู่ในช่องแสดงผล."""
    global current_expression
    try:
        # ใช้ฟังก์ชัน eval() เพื่อประเมินนิพจน์ทางคณิตศาสตร์ที่เป็นสตริง
        result = str(eval(current_expression))
        
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
    """เปิดหน้าต่างสำหรับจดบันทึก (Notes) แบบ Non-Modal (ใช้งานพร้อมเครื่องคิดเลขได้)."""
    global notes_window

    if notes_window is None or not notes_window.winfo_exists():
        notes_window = tk.Toplevel(root)
        notes_window.title("Notes / บันทึก")
        notes_window.geometry("400x300")
        
        # Non-Modal: ไม่มีการใช้ grab_set()

        # สร้าง Text widget สำหรับพิมพ์โน้ต
        notes_text = tk.Text(
            notes_window, 
            wrap=tk.WORD, 
            font=('Arial', 12),
            padx=5, 
            pady=5
        )
        notes_text.pack(expand=True, fill=tk.BOTH)

        # เพิ่ม Scrollbar
        scrollbar = tk.Scrollbar(notes_window, command=notes_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        notes_text.config(yscrollcommand=scrollbar.set)
        
        notes_window.protocol("WM_DELETE_WINDOW", notes_window.destroy)
        
def disable_keyboard_input(event):
    """ฟังก์ชันนี้ดักจับทุกการกดแป้นพิมพ์และยกเลิก (break) การทำงานนั้น."""
    return "break" # คำสั่งนี้จะยกเลิกเหตุการณ์ที่เกิดขึ้น

# ----------------------------------------------------
# การตั้งค่า GUI
# ----------------------------------------------------

# 1. สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("เครื่องคิดเลข Python")
root.geometry("250x400")
root.resizable(False, False)

# 2. สร้างช่องแสดงผล (Entry widget)
display_entry = tk.Entry(
    root, 
    width=16, 
    font=('Arial', 20), 
    bd=5, 
    relief=tk.SUNKEN, 
    justify='right'
)
display_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# *** คำสั่งใหม่: ป้องกันการพิมพ์ใน Entry ***
display_entry.bind('<Key>', disable_keyboard_input) # ดักจับเหตุการณ์การกดปุ่มใดๆ
# *****************************************

# 3. กำหนดปุ่มต่างๆ และตำแหน่ง
buttons_layout = [
    # text, row, col
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 3) # ปุ่ม '+' ถูกเลื่อนไป (4, 3)
]

# สร้างปุ่มสำหรับตัวเลขและตัวดำเนินการ
for (text, row, col) in buttons_layout:
    tk.Button(
        root, 
        text=text, 
        padx=15, 
        pady=10,
        font=('Arial', 14),
        command=lambda t=text: button_click(t)
    ).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

# ปุ่มพิเศษ: Backspace (<-)
tk.Button(
    root, 
    text='<-', 
    padx=15, 
    pady=10,
    font=('Arial', 14, 'bold'),
    bg="#EEEEEE",
    command=backspace
).grid(row=4, column=2, sticky="nsew", padx=2, pady=2) # ตำแหน่ง (4, 2) เดิมคือ 'C'

# ปุ่มพิเศษ: Clear (C)
tk.Button(
    root, 
    text='C', 
    padx=15, 
    pady=10,
    font=('Arial', 14, 'bold'),
    bg="#FFCCCC",
    command=clear_display
).grid(row=5, column=0, sticky="nsew", padx=2, pady=2) # ตำแหน่งใหม่ (5, 0)

# ปุ่มพิเศษ: เท่ากับ (=)
tk.Button(
    root, 
    text='=', 
    padx=15, 
    pady=10,
    font=('Arial', 14, 'bold'),
    bg="#ccffcc",
    command=calculate
).grid(row=5, column=1, columnspan=3, sticky="nsew", padx=2, pady=2) # ตำแหน่ง (5, 1) - (5, 3)

# ปุ่มใหม่: Notes (สำหรับเปิดหน้าต่างจดบันทึก)
tk.Button(
    root, 
    text='Notes 📝', 
    padx=15, 
    pady=10,
    font=('Arial', 12),
    bg="#CCEEFF",
    command=open_notes
).grid(row=6, column=0, columnspan=4, sticky="nsew", padx=2, pady=2) # วางปุ่ม Notes ในแถวที่ 6

# 4. ตั้งค่าให้ปุ่มขยายตามขนาดเซลล์
for i in range(7): # 0 ถึง 6
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# 5. เริ่มลูปหลักของ GUI
root.mainloop()