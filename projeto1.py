import serial

port = input("COM port [COM3]: ") or "COM3"

ser = serial.Serial(
    port=port,
    baudrate=115200,
    timeout=1
)
def cmd(comando):
    ser.write((comando + "\n").encode())

def ler_calibracao():
    respostas = []

    while True:
        linha = ser.readline().decode().strip()

        if linha:
            respostas.append(linha)
            print(linha)

        if linha.startswith("load:"):
            break

    return respostas

def calibrar_open():
    input("Conecte o OPEN e pressione ENTER")

    cmd("magnitude 1")
    cmd("calibrate open")

    ler_calibracao()


def calibrar_short():
    input("Conecte o SHORT e pressione ENTER")

    cmd("magnitude 0.2")
    cmd("calibrate short")

    ler_calibracao()


def calibrar_load():
    input("Conecte o LOAD e pressione ENTER")

    resistencia = input("Resistência do LOAD ") or "1000"
    reatancia = input("Reatância do LOAD ") or "0.822"

    cmd("magnitude 1")
    cmd(f"calibrate rt {resistencia} xt {reatancia}")

    ler_calibracao()


def calibrar_todas():
    calibrar_open()
    calibrar_short()
    calibrar_load()

def calibrar():
    print("\n--- CALIBRATION ---")

    calibracoes = {
        "open": calibrar_open,
        "short": calibrar_short,
        "load": calibrar_load,
        "todas": calibrar_todas
    }

    escolha = input(
        "Qual calibração deseja fazer? "
        "(open, short, load ou todas): "
    ).lower()

    calibracoes[escolha]()

def configurar_inicial():

    ch0 = input("Setgain ch0: ")
    ch1 = input("Setgain ch1: ")
    frequency = input("Calibration frequency: ")
    magnitude = input("Magnitude: ")
    offset = input("Offset: ")
    average = input("Average: ")
    delay = input("Trigger delay: ")


    cmd(f"setgain ch0 {ch0}")
    cmd(f"setgain ch1 {ch1}")
    cmd(f"frequency {frequency}")
    cmd(f"magnitude {magnitude}")
    cmd(f"offset {offset}")
    cmd(f"average {average} ")
    cmd(f"tdelay {delay}")


def configurar_sweep():
    print("\n--- SWEEP CONFIGURATION ---")
    display = input("Display: ") or "9"
    count = input("Count: ") or "136"

    sweep_type = input("Sweep Type Frequency: ") or "1 1000"
    inico, fim = sweep_type.split()
    sweep_scale = input("Sweep Type Scale: ") or "log"

    cmd(f"display {display}")
    cmd(f"count {count}")
    cmd(f"sweep_type frequency {inico} {fim}")
    cmd(f"sweep_scale {sweep_scale}")

    return int(count)

def medir(count):
    cmd("z")

    medidas = []

    for _ in range(count):
        medidas.append(ser.readline().decode().strip())

    return medidas

def main ():

    configurar_inicial()

    calibrado = input("O equipamento já foi calibrado? [s/n]: ")

    if calibrado.lower() != "s":
        calibrar()

    count = configurar_sweep()

    medidas = medir(count)

    return medidas

medidas = main()

for linha in medidas:
    print(linha)
