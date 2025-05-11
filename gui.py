import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from vault.lock import check_lock
from vault.operations import encrypt_and_map, decrypt_and_handle

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SafeBoxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ Fail-SafeBox")
        self.geometry("540x500")
        self.resizable(False, False)

        self.file_path = ctk.StringVar()
        self.password = ctk.StringVar()
        self.mode = ctk.StringVar(value="encrypt")
        self.auto_delete = ctk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Fail-SafeBox", font=("Segoe UI", 24, "bold"))
        title.pack(pady=(25, 10))

        subtitle = ctk.CTkLabel(self, text="Secure. Destroy. Protect.", font=("Segoe UI", 14, "italic"))
        subtitle.pack(pady=(0, 20))

        file_frame = ctk.CTkFrame(self, fg_color="transparent")
        file_frame.pack(pady=10)
        ctk.CTkLabel(file_frame, text="File Path:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=(0, 10))
        self.file_entry = ctk.CTkEntry(file_frame, textvariable=self.file_path, width=300)
        self.file_entry.grid(row=0, column=1)
        ctk.CTkButton(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=10)

        pw_frame = ctk.CTkFrame(self, fg_color="transparent")
        pw_frame.pack(pady=10)
        ctk.CTkLabel(pw_frame, text="Password:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=(0, 10))
        self.pw_entry = ctk.CTkEntry(pw_frame, textvariable=self.password, show="*", width=300)
        self.pw_entry.grid(row=0, column=1)

        ctk.CTkLabel(self, text="Mode:", font=("Segoe UI", 12)).pack(pady=(15, 5))
        ctk.CTkSegmentedButton(self, values=["encrypt", "decrypt"], variable=self.mode).pack()

        ctk.CTkCheckBox(self, text="💣 Auto-delete after decryption", variable=self.auto_delete).pack(pady=15)

        ctk.CTkButton(self, text="🚀 Execute", command=self.run, width=220, height=40, font=("Segoe UI", 14, "bold")).pack(pady=20)

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path.set(path)

    def run(self):
        check_lock()
        path = self.file_path.get()
        pwd = self.password.get()

        if not os.path.exists(path):
            messagebox.showerror("Error", "Selected file does not exist.")
            return
        if not pwd:
            messagebox.showerror("Error", "Password is required.")
            return

        try:
            if self.mode.get() == "encrypt":
                result = encrypt_and_map(path, pwd)
                messagebox.showinfo("Success", f"✅ Encrypted as:\n{result}")
            else:
                success = decrypt_and_handle(path, pwd, self.auto_delete.get())
                if success:
                    messagebox.showinfo("Success", "✅ Decryption successful.")
                else:
                    messagebox.showerror("Failed", "❌ Decryption failed or file destroyed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = SafeBoxApp()
    app.mainloop()