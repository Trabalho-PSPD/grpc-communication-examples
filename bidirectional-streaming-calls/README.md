# Bidirectional Streaming Calls — Terminal Chat Service

Este exemplo demonstra o uso de **Bidirectional Streaming Call** em gRPC por meio de uma aplicação simples de chat via terminal.

O contexto utilizado é o de uma conversa direta entre um cliente e um servidor. O servidor fica ouvindo em uma porta e, quando um cliente se conecta, os dois podem trocar mensagens durante a mesma chamada gRPC.

## Contexto da aplicação

A aplicação simula um chat simples entre cliente e servidor utilizando gRPC.

O cliente informa:

* nome do usuário no chat.

Depois de conectado, o cliente pode digitar mensagens no terminal e enviá-las para o servidor.

O servidor recebe as mensagens enviadas pelo cliente, exibe o conteúdo no terminal e também pode responder digitando mensagens diretamente no terminal do servidor.

Tanto o cliente quanto o servidor podem enviar várias mensagens durante a mesma conexão.

Cada mensagem contém:

* remetente da mensagem;
* conteúdo da mensagem;
* timestamp do envio.

Esse tipo de aplicação representa um cenário comum em sistemas de comunicação em tempo real, como chats, atendimento online, troca contínua de eventos e comunicação interativa entre sistemas.

## Tipo de comunicação

Este exemplo utiliza o modelo **Bidirectional Streaming Call**.

Nesse modelo, o cliente envia várias mensagens para o servidor, e o servidor também retorna várias mensagens para o cliente durante a mesma chamada gRPC.

Fluxo da comunicação:

```txt
Cliente  ->  ChatMessage  ->  Servidor
Cliente  <-  ChatMessage  <-  Servidor
Cliente  ->  ChatMessage  ->  Servidor
Cliente  <-  ChatMessage  <-  Servidor
```

Esse tipo de comunicação é adequado para operações em que os dois lados precisam enviar dados continuamente, como:

* chats em tempo real;
* atendimento online;
* troca de eventos entre sistemas;
* comunicação com agentes interativos;
* jogos multiplayer;
* monitoramento com respostas do servidor;
* sessões interativas entre cliente e servidor.

No exemplo implementado, cliente e servidor trocam mensagens de texto pelo terminal.

## Estrutura da pasta

```txt
bidirectional-streaming-calls/
├── README.md
├── proto/
│   └── chat.proto
└── src/
    ├── client.py
    ├── server.py
    ├── chat_pb2.py
    └── chat_pb2_grpc.py
```

Os arquivos `chat_pb2.py` e `chat_pb2_grpc.py` são gerados automaticamente a partir do arquivo `.proto`.

## Arquivo Protobuf

O contrato da comunicação está definido no arquivo:

```txt
proto/terminal_chat.proto
```

A chamada com bidirectional streaming utilizada é:

```proto
rpc Chat (stream ChatMessage) returns (stream ChatMessage);
```

A palavra-chave `stream` aparece nos dois lados da chamada:

```proto
stream ChatMessage
```

Isso indica que:

* o cliente pode enviar várias mensagens `ChatMessage`;
* o servidor também pode retornar várias mensagens `ChatMessage`;
* a comunicação acontece durante uma única chamada gRPC.

A mensagem `ChatMessage` representa uma mensagem trocada no chat:

```proto
message ChatMessage {
  string sender = 1;
  string content = 2;
  int64 timestamp = 3;
}
```

* O campo `sender` representa quem enviou a mensagem.
* O campo `content` representa o conteúdo digitado.
* O campo `timestamp` representa o horário do envio em formato numérico.

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
make generate-bidirectional-stream
```

Esse comando compila o arquivo `chat.proto` e gera os arquivos Python necessários para o cliente e o servidor.

## Executando o servidor

A partir da raiz do repositório, execute:

```bash
make run-bidirectional-stream
```

O servidor será iniciado em:

```txt
localhost:50054
```

Neste exemplo, o servidor foi configurado para usar apenas um worker:

```python
futures.ThreadPoolExecutor(max_workers=1)
```

Isso significa que o servidor atende apenas uma conversa por vez. Caso outro cliente tente se conectar enquanto uma conversa já estiver ativa, ele ficará aguardando até que o atendimento atual seja encerrado.

## Executando o cliente

Com o servidor em execução, abra outro terminal e execute o cliente a partir da raiz do repositório:

```bash
python bidirectional-streaming-calls/src/client.py --username Lucas
```

O comando segue o formato:

```bash
python bidirectional-streaming-calls/src/client.py --username <NOME_DO_USUARIO>
```

Exemplos:

```bash
python bidirectional-streaming-calls/src/client.py --username Lucas
python bidirectional-streaming-calls/src/client.py --username Cliente
python bidirectional-streaming-calls/src/client.py --username Ana
```

Caso o nome do usuário não seja informado, o cliente utilizará o valor padrão definido no código.

## Exemplo de saída

No terminal do servidor:

```txt
Servidor gRPC de chat bidirecional rodando em localhost:50054
Apenas uma conversa será atendida por vez.

