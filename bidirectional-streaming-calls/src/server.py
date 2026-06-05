from concurrent import futures
import time

import grpc

import chat_pb2
import chat_pb2_grpc


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def Chat(self, request_iterator, context):
        print("\nCliente conectado ao chat")
        print("---------------------------")
        print("Digite 'sair' para encerrar a conversa\n")

        yield chat_pb2.ChatMessage(
            sender="Servidor",
            content="Conexão aceita. Pode enviar sua mensagem...",
            timestamp=int(time.time())
        )
        for message in request_iterator:
            print(f"\n{message.sender}: {message.content}")
            if message.content.lower().strip() in ["sair", "exit", "quit"]:
                yield chat_pb2.ChatMessage(
                    sender="Servidor",
                    content="Conversa encerrada pelo cliente",
                    timestamp=int(time.time())
                )
                break
            response = input("Servidor: ")
            yield chat_pb2.ChatMessage(
                sender="Servidor",
                content=response,
                timestamp=int(time.time())
            )
            if response.lower().strip() in ["sair", "exit", "quit"]:
                break


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50054")
    server.start()

    print("Servidor gRPC de chat bidirecional rodando em localhost:50054")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
