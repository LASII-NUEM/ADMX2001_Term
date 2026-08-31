import serial

ser = serial.Serial(
    port = "COM3",
    baudrate = 115200,
    timeout = 1
)

def cmd(comando):
    ser.write((comando + "\n").encode())


#set da configuração
def configurar():
    cmd("display 9")
    cmd("count 136")
    cmd("sweep_type frequency 1 1000")
    cmd("sweep_scale log")

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
