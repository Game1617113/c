import tkinter as tk
from tkinter import messagebox
import re 
# ไม่จำเป็นต้อง import os แล้ว

# ----------------------------------------------------
# ตัวแปรและฟังก์ชันหลัก
# ----------------------------------------------------

# ตัวแปรสำหรับเก็บค่าที่แสดงในช่องแสดงผล
current_expression = ""
# ตัวแปรสำหรับเก็บหน้าต่างโน้ต เพื่อป้องกันการเปิดหลายหน้าต่าง
notes_window = None
# ตัวแปรสำหรับเก็บเนื้อหาโน้ตชั่วคราว (จะหายไปเมื่อปิดโปรแกรมหลัก)
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
    
    # ถ้าหน้าจอแสดงข้อผิดพลาด ให้เริ่มนิพจน์ใหม่เมื่อกดตัวเลข
    if str(item) not in ['+', '-', '*', '/'] and current_expression in ['Error: Div/0', 'Error']:
        current_expression = ""
        
    operators = ['+', '-', '*', '/']
    # ป้องกันการใส่ตัวดำเนินการซ้ำซ้อน (เช่น '++' หรือ '**')
    if str(item) in operators and current_expression and current_expression[-1] in operators:
        current_expression = current_expression[:-1] + str(item)
    else:
        current_expression += str(item)

    # จำกัดความยาวของนิพจน์ที่แสดง
    if len(current_expression) > 20:
        current_expression = current_expression[:20] 

    display_entry.delete(0, tk.END)
    display_entry.insert(0, current_expression)

def clean_expression_for_eval(expression):
    """
    ใช้ Regular Expression ลบศูนย์นำหน้าออกจากตัวเลขในนิพจน์ (เช่น 01 -> 1, 5+007 -> 5+7)
    """
    # รูปแบบ: (\b|\D) คือขอบเขตคำหรือตัวอักษรที่ไม่ใช่ตัวเลข (ตัวดำเนินการ)
    # 0+ คือ เลขศูนย์หนึ่งตัวหรือมากกว่า
    # (\d+) คือ ตัวเลขหนึ่งตัวหรือมากกว่า
    # แทนที่ด้วย \g<1> (ตัวดำเนินการ/ขอบเขต) ตามด้วย \g<2> (ตัวเลขที่เหลือ)
    return re.sub(r'(\b|\D)0+(\d+)', r'\g<1>\g<2>', expression)

def calculate():
    """คำนวณผลลัพธ์ของนิพจน์ที่อยู่ในช่องแสดงผล."""
    global current_expression
    
    # เตรียมสตริงสำหรับ eval() โดยการล้างศูนย์นำหน้า
    expression_to_eval = clean_expression_for_eval(current_expression)
    
    try:
        # ใช้ฟังก์ชัน eval() ในการคำนวณผลลัพธ์ทางคณิตศาสตร์
        result = str(eval(expression_to_eval))
        
        display_entry.delete(0, tk.END)
        display_entry.insert(0, result)
        
        current_expression = result
        
    except ZeroDivisionError:
        # จัดการข้อผิดพลาดเมื่อมีการหารด้วยศูนย์
        messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถหารด้วยศูนย์ได้!")
        current_expression = "Error: Div/0"
        display_entry.delete(0, tk.END)
        display_entry.insert(0, current_expression)
    except Exception:
        # จัดการข้อผิดพลาดอื่นๆ ที่เกิดจากนิพจน์ไม่ถูกต้อง
        messagebox.showerror("ข้อผิดพลาด", "นิพจน์ไม่ถูกต้อง!")
        current_expression = "Error"
        display_entry.delete(0, tk.END)
        display_entry.insert(0, current_expression)