Cliente conectado ao chat
-------------------------
Digite 'sair' para encerrar a conversa.

Lucas: Olá servidor
Servidor: Olá Lucas, recebi sua mensagem

Lucas: Tudo certo?
Servidor: Tudo certo por aqui
```

No terminal do cliente:

```txt
Chat com o servidor
-------------------
Digite sua mensagem.
Para encerrar, digite: sair

Lucas: Olá servidor

Servidor: Olá Lucas, recebi sua mensagem

Lucas: Tudo certo?

Servidor: Tudo certo por aqui
```

Para encerrar a conversa, o cliente ou o servidor pode digitar:

```txt
sair
```

Também podem ser usados os comandos:

```txt
exit
quit
```

## Funcionamento do cliente

O cliente cria uma conexão gRPC com o servidor:

```python
with grpc.insecure_channel("localhost:50054") as channel:
    stub = chat_pb2_grpc.ChatServiceStub(channel)
```

Em seguida, o cliente envia mensagens utilizando um gerador Python:

```python
def generate_messages(username: str):
    while True:
        content = input(f"{username}: ")

        yield chat_pb2.ChatMessage(
            sender=username,
            content=content,
            timestamp=int(time.time()),
        )
```

O uso de `yield` permite que o cliente envie várias mensagens durante a mesma chamada gRPC.

A chamada realizada pelo cliente é:

```python
responses = stub.Chat(generate_messages(username))
```

Como o servidor também responde em stream, o cliente percorre as respostas com um `for`:

```python
for response in responses:
    print(f"{response.sender}: {response.content}")
```

## Funcionamento do servidor

O servidor implementa o método `Chat`, que recebe um iterador de mensagens enviadas pelo cliente:

```python
def Chat(self, request_iterator, context):
```

Cada mensagem recebida é processada em um `for`:

```python
for message in request_iterator:
    print(f"{message.sender}: {message.content}")
```

Depois de receber uma mensagem do cliente, o servidor permite que o operador digite uma resposta pelo terminal:

```python
response = input("Servidor: ")
```

A resposta é enviada para o cliente usando `yield`:

```python
yield chat_pb2.ChatMessage(
    sender="Servidor",
    content=response,
    timestamp=int(time.time())
)
```

O uso de `yield` no servidor permite que várias mensagens sejam enviadas de volta para o cliente durante a mesma chamada gRPC.

## Observação sobre o uso de input

Este exemplo utiliza a função `input()` para permitir que cliente e servidor digitem mensagens pelo terminal.

Essa abordagem deixa o exemplo mais simples e fácil de entender, mas possui uma limitação importante: o `input()` é uma operação bloqueante.

Isso significa que, enquanto um lado está aguardando digitação no terminal, a exibição de novas mensagens pode não acontecer imediatamente. Em alguns casos, mensagens podem parecer acumuladas até que o fluxo continue.

Essa limitação não é do gRPC em si, mas sim da forma simples como o terminal está sendo usado neste exemplo.

O objetivo deste exemplo é demonstrar o funcionamento do modelo **Bidirectional Streaming Call** de forma didática, mostrando que cliente e servidor podem enviar múltiplas mensagens durante a mesma conexão.

## Possível melhoria

Uma melhoria possível seria separar o envio e o recebimento de mensagens usando `threading` e `queue`.

Com essa abordagem, uma thread ficaria responsável por ler mensagens digitadas no terminal, enquanto outra thread ficaria responsável por receber e exibir mensagens vindas do outro lado da conexão.

Essa melhoria permitiria que as mensagens aparecessem de forma mais imediata, sem depender tanto do bloqueio causado pelo `input()`.

Exemplo conceitual:

```txt
Thread 1 -> lê o input do terminal
Thread 2 -> recebe mensagens do stream gRPC
Queue    -> organiza mensagens que precisam ser enviadas
```

Essa versão seria mais próxima de um chat real, mas também deixaria o código mais complexo.

Por isso, neste exemplo acadêmico, a implementação foi mantida de forma simples, com foco em demonstrar o conceito principal do bidirectional streaming.

## Tratamento de erros

Exemplos de situações que podem gerar erro:

* servidor não está em execução;
* porta incorreta;
* falha de conexão com o servidor;
* interrupção inesperada da chamada;
* encerramento manual do processo.

Quando ocorre algum erro na chamada gRPC, o cliente exibe o código e os detalhes do erro retornado.

## Conclusão

Este exemplo demonstra uma aplicação prática de **Bidirectional Streaming Call** em gRPC. O modelo é adequado para cenários em que cliente e servidor precisam trocar várias mensagens durante a mesma conexão.

No caso do chat pelo terminal, o cliente envia mensagens para o servidor, e o servidor também envia respostas para o cliente sem criar uma nova chamada para cada mensagem. Apesar de simples, o exemplo mostra claramente a principal característica do bidirectional streaming: os dois lados da comunicação trabalham com streams de mensagens.

A aplicação utiliza Protocol Buffers para definir o contrato entre cliente e servidor, e gRPC para realizar a comunicação remota de forma estruturada e eficiente.
