import tkinter as tk
import os
import subprocess
import winreg
import time
import sys
from tkinter import messagebox, filedialog  # Import messagebox and filedialog for better UI

# --- Cấu hình ---
DEFAULT_TLP_FILENAME = r"C:\Users\Luvideez\Desktop\ditucogivui.tlp" # Đường dẫn file TLP mặc định
BITVISE_EXECUTABLE_NAME = "BvSsh.exe" # Define process name for taskkill

start_time = None
timer_running = False
tlp_file_path = DEFAULT_TLP_FILENAME # Mặc định là file TLP theo đường dẫn cứng

def bat_socks_action():
    """Bật Socks: Chạy file TLP, thiết lập Proxy, bắt đầu timer."""
    global start_time, timer_running, tlp_file_path

    if timer_running:
        messagebox.showinfo("Thông báo", "Socks đang hoạt động rồi!")
        return

    status_label.config(text="Đang bật Socks...")

    # --- Kiểm tra file TLP ---
    if not os.path.exists(tlp_file_path):
        status_label.config(text=f"Lỗi: Không tìm thấy file cấu hình TLP: {tlp_file_path}")
        messagebox.showerror("Lỗi", f"Không tìm thấy file cấu hình TLP:\n{tlp_file_path}\nVui lòng đảm bảo file này tồn tại hoặc chọn lại file.")
        return

    # --- Chạy file TLP ---
    status_label.config(text="Đang chạy cấu hình VPN...")
    try:
        os.startfile(tlp_file_path) # Chạy file TLP trực tiếp
        time.sleep(2) # Chờ TLP file xử lý (có thể cần điều chỉnh thời gian)
    except Exception as e:
        status_label.config(text=f"Lỗi chạy file TLP: {e}")
        messagebox.showerror("Lỗi", f"Lỗi không xác định khi chạy file TLP:\n{e}")
        return

    # --- Bật Proxy Server ---
    status_label.config(text="Đang thiết lập Proxy Server...")
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "127.0.0.1:9999")
        status_label.config(text="Socks đã bật và Proxy Server đã thiết lập.")
    except Exception as e:
        status_label.config(text=f"Lỗi bật Proxy: {e}")
        messagebox.showerror("Lỗi", f"Lỗi khi bật Proxy Server:\n{e}\nVui lòng kiểm tra quyền truy cập Registry.")
        return

    start_time = time.time()
    timer_running = True
    update_timer()
    status_label.config(text="Socks đã bật và Proxy Server đã thiết lập. Đang hoạt động...")

def tat_socks_action():
    """Tắt Socks: Tắt Proxy, dừng Bitvise, đóng ứng dụng."""
    global timer_running
    status_label.config(text="Đang tắt Socks...")
    timer_running = False # Dừng timer

    # --- Tắt Proxy ---
    status_label.config(text="Đang tắt Proxy Server...")
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            try:
                winreg.DeleteValue(key, "ProxyServer") # Xóa giá trị ProxyServer
            except FileNotFoundError:
                pass # Không có ProxyServer cũng không sao
        status_label.config(text="Proxy Server đã tắt.")
    except Exception as e:
        status_label.config(text=f"Lỗi tắt Proxy: {e}")
        messagebox.showerror("Lỗi", f"Lỗi khi tắt Proxy Server:\n{e}\nVui lòng kiểm tra quyền truy cập Registry.")
        return

    # --- Dừng Bitvise ---
    status_label.config(text="Đang dừng Bitvise...")
    try:
        subprocess.run(['taskkill', '/F', '/IM', BITVISE_EXECUTABLE_NAME], check=False, creationflags=subprocess.CREATE_NO_WINDOW)
        status_label.config(text="Bitvise SSH Client đã dừng.")
    except Exception as e:
        status_label.config(text=f"Lỗi dừng Bitvise: {e}")
        messagebox.showerror("Lỗi", f"Lỗi khi dừng Bitvise SSH Client:\n{e}")

    status_label.config(text="Socks đã tắt và Proxy Server đã tắt. Ứng dụng sẽ đóng sau 2 giây...")
    window.after(2000, window.destroy)

