import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from ttkthemes import ThemedStyle
from contextlib import redirect_stdout, redirect_stderr
import io
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name, get_all_styles
from pygments.util import ClassNotFound
from ptpython.translate import translate
import subprocess
from tempfile import NamedTemporaryFile
import os

class PtPythonIDE(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PtPython IDE")
        self.geometry("800x600")

        self.filename = None

        self.current_theme = "monokai"
        self.style = ThemedStyle(self)
        self.style.set_theme("equilux")

        s = ttk.Style()
        s.theme_use("equilux")

        self.show_line_numbers = tk.BooleanVar(value=True)

        self.font_size = 12

        self.column_selection_mode = False
        self.start_index = None
        self.end_index = None
        self.selected_columns = []  # Track selected columns

        self.create_menu()

        self.text_frame = tk.Frame(self, bg='#2b2b2b')
        self.text_frame.pack(fill="both", expand=1)

        self.line_numbers = tk.Text(self.text_frame, width=4, padx=4, takefocus=0, border=0,
                                    background='#333333', foreground='#ffffff', state='disabled', wrap='none', font=("Consolas", self.font_size, "bold"))
        self.line_numbers.pack(side="left", fill="y")

        self.text = ScrolledText(self.text_frame, wrap="none", undo=True, maxundo=-1, font=("Consolas", self.font_size), bg='#1e1e1e', fg='#ffffff', insertbackground='#ffffff')
        self.text.pack(side="right", fill="both", expand=1)

        self.output_text = ScrolledText(self, wrap="none", height=10, bg="black", fg="white", font=("Consolas", self.font_size))
        self.output_text.pack(fill="x", side="bottom")

        self.text.bind("<KeyRelease>", self.on_key_release)
        self.text.bind("<MouseWheel>", self.on_key_release)
        self.text.bind("<Button-4>", self.on_key_release)
        self.text.bind("<Button-5>", self.on_key_release)
        self.text.bind("<Key>", self.update_column_selection)

        self.bind_shortcuts()

        self.update_line_numbers()

    def create_menu(self):
        menubar = tk.Menu(self, bg='#2b2b2b', fg='#ffffff', activebackground='#3e3e3e', activeforeground='#ffffff')

        filemenu = tk.Menu(menubar, tearoff=0, bg='#2b2b2b', fg='#ffffff', activebackground='#3e3e3e', activeforeground='#ffffff')
        filemenu.add_command(label="Novo", command=self.new_file)
        filemenu.add_command(label="Abrir", command=self.open_file)
        filemenu.add_command(label="Salvar", command=self.save_file)
        filemenu.add_command(label="Salvar como...", command=self.save_as_file)
        filemenu.add_separator()
        filemenu.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Arquivo", menu=filemenu)

        runmenu = tk.Menu(menubar, tearoff=0, bg='#2b2b2b', fg='#ffffff', activebackground='#3e3e3e', activeforeground='#ffffff')
        runmenu.add_command(label="Executar", command=self.run_code)
        menubar.add_cascade(label="Executar", menu=runmenu)

        editmenu = tk.Menu(menubar, tearoff=0, bg='#2b2b2b', fg='#ffffff', activebackground='#3e3e3e', activeforeground='#ffffff')
        thememenu = tk.Menu(editmenu, tearoff=0, bg='#2b2b2b', fg='#ffffff', activebackground='#3e3e3e', activeforeground='#ffffff')
        for style in sorted(get_all_styles()):
            thememenu.add_command(label=style, command=lambda style=style: self.set_code_theme(style))
        editmenu.add_cascade(label="Tema de Código", menu=thememenu)

        interfacemenu = tk.Menu(editmenu, tearoff=0, bg='#2b2b2b', fg='#ffffff', activebackground='#3e3e3e', activeforeground='#ffffff')
        for theme in sorted(self.style.theme_names()):
            interfacemenu.add_command(label=theme, command=lambda theme=theme: self.set_interface_theme(theme))
        editmenu.add_cascade(label="Tema da Interface", menu=interfacemenu)

        editmenu.add_checkbutton(label="Mostrar Números das Linhas", onvalue=True, offvalue=False,
                                 variable=self.show_line_numbers, command=self.update_line_numbers)
        menubar.add_cascade(label="Editar", menu=editmenu)

        helpmenu = tk.Menu(menubar, tearoff=0, bg='#2b2b2b', fg='#ffffff', activebackground='#3e3e3e', activeforeground='#ffffff')
        helpmenu.add_command(label="Atalhos", command=self.show_shortcuts)
        menubar.add_cascade(label="Ajuda", menu=helpmenu)

        self.config(menu=menubar)

    def bind_shortcuts(self):
        self.bind('<Control-a>', self.select_all)
        self.bind('<Control-s>', self.save_file)
        self.bind('<Control-equal>', self.increase_font_size)
        self.bind('<Control-minus>', self.decrease_font_size)
        self.bind('<Control-Shift-Button-3>', self.toggle_column_selection_mode)
        self.bind('<Control-z>', self.undo)
        self.bind('<Control-y>', self.redo)
        self.bind('<Left>', self.move_column_left)
        self.bind('<Right>', self.move_column_right)

    def select_all(self, event=None):
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
        return 'break'

    def toggle_column_selection_mode(self, event):
        self.column_selection_mode = not self.column_selection_mode
        if self.column_selection_mode:
            self.start_index = self.text.index("@%d,%d" % (event.x, event.y))
            self.end_index = self.start_index
            self.text.bind('<B3-Motion>', self.update_column_end_index)
        else:
            self.text.tag_remove(tk.SEL, "1.0", tk.END)
            self.start_index = None
            self.end_index = None
            self.selected_columns = []
            self.text.unbind('<B3-Motion>')

    def update_column_end_index(self, event):
        self.end_index = self.text.index("@%d,%d" % (event.x, event.y))
        start_col = int(self.start_index.split('.')[1])
        end_col = int(self.end_index.split('.')[1])
        self.selected_columns = list(range(start_col, end_col + 1))
        self.select_column()

    def select_column(self, event=None):
        self.text.tag_remove(tk.SEL, "1.0", tk.END)
        if not self.start_index or not self.end_index:
            return
        start_line = int(self.start_index.split('.')[0])
        end_line = int(self.end_index.split('.')[0])

        for line in range(start_line, end_line + 1):
            for col in self.selected_columns:
                start = f"{line}.{col}"
                end = f"{line}.{col+1}"
                self.text.tag_add(tk.SEL, start, end)

        self.text.see(tk.INSERT)

    def update_column_selection(self, event):
        if self.column_selection_mode and self.text.tag_ranges(tk.SEL):
            new_text = event.char
            if new_text:
                self.text.edit_separator()
                start_line = int(self.start_index.split('.')[0])
                end_line = int(self.end_index.split('.')[0])
                for line in range(start_line, end_line + 1):
                    for col in self.selected_columns:
                        start = f"{line}.{col}"
                        end = f"{line}.{col+1}"
                        self.text.delete(start, end)
                        self.text.insert(start, new_text)

    def move_column_left(self, event=None):
        if self.column_selection_mode and self.text.tag_ranges(tk.SEL):
            self.selected_columns = [max(0, col - 1) for col in self.selected_columns]
            self.select_column()

    def move_column_right(self, event=None):
        if self.column_selection_mode and self.text.tag_ranges(tk.SEL):
            self.selected_columns = [col + 1 for col in self.selected_columns]
            self.select_column()

    def undo(self, event=None):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass
        return 'break'

    def redo(self, event=None):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass
        return 'break'

    def increase_font_size(self, event=None):
        self.font_size += 2
        self.text.config(font=("Consolas", self.font_size))
        self.line_numbers.config(font=("Consolas", self.font_size, "bold"))
        self.output_text.config(font=("Consolas", self.font_size))

    def decrease_font_size(self, event=None):
        if self.font_size > 8:
            self.font_size -= 2
            self.text.config(font=("Consolas", self.font_size))
            self.line_numbers.config(font=("Consolas", self.font_size, "bold"))
            self.output_text.config(font=("Consolas", self.font_size))

    def show_shortcuts(self):
        shortcuts = (
            "Atalhos Disponíveis:\n\n"
            "Ctrl+A: Selecionar todo o texto\n"
            "Ctrl+Shift+Botão direito do mouse: Selecionar/Desativar seleção de coluna do texto\n"
            "Ctrl+S: Salvar o texto no arquivo aberto\n"
            "Ctrl e +: Aumentar o tamanho da fonte do texto da IDE\n"
            "Ctrl e -: Diminuir o tamanho da fonte do texto da IDE\n"
            "Ctrl+Z: Desfazer\n"
            "Ctrl+Y: Refazer\n"
            "Seta Esquerda: Mover coluna selecionada para a esquerda\n"
            "Seta Direita: Mover coluna selecionada para a direita\n"
        )
        messagebox.showinfo("Atalhos", shortcuts)

    def new_file(self):
        self.filename = None
        self.text.delete("1.0", tk.END)

    def open_file(self):
        options = {
            'defaultextension': '.ptpy',
            'filetypes': [("PtPython Files", "*.ptpy"), ("All Files", "*.*")],
            'initialdir': os.getcwd(),
            'title': 'Abrir arquivo',
        }

        self.filename = filedialog.askopenfilename(**options)
        if self.filename:
            with open(self.filename, "r", encoding="utf-8") as file:
                code = file.read()
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", code)
            self.update_line_numbers()
            self.highlight_code()

    def save_file(self, event=None):
        if self.filename:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(self.text.get("1.0", tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        options = {
            'defaultextension': '.ptpy',
            'filetypes': [("PtPython Files", "*.ptpy"), ("All Files", "*.*")],
            'initialdir': os.getcwd(),
            'title': 'Salvar arquivo',
        }

        self.filename = filedialog.asksaveasfilename(**options)
        if self.filename:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(self.text.get("1.0", tk.END))

    def run_code(self):
        code = self.text.get("1.0", tk.END)
        translated_code = translate(code)

        self.output_text.delete("1.0", tk.END)

        with NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
            temp_file.write(translated_code)
            temp_file.flush()
            temp_filename = temp_file.name

        try:
            result = subprocess.run(['python3.10', temp_filename], capture_output=True, text=True, check=True)
            self.output_text.insert(tk.END, result.stdout)
        except subprocess.CalledProcessError as e:
            self.output_text.insert(tk.END, f"Erro na execução: {e}\n{e.stderr}")
        finally:
            os.remove(temp_filename)

    def on_key_release(self, event=None):
        self.highlight_code()
        self.update_line_numbers()

    def highlight_code(self):
        code = self.text.get("1.0", tk.END)
        self.text.mark_set("range_start", "1.0")

        for token, content in lex(code, PythonLexer()):
            self.text.mark_set("range_end", f"range_start + {len(content)}c")
            self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")

        self.apply_highlighting_styles()

    def apply_highlighting_styles(self):
        try:
            style = get_style_by_name(self.current_theme)
        except ClassNotFound:
            style = get_style_by_name("monokai")

        for token, settings in style:
            fg = settings["color"]
            bg = settings["bgcolor"]
            font = settings["italic"] and "italic" or settings["bold"] and "bold" or None
            if fg:
                self.text.tag_configure(str(token), foreground=f"#{fg}", font=font)
            if bg:
                self.text.tag_configure(str(token), background=f"#{bg}")

    def set_code_theme(self, theme):
        self.current_theme = theme
        self.apply_highlighting_styles()

    def set_interface_theme(self, theme):
        self.style.set_theme(theme)
        self.text.config(bg=self.style.lookup('TFrame', 'background'), fg=self.style.lookup('TLabel', 'foreground'))

    def update_line_numbers(self, event=None):
        if self.show_line_numbers.get():
            self.line_numbers.pack(side="left", fill="y")
            self.update_line_numbers_content()
        else:
            self.line_numbers.pack_forget()

    def update_line_numbers_content(self, event=None):
        if self.show_line_numbers.get():
            line_numbers_content = "\n".join(str(i) for i in range(1, int(self.text.index('end').split('.')[0])))
            self.line_numbers.config(state='normal')
            self.line_numbers.delete('1.0', 'end')
            self.line_numbers.insert('1.0', line_numbers_content)
            self.line_numbers.config(state='disabled')

if __name__ == "__main__":
    app = PtPythonIDE()
    app.mainloop()
