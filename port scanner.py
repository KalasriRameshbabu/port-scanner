
import socket
import threading
from queue import Queue
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Port scanning logic
def scan_port(ip, port, output_text, open_ports):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        if result == 0:
            output_text.insert(tk.END, f"✅ Port {port} is OPEN\n")
            open_ports.append(port)
        s.close()
    except:
        pass

def threader(ip, output_text, open_ports, q):
    while True:
        worker = q.get()
        scan_port(ip, worker, output_text, open_ports)
        q.task_done()

# GUI Logic
def start_scan():
    target = ip_entry.get().strip()
    if not target:
        messagebox.showerror("Input Error", "Please enter a target IP or domain.")
        return

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        messagebox.showerror("Error", "Invalid IP or domain.")
        return

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Scanning {ip} for open ports (1-1024)...\n")

    open_ports = []
    q = Queue()

    for x in range(100):
        t = threading.Thread(target=threader, args=(ip, output_text, open_ports, q))
        t.daemon = True
        t.start()

    for port in range(1, 1025):
        q.put(port)

    def finish():
        q.join()
        output_text.insert(tk.END, "\n🔎 Scan Complete\n")
        if open_ports:
            output_text.insert(tk.END, "Open ports: " + ", ".join(map(str, open_ports)))
        else:
            output_text.insert(tk.END, "No open ports found.")

    threading.Thread(target=finish).start()

# Build GUI
window = tk.Tk()
window.title("Port Scanner")
window.geometry("500x400")
window.config(bg="#e6f2ff")

# Heading
tk.Label(window, text="Port Scanner", font=("Segoe UI", 20, "bold"), bg="#e6f2ff", fg="#2c3e50").pack(pady=20)

# IP input
tk.Label(window, text="Enter target IP or domain:", font=("Segoe UI", 14), bg="#e6f2ff").pack()
ip_entry = tk.Entry(window, font=("Segoe UI", 14), width=30)
ip_entry.pack(pady=10)

# Scan button
tk.Button(window, text="Start Scan", command=start_scan, font=("Segoe UI", 12, "bold"), bg="#007bff", fg="white", width=20).pack(pady=10)

# Output box
tk.Label(window, text="Scan Output:", font=("Segoe UI", 13), bg="#e6f2ff").pack(pady=(10, 5))
output_text = tk.Text(window, font=("Segoe UI", 11), width=55, height=10, wrap="word", bg="#f0f5f5", relief="sunken", bd=2)
output_text.pack(pady=10)

# Run the app
window.mainloop()
