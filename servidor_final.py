import socket
import struct
from schemdraw.parsing import logicparse
import os


def convert_hex(hex_value):
    return str(int(hex_value, 16))


def convert_bin(binary):
    return str(int(binary, 2))


def operacao_binaria(bin1, bin2, operacao):
    def binario_para_decimal(binario):
        if binario[0] == "1":
            # Complemento de dois para números negativos
            return -(int("".join("1" if b == "0" else "0" for b in binario), 2) + 1)
        return int(binario, 2)

    def decimal_para_binario(decimal):
        if decimal < 0:
            # Complemento de dois para números negativos
            positivo = bin(abs(decimal))[2:].zfill(8)
            return "".join("1" if b == "0" else "0" for b in positivo)[:-1] + "1"
        return format(decimal & 0xFF, "08b")

    dec1 = binario_para_decimal(bin1)
    dec2 = binario_para_decimal(bin2)

    if operacao == "+":
        resultado_dec = dec1 + dec2
    elif operacao == "-":
        resultado_dec = dec1 - dec2
    else:
        return "Operação inválida. Use '+' para soma ou '-' para subtração."

    overflow = resultado_dec > 127 or resultado_dec < -128
    resultado_bin = decimal_para_binario(resultado_dec)

    return f"Resultado: {resultado_bin} ({resultado_dec}), Overflow: {'Sim' if overflow else 'Não'}"


def binary_division(dividendo, divisor):
    def binary_to_decimal(binary):
        if binary[0] == "1":
            inverted = "".join("1" if bit == "0" else "0" for bit in binary)
            return -(int(inverted, 2) + 1)
        return int(binary, 2)

    def decimal_to_binary(decimal):
        if decimal < 0:
            positive = bin(abs(decimal))[2:].zfill(8)
            inverted = "".join("1" if bit == "0" else "0" for bit in positive)
            return bin(int(inverted, 2) + 1)[2:].zfill(8)
        return bin(decimal)[2:].zfill(8)

    dec_dividendo = binary_to_decimal(dividendo)
    dec_divisor = binary_to_decimal(divisor)

    if dec_divisor != 0:
        quociente = dec_dividendo // dec_divisor
        resultado_binario = decimal_to_binary(quociente)
        overflow = quociente > 127 or quociente < -128
        return f"Quociente: {resultado_binario} ({quociente}), Overflow: {'Sim' if overflow else 'Não'}"
    else:
        return "Erro: Divisão por zero"


def float_to_ieee754(num):
    pacote = struct.pack(">f", float(num))
    variavel = struct.unpack(">I", pacote)[0]
    binario = format(variavel, "032b")
    hexadecimal = format(variavel, "08X")
    sinal = binario[0]
    expoente = binario[1:9]
    mantissa = binario[9:]
    return f"sinal: {sinal}\nexpoente: {expoente}\nmantissa: {mantissa}\nhexadecimal: {hexadecimal}"


def find_char_position(char):
    ascii_matrix = [
        [
            "NUL",
            "SOH",
            "STX",
            "ETX",
            "EOT",
            "ENO",
            "ACK",
            "BEL",
            "BS",
            "TAB",
            "LF",
            "VT",
            "FF",
            "CR",
            "SO",
            "SI",
        ],
        [
            "DLE",
            "DC1",
            "DC2",
            "DC3",
            "DC4",
            "NAK",
            "SYN",
            "ETB",
            "CAN",
            "EM",
            "SUB",
            "ESC",
            "FS",
            "GS",
            "RS",
            "US",
        ],
        [
            " ",
            "!",
            '"',
            "#",
            "$",
            "%",
            "&",
            "'",
            "(",
            ")",
            "*",
            "+",
            ",",
            "-",
            ".",
            "/",
        ],
        [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            ":",
            ";",
            "<",
            "=",
            ">",
            "?",
        ],
        [
            "@",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
        ],
        [
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "[",
            "\\",
            "]",
            "^",
            "_",
        ],
        [
            "`",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
        ],
        [
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "{",
            "|",
            "}",
            "~",
            "DEL",
        ],
    ]
    for i, row in enumerate(ascii_matrix):
        if char in row:
            return i, row.index(char)
    return None


def char_to_hex(char):
    position = find_char_position(char)
    if position:
        row, col = position
        hex_value = row * 16 + col
        return f"{hex_value:02X}"
    return None


def word_to_hex(word):
    hex_values = []
    for char in word:
        hex_value = char_to_hex(char)
        if hex_value:
            hex_values.append(hex_value)
        else:
            hex_values.append("??")
    return " ".join(hex_values)


BUFFER_SIZE = 64 * 1024  # 64 KB

def process_request(data):
    parts = data.split('|')
    question = int(parts[0])

    if question == 1:
        if parts[1] == 'hex':
            return convert_hex(parts[2])
        elif parts[1] == 'bin':
            return convert_bin(parts[2])
    elif question == 2:
        return operacao_binaria(parts[1], parts[2], parts[3])
    elif question == 3:
        return binary_division(parts[1], parts[2])
    elif question == 4:
        return float_to_ieee754(parts[1])
    elif question == 5:
        if parts[1] == 'ascii_to_hex':
            return word_to_hex(parts[2])
        elif parts[1] == 'utf8_compare':
            phrase1, phrase2 = parts[2], parts[3]
            bytes1 = phrase1.encode('utf-8')
            bytes2 = phrase2.encode('utf-8')
            return f"Frase 1: {len(bytes1)} bytes, hex: {bytes1.hex()}\nFrase 2: {len(bytes2)} bytes, hex: {bytes2.hex()}\nDiferença: {len(bytes2) - len(bytes1)} bytes"
    elif question == 6:
        logic_expr = parts[1]
        d = logicparse(logic_expr)
        d.save("image.jpg")
        with open("image.jpg", 'rb') as f:
            file_data = f.read()
        return file_data
    elif question == 7:
        params = parts[1:]
        if len(params) >= 5:
            return "Parâmetros demais"
        else:
            # Preenche com '1' até ter 4 'and's
            while len(params) < 4:
                params.append('T')
            concatenated = ' and '.join(params)
            d = logicparse(concatenated)
            d.save("image.jpg")
            with open("image.jpg", 'rb') as f:
                file_data = f.read()
            return file_data
    else:
        return "Questão inválida"

def start_server():
    host = '25.0.111.214'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor escutando em {host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conectado por {addr}")
                while True:
                    data = conn.recv(BUFFER_SIZE).decode()
                    if not data:
                        break
                    response = process_request(data)
                    if isinstance(response, bytes):  # Check if response is binary data
                        # Send file size first
                        file_size = struct.pack('>I', len(response))
                        conn.sendall(file_size)
                        # Send file data
                        conn.sendall(response)
                    else:
                        conn.sendall(response.encode())

if __name__ == "__main__":
    start_server()