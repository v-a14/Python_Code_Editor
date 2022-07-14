
from sys import stderr
import tkinter as tk
from PIL import ImageTk
# Message box helps to show different types of pop ups
# file dialog helps to save/open the file
from tkinter import END, StringVar, messagebox, filedialog

# Backend mei ek process chalega, jisse through hi saara input or output
# jaaega,
import subprocess

from setuptools import Command


class Vs_code:
    # Initializing the constructor
    def __init__(self, root):
        self.root = root
        # Title Initialize kia h
        self.root.title("Vs Code Editor - Developed by Vaibhav")
        # yeh basically bta rha h, ki jab launch ho toh uski width kya ho
        # aur x axis se kitna gap ho starting mei
        # aur y axis se kitne gap ho starting mei
        self.root.geometry("1280x720+0+0")

        self.path_name = ''
        self.color_theme = StringVar()
        # Setting the deafult color theme
        self.color_theme.set('Light Default')

        # ====== Menu Icons ======

        # ======= File Icons
        self.open_icon = ImageTk.PhotoImage(file='Icons/open.png')
        self.save_icon = ImageTk.PhotoImage(file='Icons/save.png')
        self.saveas_icon = ImageTk.PhotoImage(file='Icons/saveas.png')
        self.exit_icon = ImageTk.PhotoImage(file='Icons/exit.png')
        self.new_icon = ImageTk.PhotoImage(file='Icons/new.png')
        # ===========Color Theme Icons ================
        self.light_default_icon = ImageTk.PhotoImage(
            file='Icons/Light_default.png')
        self.light_plus_icon = ImageTk.PhotoImage(file='Icons/Light_Plus.png')
        self.dark_icon = ImageTk.PhotoImage(file='Icons/Dark.png')
        self.red_icon = ImageTk.PhotoImage(file='Icons/Red.png')
        self.monokai_icon = ImageTk.PhotoImage(file='Icons/monokai.png')
        self.night_blue_icon = ImageTk.PhotoImage(file='Icons/night_blue.png')
        # Menu class ka object bna liya
        # aur bta diya kiske andar hona chaiye
        Mymenu = tk.Menu(self.root)

        Filemenu = tk.Menu(Mymenu, tearoff=False)
        Filemenu.add_command(
            label='New File', image=self.new_icon, compound=tk.LEFT, accelerator="Ctl+N", command=self.new_file)
        Filemenu.add_command(
            label='Open File', image=self.open_icon, compound=tk.LEFT, accelerator="Ctl+O", command=self.open_file)
        Filemenu.add_command(label='save', image=self.open_icon,
                             compound=tk.LEFT, accelerator="Ctl+S", command=self.save_file)
        Filemenu.add_command(label='save As', image=self.saveas_icon,
                             compound=tk.LEFT, accelerator="Ctl+Alt+S", command=self.save_as_file)
        Filemenu.add_command(label='Exit', image=self.exit_icon,
                             compound=tk.LEFT, accelerator="Ctl+Q", command=self.exit_function)

        color_theme = tk.Menu(Mymenu, tearoff=False)
        color_theme.add_radiobutton(label='Light Default', value='Light Default', image=self.light_default_icon,
                                    compound=tk.LEFT, variable=self.color_theme, command=self.color_change)
        color_theme.add_radiobutton(label='Light Plus', value='Light Plus', image=self.light_plus_icon,
                                    compound=tk.LEFT, variable=self.color_theme, command=self.color_change)
        color_theme.add_radiobutton(label='Dark', value='Dark', image=self.dark_icon,
                                    compound=tk.LEFT, variable=self.color_theme, command=self.color_change)
        color_theme.add_radiobutton(label='Red', value='Red', image=self.red_icon,
                                    compound=tk.LEFT, variable=self.color_theme, command=self.color_change)
        color_theme.add_radiobutton(label='Monokai', value='Monokai', image=self.monokai_icon,
                                    compound=tk.LEFT, variable=self.color_theme, command=self.color_change)
        color_theme.add_radiobutton(label='Night Blue', value='Night Blue',  image=self.night_blue_icon,
                                    compound=tk.LEFT, variable=self.color_theme, command=self.color_change)

        Mymenu.add_cascade(label="File", menu=Filemenu)
        Mymenu.add_cascade(label="Color Theme", menu=color_theme)
        # Ab hume cascde nhi krna h toh normally add command kr denge
        Mymenu.add_command(label="Clear", command=self.clear_all)
        Mymenu.add_separator()
        Mymenu.add_separator()
        Mymenu.add_command(label="Run", command=self.run)

        # Jo hamara tinker ka object h hum uske functions
        # call kr rhe h basically
        self.root.config(menu=Mymenu)

        # ================= Menu Part Ended Here ================= #

        # ===============Edtior Frame =============== #
        # Default font size
        self.font_size = 18

        # Frame le liye editor type ka
        EditorFrame = tk.Frame(self.root, bg="white")
        # Place kr dia with y and x axis
        EditorFrame.place(x=0, y=0, relwidth=1, height=500)

        # scroll bar ke liye object bna liya
        scrolly = tk.Scrollbar(EditorFrame, orient=tk.VERTICAL)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_editor = tk.Text(EditorFrame, bg='white', font=(
            'times new roman', self.font_size), yscrollcommand=scrolly.set)
        self.txt_editor.pack(fill=tk.BOTH, expand=1)
        scrolly.config(command=self.txt_editor.yview)

        #================Output Frame=====================#
        OutputFrame = tk.Frame(self.root, bg="white")
        # Place kr dia with y and x axis
        OutputFrame.place(x=0, y=500, relwidth=1, height=500)

        # scroll bar ke liye object bna liya
        scrolly = tk.Scrollbar(OutputFrame, orient=tk.VERTICAL)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_output = tk.Text(OutputFrame, bg='white', font=(
            'times new roman', self.font_size), yscrollcommand=scrolly.set)
        self.txt_output.pack(fill=tk.BOTH, expand=1)
        scrolly.config(command=self.txt_output.yview)

        # ======== Outframe Ends here =================#

        # ====== All functions starts here ====== #

    # Run Function

    def run(self):
        if self.path_name == '':
            messagebox.showerror(
                'Error', "Please Save the file to execute the code", parent=self.root)
        else:
            # Jaise hum call krte h python likh kr, vhi call ho rha h
            # print(self.path_name)
            command = f'python {self.path_name}'
            # background mei subprocess module use kr kr run kr rhe h
            run_file = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # pura communicate krega, uske baad output aur error jo bhi honge
            # vo hume return kr dega
            output, error = run_file.communicate()
            # print(output)
            # agar output vaali window mei kuch h toh pura clear kr do
            self.txt_output.delete('1.0', END)
            # output daal do, jo bhi aaya
            self.txt_output.insert('1.0', output)
            # agar error aaya h toh vo bhi daal do
            self.txt_output.insert('1.0', error)

    # Clear Function

    def clear_all(self):
        self.txt_editor.delete('1.0', END)
        self.txt_output.delete('1.0', END)

    # Save as function
    def save_as_file(self):
        path = filedialog.asksaveasfilename(
            filetypes=[('Python Files', '*.py')], defaultextension=('.py'))
        # agar path empty nhi h toh hi aage bdo
        if path != '':
            self.path_name = path
            fp = open(self.path_name, 'w')
            fp.write(self.txt_editor.get('1.0', END))
            fp.close()

    # Open Function
    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[('Python Files', '*.py')], defaultextension=('.py'))
        # agar path empty nhi h toh hi aage bdo
        if path != '':
            self.path_name = path
            fp = open(self.path_name, 'r')
            data = fp.read()
            self.txt_editor.delete('1.0', tk.END)
            self.txt_editor.insert('1.0', data)
            fp.close()

    # Save File Function
    def save_file(self):
        # Agar file pehli baar save ho rhi h toh
        if self.path_name == "":
            self.save_as_file()
        # agar file mei pehle se hi kuh kaam ho rha h toh
        else:
            fp = open(self.path_name, 'w')
            fp.write(self.txt_editor.get('1.0', tk.END))
            fp.close()

    # New File Function
    def new_file(self):
        self.path_name = ''
        # Text editor ko clear kia
        self.txt_editor.delete('1.0', END)
        self.txt_output.delete('1.0', END)

    # Exit Function
    def exit_function(self):
        self.root.destroy()
    # ======= color Change Functions ====== #

    def color_change(self):
        if self.color_theme.get() == 'Light Default':
            self.txt_editor.config(bg='#ffffff', fg='#000000')
            self.txt_output.config(bg='ffffff', fg='#000000')
        if self.color_theme.get() == 'Light Plus':
            self.txt_editor.config(bg='#e0e0e0', fg='#474747')
            self.txt_output.config(bg='#e0e0e0', fg='#474747')
        if self.color_theme.get() == 'Dark':
            self.txt_editor.config(bg='#2d2d2d', fg='#c4c4c4')
            self.txt_output.config(bg='#2d2d2d', fg='#c4c4c4')
        if self.color_theme.get() == 'Red':
            self.txt_editor.config(bg='#ffe8e8', fg='#2d2d2d')
            self.txt_output.config(bg='#ffe8e8', fg='#2d2d2d')
        if self.color_theme.get() == 'Monokai':
            self.txt_editor.config(bg='#d3b774', fg='#474747')
            self.txt_output.config(bg='#d3b774', fg='#474747')
        if self.color_theme.get() == 'Night Blue':
            self.txt_editor.config(bg='#6b9dc2', fg='#ededed')
            self.txt_output.config(bg='#6b9dc2', fg='#ededed')


# Ofject of Tkinter Class
root = tk.Tk()

# object of the Vs_code class
# uske andar humne root(Tkinter ka jo obect h) usko pass kr dia
obj = Vs_code(root)

# Screen jisse bani rhe, chali naa jaaye
root.mainloop()
