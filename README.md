# gRPC Communication Examples

Este repositório reúne exemplos práticos dos principais tipos de comunicação suportados pelo **gRPC**, desenvolvidos para o trabalho da disciplina **Programação para Sistemas Paralelos e Distribuídos (PSPD)**.

O objetivo é demonstrar, por meio de aplicações simples em Python, como funcionam os quatro modelos de comunicação do gRPC:

* Unary Calls
* Server Streaming Calls
* Client Streaming Calls
* Bidirectional Streaming Calls

Cada exemplo possui seu próprio arquivo `.proto`, implementação de `server`, implementação de `client` e documentação específica.

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
* os comandos necessários para gerar os arquivos gRPC;
* os comandos necessários para executar o servidor e o cliente.

## Tipos de comunicação

### Unary Calls

No modelo **Unary Call**, o cliente envia uma única requisição e o servidor retorna uma única resposta.

Esse modelo é semelhante ao funcionamento tradicional de uma API REST, sendo adequado para operações como consultas, cálculos, validações e cadastros.

Neste repositório, o exemplo de Unary Call simula um serviço de **cotação de frete**, em que o cliente informa os dados de um pedido e o servidor retorna o valor estimado do frete e o prazo de entrega.

Exemplo no repositório: [unary-calls](./unary-calls)

---

### Server Streaming Calls

No modelo **Server Streaming**, o cliente envia uma única requisição e o servidor retorna várias respostas em sequência.

Esse modelo é útil quando o servidor precisa enviar dados progressivamente, como arquivos grandes, atualizações, logs, eventos ou progresso de processamento.

Neste repositório, o exemplo de Server Streaming simula um serviço de **streaming/download de vídeo**, em que o cliente solicita um vídeo e o servidor envia o conteúdo em vários chunks.

Exemplo no repositório: [server-streaming-calls](./server-streaming-calls)

---

### Client Streaming Calls

No modelo **Client Streaming**, o cliente envia várias mensagens para o servidor e, ao final, o servidor retorna uma única resposta.

Esse modelo pode ser utilizado em cenários como upload de arquivos grandes, envio de lotes de dados, envio de métricas ou agregação de informações enviadas pelo cliente.

Neste repositório, o exemplo de Client Streaming simula um serviço de **upload de vídeo**, em que o cliente envia um arquivo em chunks e o servidor retorna uma URL simulada do vídeo armazenado.

Exemplo no repositório: [client-streaming-calls](./client-streaming-calls)

---

### Bidirectional Streaming Calls

No modelo **Bidirectional Streaming**, cliente e servidor enviam múltiplas mensagens durante a mesma conexão.

Esse modelo é adequado para aplicações que exigem troca contínua de mensagens, como chats, atendimento em tempo real, comunicação interativa, transmissão de eventos ou processamento contínuo.

Neste repositório, o exemplo de Bidirectional Streaming simula um **chat simples via terminal** entre cliente e servidor. O servidor fica ouvindo em uma porta e, quando um cliente se conecta, os dois podem trocar mensagens durante a mesma chamada gRPC.

A implementação foi mantida simples para fins didáticos. Como o exemplo utiliza `input()` no terminal, a comunicação acontece de forma sequencial e pode apresentar bloqueios enquanto um dos lados está digitando. Uma possível melhoria seria utilizar `threading` e `queue` para separar leitura do terminal e recebimento das mensagens.

Exemplo no repositório: [bidirectional-streaming-calls](./bidirectional-streaming-calls)

---

## Requisitos

Para executar os exemplos, é necessário ter o Python instalado:

```txt
Python >= 3.12
```

Crie um ambiente virtual e instale as dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

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

---

## Executando os exemplos

Cada exemplo possui comandos próprios no `Makefile` para executar o servidor.

### Unary Calls

Executar o servidor:

```bash
make run-unary-call
```

Executar o cliente:

```bash
python unary-calls/src/client.py DF 2.0 120
```

### Server Streaming Calls

Executar o servidor:

```bash
make run-server-stream
```

Executar o cliente:

```bash
python server-streaming-calls/src/client.py flower --output downloads/flower.mp4
```

### Client Streaming Calls

Executar o servidor:

```bash
make run-client-stream
```

Executar o cliente:

```bash
python client-streaming-calls/src/client.py downloads/flower.mp4
```

Os arquivos utilizados no exemplo de Client Streaming podem ser obtidos previamente usando o serviço de Server Streaming.

### Bidirectional Streaming Calls

Executar o servidor:

```bash
make run-bidirectional-stream
```

Executar o cliente:

```bash
python bidirectional-streaming-calls/src/client.py --username Lucas
```

---

## Observação sobre os comandos

Os comandos principais de compilação e execução devem ser consultados no arquivo `Makefile`, pois ele centraliza a forma correta de gerar os arquivos `.proto` e executar cada exemplo.

Cada pasta também contém um `README.md` próprio com instruções mais detalhadas sobre o contexto da aplicação e os passos para rodar o exemplo correspondente.

---

## Objetivo acadêmico

Este repositório tem finalidade acadêmica e foi criado para demonstrar, testar e documentar os diferentes tipos de comunicação suportados pelo gRPC.

Os exemplos utilizam **Protocol Buffers** para definir os contratos de comunicação e **gRPC com Python** para implementar clientes e servidores.

O foco do projeto é apresentar, de forma prática e didática, as diferenças entre chamadas unárias, streaming do servidor, streaming do cliente e streaming bidirecional.
