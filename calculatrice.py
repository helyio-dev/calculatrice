import customtkinter
import math

class CalculatriceApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculatrice")
        self.geometry("450x650")
        self.resizable(False, False)

        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        self.expression = ""
        self.result_var = customtkinter.StringVar(value="0")
        self.last_result = "0"
        self.history = []
        self.memory = 0
        self.angle_mode = "degrees"
        self.decimal_places = 4

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)

        self.display_frame = customtkinter.CTkFrame(self)
        self.display_frame.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(1, weight=1)

        self.history_display = customtkinter.CTkTextbox(self.display_frame,
                                                        height=70,
                                                        font=("Arial", 14),
                                                        state="disabled")
        self.history_display.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.display = customtkinter.CTkEntry(self.display_frame,
                                              textvariable=self.result_var,
                                              font=("Arial", 35),
                                              justify="right",
                                              state="readonly")
        self.display.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.options_frame = customtkinter.CTkFrame(self)
        self.options_frame.grid(row=1, column=0, columnspan=6, padx=10, pady=5, sticky="ew")
        self.options_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.mode_label = customtkinter.CTkLabel(self.options_frame, text="Mode:")
        self.mode_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.mode_switch = customtkinter.CTkSwitch(self.options_frame,
                                                   text="Deg/Rad",
                                                   command=self.toggle_angle_mode_calc)
        self.mode_switch.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        self.precision_label = customtkinter.CTkLabel(self.options_frame, text="Décimales:")
        self.precision_label.grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.precision_optionmenu = customtkinter.CTkOptionMenu(self.options_frame,
                                                               values=["2", "4", "6", "8", "Full"],
                                                               command=self.set_decimal_precision)
        self.precision_optionmenu.set("4")
        self.precision_optionmenu.grid(row=0, column=3, padx=5, pady=2, sticky="ew")

        buttons_layout = [
            ('C', 2, 0, 1, "red"), ('DEL', 2, 1, 1, "orange"), ('Ans', 2, 2, 1, None), ('(', 2, 3, 1, None), (')', 2, 4, 1, None), ('%', 2, 5, 1, None),

            ('sin', 3, 0, 1, "grey"), ('cos', 3, 1, 1, "grey"), ('tan', 3, 2, 1, "grey"), ('^', 3, 3, 1, None), ('log', 3, 4, 1, "grey"), ('ln', 3, 5, 1, "grey"),

            ('7', 4, 0, 1), ('8', 4, 1, 1), ('9', 4, 2, 1), ('/', 4, 3, 1, None), ('sqrt', 4, 4, 1, None), ('1/x', 4, 5, 1, None),

            ('4', 5, 0, 1), ('5', 5, 1, 1), ('6', 5, 2, 1), ('*', 5, 3, 1, None), ('M+', 5, 4, 1, "purple"), ('M-', 5, 5, 1, "purple"),

            ('1', 6, 0, 1), ('2', 6, 1, 1), ('3', 6, 2, 1), ('-', 6, 3, 1, None), ('MR', 6, 4, 1, "purple"), ('MC', 6, 5, 1, "purple"), # '-' est bien là

            ('pi', 7, 0, 1, "grey"), ('0', 7, 1, 1), ('.', 7, 2, 1), ('+', 7, 3, 1, None), ('=', 7, 4, 2, "green") # '+' est bien là
        ]

        for btn_info in buttons_layout:
            text = btn_info[0]
            row = btn_info[1]
            col = btn_info[2]
            colspan = btn_info[3]
            color = btn_info[4] if len(btn_info) > 4 else None

            button_command = None
            fg_color_to_use = color if color else customtkinter.ThemeManager.theme["CTkButton"]["fg_color"]

            if text == '=':
                button_command = self.calculate
            elif text == 'C':
                button_command = self.clear
            elif text == 'DEL':
                button_command = self.backspace
            elif text == '+/-':
                button_command = self.toggle_sign
            elif text == '%':
                button_command = self.add_percentage
            elif text == 'sqrt':
                button_command = self.add_sqrt
            elif text == '1/x':
                button_command = self.add_inverse
            elif text in ['sin', 'cos', 'tan', 'log', 'ln']:
                button_command = lambda t=text: self.add_function(t)
            elif text == '^':
                button_command = lambda t="**": self.press(t)
            elif text == 'pi':
                button_command = lambda t="math.pi": self.press(t)
            elif text == 'Ans':
                button_command = self.insert_ans
            elif text == 'M+':
                button_command = self.memory_add
            elif text == 'M-':
                button_command = self.memory_subtract
            elif text == 'MR':
                button_command = self.memory_recall
            elif text == 'MC':
                button_command = self.memory_clear
            else:
                button_command = lambda t=text: self.press(t)

            button = customtkinter.CTkButton(self, text=text,
                                             command=button_command,
                                             font=("Arial", 18, "bold" if text in ['=', 'C', 'DEL'] else "normal"),
                                             height=50, width=50,
                                             fg_color=fg_color_to_use)
            button.grid(row=row, column=col, columnspan=colspan, padx=3, pady=3, sticky="nsew")

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)

    def _update_display(self, text):
        self.result_var.set(text)

    def _format_result(self, value):
        if self.decimal_places == "Full":
            return str(value)
        else:
            try:
                if isinstance(value, (int, float)) and value == int(value):
                    return str(int(value))
                formatted_value = f"{value:.{int(self.decimal_places)}f}"
                if '.' in formatted_value:
                    formatted_value = formatted_value.rstrip('0').rstrip('.')
                return formatted_value if formatted_value else "0"
            except ValueError:
                return str(value)

    def press(self, char):
        if self.expression == "0" and char.isdigit() and char != '0':
            self.expression = char
        elif self.expression == "0" and char == '0':
            return
        elif char == '.':
            if not self.expression or self.expression[-1] in ['+', '-', '*', '/', '(', '^', '**']:
                self.expression += "0."
            elif '.' not in self.expression.split()[-1] and not self.expression.endswith('.') and (self.expression[-1].isdigit() or self.expression[-1] == ')' or self.expression.endswith('math.pi')):
                 self.expression += char
            else:
                return
        elif char in ['+', '-', '*', '/', '**']:
            if not self.expression and char in ['*', '/', '**']:
                return
            if self.expression and self.expression.endswith(('/', '*', '+', '-', '**')):
                self.expression = self.expression[:-len(self.expression.split()[-1])] + char
            else:
                self.expression += char
        elif char == '(':
            if self.expression and (self.expression[-1].isdigit() or self.expression[-1] == ')' or self.expression.endswith('math.pi')):
                self.expression += "*" + char
            else:
                self.expression += char
        elif char == ')':
            if self.expression.count('(') > self.expression.count(')'):
                self.expression += char
            else:
                return
        elif char == "math.pi":
            if self.expression and (self.expression[-1].isdigit() or self.expression[-1] == ')'):
                self.expression += "*math.pi"
            else:
                self.expression += char
        else:
            self.expression += str(char)
        
        self._update_display(self.expression)

    def clear(self):
        self.expression = ""
        self._update_display("0")

    def backspace(self):
        if self.expression:
            if self.expression.endswith("math.pi"):
                self.expression = self.expression[:-8]
            elif self.expression.endswith("math.sqrt("):
                self.expression = self.expression[:-11]
            elif self.expression.endswith("math.sin("):
                self.expression = self.expression[:-10]
            elif self.expression.endswith("math.cos("):
                self.expression = self.expression[:-10]
            elif self.expression.endswith("math.tan("):
                self.expression = self.expression[:-10]
            elif self.expression.endswith("math.log("):
                self.expression = self.expression[:-10]
            elif self.expression.endswith("1/("):
                self.expression = self.expression[:-3]
            elif self.expression.endswith("**"):
                self.expression = self.expression[:-2]
            else:
                self.expression = self.expression[:-1]

            if not self.expression:
                self._update_display("0")
            else:
                self._update_display(self.expression)
        else:
            self._update_display("0")

    def toggle_sign(self):
        current_val = self.result_var.get()
        if current_val in ["0", "Erreur"]:
            return
        try:
            val = float(current_val)
            self.expression = str(-val)
            self._update_display(self._format_result(-val))
        except ValueError:
            pass

    def add_percentage(self):
        current_display = self.result_var.get()
        if not current_display or current_display in ["0", "Erreur"]:
            return
        try:
            value = eval(self.expression)
            self.expression = str(value / 100)
            self._update_display(self._format_result(value / 100))
        except Exception:
            self._update_display("Erreur")
            self.expression = ""

    def add_sqrt(self):
        if self.expression and (self.expression[-1].isdigit() or self.expression[-1] == ')' or self.expression.endswith('math.pi')):
            self.expression += "*math.sqrt("
        else:
            self.expression += "math.sqrt("
        self._update_display(self.expression)

    def add_inverse(self):
        if self.expression and (self.expression[-1].isdigit() or self.expression[-1] == ')' or self.expression.endswith('math.pi')):
            self.expression += "*1/("
        else:
            self.expression += "1/("
        self._update_display(self.expression)

    def add_function(self, func_name):
        prefix = "math."
        if func_name == 'ln':
            func_name = 'log'

        if self.expression and (self.expression[-1].isdigit() or self.expression[-1] == ')' or self.expression.endswith('math.pi')):
            self.expression += "*" + prefix + func_name + "("
        else:
            self.expression += prefix + func_name + "("
        self._update_display(self.expression)

    def insert_ans(self):
        if self.last_result != "0":
            if self.expression == "0":
                self.expression = self.last_result
            elif self.expression and (self.expression[-1].isdigit() or self.expression[-1] == ')'):
                self.expression += "*" + self.last_result
            else:
                self.expression += self.last_result
            self._update_display(self.expression)

    def memory_add(self):
        try:
            value = float(self.result_var.get())
            self.memory += value
        except ValueError:
            pass

    def memory_subtract(self):
        try:
            value = float(self.result_var.get())
            self.memory -= value
        except ValueError:
            pass

    def memory_recall(self):
        self.expression = str(self._format_result(self.memory))
        self._update_display(self.expression)

    def memory_clear(self):
        self.memory = 0

    def toggle_angle_mode_calc(self):
        if self.angle_mode == "degrees":
            self.angle_mode = "radians"
            self.mode_switch.configure(text="Rad")
        else:
            self.angle_mode = "degrees"
            self.mode_switch.configure(text="Deg")

    def set_decimal_precision(self, choice):
        self.decimal_places = choice
        if self.result_var.get() not in ["0", "Erreur"]:
            try:
                current_value = float(self.result_var.get())
                self._update_display(self._format_result(current_value))
            except ValueError:
                pass

    def calculate(self):
        try:
            temp_expression = self.expression.replace('^', '**')

            if self.angle_mode == "degrees":
                temp_expression = temp_expression.replace("math.sin(", "math.sin(math.radians(")
                temp_expression = temp_expression.replace("math.cos(", "math.cos(math.radians(")
                temp_expression = temp_expression.replace("math.tan(", "math.tan(math.radians(")

            open_paren = temp_expression.count('(')
            close_paren = temp_expression.count(')')
            if open_paren > close_paren:
                temp_expression += ')' * (open_paren - close_paren)

            result_raw = eval(temp_expression)

            self.last_result = str(result_raw)
            formatted_result = self._format_result(result_raw)
            self._update_display(formatted_result)

            self._add_to_history(f"{self.expression} = {formatted_result}")
            self.expression = formatted_result

        except SyntaxError:
            self._update_display("Erreur: Syntaxe")
            self.expression = ""
        except ZeroDivisionError:
            self._update_display("Erreur: Div par 0")
            self.expression = ""
        except NameError:
            self._update_display("Erreur: Fonction")
            self.expression = ""
        except ValueError:
            self._update_display("Erreur: Valeur invalide")
            self.expression = ""
        except OverflowError:
            self._update_display("Erreur: Trop grand")
            self.expression = ""
        except Exception as e:
            self._update_display(f"Erreur: {e}")
            self.expression = ""

    def _add_to_history(self, entry):
        self.history.append(entry)
        if len(self.history) > 10:
            self.history.pop(0)

        self.history_display.configure(state="normal")
        self.history_display.delete("1.0", "end")
        for item in self.history:
            self.history_display.insert("end", item + "\n")
        self.history_display.see("end")
        self.history_display.configure(state="disabled")

if __name__ == "__main__":
    app = CalculatriceApp()
    app.mainloop()