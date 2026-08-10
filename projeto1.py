import serial

ser = serial.Serial(
    port = "COM3",
    baudrate = 115200,
    timeout = 1
)
def cmd(comando):
    ser.write((comando + "\n").encode())

def configurar():

    display = input("Display: ") or "9"
    ch0 = input("Setgain ch0: ") or "0"
    ch1 = input("Setgain ch1: ") or "1"
    magnitude = input("Magnitude: ")or "1"
    count = input("Count: ") or "136"

    sweep_type = input("Sweep Type Frequency: ") or "1 1000"
    inico,fim = sweep_type.split()
    sweep_scale = input("Sweep Type Scale: ") or "log"

    cmd(f"display {display}")
    cmd(f"ch0 {ch0}")
    cmd(f"ch1 {ch1}")
    cmd(f"magnitude {magnitude}")
    cmd(f"count {count}")
    cmd(f"sweep_type frequency {inico} {fim}")
    cmd(f"sweep_scale {sweep_scale}")

def medir():
    cmd("z")

    medidas = []

    for _ in range(136):
        medidas.append(ser.readline().decode().strip())

    return medidas

def main ():
    configurar()
    return medir()

if __name__ == "__main__":
    dados = main()

    medidas = main()

    for linha in medidas:
        print(linha)


#short
##Short calibration can be performed only when gain channel 1 is set to 0 or 1. When channel 1 is in gain 1, the magnitude of the source must be less than 0.2Vpk.
#a unica diferença entre os 3 é a magnitude do short


##ser.write(b"setgain ch0 \r\n")
#ouu se usa cmd


#coisas que da pra mudar
##display
##count
##sweep_type frequency 1 1000
##?delay
##magnitude
##ch0 e ch1
##sweep_scale
##??frequency
##average
##?offset

