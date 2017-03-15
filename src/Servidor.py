from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import psycopg2
import xmlrpclib
from datetime import datetime
import threading
from time import gmtime, strftime

global topicosLista
topicosLista = []

def printarTuplas(tuplas):

	global topicosLista
	topicosLista = []

	tam = len(tuplas)
	i = 0

	while(i<tam):
		texto = tuplas[i]
		topicosLista.append(texto[0])
		i = i + 1


# -------------- Conecta ao Banco de Dados -------------- #
conectarBd = psycopg2.connect("dbname=sakuray user=vitor password=vitor")
#Cursor para operar no Banco
cursor = conectarBd.cursor()
# -------------- Conecta ao Banco de Dados -------------- #

global urlveio
urlveio = ""

# -------------- CAche -------------- #

global mandarUsuario			
global mandarTopico
global mandarTexto
global mandarTempo

mandarUsuario = []
mandarTopico = []
mandarTexto = []
mandarTempo = []

global postUsuarioes			
global postTopicoes
global postTextoes
global postQntes
global postTempoes
postQntes = 0

postUsuarioes = []
postTopicoes = []
postTextoes = []
postTempoes = []


global total
total = 3

global postUsuario
postUsuario = []
global postTopico
postTopico = []
global postTexto
postTexto = []
global postTempo
postTempo = []
global postId
postId = []
	

global postQnt
postQnt = 0

# Informa o id do Servidor para mandar junto com a resposta, assim o cliente sabe qual Servidor atendeu a requiscao
def mandarString():
	return " (servidor " + str(numero) + ")"

def insertCache(usuario, topico, texto, ide):
	
	
	tempo = strftime("%Y-%m-%d %H:%M:%S", gmtime()  )

	#Postar no Banco
	postar(usuario,topico,texto,tempo)

	#Postar no Banco Espelho
	try:
		espelho = xmlrpclib.ServerProxy(urlveio)
		espelho.postar(usuario,topico,texto,tempo)
	except:
		a = 0
	else:
		a = 0 
	finally:
		a = 0

	global mandarUsuario			
	global mandarTopico
	global mandarTexto
	global mandarTempo

	mandarUsuario = []
	mandarTopico = []
	mandarTexto = []
	mandarTempo = []	

	if(postQnt>total):


		# 
	
		k1 = postUsuario[0]
		k2 = postTopico[0]
		k3 = postTexto[0]

		aux1 = postUsuario[1:]
		aux2 = postTopico[1:]
		aux3 = postTexto[1:]
		aux4 = postTempo[1:]

		global postUsuario
		global postTopico
		global postTexto
		global postTempo

		postUsuario = aux1
		postTopico = aux2
		postTexto = aux3
		postTempo = aux4	
		

		
		

	postUsuario.append(usuario)	
	postTopico.append(topico)	
	postTexto.append(texto)	
	postTempo.append(tempo)  
	postId.append(ide)	

	aux = postQnt
	global postQnt
	postQnt = aux + 1

	if(urlveio==""):
		return "Servidor espelho nao esta conectado"
	else:
		try:
			espelho = xmlrpclib.ServerProxy(urlveio)			
			espelho.resetingCache(postUsuario,postTopico,postTexto,postTempo)
		finally: return mandarString()
	
	


def printCache():

	# gettingCache()
	aux = postQnt
	i = 0

	print(postQnt)
	while(i<len(postUsuario)):
		
		print(postUsuario[i], postTopico[i] ,postTexto[i], postTempo[i])		
		i = i + 1
	
def getCache():

	aux1 = mandarUsuario
	aux2 = mandarTopico
	aux3 = mandarTexto
	aux4 = mandarTempo

	global mandarUsuario			
	global mandarTopico
	global mandarTexto
	global mandarTempo

	mandarUsuario = []
	mandarTopico = []
	mandarTexto = []
	mandarTempo = []

	return aux1, aux2, aux3, aux4

