


import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from tkinter import ttk
from tkinter.font import Font
import tkinter.scrolledtext as st
import os
# import win32print
# import win32api
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.root.geometry("800x600")

        self.text_area = st.ScrolledText(self.root, wrap='word', undo=True)
        self.text_area.pack(fill='both', expand=1)

        self.font_size = 12
        self.font_family = "Arial"
        self.text_area.config(font=(self.font_family, self.font_size))
        
        self.current_file = None
        self.is_dark_mode = False

        self.create_menu()
        self.create_toolbar()
        self.create_find_replace_dialog()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_command(label="Print", command=self.print_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        menu_bar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        menu_bar.add_cascade(label="View", menu=view_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Find and Replace", command=self.show_find_replace_dialog)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menu_bar)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        
        copy_button = tk.Button(toolbar, text="Copy", command=self.copy_text)
        copy_button.pack(side=tk.LEFT, padx=2, pady=2)

        paste_button = tk.Button(toolbar, text="Paste", command=self.paste_text)
        paste_button.pack(side=tk.LEFT, padx=2, pady=2)

        increase_font_button = tk.Button(toolbar, text="A+", command=self.increase_font_size)
        increase_font_button.pack(side=tk.LEFT, padx=2, pady=2)

        decrease_font_button = tk.Button(toolbar, text="A-", command=self.decrease_font_size)
        decrease_font_button.pack(side=tk.LEFT, padx=2, pady=2)

        change_color_button = tk.Button(toolbar, text="Change Font Color", command=self.change_font_color)
        change_color_button.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_find_replace_dialog(self):
        self.find_replace_window = None
        self.find_entry = None
        self.replace_entry = None

    def show_find_replace_dialog(self):
        if self.find_replace_window is None:
            self.find_replace_window = tk.Toplevel(self.root)
            self.find_replace_window.title("Find and Replace")

            tk.Label(self.find_replace_window, text="Find:").grid(row=0, column=0, padx=4, pady=4)
            self.find_entry = tk.Entry(self.find_replace_window)
            self.find_entry.grid(row=0, column=1, padx=4, pady=4)

            tk.Label(self.find_replace_window, text="Replace:").grid(row=1, column=0, padx=4, pady=4)
            self.replace_entry = tk.Entry(self.find_replace_window)
            self.replace_entry.grid(row=1, column=1, padx=4, pady=4)

            find_button = tk.Button(self.find_replace_window, text="Find", command=self.find_text)
            find_button.grid(row=2, column=0, padx=4, pady=4)

            replace_button = tk.Button(self.find_replace_window, text="Replace", command=self.replace_text)
            replace_button.grid(row=2, column=1, padx=4, pady=4)

            close_button = tk.Button(self.find_replace_window, text="Close", command=self.close_find_replace_dialog)
            close_button.grid(row=2, column=2, padx=4, pady=4)

    def close_find_replace_dialog(self):
        if self.find_replace_window:
            self.find_replace_window.destroy()
            self.find_replace_window = None

    def find_text(self):
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        find_str = self.find_entry.get()
        if find_str:
            start_idx = "1.0"
            while True:
                start_idx = self.text_area.search(find_str, start_idx, tk.END)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(find_str)}c"
                self.text_area.tag_add("highlight", start_idx, end_idx)
                start_idx = end_idx
            self.text_area.tag_config("highlight", background="yellow")

    def replace_text(self):
        find_str = self.find_entry.get()
        replace_str = self.replace_entry.get()
        content = self.text_area.get("1.0", tk.END)
        new_content = content.replace(find_str, replace_str)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", new_content)

    def new_file(self):
        self.current_file = None
        self.text_area.delete(1.0, tk.END)
        self.root.title("Notepad - New File")

    def open_file(self):
        self.current_file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
        if self.current_file:
            self.text_area.delete(1.0, tk.END)
            with open(self.current_file, "r") as file:
                self.text_area.insert(1.0, file.read())
            self.root.title(f"Notepad - {self.current_file}")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        self.current_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.root.title(f"Notepad - {self.current_file}")

    def print_file(self):
        if self.current_file:
            pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if pdf_file:
                with open(pdf_file, "wb") as file:
                    c = canvas.Canvas(file, pagesize=letter)
                    c.drawString(100, 750, self.text_area.get(1.0, tk.END))
                    c.save()
                messagebox.showinfo("Success", "PDF file created successfully")
        else:
            messagebox.showerror("Error", "Save the file before printing")

    def exit_application(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

    def toggle_dark_mode(self):
        if self.is_dark_mode:
            self.text_area.config(bg="white", fg="black")
            self.root.config(bg="white")
        else:
            self.text_area.config(bg="black", fg="white")
            self.root.config(bg="black")
        self.is_dark_mode = not self.is_dark_mode

    def copy_text(self):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.text_area.selection_get())
        except tk.TclError:
            pass

    def paste_text(self):
        try:
            self.text_area.insert(tk.INSERT, self.root.clipboard_get())
        except tk.TclError:
            pass

    def increase_font_size(self):
        self.font_size += 2
        self.text_area.config(font=(self.font_family, self.font_size))

    def decrease_font_size(self):
        if self.font_size > 2:
            self.font_size -= 2
            self.text_area.config(font=(self.font_family, self.font_size))

    def change_font_color(self):
        color = colorchooser.askcolor(title="Choose font color")
        if color[1]:
            self.text_area.config(fg=color[1])

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
