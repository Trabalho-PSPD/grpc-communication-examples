import argparse
import mimetypes
from pathlib import Path

import grpc

import video_upload_pb2
import video_upload_pb2_grpc


CHUNK_SIZE = 64 * 1024


def generate_video_chunks(video_path: Path):
    total_bytes = video_path.stat().st_size
    filename = video_path.name

    content_type, _ = mimetypes.guess_type(filename)

    if content_type is None:
        content_type = "application/octet-stream"

    chunk_number = 1
    sent_bytes = 0

    with open(video_path, "rb") as file:
        while True:
            data = file.read(CHUNK_SIZE)

            if not data:
                break

            sent_bytes += len(data)

            if total_bytes > 0:
                percent = (sent_bytes / total_bytes) * 100
                print(f"Enviando chunk {chunk_number} - {percent:.2f}%")
            else:
                print(f"Enviando chunk {chunk_number} - {sent_bytes} bytes")
            yield video_upload_pb2.VideoChunk(
                filename=filename,
                data=data,
                chunk_number=chunk_number,
                total_bytes=total_bytes,
                content_type=content_type
            )
            chunk_number += 1


def upload_video(video_path: str):
    path = Path(video_path)

    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        return

    if not path.is_file():
        print(f"O caminho informado não é um arquivo: {path}")
        return

    with grpc.insecure_channel(
            "localhost:50053",
            options=[
                ("grpc.max_send_message_length", 10 * 1024 * 1024),
                ("grpc.max_receive_message_length", 10 * 1024 * 1024),
            ],
    ) as channel:
        stub = video_upload_pb2_grpc.VideoUploadServiceStub(channel)

        try:
            print("\nUpload de vídeo")
            print("---------------")
            print(f"Arquivo: {path}\n")

            response = stub.UploadVideo(generate_video_chunks(video_path=path))

            print("\nResumo do upload")
            print("----------------")
            print(f"Arquivo: {response.filename}")
            print(f"Chunks enviados: {response.chunks_received}")
            print(f"Bytes recebidos: {response.total_bytes_received}")
            print(f"URL do vídeo: {response.video_url}")
            print(f"Mensagem: {response.message}\n")


        except grpc.RpcError as err:
            print("Erro na chamada gRPC")
            print(f"Código: {err.code()}")
            print(f"Detalhes: {err.details()}")


def main():
    parser = argparse.ArgumentParser(description="Client gRPC para upload de vídeo com client streaming")
    parser.add_argument("video_path", help="Caminho do vídeo que será enviado")
    args = parser.parse_args()

    upload_video(video_path=args.video_path)


if __name__ == "__main__":
    main()
