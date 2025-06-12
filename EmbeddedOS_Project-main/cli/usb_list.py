import dbus

bus = dbus.SystemBus()
usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
devices = usb_manager.ListDevices(dbus_interface='org.example.USBManager')

print(f"{'Vendor':20} {'Product':25} {'VendorID':8} {'ProductID':9} {'Status':10} {'Serial'}")
for dev in devices:
    dev = dict(dev)
    print(f"{dev.get('vendor',''):20} {dev.get('product',''):25} {dev.get('vendor_id',''):8} {dev.get('product_id',''):9} {dev.get('status',''):10} {dev.get('serial','')}")