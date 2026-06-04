# Server Streaming Calls — Video Streaming Service

Este exemplo demonstra o uso de **Server Streaming Call** em gRPC por meio de uma aplicação simples de streaming de vídeo.

O contexto utilizado é o de um serviço de vídeo sob demanda, em que o cliente solicita um vídeo ao servidor e recebe o conteúdo em vários pedaços, chamados de **chunks**.

## Contexto da aplicação

A aplicação simula um serviço de streaming/download de vídeos utilizando gRPC.

O cliente informa:

* ID do vídeo desejado;
* caminho do arquivo de saída.

O servidor gRPC processa essa solicitação, busca o vídeo em uma URL pública configurada no catálogo e envia o conteúdo do arquivo em partes.

O cliente recebe cada pedaço enviado pelo servidor e reconstrói o vídeo em um arquivo `.mp4`.

O servidor retorna, em cada chunk:

* ID do vídeo;
* título do vídeo;
* dados binários do pedaço do vídeo;
* número do chunk;
* quantidade de bytes enviados até o momento;
* tamanho total do vídeo;
* tipo do conteúdo.

Esse tipo de aplicação representa um cenário comum em sistemas de mídia, transferência de arquivos grandes e streaming de conteúdo, em que não é adequado enviar todo o arquivo em uma única resposta.

## Tipo de comunicação

Este exemplo utiliza o modelo **Server Streaming Call**.

Nesse modelo, o cliente envia uma única requisição para o servidor, e o servidor retorna várias respostas em sequência.

Fluxo da comunicação:

```txt
Cliente  ->  VideoRequest  ->  Servidor
Cliente  <-  VideoChunk    <-  Servidor
Cliente  <-  VideoChunk    <-  Servidor
Cliente  <-  VideoChunk    <-  Servidor
Cliente  <-  VideoChunk    <-  Servidor
```

Esse tipo de comunicação é adequado para operações em que o servidor precisa enviar dados progressivamente, como:

* streaming de vídeo;
* download de arquivos grandes;
* envio de logs em tempo real;
* monitoramento de progresso;
* transmissão de eventos;
* leitura paginada ou contínua de dados.

No exemplo implementado, o servidor divide o vídeo em pequenos blocos de bytes e envia cada bloco como uma mensagem gRPC separada.

## Estrutura da pasta

```txt
server-streaming-calls/
├── README.md
├── proto/
│   └── video_stream.proto
└── src/
    ├── client.py
    ├── server.py
    ├── video_catalog.py
    ├── video_stream_pb2.py
    └── video_stream_pb2_grpc.py
```

Os arquivos `video_stream_pb2.py` e `video_stream_pb2_grpc.py` são gerados automaticamente a partir do arquivo `.proto`.

## Arquivo Protobuf

O contrato da comunicação está definido no arquivo:

```txt
proto/video_stream.proto
```

A chamada com server streaming utilizada é:

```proto
rpc StreamVideo (VideoRequest) returns (stream VideoChunk);
```

A palavra-chave `stream` indica que o servidor pode retornar várias mensagens `VideoChunk` para uma única requisição `VideoRequest`.

A mensagem `VideoRequest` representa os dados enviados pelo cliente:

```proto
message VideoRequest {
  string video_id = 1;
}
```

A mensagem `VideoChunk` representa cada pedaço do vídeo enviado pelo servidor:

```proto
message VideoChunk {
  string video_id = 1;
  string title = 2;
  bytes data = 3;
  int64 chunk_number = 4;
  int64 sent_bytes = 5;
  int64 total_bytes = 6;
  string content_type = 7;
}
```

O campo `data` utiliza o tipo `bytes`, pois cada chunk contém uma parte binária do arquivo de vídeo.

## Catálogo de vídeos

Os vídeos disponíveis para streaming são definidos no arquivo:

```txt
src/video_catalog.py
```

Esse arquivo funciona como um catálogo simples da aplicação.

Exemplo:

```python
VIDEO_CATALOG = {
    "bbb": {
        "title": "Big Buck Bunny",
        "url": "https://media.w3.org/2010/05/bunny/movie.mp4",
        "content_type": "video/mp4",
    },
    "sintel": {
        "title": "Sintel Trailer",
        "url": "https://media.w3.org/2010/05/sintel/trailer.mp4",
        "content_type": "video/mp4",
    },
    "flower": {
        "title": "Flower Sample Video",
        "url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
        "content_type": "video/mp4",
    },
}
```

