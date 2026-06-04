# Client Streaming Calls — Video Upload Service

Este exemplo demonstra o uso de **Client Streaming Call** em gRPC por meio de uma aplicação simples de upload de vídeo em partes.

O contexto utilizado é o de um serviço de armazenamento de vídeos, em que o cliente envia um arquivo de vídeo ao servidor em vários pedaços, chamados de **chunks**, e o servidor retorna uma única resposta final com a URL simulada do vídeo armazenado.

## Contexto da aplicação

A aplicação simula um serviço de upload de vídeos utilizando gRPC.

O cliente informa:

* caminho do arquivo de vídeo que será enviado.

O cliente lê o arquivo local em partes e envia cada pedaço para o servidor gRPC.

O servidor recebe todos os chunks, processa o conteúdo enviado e, ao final do recebimento, retorna uma resposta única contendo a URL simulada do vídeo no storage.

O cliente envia, em cada chunk:

* nome do arquivo;
* dados binários do pedaço do vídeo;
* número do chunk;
* tamanho total do arquivo;
* tipo do conteúdo.

O servidor retorna, ao final do upload:

* nome do arquivo;
* quantidade de chunks recebidos;
* quantidade total de bytes recebidos;
* URL simulada do vídeo;
* mensagem explicativa.

Esse tipo de aplicação representa um cenário comum em sistemas de mídia, armazenamento de arquivos, upload de vídeos e envio de arquivos grandes, em que não é adequado enviar todo o conteúdo em uma única mensagem.

## Tipo de comunicação

Este exemplo utiliza o modelo **Client Streaming Call**.

Nesse modelo, o cliente envia várias mensagens para o servidor, e o servidor retorna uma única resposta ao final do stream.

Fluxo da comunicação:

```txt
Cliente  ->  VideoChunk     ->  Servidor
Cliente  ->  VideoChunk     ->  Servidor
Cliente  ->  VideoChunk     ->  Servidor
Cliente  ->  VideoChunk     ->  Servidor
Cliente  <-  UploadSummary  <-  Servidor
```

Esse tipo de comunicação é adequado para operações em que o cliente precisa enviar dados progressivamente, como:

* upload de vídeos;
* upload de arquivos grandes;
* envio de logs em lote;
* envio de métricas;
* importação de dados;
* backup de arquivos;
* envio de dados coletados localmente.

No exemplo implementado, o cliente divide o vídeo em pequenos blocos de bytes e envia cada bloco como uma mensagem gRPC separada.

## Estrutura da pasta

```txt
client-streaming-calls/
├── README.md
├── proto/
│   └── video_upload.proto
└── src/
    ├── client.py
    ├── server.py
    ├── video_upload_pb2.py
    └── video_upload_pb2_grpc.py
```

Os arquivos `video_upload_pb2.py` e `video_upload_pb2_grpc.py` são gerados automaticamente a partir do arquivo `.proto`.

## Arquivo Protobuf

O contrato da comunicação está definido no arquivo:

```txt
proto/video_upload.proto
```

A chamada com client streaming utilizada é:

```proto
rpc UploadVideo (stream VideoChunk) returns (UploadSummary);
```

A palavra-chave `stream` antes de `VideoChunk` indica que o cliente pode enviar várias mensagens `VideoChunk` para uma única chamada `UploadVideo`.

A mensagem `VideoChunk` representa cada pedaço do vídeo enviado pelo cliente:

```proto
message VideoChunk {
  string filename = 1;
  bytes data = 2;
  int64 chunk_number = 3;
  int64 total_bytes = 4;
  string content_type = 5;
}
```

A mensagem `UploadSummary` representa a resposta final enviada pelo servidor após receber todos os chunks:

```proto
message UploadSummary {
  string filename = 1;
  int64 chunks_received = 2;
  int64 total_bytes_received = 3;
  string video_url = 4;
  string message = 5;
}
```

O campo `data` utiliza o tipo `bytes`, pois cada chunk contém uma parte binária do arquivo de vídeo.

## Simulação de storage

O servidor simula o armazenamento do vídeo em um serviço externo, semelhante a um storage como S3.

Neste exemplo, o arquivo não é salvo localmente. O servidor recebe os chunks, processa os dados e gera uma URL simulada para representar onde o vídeo estaria disponível após o upload.

A URL retornada segue o formato:

```txt
https://pspd.com/v/<hash-do-video>
```

Exemplo:

```txt
https://pspd.com/v/8f91c4f4d6c4e8a27d0c2f9b2c9e5f...
```

O hash é calculado internamente pelo servidor a partir do conteúdo recebido, mas o cliente recebe apenas a URL final do vídeo.

