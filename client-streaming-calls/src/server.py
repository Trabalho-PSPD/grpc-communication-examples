from concurrent import futures
from pathlib import Path
import hashlib

import grpc

import video_upload_pb2
import video_upload_pb2_grpc

# Apenas para exemplo (fake domain para simular envio para um storage da vida)
STORAGE_DOMAIN = "https://pspd.com"


class VideoUploadService(video_upload_pb2_grpc.VideoUploadServiceServicer):
    def UploadVideo(self, request_iterator, context):
        filename = None
        expected_total_bytes = 0
        chunks_received = 0
        total_bytes_received = 0
        sha256_hash = hashlib.sha256()

        try:
            for chunk in request_iterator:
                if chunks_received == 0:
                    filename = Path(chunk.filename).name
                    expected_total_bytes = chunk.total_bytes

                    if not filename:
                        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "O nome do arquivo é obrigatório.")

                    print("Iniciando upload de vídeo")
                    print("-------------------------")
                    print(f"Arquivo: {filename}")
                    print(f"Tamanho esperado: {expected_total_bytes} bytes\n")

                if not chunk.data:
                    context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Chunk vazio recebido.")

                sha256_hash.update(chunk.data)

                chunks_received += 1
                total_bytes_received += len(chunk.data)

                if expected_total_bytes > 0:
                    percent = (total_bytes_received / expected_total_bytes) * 100
                    print(f"Chunk {chunk.chunk_number} recebido - {percent:.2f}%")
                else:
                    print(f"Chunk {chunk.chunk_number} recebido - {total_bytes_received} bytes")

            if chunks_received == 0:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Nenhum chunk foi enviado pelo cliente.")

            if expected_total_bytes > 0 and total_bytes_received != expected_total_bytes:
                context.abort(
                    grpc.StatusCode.DATA_LOSS,
                    "A quantidade de bytes recebida é diferente do tamanho esperado."
                )
            video_hash = sha256_hash.hexdigest()
            video_url = f"{STORAGE_DOMAIN}/v/{video_hash}"

            print("\nUpload finalizado com sucesso")
            print("-----------------------------")
            print(f"Chunks recebidos: {chunks_received}")
            print(f"Bytes recebidos: {total_bytes_received}")
            print(f"URL do vídeo: {video_url}\n")

            return video_upload_pb2.UploadSummary(
                filename=filename,
                chunks_received=chunks_received,
                total_bytes_received=total_bytes_received,
                video_url=video_url,
                message="Upload de vídeo concluído e armazenado no storage simulado.",
            )

        except grpc.RpcError:
            raise

        except Exception as err:
            context.abort(grpc.StatusCode.INTERNAL, f"Erro ao processar upload: {err}")


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_send_message_length", 10 * 1024 * 1024),
            ("grpc.max_receive_message_length", 10 * 1024 * 1024)
        ]
    )
    video_upload_pb2_grpc.add_VideoUploadServiceServicer_to_server(VideoUploadService(), server)
    server.add_insecure_port("[::]:50053")
    server.start()

    print("Servidor gRPC de upload de vídeos rodando em localhost:50053")
    print(f"Storage simulado: {STORAGE_DOMAIN}")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
