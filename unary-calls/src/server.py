from concurrent import futures

import grpc

import shipping_pb2
import shipping_pb2_grpc
from shipping_rules import MIN_VALUE_FREE_SHIPPING, STATES_RULES


class ShippingService(shipping_pb2_grpc.ShippingServiceServicer):
    def CalculateShipping(self, request, context):
        destination_uf = request.destination_uf.upper().strip()
        weight_kg = request.weight_kg
        order_value = request.order_value

        if destination_uf not in STATES_RULES:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "UF inválida. Informe uma sigla válida (ex: SP, RJ, DF, ...)")

        if weight_kg <= 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "O peso do pedido deve ser maior que zero")

        if order_value < 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "O valor do pedido não pode ser negativo")

        rule = STATES_RULES[destination_uf]
        shipping_price = rule["base_price"] + (weight_kg * rule["price_per_kg"])
        message = f"Envio de SP para {destination_uf}."

        if order_value >= MIN_VALUE_FREE_SHIPPING:
            shipping_price = 0
            message += " Pedido elegível para frete grátis"

        return shipping_pb2.ShippingResponse(
            destination_uf=destination_uf,
            destination_region=rule["region"],
            shipping_price=round(shipping_price, 2),
            estimated_days=rule["days"],
            message=message
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shipping_pb2_grpc.add_ShippingServiceServicer_to_server(ShippingService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()

    print("Servidor gRPC de cotação de frete rodando em localhost:50051")
    print("Origem dos envios: filial SP")

    server.wait_for_termination()

if __name__ == '__main__':
    serve()
