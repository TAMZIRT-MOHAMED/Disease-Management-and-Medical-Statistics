import tkinter as tk

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _clear_placeholder(self, e):
        if self['fg'] == self.placeholder_color:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color

    def _add_placeholder(self, e=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color