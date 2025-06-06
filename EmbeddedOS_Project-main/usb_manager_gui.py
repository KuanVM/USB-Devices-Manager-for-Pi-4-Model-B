import tkinter as tk
from tkinter import ttk, messagebox
import dbus

def get_devices():
    try:
        bus = dbus.SystemBus()
        usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
        return usb_manager.ListDevices(dbus_interface='org.example.USBManager')
    except Exception as e:
        messagebox.showerror("Lỗi DBus", f"Không thể kết nối DBus: {e}\nHãy chắc chắn service đang chạy!")
        return []

def refresh_table(tree):
    for row in tree.get_children():
        tree.delete(row)
    devices = get_devices()
    if not devices:
        return
    for dev in devices:
        tree.insert('', 'end', values=(
            dev.get('id'),
            dev.get('name'),
            dev.get('status'),
            dev.get('serial')
        ))

def mount_selected(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("Thông báo", "Chọn thiết bị để mount")
        return
    dev_id = tree.item(selected[0])['values'][0]
    try:
        bus = dbus.SystemBus()
        usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
        result = usb_manager.MountDevice(dev_id, dbus_interface='org.example.USBManager')
        messagebox.showinfo("Kết quả", "Mount thành công!" if result else "Mount thất bại!")
    except Exception as e:
        messagebox.showerror("Lỗi DBus", f"Không thể mount: {e}")
    refresh_table(tree)

def unmount_selected(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("Thông báo", "Chọn thiết bị để unmount")
        return
    dev_id = tree.item(selected[0])['values'][0]
    try:
        bus = dbus.SystemBus()
        usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
        result = usb_manager.UnmountDevice(dev_id, dbus_interface='org.example.USBManager')
        messagebox.showinfo("Kết quả", "Unmount thành công!" if result else "Unmount thất bại!")
    except Exception as e:
        messagebox.showerror("Lỗi DBus", f"Không thể unmount: {e}")
    refresh_table(tree)

root = tk.Tk()
root.title("USB Manager GUI")

tree = ttk.Treeview(root, columns=('ID', 'Tên', 'Trạng thái', 'Serial'), show='headings')
for col in ('ID', 'Tên', 'Trạng thái', 'Serial'):
    tree.heading(col, text=col)
tree.pack(fill='both', expand=True)

btn_frame = tk.Frame(root)
btn_frame.pack(fill='x')
tk.Button(btn_frame, text="Refresh", command=lambda: refresh_table(tree)).pack(side='left')
tk.Button(btn_frame, text="Mount", command=lambda: mount_selected(tree)).pack(side='left')
tk.Button(btn_frame, text="Unmount", command=lambda: unmount_selected(tree)).pack(side='left')

refresh_table(tree)
root.mainloop()