# Pega a Cache do outro servidor
def gettingCache():

	if(urlveio==""):
		return "Servidor espelho nao esta conectado"
	else:
		try:
			espelho = xmlrpclib.ServerProxy(urlveio)

			global postUsuarioes			
			global postTopicoes
			global postTextoes
			global postTempoes
			global postQntes

			postUsuarioes, postTopicoes, postTextoes, postTempoes = espelho.getCache()

			aux = postUsuario
			global postUsuario
			postUsuario = aux + postUsuarioes

			aux = postTopico
			global postTopico
			postTopico = aux + postTopicoes

			aux = postTexto
			global postTexto
			postTexto = aux + postTextoes

			aux = postTempo
			global postTempo
			postTempo = aux + postTempoes

			global postQnt
			postQnt = len(postUsuario)

			tudo = zip(postUsuario, postTopico, postTexto, postTempo)

			tudo.sort(key=lambda tup: tup[3]) 

			global postUsuario
			global postTopico
			global postTexto
			global postTempo

			postUsuario, postTopico, postTexto, postTempo = map(list, zip(*tudo))				
			
		except:
			return "Servidor espelho nao esta conectado"
		else:
			return "Cache do servidor espelho obtida"

def getFullCache():
	
	global mandarUsuario			
	global mandarTopico
	global mandarTexto
	global mandarTempo

	mandarUsuario = []
	mandarTopico = []
	mandarTexto = []
	mandarTempo = []

	return postUsuario, postTopico, postTexto, postTempo

def gettingFullCache():

	if(urlveio==""):
		return "Servidor espelho nao esta conectado"
	else:
		try:
			espelho = xmlrpclib.ServerProxy(urlveio)

			global postUsuarioes			
			global postTopicoes
			global postTextoes
			global postQntes
			global postTempoes

			postUsuarioes, postTopicoes, postTextoes, postTempoes = espelho.getFullCache()

			aux = postUsuario
			global postUsuario
			postUsuario = aux + postUsuarioes

			aux = postTopico
			global postTopico
			postTopico = aux + postTopicoes

			aux = postTexto
			global postTexto
			postTexto = aux + postTextoes
			
			aux = postTempo
			global postTempo
			postTempo = aux + postTempoes

			global postQnt
			postQnt = len(postUsuario)	

			tudo = zip(postUsuario, postTopico, postTexto, postTempo)

			tudo.sort(key=lambda tup: tup[3]) 

			global postUsuario
			global postTopico
			global postTexto
			global postTempo
			
			postUsuario, postTopico, postTexto, postTempo = map(list, zip(*tudo))										
			
		except:
			return "Servidor espelho nao esta conectado"
		else:
			return "Cache do servidor espelho obtida"
	
def resetingCache(a,b,c,d):

	if(urlveio==""):
		return "Servidor espelho nao esta conectado"
	else:
		try:
			espelho = xmlrpclib.ServerProxy(urlveio)

			global postUsuario			
			global postTopico
			global postTexto
			global postTempo

			global postUsuarioes		
			global postTopicoes
			global postTextoes
			global postTempoes

			postUsuarioes = []		
			postTopicoes = []
			postTextoes	= []
			postTempoes	= []

			postUsuario = a
			postTopico = b
			postTexto = c
			postTempo = d 

		
			global postQnt
			postQnt = len(postUsuario)														
			
		except:
			return "Servidor espelho nao esta conectado"
		else:
			return "Cache do servidor espelho obtida"
	



def atualizarURL(url):

	global urlveio
	urlveio = url

	print("URL ATUALIZADA")
	print(urlveio)

	return 1


		

	
	
# -------------- CAche -------------- #


# -------------- ESPELHO -------------- #
def espelho():
	
	if(urlveio==""):
		print("Servidor espelho nao esta conectado")
	else:
		print("Tentando conectar ao espelho...")		

		try:
			espelho =  xmlrpclib.ServerProxy(urlveio)

			espelho.apresentar()
		except:
			print("Nao foi possivel obter a conexao")
		else:
			print("Conexao realizada")	


	

# -------------- ESPELHO -------------- #








# -------------- Strings para inserir, selecionar e deletar tuplas do Banco de Dados -------------- #
banco_inserir_post = "insert into post (usuario,topico,texto,datahora) values (%s,%s,%s,%s)"
banco_inserir_follow = "insert into follow (usuario,topico,datahora) values (%s,%s,%s)"
banco_deletar_follow = "delete from follow where usuario = %s and topico = %s"
banco_select_posts = "select usuario,topico,texto from post where datahora >= %s and topico in ( select topico from follow where usuario = %s)"
banco_select_postsTop = "select usuario,topico,texto from post where datahora >= %s and topico in ( select topico from follow where usuario = %s) and topico = %s"
banco_getTempo = "select cast(max(datahora) as varchar(50)) from post"
atualizandobanco = "select usuario,topico,texto, cast(datahora as varchar(50)) from post where datahora > %s"
pegandoTodostopicos = "select topico from follow where usuario = %s"

