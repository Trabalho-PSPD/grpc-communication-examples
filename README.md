# gRPC Communication Examples

Este repositório reúne exemplos práticos dos principais tipos de comunicação suportados pelo **gRPC**, desenvolvidos para o trabalho da disciplina **Programação para Sistemas Paralelos e Distribuídos (PSPD)**.

O objetivo é demonstrar, por meio de aplicações simples, como funcionam os quatro modelos de comunicação do gRPC:

* Unary Calls
* Server Streaming Calls
* Client Streaming Calls
* Bidirectional Streaming Calls

Cada exemplo possui seu próprio arquivo `.proto`, `server`, `client` e documentação específica.

## Organização do repositório

```txt
.
├── unary-calls/
├── server-streaming-calls/
├── client-streaming-calls/
├── bidirecional-streaming-calls/
├── .gitignore
├── Makefile
├── requirements.txt
└── README.md
```

## Estrutura dos exemplos

Cada pasta representa um tipo de comunicação gRPC e possui seu próprio `README.md`, explicando:

* o contexto da aplicação utilizada;
* o objetivo do exemplo;
* o funcionamento da comunicação;
* os arquivos principais;
* os comandos necessários para executar o servidor e o cliente.

## Tipos de comunicação

### Unary Calls

No modelo **Unary Call**, o cliente envia uma única requisição e o servidor retorna uma única resposta.

Esse modelo é semelhante ao funcionamento tradicional de uma API REST, sendo adequado para operações como consultas, cálculos, validações e cadastros.

Exemplo no repositório: [unary-calls](./unary-calls)

### Server Streaming Calls

No modelo **Server Streaming**, o cliente envia uma única requisição e o servidor retorna várias respostas em sequência.

Esse modelo é útil quando o servidor precisa enviar atualizações, progresso de processamento, logs ou uma lista de resultados ao longo do tempo.

Exemplo no repositório: [server-streaming-calls](./server-streaming-calls)

### Client Streaming Calls

No modelo **Client Streaming**, o cliente envia várias mensagens para o servidor e, ao final, o servidor retorna uma única resposta.

Esse modelo pode ser utilizado em cenários como envio de lotes de dados, upload em partes ou agregação de informações enviadas pelo cliente.

Exemplo no repositório: [client-streaming-calls](./client-streaming-calls)

### Bidirectional Streaming Calls

No modelo **Bidirectional Streaming**, cliente e servidor enviam múltiplas mensagens durante a mesma conexão.

Esse modelo é adequado para aplicações que exigem troca contínua de mensagens, como chats, monitoramento em tempo real, transmissão de eventos ou processamento contínuo.

Exemplo no repositório: [bidirectional-streaming-calls](./bidirectional-streaming-calls)

## Requisitos

Para executar os exemplos, é necessário ter o Python instalado (>=3.12)

Crie um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Gerando os arquivos a partir do Protobuf

Cada exemplo possui um arquivo `.proto`, que deve ser compilado para gerar os arquivos Python utilizados pelo cliente e pelo servidor gRPC.

Os comandos de geração estão centralizados no `Makefile`.

### Unary Calls

```bash
make generate-unary
```

### Server Streaming Calls

```bash
make generate-server-stream
```

### Client Streaming Calls

```bash
make generate-client-stream
```

### Bidirectional Streaming Calls

```bash
make generate-bidirectional-stream
```

## Executando os exemplos

Cada exemplo possui comandos próprios no `Makefile` para executar o servidor.

## Observação sobre os comandos

Os comandos principais de compilação e execução devem ser consultados no arquivo `Makefile`, pois ele centraliza a forma correta de gerar os arquivos `.proto` e executar cada exemplo.

Cada pasta também contém um `README.md` próprio com instruções mais detalhadas sobre o contexto da aplicação e os passos para rodar o exemplo correspondente.

## Objetivo acadêmico

Este repositório tem finalidade acadêmica e foi criado para demonstrar, testar e documentar os diferentes tipos de comunicação suportados pelo gRPC, incluindo a definição dos serviços com Protocol Buffers e a implementação dos clientes e servidores em Python.