Em uma aplicação real, essa etapa poderia ser substituída por um upload para um serviço como Amazon S3, Google Cloud Storage, Azure Blob Storage ou outro serviço de armazenamento de arquivos.

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
make generate-client-stream
```

Esse comando compila o arquivo `video_upload.proto` e gera os arquivos Python necessários para o cliente e o servidor.

## Executando o servidor

A partir da raiz do repositório, execute:

```bash
make run-client-stream
```

O servidor será iniciado em:

```txt
localhost:50053
```

## Executando o cliente

Com o servidor em execução, abra outro terminal e execute o cliente a partir da raiz do repositório:

```bash
python client-streaming-calls/src/client.py downloads/video.mp4
```

O comando segue o formato:

```bash
python client-streaming-calls/src/client.py <CAMINHO_DO_VIDEO>
```

Exemplos:

> O arquivo informado precisa existir localmente para que o cliente consiga lê-lo e enviar seus chunks ao servidor.

```bash
python client-streaming-calls/src/client.py downloads/video.mp4
python client-streaming-calls/src/client.py downloads/flower.mp4
python client-streaming-calls/src/client.py downloads/sintel.mp4
```

Os arquivos usados nesses exemplos podem ser obtidos previamente utilizando o serviço de **Server Streaming Calls** deste repositório. Por exemplo, é possível baixar um vídeo com o exemplo `server-streaming-calls` e depois utilizar o arquivo gerado como entrada para o exemplo de **Client Streaming Call**.

## Exemplo de saída

```txt
Upload de vídeo
---------------
Arquivo: downloads/video.mp4

Enviando chunk 1 - 1.50%
Enviando chunk 2 - 3.00%
Enviando chunk 3 - 4.50%
Enviando chunk 4 - 6.00%

Resumo do upload
----------------
Arquivo: video.mp4
Chunks enviados: 67
Bytes recebidos: 4391124
URL do vídeo: https://pspd.com/v/8f91c4f4d6c4e8a27d0c2f9b2c9e5f...
Mensagem: Upload de vídeo concluído e armazenado no storage simulado.
```

A quantidade de chunks e os percentuais podem variar conforme o tamanho do vídeo e a quantidade de bytes enviada em cada parte.

## Funcionamento do cliente

O cliente recebe o caminho do vídeo por argumento de linha de comando.

Em seguida, ele verifica se o arquivo existe e lê seu conteúdo em partes utilizando um tamanho fixo de chunk:

```python
CHUNK_SIZE = 64 * 1024
```

Cada parte lida é enviada para o servidor por meio de um `yield`:

```python
yield video_upload_pb2.VideoChunk(
    filename=filename,
    data=data,
    chunk_number=chunk_number,
    total_bytes=total_bytes,
    content_type=content_type
)
```

O uso de `yield` permite que o cliente envie várias mensagens durante a mesma chamada gRPC, sem carregar o arquivo inteiro em memória.

## Funcionamento do servidor

O servidor recebe um iterador de mensagens `VideoChunk`.

Cada chunk recebido é processado em sequência:

```python
for chunk in request_iterator:
    sha256_hash.update(chunk.data)
```

O servidor contabiliza a quantidade de chunks recebidos e a quantidade total de bytes processados.

Ao final do stream, o servidor gera uma URL simulada para o vídeo:

```python
video_hash = sha256_hash.hexdigest()
video_url = f"{STORAGE_DOMAIN}/v/{video_hash}"
```

Depois disso, o servidor retorna uma única resposta do tipo `UploadSummary`.

## Tratamento de erros

O servidor valida os dados recebidos durante o upload.

Exemplos de erros tratados:

* nenhum chunk enviado pelo cliente;
* nome de arquivo ausente;
* chunk vazio;
* quantidade de bytes recebida diferente do tamanho esperado;
* erro interno durante o processamento do upload.

Quando nenhum chunk é enviado, o servidor retorna erro gRPC com status `INVALID_ARGUMENT`.

Quando a quantidade de bytes recebida não corresponde ao tamanho esperado, o servidor retorna erro gRPC com status `DATA_LOSS`.

Quando ocorre algum erro inesperado durante o processamento, o servidor retorna erro gRPC com status `INTERNAL`.

## Conclusão

Este exemplo demonstra uma aplicação prática de **Client Streaming Call** em gRPC. O modelo é adequado para cenários em que o cliente precisa enviar várias mensagens para o servidor, e o servidor precisa retornar apenas uma resposta final.

No caso do upload de vídeo, o cliente não envia o arquivo inteiro em uma única mensagem. Em vez disso, ele divide o conteúdo em chunks e envia cada parte progressivamente para o servidor.

Ao final do recebimento, o servidor gera uma URL simulada do vídeo armazenado e retorna essa informação para o cliente.

A aplicação utiliza Protocol Buffers para definir o contrato entre cliente e servidor, e gRPC para realizar a comunicação remota de forma estruturada e eficiente.