def thoat_action():
    """Thoát ứng dụng."""
    global timer_running
    timer_running = False
    window.destroy()

def update_timer():
    """Cập nhật đồng hồ đếm thời gian."""
    global timer_running, start_time
    if timer_running and start_time:
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        hours, minutes = divmod(minutes, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        timer_label.config(text=f"Thời gian hoạt động: {time_str}")
        window.after(1000, update_timer)
    else:
        timer_label.config(text="Thời gian hoạt động: Đã tắt")

def choose_tlp_file():
    """Mở hộp thoại chọn file TLP."""
    global tlp_file_path
    file_path = filedialog.askopenfilename(
        defaultextension=".tlp",
        filetypes=[("TLP Files", "*.tlp"), ("All Files", "*.*")],
        title="Chọn file cấu hình Bitvise (.tlp)"
    )
    if file_path:
        tlp_file_path = file_path
        tlp_file_label.config(text=f"File TLP: {os.path.basename(tlp_file_path)}") # Chỉ hiển thị tên file
        print(f"Đã chọn file TLP: {tlp_file_path}") # Debug

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Bật VPN - Socks")
    window.geometry("350x400") # Tăng chiều cao để chứa thêm label file TLP

    try:
        if os.path.exists(ICON_FILENAME):
            window.iconbitmap(ICON_FILENAME)
    except Exception as e:
        print(f"Lỗi tải icon: {e}") # In lỗi nếu tải icon thất bại, nhưng không làm chương trình crash

    # --- Frame nội dung ---
    content_frame = tk.Frame(window)
    content_frame.pack(pady=20)

    software_label = tk.Label(content_frame, text="Phần mềm bật/tắt Socks VPN")
    software_label.pack()

    author_label = tk.Label(content_frame, text="Viết bởi: Luvideez")
    author_label.pack()

    server_label = tk.Label(content_frame, text="Server: ditucogivui.com") # Removed "(Ví dụ)"
    server_label.pack()

    tiktok_label = tk.Label(content_frame, text="Tiktok: ditucogivui") # Removed "(Ví dụ)"
    tiktok_label.pack()

    email_label = tk.Label(content_frame, text="Email: luvideez@outlook.com") # Removed "(Ví dụ)"
    email_label.pack()

    # --- Label hiển thị đường dẫn file TLP ---
    tlp_file_frame = tk.Frame(window)
    tlp_file_frame.pack(pady=5)
    tlp_file_label = tk.Label(tlp_file_frame, text=f"File TLP: {os.path.basename(DEFAULT_TLP_FILENAME)}") # Chỉ hiển thị tên file
    tlp_file_label.pack(side=tk.LEFT)
    choose_tlp_button = tk.Button(tlp_file_frame, text="Chọn File TLP", command=choose_tlp_file)
    choose_tlp_button.pack(side=tk.LEFT, padx=5)


    # --- Status Label ---
    status_label = tk.Label(window, text="")
    status_label.pack(pady=10)

    # --- Timer Label ---
    timer_label = tk.Label(window, text="Thời gian hoạt động: Đã tắt")
    timer_label.pack(pady=5)

    # --- Button Frame ---
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    button_bat_socks = tk.Button(button_frame, text="Bật Socks", command=bat_socks_action)
    button_tat_socks = tk.Button(button_frame, text="Tắt Socks", command=tat_socks_action)
    button_thoat = tk.Button(button_frame, text="Thoát", command=thoat_action)

    button_bat_socks.pack(side=tk.LEFT, padx=5)
    button_tat_socks.pack(side=tk.LEFT, padx=5)
    button_thoat.pack(side=tk.LEFT, padx=5)

    window.mainloop()
