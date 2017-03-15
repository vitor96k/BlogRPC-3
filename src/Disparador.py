from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
from datetime import datetime
import threading
from time import gmtime, strftime


class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)

# ---------------------------- VARIAVEIS ---------------------------- #

global url1
url1 = ""

global s1
global s2
s1 = None
s2 = None

global maxtime
maxtime = ""

global url2
url2 = ""

global ip
global porta

global s1status	
global s2status
s1status = 0
s2status = 0

# Quantidade de requisicoes atendias por cada servidor
global qnt1
global qnt2

qnt1 = 0
qnt2 = 0

global contador1
global contador2
contador1 = -1  # soma 2
contador2 = 0  # soma 2
# --------------------------- VARIAVEIS ---------------------------- #

# ---------------------------- FUNCOES "PRIVADAS" ---------------------------- #


def atualizarContador(contador):
	if contador==1:
		aux = contador1
		global contador1
		contador1 = aux + 2
	else:
		aux = contador2
		global contador2
		contador2 = aux + 2

# Cria as variaveis que definem o status dos Servidores
def criarVariaveis():	
	global s1status	
	global s2status
	s1status = 0
	s2status = 0

# Mostra quais servidores estao online
def status():
	texto=""

	if s1status==1:
		texto = "Servidor 1 esta online e "
	else: texto = "Servidor 1 esta offline e "

	if s2status==1:
		texto = texto + "Servidor 2 esta online"
	else: texto = texto + "Servidor 2 esta offline"

	return texto

# Faz a conexao RPC com o Servidor 1 na variavel s1
def definirS1(ip,porta):
	global s1status
	global s1
	s1status = 1
	global url1
	url1 = "http://" + ip + ":" + porta + "/"
	s1 =  xmlrpclib.ServerProxy(url1)

	# ------------------------- BALANCEANDO POSTS ------------------------- #
	global maxtime
	ak = str(s1.pegarTempo())
	az = ak[3:22]
	''.join(az)
	print("O ultimo post no servidor 1 ocorreu em", az)
	maxtime = [az]	

	global s2status
	s2status = testarConexao2()
	
	if s2status==1:
		if len(az) > 14:
			tuplas = s2.atualizarBanco(maxtime)
		else:
			tuplas = s2.atualizarTudo()
		i = 0
		while(i<len(tuplas)):
			texto = tuplas[i]
			tempo = texto[3]
			tempocerto = tempo[0:22]	
			''.join(tempocerto)			
			s1.postar(texto[0],texto[1],texto[2],tempocerto)
			i = i + 1
	# ------------------------- BALANCEANDO POSTS ------------------------- #

	# ------------------------- BALANCEANDO FOLLOW ------------------------- #
	global maxtime
	ak = str(s1.pegarTempoPost())
	az = ak[3:22]
	''.join(az)
	print("O ultimo follow no servidor 1 ocorreu em", az)
	maxtime = [az]	

	global s2status
	s2status = testarConexao2()
	
	if s2status==1:
		if len(az) > 14:
			tuplas = s2.atualizarBancoPost(maxtime)
		else:
			tuplas = s2.atualizarTudoPost()
		i = 0
		while(i<len(tuplas)):
			texto = tuplas[i]
			tempo = texto[2]
			tempocerto = tempo[0:22]	
			''.join(tempocerto)			
			s1.seguir(texto[0],texto[1],tempocerto)
			i = i + 1
	# ------------------------- BALANCEANDO FOLLOW ------------------------- #


	
	

# Faz a conexao RPC com o Servidor 2 na variavel s2atualiza
def definirS2(ip,porta):
	global s2status	
	global s2
	s2status = 1
	global url2
	url2 = "http://" + ip + ":" + porta + "/"
	s2 =  xmlrpclib.ServerProxy(url2)

	# ------------------------- BALANCEANDO POSTS ------------------------- #
	global maxtime
	ak = str(s2.pegarTempo())
	az = ak[3:22]
	''.join(az)
	print("O ultimo post no servidor 2 ocorreu em",az)
	maxtime = [az]

	global s1status
	s1status = testarConexao1()

	if s1status==1:
		if len(az) > 14:
			tuplas = s1.atualizarBanco(maxtime)
		else:
			tuplas = s1.atualizarTudo()
		i = 0
		while(i<len(tuplas)):
			texto = tuplas[i]
			tempo = texto[3]
			tempocerto = tempo[0:22]
			''.join(tempocerto)	
			print(texto[0],texto[1],tempocerto)			
			s2.postar(texto[0],texto[1],texto[2],tempocerto)
			i = i + 1
	# ------------------------- BALANCEANDO POSTS ------------------------- #
	

	# ------------------------- BALANCEANDO FOLLOW ------------------------- #
	global maxtime
	ak = str(s2.pegarTempoPost())
	az = ak[3:22]
	''.join(az)
	print("O ultimo follow no servidor 2 ocorreu em", az)
	maxtime = [az]	

	global s1status
	s1status = testarConexao2()
	
	if s1status==1:
		if len(az) > 14:
			tuplas = s1.atualizarBancoPost(maxtime)
		else:
			tuplas = s1.atualizarTudoPost()
		i = 0
		while(i<len(tuplas)):
			texto = tuplas[i]
			tempo = texto[2]
			tempocerto = tempo[0:22]	
			''.join(tempocerto)	
			print(texto[0],texto[1],tempocerto)		
			s2.seguir(texto[0],texto[1],tempocerto)
			i = i + 1
	# ------------------------- BALANCEANDO FOLLOW ------------------------- #




