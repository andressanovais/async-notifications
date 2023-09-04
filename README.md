![](/doc/DesenhoNotificacao.jpg)

Este projeto visa a criação de um sistema assíncrono de notificações, totalmente event-driven. O sistema busca ser escalável e resiliente.

## Notificações web
Para notificações web o fluxo é iniciado através de uma **WebSocket API**. O objetivo da utilização do protocolo WebSocket é possibilitar a comunicação pelos dois caminhos: o client se conecta com o back-end, e o back-end envia notificações quando estas estiverem disponíveis. 

![](/doc/websocketHandshake.jpg)

A conexão permanece aberta durante no máximo 2 horas. Após esse tempo a conexão deve ser reestabelecida.

### Rotas e integrações
A API possui as seguintes rotas:
- **$connect** Possui uma integração do tipo MOCK, retornando statusCode = 200 para sinalizar sucesso na abertura da conexão.

- **sendUserId** Se integra com a lambda connection_storage para *salvar* os ids do usuário e da conexão. Deve ser utilizada logo após abertura da conexão, pois não é possível enviar informações adicionais na rota connect.

- **$disconnect** Se integra com a lambda connection_storage para *remover* os ids do usuário e da conexão.

## Conexão com a API
### connection_storage
Responsável pelo armazenamento das conexões no cache. Utiliza o design pattern Strategy para definir qual ação deve ser feita de acordo com a rota: armazenamento dos ids (no caso da rota **sendUserId**), ou remoção dos ids (no caso da rota **$disconnect**).

### Elasticache Redis
Cache responsável por armazenar os ids das conexões e dos usuários em estruturas do tipo String. 

O Elasticache Redis foi escolhido devido as vantagens oferecidas em comparação a outros tipos de cache, levando em consideração minha preocupação com resiliência e escalabilidade. Essas vantagens são:
- Detecção e recuperação automática de falhas, atráves do uso de réplicas.
- Multi-AZ.
- Escalabilidade na escrita e leitura, proporcionados pelo modo cluster habilitado. Esse modo permite escalar os nós horizontalmente, possibilitando uma escrita distribuída e, consequentemente, um aumento considerável na performance.

## Envio das notificações
### notification-elegibility
O fluxo de envio de notificações se inicia através dessa Lambda. A Lambda consome de um tópico Kafka de notificações que recebe mensagens de outros sistemas, a partir disso o algoritmo se baseia em:
1. Verifica a elegibilidade do usuário a receber notificações, realizando uma consulta em um banco de dados. 
1. Se o usuário for elegível, agenda um EventBridge Scheduler no horário definido na mensagem sendo consumida.

### EventBridge Scheduler
É um serviço serverless gerencido pela AWS, que permite o agendamento de tarefas de forma resiliente e altamente escalável. Foi escolhido devido a sua escalabilidade, pois em comparação ao EventBridge Rules possibilita um número muito maior de agendamentos existentes simultaneamente. Além disso, é possível conectá-lo a uma DLQ para acompanhar casos de falha na invocação.

### send_notifications
Microsserviço responsável pelo envio das notificações, é invocado pelo EventBridge Scheduler no horário agendado. A partir do tipo de notificação recebido no evento (o evento possui como conteúdo a mensagem do tópico Kafka), decide qual tipo de notificação deve ser enviada. 

Para notificações do tipo web:
1. Busca no cache pelo id da conexão daquele usuário.
1. Envia uma requisição para o client através da conexão obtida no passo anterior, com todas as informações da notificação.

Os demais tipos de notificação não foram implementados, mas podem ser inseridos. Nesse caso, ao detectar demais tipos de notificações, o **send_notifications** enviaria notificações para diferentes tópicos SNS.
 O microsserviço implementa o design pattern Strategy para permitir diferentes estratégias no envio das notificações. 