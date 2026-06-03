import argparse

import grpc

import shipping_pb2
import shipping_pb2_grpc


def calculate_shipping(destination_uf: str, weight_kg: float, order_value: float):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = shipping_pb2_grpc.ShippingServiceStub(channel)

        request = shipping_pb2.ShippingRequest(
            destination_uf=destination_uf,
            weight_kg=weight_kg,
            order_value=order_value
        )

        try:
            response = stub.CalculateShipping(request)
            print("\n")
            print("Cotação de frete")
            print("----------------")
            print(f"Destino: {response.destination_uf}")
            print(f"Região: {response.destination_region}")
            print(f"Preço do frete: R$ {response.shipping_price:.2f}")
            print(f"Prazo médio: {response.estimated_days} dias")
            print(f"Mensagem: {response.message}")
            print("\n")

        except grpc.RpcError as err:
            print("Erro na chamada gRPC")
            print(f"Código: {err.code()}")
            print(f"Detalhes: {err.details()}")

def main():
    parser = argparse.ArgumentParser(description="Client gRPC para cotação de frete a partir da filial de SP")
    parser.add_argument("destination_uf", help="UF de destino, exemplo: SP, RJ, DF, ...")
    parser.add_argument("weight_kg", type=float, help="Peso do pedido em kg")
    parser.add_argument("order_value", type=float, help="Valor do pedido em reais")

    args = parser.parse_args()

    calculate_shipping(
        destination_uf=args.destination_uf,
        weight_kg=args.weight_kg,
        order_value=args.order_value
    )

if __name__ == '__main__':
    main()
