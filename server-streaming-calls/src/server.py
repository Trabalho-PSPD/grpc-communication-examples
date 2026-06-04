from concurrent import futures
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import grpc

import video_stream_pb2
import video_stream_pb2_grpc
from video_catalog import VIDEO_CATALOG


CHUNK_SIZE = 64 * 1024  # 64 KB


class VideoStreamingService(video_stream_pb2_grpc.VideoStreamingServiceServicer):
    def StreamVideo(self, request, context):
        video_id = request.video_id.strip().lower()

        if video_id not in VIDEO_CATALOG:
            context.abort(grpc.StatusCode.NOT_FOUND, "Vídeo não encontrado. Tente: bbb, sintel ou flower")

        video = VIDEO_CATALOG[video_id]
        video_url = video["url"]

        print(f"Cliente solicitou o vídeo: {video['title']}")
        print(f"URL: {video_url}")

        try:
            http_request = Request(
                video_url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "video/mp4,video/*,*/*",
                    "Connection": "keep-alive",
                },
            )

            with urlopen(http_request, timeout=30) as response:
                total_bytes = int(response.headers.get("Content-Length", 0))
                content_type = response.headers.get("Content-Type", video["content_type"])
                print(f"Content-Type: {content_type}")
                print(f"Tamanho total: {total_bytes} bytes")
                sent_bytes = 0
                chunk_number = 1

                while True:
                    chunk = response.read(CHUNK_SIZE)
                    if not chunk:
                        break

                    sent_bytes += len(chunk)
                    print(f"Enviando chunk {chunk_number} -> {sent_bytes}/{total_bytes} bytes")

                    yield video_stream_pb2.VideoChunk(
                        video_id=video_id,
                        title=video["title"],
                        data=chunk,
                        chunk_number=chunk_number,
                        sent_bytes=sent_bytes,
                        total_bytes=total_bytes,
                        content_type=content_type,
                    )
                    chunk_number += 1

                print("Envio finalizado pelo servidor.")

        except HTTPError as err:
            context.abort(grpc.StatusCode.UNAVAILABLE, f"Erro HTTP ao buscar vídeo: {err.code} - {err.reason}")
        except URLError as err:
            context.abort(grpc.StatusCode.UNAVAILABLE, f"Erro de conexão ao buscar vídeo: {err.reason}")
        except Exception as err:
            context.abort(grpc.StatusCode.UNAVAILABLE, f"Erro ao buscar vídeo: {err}")

def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_send_message_length", 10 * 1024 * 1024),
            ("grpc.max_receive_message_length", 10 * 1024 * 1024),
        ],
    )
    video_stream_pb2_grpc.add_VideoStreamingServiceServicer_to_server(VideoStreamingService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("Servidor gRPC de streaming de vídeos rodando em localhost:50052")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