banco_getTempoPost = "select cast(max(datahora) as varchar(50)) from follow"
atualizandobancoPost = "select usuario,topico, cast(datahora as varchar(50)) from follow where datahora > %s"
# -------------- Strings para inserir, selecionar e deletar tuplas do Banco de Dados -------------- #



# -------------- FUNCOES RPC -------------- #

# O disparador chama essa funcao para saber se o Servidor esta online
def isOn():
	return 1

# Boas vindas hehehe
def sucesso():
	return "Conectado ao Servidor"

# Como usar o blog
def apresentar():
	#Strings para ajudar o usuario
	help1 = " post(@username,#topic,text)     |  follow(@username,#topic)\n"
	help4 = " ----------------------------------------------------------------\n"
	help5 = "\n                          Formato:                     \n"
	help2 = " unsubscribe(@username,#topic)   |  retrievetime(@username,date)\n"
	help3 = " retrievetopic(@username,#topic,date)\n"

	apresenta = "\n        Bem vindo ao Blog RPC, digite quit para sair,\n"
	apresenta2 = "       caso tenha duvidas digite help para saber mais.\n"

	return (apresenta+apresenta2+help5+help4+help1+help2+help3+help4)

#Insere no banco de dados o post do usuario.
def postar(usuario, topico, texto, tempo):
	#insertCache(usuario,topico,texto, ide)
	cursor.execute(banco_inserir_post, (usuario,topico,texto,tempo))
	conectarBd.commit()
	return "Postado(Banco) com sucesso" + mandarString()

#Insere no banco de dados que tal usuario segue tal topico
def seguir(usuario,topico,datahora):
	cursor.execute(banco_inserir_follow,(usuario,topico,datahora)) #Faz a insercao
	conectarBd.commit()									  #Valida a operacao
	return "Voce esta seguindo o topico " + topico + mandarString()

#Remove do banco de dados um topico que o usuario segue
def parardeSeguir(usuario,topico):
	cursor.execute(banco_deletar_follow, (usuario,topico))
	conectarBd.commit()
	return "Voce parou de seguir o topico "  + topico + mandarString()

#Retorna do banco de dados todos posts feitos a partir de tal data
#Lembrar que sao topico que o usuario segue
def mostrarPost(usuario,datahora):

	inf = postTempo[0]
	sup = postTempo[len(postTempo) - 1]
	datahora2 = datahora + " 00:00:00"

	a = datetime.strptime(inf, "%Y-%m-%d %H:%M:%S")
	b = datetime.strptime(sup, "%Y-%m-%d %H:%M:%S")
	j = datetime.strptime(datahora2, "%Y-%m-%d %H:%M:%S")

	print(a,j,b)	

	if a <= j:
		r = "Todos os posts estao na cache, acessando cache..."
		cursor.execute(pegandoTodostopicos,(usuario,))
		tops = cursor.fetchall()
		#print("Posts q o usuario segue")
		printarTuplas(tops)
	
		us = []
		top = []
		tex = []

		i = 0
		while (i<len(postTopico)):
			if postTopico[i] in topicosLista:
				us.append(postUsuario[i])
				top.append(postTopico[i])
				tex.append(postTexto[i])
			i = i + 1				
			
	
		cursor.execute(banco_select_posts,(datahora,usuario))
		tuplas = cursor.fetchall()	
		b = 1
		
	else:
		r = "Nem todos os posts estao contidos na cache, acessando banco de dados..."
		cursor.execute(banco_select_posts,(datahora,usuario))
		tuplas = cursor.fetchall()	
		b = 0
		

	return tuplas, r, b

#Retorna do banco de dados todos posts feitos a partir de tal data

#O usuario informa o tipo de topico e ele deve segui-lo
def mostrarPostTop(usuario,topico,datahora):
	cursor.execute(banco_select_postsTop,(datahora,usuario,topico))
	tuplas = cursor.fetchall()
	return tuplas

def pegarTempo():
	cursor.execute(banco_getTempo)
	tempo = cursor.fetchall()
	return tempo

def atualizarBanco(datahora):
	cursor.execute(atualizandobanco,(datahora))
	tuplas = cursor.fetchall()	
	return tuplas

