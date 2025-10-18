import tkinter as tk
from tkinter import messagebox

# ----------------------------------------------------
# ตัวแปรและฟังก์ชันหลัก
# ----------------------------------------------------

# ตัวแปรสำหรับเก็บค่าที่แสดงในช่องแสดงผล
current_expression = ""

def clear_display():
    """ล้างช่องแสดงผลและรีเซ็ตนิพจน์."""
    global current_expression
    current_expression = ""
    display_entry.delete(0, tk.END) # ล้างข้อความทั้งหมดใน Entry

def button_click(item):
    """เพิ่มตัวเลขหรือตัวดำเนินการที่คลิกเข้าไปในนิพจน์ปัจจุบัน."""
    global current_expression
    current_expression += str(item)
    display_entry.delete(0, tk.END) # ล้างก่อน
    display_entry.insert(0, current_expression) # แสดงนิพจน์ใหม่

def calculate():
    """คำนวณผลลัพธ์ของนิพจน์ที่อยู่ในช่องแสดงผล."""
    global current_expression
    try:
        # ใช้ฟังก์ชัน eval() เพื่อประเมินนิพจน์ทางคณิตศาสตร์ที่เป็นสตริง
        # (ข้อควรระวัง: eval() ควรใช้กับอินพุตที่เชื่อถือได้เท่านั้น)
        result = str(eval(current_expression))
        
        # แสดงผลลัพธ์ในช่องแสดงผล
        display_entry.delete(0, tk.END)
        display_entry.insert(0, result)
        
        # อัปเดตนิพจน์สำหรับการคำนวณครั้งถัดไป
        current_expression = result
        
    except ZeroDivisionError:
        messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถหารด้วยศูนย์ได้!")
        clear_display()
    except Exception:
        messagebox.showerror("ข้อผิดพลาด", "นิพจน์ไม่ถูกต้อง!")
        clear_display()

# ----------------------------------------------------
# การตั้งค่า GUI
# ----------------------------------------------------

# 1. สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("เครื่องคิดเลข Python")
root.geometry("250x350") # กำหนดขนาดเริ่มต้น

# 2. สร้างช่องแสดงผล (Entry widget)
display_entry = tk.Entry(
    root, 
    width=16, 
    font=('Arial', 20), 
    bd=5, 
    relief=tk.SUNKEN, # ทำให้ดูเหมือนจมลง
    justify='right' # จัดข้อความชิดขวา
)
display_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# 3. กำหนดปุ่มต่างๆ
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 3)
]

# สร้างปุ่มสำหรับตัวเลขและตัวดำเนินการ
for (text, row, col) in buttons:
    tk.Button(
        root, 
        text=text, 
        padx=15, 
        pady=10,
        font=('Arial', 14),
        command=lambda t=text: button_click(t) # ใช้ lambda เพื่อส่งค่าที่ถูกต้อง
    ).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

# ปุ่มพิเศษ: Clear (C)
tk.Button(
    root, 
    text='C', 
    padx=15, 
    pady=10,
    font=('Arial', 14, 'bold'),
    bg="#FFCCCC",
    command=clear_display
).grid(row=4, column=2, sticky="nsew", padx=2, pady=2)

# ปุ่มพิเศษ: เท่ากับ (=)
tk.Button(
    root, 
    text='=', 
    padx=15, 
    pady=10,
    font=('Arial', 14, 'bold'),
    bg="#ccffcc",
    command=calculate
).grid(row=5, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)

# 4. ตั้งค่าให้ปุ่มขยายตามขนาดเซลล์
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# 5. เริ่มลูปหลักของ GUI

root.mainloop()
