# Blog RPC - Parte 3

 <h2> As operações permitidas no micro blogue: </h2>

• Usuários enviam post em um determinado tópico: post(@username, #tópico, texto) <br />
• Usuário ingressa em um determinado tópico: follow (@username, #tópico) <br />
• Usuário deixa de seguir e de acessar um determinado tópico: unsubscribe (@username,#tópico) <br />
• O usuário recupera todos os posts de todos os tópicos que faz parte, desde a data especificada até a data atual: retrievetime (@username, timestamp) <br />
• O usuário recupera todos os posts, apenas do tópico identificado (o usuário deve fazer parte
do tópico), desde a data especificada até a data atual: retrievetopic(@username, #tópico,timestamp) <br />

<br/>

<h2> Especificações da implementação:	</h2>

1) Replicação: Incluir um segundo servidor para armazenamento (atuando como espelho). Os servidores serão elementos remotos;  <br />

2) Disparador de requisições: Um outro serviço deve ser incluido no sistema (em um elemento
remoto), trata-se do disparador, responsável por receber requisições dos clientes e enviar
para atendimento de um dos servidores de armazenamento. Faça o balanceamento de carga
entre os servidores. O serviço do disparador será executado em um elemento remoto; <br />

3) Serviço de Cache: Em cada um dos servidores de armazenamento deve ser incluído um cache, que mantém requisições atendidas (para melhorar o tempo de resposta ao cliente). Todas as requisições atendidas serão mantidas na cache, quando uma nova requisição é endereçada ao servidor de armazenamento, antes de buscar na base de dados, deve-se consultar a cache, caso não esteja presente na cache, será realizada consulta na base, atualizada a cache e a resposta enviada ao cliente. A consistência da cache deve ser mantida quando uma requisição de post é recebida, nesse caso uma mensagem AtualizaCache deve ser enviada para a outra cache (atualizando também a base de dados remota). <br />

4) Operação que permite ao cliente verificar a quantidade de posts armazenados na base de dados durante um certo intevalo de tempo (t1, t2), o comando serápoll (t1,t2,#tópico). <br />

5) Tolerância a Falhas: O disparador de requisições deve monitorar os servidores de armazenamento, com o objetivo de detectar sua falha, com isso direcionar requisições somente ao outro servidor de armazenamento (que permanece ativo). O retorno do servidor com falha dever ser transparente, ou seja, deverá se sincronizar sua base de dados com o servidor que se manteve operacional (a operação poll ajuda nessa tarefa) <br />

<br />



![Alt text](/images/modelo.png?raw=true "Modelo")


<br />
<h2>Observações: </h2>
Inseira essas duas linhas no arquivo /etc/hosts <br /> <br />
191.52.64.201	localhost <br />
191.52.64.201	samcro <br />



<br />
<b>Feito com: </b> Vitor Oliveira (https://github.com/vhrboliveira)

