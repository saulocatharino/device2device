import numpy as np
import simpleaudio as sa


RATE = 44100
# Lista para codificação das classes em multi-frequencia
# Cada caracter será convertido uma frequência, todas serão mixada em um único pulso sonoro
encrypted = ['0ag','1bh','2ci','3dj','4ek','5fl']

# Rótulo de cada classe 
decrypted = ['esquerda','trás','direita','frente','cima','baixo']

# A frequencia selecionada será o produto do canal pelo ascii do caracter
canal = 101

def send(caracteres):
	# Duração do pulso em segundos
	seconds = .25

	# Para cada caracter da string recebida será gerado um pulso sonoro
	for e, c in enumerate(caracteres):

		# Converte caracter em INT 
		k = ord(c)

		# Multiplica o valor de ASCII por 10, aumentando a distância entre as classes
		# desta forma, temos 10hz para cima e 10hz para baixo de tolerância, também para ficar no espectro audível.
		# Ex. o caracter de ascii 49 e 50 se tornam 490hz e 500hz.

		frequencia = int(k) * canal
		# Cria array com valores entre 0 e a quantidade de segundos com X (seconds * sample_rate) intervalos. 
		t = np.linspace(0, seconds, int(seconds * RATE))

		# Cria a onda na frequencia selecionada para síntese sonora
		note = np.sin(frequencia * t * 2 * np.pi)

		# Eleva a amplitude do pulso sonoro ao limite  menos um (2**15 - 1 = 32768 - 1) , para não saturar o áudio.
		sint = note * (2**15 - 1)

		# converte array de áudio para o formato int16.
		audio_temp = sint.astype(np.int16)

		# Faz a mixagem das múltiplas frequências em um único pulso sonoro.
		if e == 0:
			audio_final = audio_temp
		else:
			audio_final = audio_final//2 + audio_temp//2

	# Executa pulso sonoro sintetizado e multi-frequencial.
	sa.play_buffer(audio_final, 1, 2, RATE)



while True:
	arq = open("canal.txt","r")
	canal = int(arq.readline())
	arq.close()
	enviado = False
	s = input("Comando: ")
	if 'canal' in s:
		val = int(s.split(' ')[1])
		print(">>> Canal alterado de {} para {}".format(canal,val))
		canal = val
		enviado = True
		arq = open("canal.txt","w")
		arq.write(str(canal))
		arq.close()

		
	for e, d in enumerate(decrypted):
		# Verifica se direção está na lista de comandos
		if s == d:
			print(">>> Canal {} -> Comando {} enviado. \n".format(canal, decrypted[e]))
			#Envia string da lista relacionada ao comando para ser convertida em pulso sonoro
			send(encrypted[int(e)])
			enviado = True
	if not enviado:
		print(">>> ERRO - Comando desconhecido. \n")


