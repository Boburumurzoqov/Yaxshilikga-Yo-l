import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QLabel, QListWidget, QGroupBox, QPushButton,
    QDialog, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux Buyruqlar Qo'llanmasi")
        self.setWindowIcon(QIcon.fromTheme("help-contents"))
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout()
        
        # Foydali buyruqlar bo'limi
        commands = {
            "Fayl tizimi": {
                "ls": "Joriy katalogdagi fayllarni ko'rsatish",
                "cd": "Katalogni o'zgartirish",
                "pwd": "Joriy ish katalogini ko'rsatish",
                "cp": "Fayllarni nusxalash",
                "mv": "Fayllarni ko'chirish yoki nomini o'zgartirish",
                "rm": "Fayllarni o'chirish",
                "mkdir": "Yangi katalog yaratish",
                "rmdir": "Bo'sh katalogni o'chirish",
                "chmod": "Fayl ruxsatlarini o'zgartirish",
                "chown": "Fayl egasini o'zgartirish"
            },
            "Tizim ma'lumotlari": {
                "uname -a": "Tizim haqida batafsil ma'lumot",
                "df -h": "Diskdan foydalanishni ko'rsatish",
                "free -h": "Xotira holatini ko'rsatish",
                "top": "Ishlayotgan jarayonlarni ko'rsatish",
                "ps aux": "Barcha jarayonlarni ko'rsatish",
                "kill": "Jarayonni to'xtatish"
            },
            "Tarmoq operatsiyalari": {
                "ping": "Tarmoq ulanishini tekshirish",
                "ifconfig": "Tarmoq interfeyslari haqida ma'lumot",
                "netstat": "Tarmoq ulanishlari va portlarni ko'rsatish",
                "ssh": "Uzoq serverga ulanish",
                "scp": "Fayllarni uzoq serverga nusxalash",
                "wget": "Internetdan fayl yuklab olish",
                "curl": "URL dan ma'lumot olish"
            },
            "Matn bilan ishlash": {
                "grep": "Matn ichidan qidirish",
                "cat": "Fayl mazmunini ko'rsatish",
                "less": "Faylni sahifalab ko'rsatish",
                "head": "Fayl boshidan bir necha satrni ko'rsatish",
                "tail": "Fayl oxiridan bir necha satrni ko'rsatish",
                "sort": "Satrlarni tartiblash",
                "uniq": "Takrorlangan satrlarni olib tashlash"
            },
            "Paketlar boshqaruvi": {
                "apt update": "Paketlar ro'yxatini yangilash (Debian/Ubuntu)",
                "apt upgrade": "Paketlarni yangilash (Debian/Ubuntu)",
                "apt install": "Yangi paket o'rnatish (Debian/Ubuntu)",
                "yum update": "Paketlarni yangilash (RHEL/CentOS)",
                "yum install": "Yangi paket o'rnatish (RHEL/CentOS)",
                "dnf install": "Yangi paket o'rnatish (Fedora)",
                "pacman -S": "Yangi paket o'rnatish (Arch)"
            }
        }
        
        for category, items in commands.items():
            group = QGroupBox(category)
            group_layout = QVBoxLayout()
            
            for cmd, desc in items.items():
                label = QLabel(f"<b>{cmd}</b>: {desc}")
                label.setMargin(5)
                group_layout.addWidget(label)
            
            group.setLayout(group_layout)
            content_layout.addWidget(group)
        
        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        close_btn = QPushButton("Yopish")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class NetworkDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarmoq Operatsiyalari")
        self.setWindowIcon(QIcon.fromTheme("network-wired"))
        self.setMinimumSize(700, 500)
        
        layout = QVBoxLayout()
        
        # Tarmoq ma'lumotlari
        self.network_info = QTextEdit()
        self.network_info.setReadOnly(True)
        self.network_info.setFont(QFont("Consolas", 10))
        
        # Tarmoq buyruqlari tugmalari
        btn_layout = QHBoxLayout()
        
        btn_ping = QPushButton("Ping Test")
        btn_ping.clicked.connect(self.run_ping_test)
        
        btn_ifconfig = QPushButton("Interfeyslar")
        btn_ifconfig.clicked.connect(self.run_ifconfig)
        
        btn_netstat = QPushButton("Faol Ulanishlar")
        btn_netstat.clicked.connect(self.run_netstat)
        
        btn_ports = QPushButton("Ochiq Portlar")
        btn_ports.clicked.connect(self.check_open_ports)
        
        btn_layout.addWidget(btn_ping)
        btn_layout.addWidget(btn_ifconfig)
        btn_layout.addWidget(btn_netstat)
        btn_layout.addWidget(btn_ports)
        
        layout.addLayout(btn_layout)
        layout.addWidget(self.network_info)
        
        # Natijalarni tozalash tugmasi
        btn_clear = QPushButton("Natijalarni Tozalash")
        btn_clear.clicked.connect(lambda: self.network_info.clear())
        layout.addWidget(btn_clear)
        
        self.setLayout(layout)
        self.update_network_info()
    
    def update_network_info(self):
        self.run_command("ifconfig", "Tarmoq interfeyslari:")
    
    def run_command(self, cmd, title):
        try:
            result = subprocess.check_output(cmd, shell=True, text=True)
            self.network_info.append(f"=== {title} ===\n{result}\n")
        except subprocess.CalledProcessError as e:
            self.network_info.append(f"Xato: {cmd}\n{e.output}\n")
    
    def run_ping_test(self):
        host, ok = QInputDialog.getText(self, "Ping Test", "Ping uchun manzil (masalan: google.com):")
        if ok and host:
            self.run_command(f"ping -c 4 {host}", f"Ping natijalari: {host}")
    
    def run_ifconfig(self):
        self.run_command("ifconfig", "Tarmoq interfeyslari")
    
    def run_netstat(self):
        self.run_command("netstat -tuln", "Faol tarmoq ulanishlari")
    
    def check_open_ports(self):
        self.run_command("ss -tuln", "Ochiq portlar")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zamoniy Terminal GUI")
        self.setWindowIcon(QIcon.fromTheme("utilities-terminal"))
        self.setMinimumSize(1280, 720)
        self.setStyleSheet("""
            QGroupBox { font-weight: bold; }
            QPushButton { padding: 5px; }
        """)
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Qidiruv paneli
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Tizim ma'lumotlari yoki buyruqlarni qidirish...")
        self.search_bar.setFixedHeight(35)
        self.search_bar.setStyleSheet("padding-left: 12px; font-size: 15px;")
        main_layout.addWidget(self.search_bar)

        # Asosiy kontent
        content_layout = QHBoxLayout()

        # Chap: Tizim ma'lumotlari
        self.system_info_group = QGroupBox("Tizim Ma'lumotlari")
        self.system_info_group.setMinimumWidth(250)
        sys_info_layout = QVBoxLayout()
        
        # Tugmalar qatori
        btn_layout = QHBoxLayout()
        
        self.btn_help = QPushButton("Yordam")
        self.btn_help.setIcon(QIcon.fromTheme("help-contents"))
        self.btn_help.clicked.connect(self.show_help)
        
        self.btn_network = QPushButton("Tarmoq")
        self.btn_network.setIcon(QIcon.fromTheme("network-wired"))
        self.btn_network.clicked.connect(self.show_network_tools)
        
        btn_layout.addWidget(self.btn_help)
        btn_layout.addWidget(self.btn_network)
        sys_info_layout.addLayout(btn_layout)
        
        self.system_info_list = QListWidget()
        sys_info_layout.addWidget(self.system_info_list)
        self.system_info_group.setLayout(sys_info_layout)
        content_layout.addWidget(self.system_info_group)

        # Markaz: Terminal
        center_layout = QVBoxLayout()
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setFont(QFont("Consolas", 12))
        self.terminal_output.setStyleSheet("background-color: #1e1e1e; color: #00ffcc;")

        self.terminal_input = QLineEdit()
        self.terminal_input.setPlaceholderText("Linux buyrug'ini kiriting...")
        self.terminal_input.setFont(QFont("Consolas", 11))
        self.terminal_input.setStyleSheet("background-color: #2e2e2e; color: white; padding-left: 10px;")
        self.terminal_input.returnPressed
        self.terminal_input.returnPressed.connect(self.run_terminal_command)

        center_layout.addWidget(self.terminal_output)
        center_layout.addWidget(self.terminal_input)

        content_layout.addLayout(center_layout)

        main_layout.addLayout(content_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.load_system_info()

    def run_terminal_command(self):
        command = self.terminal_input.text().strip()
        if not command:
            return 
        self.terminal_output.append(f"$ {command}")
        try:
            output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
            self.terminal_output.append(output)
        except subprocess.CalledProcessError as e:
            self.terminal_output.append(f"Xato: {e.output}")
        self.terminal_input.clear()

    def load_system_info(self):
        try:
            uname_output = subprocess.check_output("uname -a", shell=True, text=True)
            self.system_info_list.addItem(f"Tizim: {uname_output.strip()}")
            cpu_output = subprocess.check_output("lscpu | grep ‘Model name’", shell=True, text=True)
            self.system_info_list.addItem(cpu_output.strip())
            mem_output = subprocess.check_output("free -h | grep Mem", shell=True, text=True)
            self.system_info_list.addItem(f"Xotira: {mem_output.strip()}")
        except subprocess.CalledProcessError:
            self.system_info_list.addItem("Tizim ma’lumotlarini yuklashda xatolik yuz berdi.")

    def show_help(self):
        help_dialog = HelpDialog()
        help_dialog.exec()

    def show_network_tools(self):
        network_dialog = NetworkDialog()
        network_dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
