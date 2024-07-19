import socket
import sys
import struct

BUFFER_SIZE = 64 * 1024  # 64 KB

def receive_all(sock, file_path):
    """Recebe todos os dados do socket e salva em um arquivo."""
    # Receive the file size first
    file_size_data = sock.recv(4)
    file_size = struct.unpack('>I', file_size_data)[0]
    
    # Open file for writing binary data
    with open(file_path, 'wb') as f:
        bytes_received = 0
        while bytes_received < file_size:
            chunk = sock.recv(min(BUFFER_SIZE, file_size - bytes_received))
            if not chunk:
                break
            f.write(chunk)
            bytes_received += len(chunk)

def send_request(question, *args):
    host = "25.0.111.214"
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        request = f"{question}|{'|'.join(args)}"
        s.sendall(request.encode())

        if question == 6 or question == 7:
            # Receber o arquivo e salvar localmente
            receive_all(s, "received_logic_diagram.jpg" if question == 6 else "received_logic_diagram.jpg")
            return "Diagrama lógico recebido e salvo como received_logic_diagram.jpg"
        else:
            response = s.recv(BUFFER_SIZE).decode()
            return response

def print_utf8_table():
    utf8_table = [
        {"bytes": 1, "bits": 7, "first": "U+0000", "last": "U+007F"},
        {"bytes": 2, "bits": 11, "first": "U+0080", "last": "U+07FF"},
        {"bytes": 3, "bits": 16, "first": "U+0800", "last": "U+FFFF"},
        {"bytes": 4, "bits": 21, "first": "U+10000", "last": "U+10FFFF"},
    ]
    print("\nTabela UTF-8:")
    print(
        "| Number of bytes | Bits for code point | First code point | Last code point |"
    )
    print(
        "|-----------------|---------------------|------------------|-----------------|"
    )
    for row in utf8_table:
        print(
            f"| {row['bytes']:15d} | {row['bits']:19d} | {row['first']:16s} | {row['last']:14s} |"
        )
    print()

def print_ascii_table():
    ascii_matrix = [
        [
            "NUL", "SOH", "STX", "ETX", "EOT", "ENO", "ACK", "BEL", "BS", "TAB", "LF", "VT", "FF", "CR", "SO", "SI",
        ],
        [
            "DLE", "DC1", "DC2", "DC3", "DC4", "NAK", "SYN", "ETB", "CAN", "EM", "SUB", "ESC", "FS", "GS", "RS", "US",
        ],
        [
            " ", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
        ],
        [
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",
        ],
        [
            "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
        ],
        [
            "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_",
        ],
        [
            "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
        ],
        [
            "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "DEL",
        ],
    ]
    print("\nTabela ASCII:")
    for i, row in enumerate(ascii_matrix):
        print(f"Row {i}: {' '.join(row)}")
    print()

def main_menu():
    while True:
        print("\nEscolha uma questão:")
        print("1. Conversão Hexadecimal/Binário")
        print("2. Operação Binária")
        print("3. Divisão Binária")
        print("4. Conversão para IEEE 754")
        print("5. ASCII para Hexadecimal e UTF-8")
        print("6. Gerar Diagrama Lógico")
        print("7. Parâmetros Variáveis para Expressão Lógica")
        print("8. Sair")

        choice = input("Digite o número da questão desejada: ")

        if choice == "1":
            sub_choice = input("Escolha 'hex' para hexadecimal ou 'bin' para binário: ")
            value = input("Digite o valor para conversão: ")
            result = send_request(1, sub_choice, value)
            print(f"Resultado: {result}")

        elif choice == "2":
            bin1 = input("Digite o primeiro número binário de 8 bits: ")
            bin2 = input("Digite o segundo número binário de 8 bits: ")
            op = input("Digite a operação desejada (+ para soma, - para subtração): ")
            result = send_request(2, bin1, bin2, op)
            print(f"Resultado: {result}")

        elif choice == "3":
            dividendo = input("Digite o dividendo binário: ")
            divisor = input("Digite o divisor binário: ")
            result = send_request(3, dividendo, divisor)
            print(f"Resultado: {result}")

        elif choice == "4":
            num = input("Digite o número float: ")
            result = send_request(4, num)
            print(f"Resultado:\n{result}")

        elif choice == "5":
            print("\nEscolha uma opção:")
            print("1. Converter ASCII para Hexadecimal")
            print("2. Comparar bytes em UTF-8")
            sub_choice = input("Digite o número da opção desejada: ")

            if sub_choice == "1":
                print_ascii_table()
                word = input("Digite uma palavra: ")
                result = send_request(5, "ascii_to_hex", word)
                print(f"Valor em hexadecimal: {result}")

            elif sub_choice == "2":
                phrase1 = input("Digite a primeira frase: ")
                phrase2 = input("Digite a segunda frase: ")
                result = send_request(5, "utf8_compare", phrase1, phrase2)
                print(f"Comparação UTF-8:\n{result}")

        elif choice == "6":
            logic_expr = input("Digite a expressão lógica: ")
            result = send_request(6, logic_expr)
            print(result)

        elif choice == "7":
            num_params = int(input("Digite o número de parâmetros: "))
            params = [input(f"Digite o parâmetro {i + 1}: ") for i in range(num_params)]
            result = send_request(7, *params)
            print(result)

        elif choice == "8":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()