#Testar conexao com o servidor
def testarConexao1():
	try:
		s1.apresentar()
	except:
		# print("Ouve um erro no Servidor 1")
		encerrarServidor(1)
		return 0
	else:
		# print("Nao ouve erro no Servidor 1")
		return 1
	

def testarConexao2():
	try:
		s2.apresentar()
	except:
		 # print("Ouve um erro no Servidor 2")
		encerrarServidor(2)
		return 0
	else:
		# print("Nao ouve erro no Servidor 2")
		return 1


	
# ---------------------------- FUNCOES "PRIVADAS" ---------------------------- #

# ---------------------------- FUNCOES RPC ---------------------------- #

# Servidor avisa que vai ficar off
def encerrarServidor(serv):
	if serv==1:
		global s1
		global s1status
		s1status = 0
		global url1
		url1 = ""

	if serv==2:
		global s2
		global s2status
		s2status = 0
		global url2
		url2 = ""

	return ""

# Boas vindas hehe
def sucesso():
	return "Conectado ao Disparador"

# Definir cada servidor e sua situacao
def setInfo(ide,status,ip,porta):
	if ide==1 and status==1:
		definirS1(ip,porta)
		print("Conectado ao Servidor 1")
		return "Disparador sabe que esta online"

	if  ide==2 and status==1:
		definirS2(ip,porta)
		print("Conectado ao Servidor 2")
		return "Disparador sabe que esta online"

# Informar a situacao do outro Servidor quando um Servidor pedir
def outroServidor(serv):

	texto1 = ""
	texto2 = ""

	if s1status==1:
		texto1 = "O outro Servidor esta online"
	else: texto1 = "O outro Servidor esta offline"

	if s2status==1:
		texto2 = "O outro Servidor esta online"
	else: texto2 = "O outro Servidor esta offline"

	if serv==1:
		return texto2
	else: return texto1

# Enumerar quantidade de requisicoes atendidas por cada servidor, se tiver somente um o nenhum a contagem para.
def incrementar(serv):
	if serv == 2:
		copia = qnt2
		global qnt2
		qnt2 = copia + 1
	elif serv == 1:
		copia = qnt1
		global qnt1
		qnt1 = copia + 1

def postar(usuario,topico,texto):

	try:
		global s1status
		s1status = testarConexao1()
		global s2status
		s2status = testarConexao2()	

		atualizarURLSS()
	finally: a = 0

	#Caso os dois servidores estejam online
	try:
		if s1status == 1 and s2status==1:
			if qnt1 > qnt2:
				incrementar(2)
				atualizarContador(2)				
				return s2.insertCache(usuario,topico,texto,contador2)			
			else:
				incrementar(1)
				atualizarContador(1)
				return s1.insertCache(usuario,topico,texto,contador1)

		elif s1status == 1 and s2status!=1:
			# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
			atualizarContador(1)
			return s1.insertCache(usuario,topico,texto,contador1)

		elif s2status == 1 and s1status!=1:
			# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
			atualizarContador(2)
			return s2.insertCache(usuario,topico,texto,contador2)

		else: return "Nenhum Servidor esta Online"

	finally: atualizarCaches()
		

	
	

def apresentar():
	if s1status == 1 and s2status==1:
		if qnt1 > qnt2:
			incrementar(2)
			return s2.apresentar()
		else:
			incrementar(1)
			return s1.apresentar()

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s1.apresentar()
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s2.apresentar()
	else: return "Nenhum Servidor esta Online"

def seguir(usuario,topico):

	global s1status
	s1status = testarConexao1()
	global s2status
	s2status = testarConexao2()	

	tempo = strftime("%Y-%m-%d %H:%M:%S", gmtime()  )

	#Caso os dois servidores estejam online
	if s1status == 1 and s2status==1:
		a = s2.seguir(usuario,topico,tempo)		
		b = s1.seguir(usuario,topico,tempo)
		return "Vc esta seguindo o topico " + topico

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		a = s1.seguir(usuario,topico,tempo)
		return "Vc esta seguindo o topico " + topico
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		a = s2.seguir(usuario,topico,tempo)
		return "Vc esta seguindo o topico " + topico
	else: return "Nenhum Servidor esta Online"

