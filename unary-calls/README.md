# Unary Calls — Shipping Service

Este exemplo demonstra o uso de **Unary Call** em gRPC por meio de uma aplicação simples de cotação de frete.

O contexto utilizado é o de uma loja que possui uma filial localizada em **São Paulo (SP)** e precisa calcular o valor estimado do frete e o prazo médio de entrega para diferentes estados do Brasil.

## Contexto da aplicação

A aplicação simula uma cotação de frete a partir da filial de SP.

O cliente informa:

* UF de destino
* peso do pedido em kg
* valor total do pedido

O servidor gRPC processa esses dados e retorna:

* UF de destino
* região do estado
* valor estimado do frete
* prazo médio de entrega
* mensagem explicativa

Estados mais próximos de São Paulo, especialmente os da região Sudeste, possuem prazos menores. Estados mais distantes possuem prazos e tarifas maiores.

## Tipo de comunicação

Este exemplo utiliza o modelo **Unary Call**.

Nesse modelo, o cliente envia uma única requisição para o servidor, e o servidor retorna uma única resposta.

Fluxo da comunicação:

```txt
Cliente  ->  ShippingRequest  ->  Servidor
Cliente  <-  ShippingResponse <-  Servidor
```

Esse tipo de comunicação é adequado para operações simples de consulta ou cálculo, como:

* cotação de frete
* consulta de estoque
* autenticação
* validação de dados
* cálculo de preço
* busca de informações pontuais

## Estrutura da pasta

```txt
unary-calls/
├── README.md
├── proto/
│   └── shipping.proto
└── src/
    ├── client.py
    ├── server.py
    ├── shipping_rules.py
    ├── shipping_pb2.py
    └── shipping_pb2_grpc.py
```

Os arquivos `shipping_pb2.py` e `shipping_pb2_grpc.py` são gerados automaticamente a partir do arquivo `.proto`.

## Arquivo Protobuf

O contrato da comunicação está definido no arquivo:

```txt
proto/shipping.proto
```

A chamada unária utilizada é:

```proto
rpc CalculateShipping (ShippingRequest) returns (ShippingResponse);
```

A mensagem `ShippingRequest` representa os dados enviados pelo cliente:

```proto
message ShippingRequest {
  string destination_uf = 1;
  double weight_kg = 2;
  double order_value = 3;
}
```

A mensagem `ShippingResponse` representa a resposta enviada pelo servidor:

```proto
message ShippingResponse {
  string destination_uf = 1;
  string destination_region = 2;
  double shipping_price = 3;
  int32 estimated_days = 4;
  string message = 5;
}
```

## Requisitos

Para executar o exemplo, instale as dependências a partir da raiz do repositório:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Gerando os arquivos gRPC

A partir da raiz do repositório, execute:

```bash
make generate-unary
```

Esse comando compila o arquivo `shipping.proto` e gera os arquivos Python necessários para o cliente e o servidor.

## Executando o servidor

A partir da raiz do repositório, execute:

```bash
make unary-server
```

O servidor será iniciado em:

```txt
localhost:50051
```

## Executando o cliente

Com o servidor em execução, abra outro terminal e execute o cliente a partir da raiz do repositório:

```bash
python unary-calls/src/client.py DF 2.0 120
```

O comando segue o formato:

```bash
python unary-calls/src/client.py <UF> <PESO_KG> <VALOR_PEDIDO>
```

Exemplos:

```bash
python unary-calls/src/client.py RS 2.0 120
python unary-calls/src/client.py RJ 2.5 180
python unary-calls/src/client.py DF 3.0 300
python unary-calls/src/client.py AM 1.5 600
```

## Exemplo de saída

```txt
Cotação de frete
----------------
Destino: RJ
Região: Sudeste
Preço do frete: R$ 24.00
Prazo médio: 2 dias
Mensagem: Envio de SP para RJ.
```

Caso o valor do pedido seja maior ou igual ao valor mínimo definido para frete grátis (definido no arquivo `shipping_rules.py`), o servidor retorna frete igual a zero.

## Tratamento de erros

O servidor valida os dados recebidos na requisição.

Exemplos de erros tratados:

* UF inválida
* peso menor ou igual a zero
* valor do pedido negativo

Quando algum dado inválido é enviado, o servidor retorna erro gRPC com status `INVALID_ARGUMENT`.

## Conclusão

Este exemplo demonstra uma aplicação prática de **Unary Call** em gRPC. O modelo é adequado para cenários em que o cliente precisa enviar uma única solicitação e receber uma única resposta, como ocorre na cotação de frete.