def atualizarTudo():
	at = "select usuario,topico,texto, cast(datahora as varchar(50)) from post"
	cursor.execute(at)
	tuplas = cursor.fetchall()
	return tuplas

def pegarTempoPost():
	cursor.execute(banco_getTempoPost)
	tempo = cursor.fetchall()
	return tempo

def atualizarBancoPost(datahora):
	cursor.execute(atualizandobancoPost,(datahora))
	tuplas = cursor.fetchall()	
	return tuplas

def atualizarTudoPost():
	at = "select usuario,topico, cast(datahora as varchar(50)) from follow"
	cursor.execute(at)
	tuplas = cursor.fetchall()
	return tuplas





	

	

# -------------- FUNCOES RPC -------------- #


# -------------- Dados do Servidor -------------- #
global porta
porta = input("Porta: ")
global numero
numero = 1
global ip 
ip = "191.52.64.201"
# -------------- Dados do Servidor -------------- #






# -------------- Criar o servidor -------------- #
class ServerThread(threading.Thread):
    def __init__(self):
         threading.Thread.__init__(self)
         self.servidor = SimpleXMLRPCServer((ip,porta),allow_none=True)
         self.servidor.register_function(sucesso,"sucesso")
         self.servidor.register_function(apresentar,"apresentar")
         self.servidor.register_function(postar,"postar")
         self.servidor.register_function(isOn,"isOn")
	 self.servidor.register_function(seguir,"seguir")
	 self.servidor.register_function(parardeSeguir,"parardeSeguir")
         self.servidor.register_function(mostrarPost,"mostrarPost")
         self.servidor.register_function(mostrarPostTop,"mostrarPostTop")
	 self.servidor.register_function(getCache,"getCache")
	 self.servidor.register_function(gettingCache,"gettingCache")
	 self.servidor.register_function(atualizarURL,"atualizarURL")
	 self.servidor.register_function(getFullCache,"getFullCache")
	 self.servidor.register_function(gettingFullCache,"gettingFullCache")
	 self.servidor.register_function(insertCache,"insertCache")
	 self.servidor.register_function(resetingCache,"resetingCache")
	 self.servidor.register_function(pegarTempo,"pegarTempo")
	 self.servidor.register_function(atualizarBanco,"atualizarBanco")
	 self.servidor.register_function(atualizarTudo,"atualizarTudo")
	 self.servidor.register_function(pegarTempoPost,"pegarTempoPost")
	 self.servidor.register_function(atualizarBancoPost,"atualizarBancoPost")
	 self.servidor.register_function(atualizarTudoPost,"atualizarTudoPost")
	 
         
         print ("Servidor criado na porta", porta)   

    def run(self):
         self.servidor.serve_forever()

server = ServerThread()
server.start()
# -------------- Criar o servidor -------------- #

# -------------- Obter conexao do Disparador -------------- #
portaDis = raw_input("Porta do Disparador: ")
ipDis="191.52.64.201"
url = "http://" + ipDis + ":" + portaDis + "/"

disparador =  xmlrpclib.ServerProxy(url)
# -------------- Obter conexao do Disparador -------------- #


# -------------- pegando cache do espelho ----------------- #
abc = disparador.conectarEspelho(numero)
global urlveio
urlveio = abc
gettingFullCache()
# -------------- pegando cache do espelho ----------------- #






a = str (porta)
print(disparador.setInfo(numero,1,ip,a))

entrada = raw_input("-> ")
while(entrada!='asudhasuduas'):
	if(entrada=='quit'):
		print(disparador.quit(numero))
	if(entrada=='info'):
		print("Essa funcao obtem o status do servidor espelho atraves do disparador")
		print(disparador.statusEspelho(numero))
	if(entrada=='cache'):
		abc = disparador.conectarEspelho(numero)
		global urlveio
		urlveio = abc
		print(printCache())
	if(entrada=='espelho'):
		print("Essa funcao obtem o status do servdor conectando ao servidor espelho")
		abc = disparador.conectarEspelho(numero)
		global urlveio
		urlveio = abc
		print(abc)
		espelho()
	if(entrada=='getCache'):
		abc = disparador.conectarEspelho(numero)
		global urlveio
		urlveio = abc
		gettingCache()
		
	

	
		

	

	entrada = raw_input("-> ")
