import xmlrpclib
from datetime import datetime

# ---------------------------- INFORMACOES PARA CONECTAR AO DISPADRADOR ---------------------------- #
ok = 0

while(ok==0):

	# Definicoes de porta e IP do servidor
	porta = raw_input("Porta do Disparador: ")
	ip="191.52.64.201"
	url = "http://" + ip + ":" + porta + "/"

	# Faz a conexao com o servidor RPC
	disparador =  xmlrpclib.ServerProxy(url)

	# Ve se a conexao foi feita
	try:
		ok = 1
		print(disparador.sucesso())
	except:
		ok = 0
# ---------------------------- INFORMACOES PARA CONECTAR AO DISPADRADOR ---------------------------- #

def printarTuplas(tuplas):
	tam = len(tuplas)
	i = 0

	while(i<tam):
		texto = tuplas[i]
		print("Usuario: %s Topico: %s Texto: %s" % (texto[0],texto[1],texto[2]))
		i = i + 1

# ---------------------------- Prompt Cliente ---------------------------- #
print(disparador.apresentar())
user = raw_input("\nUsuario: ")
entrada = raw_input("-> ")
while(entrada!='quit'):

	if entrada=='post':
		topico = raw_input("Topico: ")                 
		texto = raw_input("Texto: ")  		
		print(disparador.postar(user,topico,texto))
		

	if entrada=='follow':
		topico = raw_input("Topico: ") 
		print(disparador.seguir(user,topico))		

	if entrada=='unsubscribe':
		topico = raw_input("Topico: ") 
		print(disparador.parardeSeguir(user,topico))	

	if entrada=='retrievetime':
		dia = raw_input("Dia: ")   
		mes = raw_input("Mes: ")
		ano = raw_input("Ano: ")
		
		data = ano + "-" + mes + "-" + dia

		tuplas, msg, gk = disparador.mostrarPost(user,data)
		
		#print(msg)
		if gk == 0 :
			printarTuplas(tuplas)	
		elif gk ==1:
			print("Printar Diferente")
		else:
			print("Nenhum Servidor online")



	if entrada=='retrievetopic':

		topico = raw_input("Topico: ") 

		dia = raw_input("Dia: ")   
		mes = raw_input("Mes: ")
		ano = raw_input("Ano: ")
		
		data = ano + "-" + mes + "-" + dia

		tuplas = disparador.mostrarPostTop(user,topico,data)
		
		printarTuplas(tuplas)	
		

	




	

	entrada = raw_input("-> ")
# ---------------------------- Prompt Cliente ---------------------------- #