def open_notes():
    """เปิดหน้าต่างสำหรับจดบันทึก (Notes) ที่ข้อมูลจะอยู่แค่ในหน่วยความจำ (RAM)."""
    global notes_window, notes_content

    # ป้องกันการเปิดหน้าต่างซ้ำซ้อน
    if notes_window is None or not notes_window.winfo_exists():
        notes_window = tk.Toplevel(root)
        notes_window.title("Notes / บันทึกชั่วคราว")
        notes_window.geometry("400x300")
        
        # สร้าง Scrollbar ก่อน Text widget 
        scrollbar = tk.Scrollbar(notes_window) # สร้าง Scrollbar
        # จัดวาง Scrollbar ทางด้านขวาและเติมเต็มความสูง
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 
        
        # สร้าง Text widget และผูกกับ Scrollbar
        notes_text = tk.Text(
            notes_window, 
            wrap=tk.WORD, 
            font=('Arial', 12),
            padx=5, 
            pady=5,
            yscrollcommand=scrollbar.set # ผูก Scrollbar เข้ากับ Text
        )
        # จัดวาง Text widget ทางซ้ายและขยายเต็มพื้นที่ที่เหลือ
        notes_text.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        notes_text.insert(tk.END, notes_content)

        # ผูก Scrollbar เข้ากับ Text widget อีกครั้ง (กำหนด Scrollbar ให้ควบคุม Text)
        scrollbar.config(command=notes_text.yview)
        
        # ฟังก์ชันที่ทำหน้าที่เก็บข้อมูลกลับเข้าตัวแปรส่วนกลางเมื่อปิดหน้าต่าง
        def close_notes_and_store():
            nonlocal notes_text
            global notes_content
            # เก็บเนื้อหาปัจจุบันลงในตัวแปรส่วนกลาง notes_content
            notes_content = notes_text.get("1.0", tk.END)
            notes_window.destroy()
        
        # ผูกฟังก์ชันเก็บข้อมูลเข้ากับปุ่มปิดหน้าต่าง (X)
        notes_window.protocol("WM_DELETE_WINDOW", close_notes_and_store)
        
def disable_keyboard_input(event):
    """ฟังก์ชันดักจับการกดแป้นพิมพ์และยกเลิกการทำงานเพื่อป้องกันการพิมพ์ลง Entry."""
    return "break"

# ----------------------------------------------------
# การตั้งค่า GUI
# ----------------------------------------------------

# 1. สร้างหน้าต่างหลัก (Root Window)
root = tk.Tk()
root.title("เครื่องคิดเลข Python")
root.geometry("250x400")

# 2. สร้างช่องแสดงผล (Entry widget)
display_entry = tk.Entry(
    root, 
    width=120, 
    font=('Arial', 20), 
    bd=5, 
    relief=tk.SUNKEN, 
    justify='right'
)
display_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
# ป้องกันการพิมพ์จากแป้นพิมพ์โดยตรง
display_entry.bind('<Key>', disable_keyboard_input)

# 3. กำหนดปุ่มต่างๆ และตำแหน่ง (Grid Layout)
buttons_layout = [
    # text, row, col
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 3) 
]

# สร้างปุ่มสำหรับตัวเลขและตัวดำเนินการโดยใช้ลูป
for (text, row, col) in buttons_layout:
    tk.Button(
        root, 
        text=text, 
        padx=15, 
        pady=10,
        font=('Arial', 14),
        # ใช้ lambda เพื่อส่งค่า text ไปยังฟังก์ชัน button_click
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
).grid(row=4, column=2, sticky="nsew", padx=2, pady=2)

# ปุ่มพิเศษ: Clear (C)
tk.Button(
    root, 
    text='C', 
    padx=15, 
    pady=10,
    font=('Arial', 14, 'bold'),
    bg="#FFCCCC",
    command=clear_display
).grid(row=5, column=0, sticky="nsew", padx=2, pady=2)

# ปุ่มพิเศษ: เท่ากับ (=) - ครอบคลุม 3 คอลัมน์
tk.Button(
    root, 
    text='=', 
    padx=15, 
    pady=10,
    font=('Arial', 14, 'bold'),
    bg="#ccffcc",
    command=calculate
).grid(row=5, column=1, columnspan=3, sticky="nsew", padx=2, pady=2)

# ปุ่มใหม่: Notes (สำหรับเปิดหน้าต่างจดบันทึก)
tk.Button(
    root, 
    text='Notes', 
    padx=15, 
    pady=10,
    font=('Arial', 12),
    bg="#CCEEFF",
    command=open_notes
).grid(row=6, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)

# 4. ตั้งค่าให้ปุ่มขยายตามขนาดเซลล์เมื่อหน้าต่างถูกปรับขนาด
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# 5. เริ่มลูปหลักของ GUI
root.mainloop()