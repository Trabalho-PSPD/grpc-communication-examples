import argparse
from pathlib import Path

import grpc

import video_stream_pb2
import video_stream_pb2_grpc


def stream_video(video_id: str, output_path: str):
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with grpc.insecure_channel(
        "localhost:50052",
        options=[
            ("grpc.max_send_message_length", 10 * 1024 * 1024),
            ("grpc.max_receive_message_length", 10 * 1024 * 1024)
        ]
    ) as channel:
        stub = video_stream_pb2_grpc.VideoStreamingServiceStub(channel)
        request = video_stream_pb2.VideoRequest(video_id=video_id)

        try:
            print("\nStreaming de vídeo")
            print("------------------")
            print(f"Vídeo solicitado: {video_id}")
            print(f"Arquivo de saída: {output_file}")
            print()

            with open(output_file, "wb") as file:
                for chunk in stub.StreamVideo(request):
                    file.write(chunk.data)

                    if chunk.total_bytes > 0:
                        percent = (chunk.sent_bytes / chunk.total_bytes) * 100
                        print(f"Chunk {chunk.chunk_number} recebido")
                        print(f" - {percent:.2f}%")
                    else:
                        print(f"Chunk {chunk.chunk_number} recebido")
                        print(f" - {chunk.sent_bytes} bytes")
            print("\nDownload via gRPC finalizado")
            print(f"Video salvo em {output_file}\n")
        except grpc.RpcError as err:
            print("Erro na chamada gRPC")
            print(f"Código: {err.code()}")
            print(f"Detalhes: {err.details()}")

def main():
    parser = argparse.ArgumentParser(description="Client gRPC para streaming de vídeo com server streaming")
    parser.add_argument("video_id", help="ID do vídeo. Exemplos: bbb ou sintel")
    parser.add_argument(
        "--output",
        default="downloads/video.mp4",
        help="Caminho do arquivo de saída, padrão: downloads/video.mp4"
    )
    args = parser.parse_args()
    stream_video(video_id=args.video_id, output_path=args.output)


if __name__ == "__main__":
    main()