Em uma aplicação real, esse catálogo poderia ser substituído por uma base de dados, serviço de armazenamento de arquivos ou plataforma de mídia.

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
make generate-server-stream
```

Esse comando compila o arquivo `video_stream.proto` e gera os arquivos Python necessários para o cliente e o servidor.

## Executando o servidor

A partir da raiz do repositório, execute:

```bash
make run-server-stream
```

O servidor será iniciado em:

```txt
localhost:50052
```

## Executando o cliente

Com o servidor em execução, abra outro terminal e execute o cliente a partir da raiz do repositório:

```bash
python server-streaming-calls/src/client.py flower --output downloads/flower.mp4
```

O comando segue o formato:

```bash
python server-streaming-calls/src/client.py <VIDEO_ID> --output <CAMINHO_ARQUIVO>
```

Exemplos:

```bash
python server-streaming-calls/src/client.py flower --output downloads/flower.mp4
python server-streaming-calls/src/client.py sintel --output downloads/sintel.mp4
```

Também é possível executar o cliente usando o valor padrão do arquivo de saída:

```bash
python server-streaming-calls/src/client.py flower
```

Nesse caso, o vídeo será salvo em:

```txt
downloads/video.mp4
```

## Exemplo de saída

```txt
Streaming de vídeo
------------------
Vídeo solicitado: flower
Arquivo de saída: downloads/flower.mp4

Chunk 1 recebido
 - 8.42%
Chunk 2 recebido
 - 16.84%
Chunk 3 recebido
 - 25.26%
Chunk 4 recebido
 - 33.68%
Chunk 5 recebido
 - 42.10%

Download via gRPC finalizado
Video salvo em downloads/flower.mp4
```

A quantidade de chunks e os percentuais podem variar conforme o tamanho do vídeo e a quantidade de bytes enviada em cada parte.

## Funcionamento do servidor

O servidor recebe o `video_id`, verifica se o vídeo existe no catálogo e abre a URL correspondente.

Em seguida, o arquivo é lido em partes utilizando um tamanho fixo de chunk:

```python
CHUNK_SIZE = 64 * 1024
```

Cada parte lida é enviada para o cliente usando `yield`:

```python
yield video_stream_pb2.VideoChunk(
    video_id=video_id,
    title=video["title"],
    data=chunk,
    chunk_number=chunk_number,
    sent_bytes=sent_bytes,
    total_bytes=total_bytes,
    content_type=content_type
)
```

O uso de `yield` permite que o servidor envie várias respostas durante a mesma chamada gRPC.

## Funcionamento do cliente

O cliente faz uma única chamada para o servidor:

```python
stub.StreamVideo(request)
```

Como essa chamada retorna um stream, o cliente percorre as respostas com um `for`:

```python
for chunk in stub.StreamVideo(request):
    file.write(chunk.data)
```

Cada `VideoChunk` recebido é escrito no arquivo de saída. Ao final do stream, o arquivo `.mp4` estará reconstruído localmente.

## Tratamento de erros

O servidor valida os dados recebidos na requisição.

Exemplos de erros tratados:

* vídeo inexistente no catálogo;
* erro ao acessar a URL externa do vídeo;
* falha de conexão durante o download do vídeo;
* indisponibilidade do servidor externo.

Quando o vídeo solicitado não existe, o servidor retorna erro gRPC com status `NOT_FOUND`.

Quando ocorre algum problema ao buscar o vídeo externo, o servidor retorna erro gRPC com status `UNAVAILABLE`.

## Conclusão

Este exemplo demonstra uma aplicação prática de **Server Streaming Call** em gRPC. O modelo é adequado para cenários em que o cliente faz uma única solicitação, mas o servidor precisa retornar várias mensagens ao longo do tempo.

No caso do streaming de vídeo, o servidor não envia o arquivo inteiro em uma única resposta. Em vez disso, ele divide o conteúdo em chunks e envia cada parte progressivamente para o cliente.

A aplicação utiliza Protocol Buffers para definir o contrato entre cliente e servidor, e gRPC para realizar a comunicação remota de forma estruturada e eficiente.
