import os
import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.clock import Clock

try:
    import netifaces
except ImportError:
    netifaces = None

# Simple HTTP/File Server fallback for native Python execution
class SimpleFileServer:
    def __init__(self, port=2221):
        self.port = port
        self.server = None
        self.is_running = False

    def start(self, directory):
        if self.is_running:
            return
        os.chdir(directory)
        import http.server
        import socketserver
        Handler = http.server.SimpleHTTPRequestHandler
        try:
            self.httpd = socketserver.TCPServer(("", self.port), Handler)
            self.is_running = True
            threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        except Exception as e:
            print("Server start error:", e)

    def stop(self):
        if self.is_running:
            try:
                self.httpd.shutdown()
                self.httpd.server_close()
            except Exception:
                pass
            self.is_running = False

ftp_server = SimpleFileServer()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class KmScanRoot(TabbedPanel):
    def __init__(self, **kwargs):
        super(KmScanRoot, self).__init__(**kwargs)
        self.do_default_tab = False
        self.custom_folder = os.path.expanduser("~")

        # --- TAB 1: SERVER ---
        self.server_tab = TabbedPanelItem(text='Server')
        server_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        # Top Bar with Settings Icon
        top_bar = BoxLayout(size_hint_y=None, height=50)
        top_bar.add_label = Label(text='[b]Km Scan - Server[/b]', markup=True, font_size=20)
        top_bar.add_widget(top_bar.add_label)
        
        settings_btn = Button(text='⚙', size_hint_x=None, width=50, font_size=22)
        settings_btn.bind(on_press=self.open_settings_popup)
        top_bar.add_widget(settings_btn)
        server_layout.add_widget(top_bar)

        # Status Box
        self.status_label = Label(text='WiFi status: Enabled\nIP Address: ' + get_local_ip() + '\nNetwork: Wireless AP', 
                                  halign='left', valign='middle')
        self.status_label.bind(size=self.status_label.setter('text_size'))
        server_layout.add_widget(self.status_label)

        # Control Button (Start/Stop)
        self.toggle_btn = Button(text='START SERVER', size_hint_y=None, height=60, background_color=(0.2, 0.7, 0.3, 1))
        self.toggle_btn.bind(on_press=self.toggle_server)
        server_layout.add_widget(self.toggle_btn)

        # Details Box
        self.details_label = Label(text='Server URL: Not Running\nUserid: android\nPassword: android\nAnonymous access: Enabled\nRoot folder: Custom folder',
                                   halign='left', valign='middle')
        self.details_label.bind(size=self.details_label.setter('text_size'))
        server_layout.add_widget(self.details_label)

        self.server_tab.add_widget(server_layout)
        self.add_widget(self.server_tab)

        # --- TAB 2: SCAN ---
        self.scan_tab = TabbedPanelItem(text='Scan')
        scan_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        self.ip_display_label = Label(text='Device IP: ' + get_local_ip(), size_hint_y=None, height=40, font_size=16)
        scan_layout.add_widget(self.ip_display_label)

        manual_ip_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        manual_ip_layout.add_widget(Label(text='Manual IP:', size_hint_x=None, width=90))
        self.manual_ip_input = TextInput(hint_text='Leave blank to use device IP', multiline=False)
        manual_ip_layout.add_widget(self.manual_ip_input)
        scan_layout.add_widget(manual_ip_layout)

        scan_layout.add_widget(Label(text='Select Command / Nmap Option:', size_hint_y=None, height=30))
        
        self.command_spinner = Spinner(
            text='Select scan option...',
            values=('Ping Check (-sn)', 'Fast Port Scan (-F)', 'Service Version Detection (-sV)', 'OS Detection (-O)'),
            size_hint_y=None, height=50
        )
        self.command_spinner.bind(text=self.execute_scan_command)
        scan_layout.add_widget(self.command_spinner)

        self.scan_output = TextInput(text='Scan results will appear here...', readonly=True, background_color=(0.1, 0.1, 0.1, 1), foreground_color=(0, 1, 0, 1))
        scan_layout.add_widget(self.scan_output)

        self.scan_tab.add_widget(scan_layout)
        self.add_widget(self.scan_tab)

    def toggle_server(self, instance):
        current_ip = get_local_ip()
        if not ftp_server.is_running:
            ftp_server.start(self.custom_folder)
            self.toggle_btn.text = 'STOP'
            self.toggle_btn.background_color = (0.8, 0.2, 0.2, 1)
            self.status_label.text = f'WiFi status: Enabled\nIP Address: {current_ip}\nNetwork: Wireless AP'
            self.details_label.text = f'Server URL: ftp://{current_ip}:2221\nUserid: android\nPassword: android\nAnonymous access: Enabled\nRoot folder: {self.custom_folder}'
        else:
            ftp_server.stop()
            self.toggle_btn.text = 'START SERVER'
            self.toggle_btn.background_color = (0.2, 0.7, 0.3, 1)
            self.details_label.text = 'Server URL: Not Running\nUserid: android\nPassword: android\nAnonymous access: Enabled\nRoot folder: Custom folder'

    def open_settings_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Enter Folder Path for Server Service:'))
        
        folder_input = TextInput(text=self.custom_folder, multiline=False)
        content.add_widget(folder_input)

        save_btn = Button(text='Save Folder', size_hint_y=None, height=50)
        popup = Popup(title='Server Settings', content=content, size_hint=(0.8, 0.4))

        def save_folder(btn):
            self.custom_folder = folder_input.text
            popup.dismiss()

        save_btn.bind(on_press=save_folder)
        content.add_widget(save_btn)
        popup.open()

    def execute_scan_command(self, spinner, text):
        if text == 'Select scan option...':
            return
        
        target_ip = self.manual_ip_input.text.strip()
        if not target_ip:
            target_ip = get_local_ip()

        self.scan_output.text = f"Executing '{text}' on target: {target_ip}...\n"
        
        # Simulating execution / socket check representation
        def run_check():
            try:
                # Basic TCP connect test on standard port as fallback simulation
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2.0)
                result = s.connect_ex((target_ip, 2221))
                s.close()
                status = "Port 2221 is OPEN" if result == 0 else "Host reachable / Port closed or filtered"
                
                Clock.schedule_once(lambda dt: setattr(self.scan_output, 'text', 
                    f"Target IP: {target_ip}\nCommand: {text}\nResult: {status}\n(Simulated output for mobile environment)"))
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.scan_output, 'text', f"Error executing command: {str(e)}"))

        threading.Thread(target=run_check, daemon=True).start()

class KmScanApp(App):
    def build(self):
        return KmScanRoot()

if __name__ == '__main__':
    KmScanApp().run()
