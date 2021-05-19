# lib_photo_scanner
Scanner library using TWAIN in Windows and SANE in MAC/Linux

# For Windows 

To install Driver: 
1. Download and install the corresponding driver of the device 
    For example: 
    1. Fujitsu: [Link](https://imagescanner.fujitsu.com/global/dl/)
        Then Download PaperStream IP (TWAIN) 
    2. To be continue 

2. Install it 

To install TWAIN 
1. Step 1: Download **twain-dsm** here [Link](https://sourceforge.net/projects/twain-dsm/)
2. Step 2: Copy DLL of 64 bit (Or 32 bit) to: 
    1. C://Windows/
    2. C://Windows/System32/
    3. C://Windows/SysWOW64 

To build the service
```bash
pyinstaller --onefile --hidden-import win32timezone win32_service.py
```

To install the sevice
```bash
./dist/win32_service.exe install
```

To start the sevice
```bash
./dist/win32_service.exe start
```

To stop the sevice
```bash
./dist/win32_service.exe stop
```

To remove the sevice
```bash
./dist/win32_service.exe remove
```

# For Mac

Install Sane Backends, SANE Preference Pane, TWAIN SANE Interface from: [Link](http://www.ellert.se/twain-sane/)

Append these line to the last of to System Preferences -> SANE -> Drivers -> Configure -> epjitsu (/usr/local/etc/sane.d/epjitsu.conf)

```
#fi-65F
firmware /usr/local/share/sane/epjitsu/65f_0A01.nal
usb 0x04c5 0x11bd
```
