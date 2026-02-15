import customtkinter as ctk
from blocker_manager import BlockerManager
import tkinter.messagebox as messagebox
import threading
import time

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CyberBarrierApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CyberBarrier")
        self.geometry("700x600")
        
        # Initialize Backend
        self.blocker = BlockerManager()

        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (Navigation/Stats)
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Cyber\nBarrier", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.stats_label = ctk.CTkLabel(self.sidebar_frame, text="Active Blocks:\n0", font=ctk.CTkFont(size=14))
        self.stats_label.grid(row=1, column=0, padx=20, pady=20)

        self.flush_btn = ctk.CTkButton(self.sidebar_frame, text="Flush DNS", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.flush_dns)
        self.flush_btn.grid(row=2, column=0, padx=20, pady=10)
        
        # Main Content Area
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Input Area
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="www.example.com", height=40, font=ctk.CTkFont(size=14))
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(20, 10), pady=20)
        
        self.block_button = ctk.CTkButton(self.input_frame, text="BLOCK ACCESS", height=40, font=ctk.CTkFont(size=14, weight="bold"), fg_color="#c0392b", hover_color="#e74c3c", command=self.block_website)
        self.block_button.pack(side="right", padx=(0, 20), pady=20)

        # Blocked List
        self.list_label = ctk.CTkLabel(self.main_frame, text="Protected Zone (Blocked Sites)", font=ctk.CTkFont(size=16, weight="bold"))
        self.list_label.grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.list_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="")
        self.list_frame.grid(row=2, column=0, sticky="nsew")

        # Notification Label (bottom)
        self.notification_label = ctk.CTkLabel(self.main_frame, text="", text_color="gray")
        self.notification_label.grid(row=3, column=0, pady=10)

        self.refresh_list()

    def show_notification(self, message, is_error=False):
        color = "#e74c3c" if is_error else "#2ecc71"
        self.notification_label.configure(text=message, text_color=color)
        # Auto-hide after 3 seconds
        self.after(3000, lambda: self.notification_label.configure(text=""))

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        blocked_sites = self.blocker.get_blocked_sites()
        self.stats_label.configure(text=f"Active Blocks:\n{len(blocked_sites)}")

        if not blocked_sites:
             label = ctk.CTkLabel(self.list_frame, text="No active barriers.", font=ctk.CTkFont(slant="italic"))
             label.pack(pady=20)
             return

        for site in blocked_sites:
            self.create_list_item(site)

    def create_list_item(self, site):
        item_frame = ctk.CTkFrame(self.list_frame, fg_color=("gray80", "gray25"))
        item_frame.pack(fill="x", pady=5, padx=5)
        
        label = ctk.CTkLabel(item_frame, text=site, font=ctk.CTkFont(size=14))
        label.pack(side="left", padx=15, pady=10)
        
        unblock_btn = ctk.CTkButton(item_frame, text="ALLOW", width=80, height=30, fg_color="transparent", border_width=1, border_color="#e74c3c", text_color="#e74c3c", hover_color="#e74c3c", 
                                    command=lambda s=site: self.unblock_website(s))
        unblock_btn.pack(side="right", padx=15, pady=10)

    def block_website(self):
        url = self.url_entry.get()
        if not url:
            self.show_notification("Please enter a URL first.", is_error=True)
            return

        success = self.blocker.block_site(url)
        if success:
            self.url_entry.delete(0, 'end')
            self.refresh_list()
            self.show_notification(f"Access to {url} blocked.")
        else:
            self.show_notification("Failed. Run as Admin.", is_error=True)

    def unblock_website(self, site):
        success = self.blocker.unblock_site(site)
        if success:
            self.refresh_list()
            self.show_notification(f"Access to {site} restored.")
        else:
            self.show_notification("Failed. Run as Admin.", is_error=True)
            
    def flush_dns(self):
        self.blocker._flush_dns()
        self.show_notification("DNS Cache Flushed.")

if __name__ == "__main__":
    app = CyberBarrierApp()
    app.mainloop()
