import os
import sys
import tkinter as tk
import customtkinter as ctk

#TO IMPORT FILES FROM PC
def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

#WINDOW
window = ctk.CTk(fg_color="#0B132B")
window.geometry("400x550")
window.title("CALCULATOR")
window.iconbitmap(resource_path("calculator-ico.ico"))
icon = tk.PhotoImage(file=resource_path("calculator.png"))
window.iconphoto(False, icon)
window.resizable(False,False)

#DISPLAY FRAME
display_frame = ctk.CTkFrame(window,
                           fg_color="#0B132B")
display_frame.pack()

#DISPLAY LABEL
display_strvar = ctk.StringVar(value="0")
display_label = ctk.CTkLabel(display_frame,
                             textvariable = display_strvar,
                             fg_color="#1C2541",
                             text_color="#ccdffc",
                             font=("Consolas", 36, "bold"),
                             width=385,
                             height=150,
                             anchor="e")
display_label.pack(padx=10,pady=10,ipadx=30,expand=True,fill="both")

#BUTTONS FRAME
button_frame = ctk.CTkFrame(window,
                             fg_color="#0B132B")
button_frame.pack(expand=True,fill="both",padx=10,pady=2)

#BUTTONS
keyboard = [
    ['AC', '%', '+/-', '÷'],
    ['7', '8', '9', 'x'],
    ['4', '5', '6', '-'],                                                 
    ['1', '2', '3', '+'],
    ['←', '0', '.', '=']
]

ROW_COUNT = 5
COLUMN_COUNT = 4
up_keyboard = ['AC', '%', '+/-']
right_keyboard = ['÷','x','-','+','=']
reset_screen = False

for row in range(ROW_COUNT) :
    button_frame.rowconfigure(row,weight=1)
for column in range(COLUMN_COUNT) :
    button_frame.columnconfigure(column,weight=1)

for rows in range(ROW_COUNT) :
    for columns in range(COLUMN_COUNT) :
        button_text = keyboard[rows][columns]
        buttons = ctk.CTkButton(button_frame,
                                command=lambda button_text=button_text : button_func(button_text),
                                fg_color="#3A506B",
                                text_color="#ccdffc",
                                text=button_text,
                                font=("Segoe UI", 22, "bold"),
                                corner_radius=0,
                                border_width=0,
                                hover=True,
                                hover_color="#2C3E50")
        buttons.grid(row=rows,column=columns,padx=3,pady=3,sticky="nsew")

        if button_text in up_keyboard :
            buttons.configure(fg_color="#5BC0BE",
                              hover_color="#489F9E",
                              text_color="#0B132B")
        elif button_text in right_keyboard :
            buttons.configure(fg_color="#0077B6",
                              hover_color="#005B8C",
                              text_color="#ccdffc")
            if button_text == '=' :
                buttons.configure(fg_color="#00B4D8",
                                  hover_color="#0091AE",
                                  text_color="#0B132B")

#BUTTONS FUNCTION
A = None
B = None
operator = None
reset_screen = False
current_value = display_strvar.get()

def clear_all() :
    global A,B,operator,display_strvar,reset_screen
    A = None
    B = None
    operator = None
    reset_screen = False

def backspace() :
    global current_value,display_strvar

    current_value = display_strvar.get()
    if len(current_value) <= 1 or current_value == "Error" :
        display_strvar.set("0")
    else :
        display_strvar.set(current_value[:-1])

def remove_decimal_zero(num) :
    if isinstance(num,str) :
        return num
    if num % 1 == 0 :
        num = int(num)
    return str(num)

def calculate(numA,numB,operator) :
    if operator == '+' :
        return numA + numB
    elif operator == '-' :
        return numA - numB
    elif operator == 'x' :
        return numA * numB
    elif operator == '÷' :
        if numB == 0 :
            return "Error"
        return numA / numB

def button_func(button_text) :
    global A,B,operator,reset_screen,current_value,display_strvar,right_keyboard,up_keyboard
    current_value = display_strvar.get()
    
    if button_text in right_keyboard :

        if button_text == '=' :

            if A is not None and operator is not None :
                B = current_value
                numA = float(A)
                numB = float(B)
                
                result = calculate(numA,numB,operator)
                if result == "Error" :
                    display_strvar.set("Error")
                    clear_all()
                
                else :
                    result = remove_decimal_zero(result)
                    display_strvar.set(result)
                    A = result
                    operator = None
                    reset_screen = True
            
        elif button_text in "+-x÷" :

            if A is not None and operator is not None and not reset_screen :
                B = current_value
                numA = float(A)
                numB = float(B)

                result = calculate(numA,numB,operator)
                if result == "Error" :
                    display_strvar.set("Error")
                    clear_all()
                    return

                result = remove_decimal_zero(result)
                display_strvar.set(result)
                A = result

            else :
                A = current_value

            operator = button_text
            reset_screen = True
                
    elif button_text in up_keyboard :

        if button_text == "AC" :
            clear_all()
            display_strvar.set("0")

        elif button_text == '%' :
            if current_value != "Error" :
                num = float(current_value) / 100
                num = remove_decimal_zero(num)
                display_strvar.set(num)

        elif button_text == '+/-' :
            if current_value != "Error" :
                num = float(current_value) * -1
                num = remove_decimal_zero(num)
                display_strvar.set(num)

    elif button_text == '.' :

        if reset_screen or current_value == "Error":
            display_strvar.set("0.")
            reset_screen = False

        elif not '.' in current_value :
            display_strvar.set(current_value + ".")

    elif button_text == '←' :
        backspace()

    elif button_text in "0123456789" :

        if reset_screen or current_value == "0" or current_value == "Error":
            display_strvar.set(button_text)
            reset_screen = False

        else :
            display_strvar.set(current_value + button_text)

window.mainloop()