generate-unary:
	python3 -m grpc_tools.protoc -I unary-calls/proto \
	--python_out=unary-calls/src --grpc_python_out=unary-calls/src \
	unary-calls/proto/shipping.proto

run-unary-call:
	cd unary-calls && python3 src/server.py
