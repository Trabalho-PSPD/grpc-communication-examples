import argparse
import time

import grpc

import chat_pb2
import chat_pb2_grpc


def generate_messages(username: str):
    while True:
        content = input(f"{username}: ")

        yield chat_pb2.ChatMessage(sender=username, content=content, timestamp=int(time.time()))
        if content.lower().strip() in ["sair", "exit", "quit"]:
            break

def start_chat(username: str):
    with grpc.insecure_channel("localhost:50054") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        try:
            print("\nChat com o servidor")
            print("---------------------")
            print("Digite sua mensagem")
            print("Para encerrar, digitar 'sair'\n")

            responses = stub.Chat(generate_messages(username))

            for response in responses:
                print(f"\n{response.sender}: {response.content}")
        except grpc.RpcError as err:
            print("Erro na chamada gRPC")
            print(f"Código: {err.code()}")
            print(f"Detalhes: {err.details()}")


def main():
    parser = argparse.ArgumentParser(description="Client gRPC para chat com bidirectional streaming")
    parser.add_argument("--username", default="Cliente", help="Nome do usuário. Padrão: 'Cliente'")
    args = parser.parse_args()
    start_chat(username=args.username)


if __name__ == "__main__":
    main()
