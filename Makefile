# ========= Unary Calls =========

generate-unary:
	python3 -m grpc_tools.protoc -I unary-calls/proto \
	--python_out=unary-calls/src --grpc_python_out=unary-calls/src \
	unary-calls/proto/shipping.proto

run-unary-call:
	cd unary-calls && python3 src/server.py


# ========= Server Streaming Calls =========

generate-server-stream:
	python3 -m grpc_tools.protoc -I server-streaming-calls/proto \
	--python_out=server-streaming-calls/src --grpc_python_out=server-streaming-calls/src \
	server-streaming-calls/proto/video_stream.proto

run-server-stream:
	cd server-streaming-calls && python3 src/server.py


# ========= Client Streaming Calls =========

generate-client-stream:
	python3 -m grpc_tools.protoc -I client-streaming-calls/proto \
	--python_out=client-streaming-calls/src --grpc_python_out=client-streaming-calls/src \
	client-streaming-calls/proto/video_upload.proto

run-client-stream:
	cd client-streaming-calls && python3 src/server.py
