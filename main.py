from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import platform

# Import logic from parent directory (requires path hacking or proper structure)
import sys
import os

# Add parent dir to sys.path to find blocker_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blocker_manager import BlockerManager

class CyberBarrierAndroid(App):
    def build(self):
        self.blocker = BlockerManager()
        self.title = "CyberBarrier Mobile"
        
        # Main Layout
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(text="CyberBarrier", font_size='24sp', size_hint_y=None, height=50, bold=True)
        root.add_widget(header)
        
        # Input Area
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.url_input = TextInput(hint_text="example.com", multiline=False)
        btn_block = Button(text="BLOCK", size_hint_x=None, width=100, background_color=(0.9, 0.3, 0.3, 1))
        btn_block.bind(on_press=self.do_block)
        
        input_layout.add_widget(self.url_input)
        input_layout.add_widget(btn_block)
        root.add_widget(input_layout)

        # Server Sync Area
        sync_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.server_input = TextInput(hint_text="Server IP:8000", multiline=False)
        btn_sync = Button(text="SYNC", size_hint_x=None, width=100, background_color=(0.3, 0.3, 0.9, 1))
        btn_sync.bind(on_press=self.do_sync)
        
        sync_layout.add_widget(self.server_input)
        sync_layout.add_widget(btn_sync)
        root.add_widget(sync_layout)
        
        # Status Label
        self.status_label = Label(text="Ready", size_hint_y=None, height=30, color=(0.7, 0.7, 0.7, 1))
        root.add_widget(self.status_label)
        
        # List Header
        list_header = Label(text="Blocked Sites", size_hint_y=None, height=40, bold=True)
        root.add_widget(list_header)
        
        # Scrollable List
        self.scroll_view = ScrollView()
        self.list_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        
        self.scroll_view.add_widget(self.list_layout)
        root.add_widget(self.scroll_view)
        
        self.refresh_list()
        
        return root

    def refresh_list(self):
        self.list_layout.clear_widgets()
        sites = self.blocker.get_blocked_sites()
        
        if not sites:
            self.list_layout.add_widget(Label(text="No active blocks", size_hint_y=None, height=40))
        
        for site in sites:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            lbl = Label(text=site)
            btn_unblock = Button(text="X", size_hint_x=None, width=40, background_color=(0.5, 0.5, 0.5, 1))
            btn_unblock.bind(on_press=lambda x, s=site: self.do_unblock(s))
            
            row.add_widget(lbl)
            row.add_widget(btn_unblock)
            self.list_layout.add_widget(row)

    def do_sync(self, instance):
        server_url = self.server_input.text
        if not server_url:
             self.status_label.text = "Enter Server URL"
             return
             
        self.status_label.text = "Syncing..."
        
        # Run in thread to avoid freezing UI
        import threading
        def sync_thread():
            new_blocks = self.blocker.fetch_from_server(server_url)
            if new_blocks is None:
                self.status_label.text = "Sync Failed"
            else:
                count = len(new_blocks)
                self.status_label.text = f"Synced. Added {count} new."
                # Schedule UI update on main thread
                # (Kivy requires UI updates on main thread, but this simple label set might be unsafe. 
                # Ideally use Clock.schedule_once)
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: self.refresh_list(), 0)

        threading.Thread(target=sync_thread).start()

    def do_block(self, instance):
        url = self.url_input.text
        if not url:
            self.status_label.text = "Please enter a URL"
            return
            
        success = self.blocker.block_site(url)
        if success:
            self.url_input.text = ""
            self.status_label.text = f"Blocked {url}"
            self.refresh_list()
        else:
            self.status_label.text = "Failed (Root required?)"

    def do_unblock(self, site):
        success = self.blocker.unblock_site(site)
        if success:
            self.status_label.text = f"Unblocked {site}"
            self.refresh_list()
        else:
             self.status_label.text = "Failed to unblock"

if __name__ == '__main__':
    CyberBarrierAndroid().run()
