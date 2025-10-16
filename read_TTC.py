import serial
import time
from datetime import datetime
import serial.tools.list_ports

def list_available_ports():
    print("🔌 Available serial ports:")
    for port in serial.tools.list_ports.comports():
        print(f" - {port.device}: {port.description}")

def read_from_controller(port="COM9", baudrate=9600, timeout=1):
    try:
        # List available ports for debugging
        list_available_ports()

        # Open serial port
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout
        )
        print(f"\n✅ Connected to {port} at {baudrate} baud\n")

        # Start logging loop
        while True:
            bytes_waiting = ser.in_waiting
            print(f"Bytes waiting: {bytes_waiting}")

            data = ser.read(bytes_waiting or 1)  # Read available bytes or at least one
            if data:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                print(f"[{timestamp}] Raw:", data)
                print("Hex:", data.hex(" "))

            time.sleep(0.1)  # Avoid busy waiting

    except serial.SerialException as e:
        print("❌ Serial error:", e)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("🔒 Serial port closed.")

if __name__ == "__main__":
    read_from_controller()