def parardeSeguir(usuario,topico):

	global s1status
	s1status = testarConexao1()
	global s2status
	s2status = testarConexao2()	

	#Caso os dois servidores estejam online
	if s1status == 1 and s2status==1:
		if qnt1 > qnt2:
			incrementar(2)
			return s2.parardeSeguir(usuario,topico)
		else:
			incrementar(1)
			return s1.parardeSeguir(usuario,topico)

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s1.parardeSeguir(usuario,topico)
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s2.parardeSeguir(usuario,topico)
	else: return "Nenhum Servidor esta Online"

def pegarCache():
	global s1status
	s1status = testarConexao1()
	global s2status
	s2status = testarConexao2()

	if s1status==1:
		return s1.getCache()
	if s2status==1:
		return s2.getCache()
	else: return 1

def pegarTopico(user):
	return 1


def mostrarPost(usuario,datahora):

	atualizarCaches()

	

	#global s1status
	#s1status = testarConexao1()
	#global s2status
	#s2status = testarConexao2()	

	#Caso os dois servidores estejam online
	if s1status == 1 and s2status==1:
		if qnt1 > qnt2:
			incrementar(2)
			a, k, z = s2.mostrarPost(usuario,datahora)
			return a, k, z
		else:
			incrementar(1)
			a,k,z = s1.mostrarPost(usuario,datahora)
			return a, k, z

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		a, k, z = s1.mostrarPost(usuario,datahora)
		return a, k, z
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		a, k, z = s2.mostrarPost(usuario,datahora)
		return a, k, z
	else: return "Nenhum Servidor esta Online", "[ERRO DE CONEXAO]", 3

def mostrarParalelo(usuario,datahora):
	t1 = FuncThread(mostrarPost, usuario,datahora)
	t1.start()
	t1.join

def mostrarPostTop(usuario,topico,datahora):
	
	atualizarCaches()

	global s1status
	s1status = testarConexao1()
	global s2status
	s2status = testarConexao2()	

	#Caso os dois servidores estejam online
	if s1status == 1 and s2status==1:
		if qnt1 > qnt2:
			incrementar(2)
			return s2.mostrarPostTop(usuario,topico,datahora)
		else:
			incrementar(1)
			return s1.mostrarPostTop(usuario,topico,datahora)

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s1.mostrarPostTop(usuario,topico,datahora)
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s2.mostrarPostTop(usuario,topico,datahora)
	else: return "Nenhum Servidor esta Online"


def conectarEspelho(servidor):
	
	global s1status

	if servidor==1:
		global s2status
		s2status = testarConexao2()
		return url2
	else:
		global s1status
		s1status = testarConexao1()
		return url1


def atualizarCaches():

	try:
		global s1status
		s1status = testarConexao1()
		global s2status
		s2status = testarConexao2()	

		#Caso os dois servidores estejam online
		if s1status == 1 and s2status==1:
			s1.atualizarURL(url2)
			s2.atualizarURL(url1)
			s1.gettingCache()
			s2.gettingCache()

	finally: return 1

def atualizarURLSS():

	if s1status == 1:
		s1.atualizarURL(url2)
	if s2status == 1:
		s2.atualizarURL(url1)




# ---------------------------- FUNCOES RPC ---------------------------- #

ip = "191.52.64.201"
porta = input("Porta: ")

# -------------- Criar o Disparador -------------- #
class ServerThread(threading.Thread):
    def __init__(self):
         threading.Thread.__init__(self)
         self.disparador = SimpleXMLRPCServer((ip,porta), allow_none=True)
         self.disparador.register_function(sucesso,"sucesso") #just return a string
         self.disparador.register_function(setInfo,"setInfo")
         self.disparador.register_function(encerrarServidor,"quit")
         self.disparador.register_function(outroServidor,"statusEspelho")
         self.disparador.register_function(postar,"postar")
       	 self.disparador.register_function(apresentar,"apresentar")
	 self.disparador.register_function(seguir,"seguir")
	 self.disparador.register_function(parardeSeguir,"parardeSeguir")
         self.disparador.register_function(mostrarPost,"mostrarPost")
         self.disparador.register_function(mostrarPostTop,"mostrarPostTop")
         self.disparador.register_function(conectarEspelho,"conectarEspelho")
	 self.disparador.register_function(atualizarCaches,"atualizarCaches")
	 self.disparador.register_function(pegarCache, "pegarCache")


         print ("Disparador criado na porta", porta)   

    def run(self):
         self.disparador.serve_forever()

disp = ServerThread()
disp.start()
# -------------- Criar o Disparador -------------- #

criarVariaveis()


# -------------- Prompt Disparador -------------- #
entrada = raw_input("-> ")
while(entrada!='sadasuhduache'):
	if entrada=='info':
		testarConexao1()
		testarConexao2()
		print(status())
	


	entrada = raw_input("-> ")
# -------------- Prompt Disparador -------------- #




