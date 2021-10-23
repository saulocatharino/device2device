import pyaudio
import numpy as np


# Lista para codificação das classes em multi-frequencia
# Cada caracter representa uma frequencia mixada no pulso sonoro.
# É preciso que seja em ordem numérica-alfabética, pois, o resultado da transformada vem nesta ordem,
# Já que o áudio é mixado e enviado paralelamente, não em série
encrypted = ['0ag','1bh','2ci','3dj','4ek','5fl']

# Rótulos das classes
decrypted = ['esquerda','trás','direita','frente','cima','baixo']


# Cria lista com frequências permitidas, derivadas dos valores do código ASCII de cada caracter.


def recog(arr):

	# Valor entre 0 e 1 para corte de ruído de fundo
	threshold = .3

	# Transformada de Fourier no sinal 
	fft_spectrum = np.fft.rfft(arr)
	
	# Calcula o absoluto da intensidade de cada frequência do sinal
	fft_spectrum_abs = np.abs(fft_spectrum)  


	# cria array com as frequencias do sinal de acordo com o bitrate	
	freq = np.fft.rfftfreq(len(arr), d=1./RATE)

	# Normaliza as intensidades entre 0 e 1 para aplicar o filtro de corte de ruído de fundo
	fft_spectrum_abs_norm = fft_spectrum_abs / fft_spectrum_abs.max()

	# Cria máscara com os index das intensidades acima do threshold de ruído de fundo
	mask = np.where(fft_spectrum_abs_norm >= threshold)

	# Cria array com os index aplicando a máscara nas frequências detectadas
	filtered = freq[mask]

	finded = ''
	temp = []
	# Loop em cada frequência detectada acima do Threshold
	for f in filtered:
		# Loop em cada frequência do Range

		for allowed in alloweds:
			# Aplica tolerância de 5 Hz para cima e para baixo das notas filtradas
			if f > allowed -5 and f < allowed + 5:
				# Caso essa frequencia esteja no range de tolerância é substituida pela frequencia relativa
				# Da lista de permitidos mais próxima do valor obtido na transformada
				if allowed not in temp:
					temp.append(allowed)
					finded += chr(allowed//canal)
	return finded


RATE = 44100 

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, input_device_index = 8, frames_per_buffer=RATE)


while True:
	arq = open("canal.txt","r")
	canal = int(arq.readline())
	arq.close()

	alloweds = []
	for i in range(33,123):
		alloweds.append(i * canal)

	#print(canal)

	# Adquire 1 segundo de áudio do streaming
	data = stream.read(int(RATE))

	# Converte string em array 
	arr = np.fromstring(data, np.int16)



	# Função para transformada, filtros e conversão da frequencia em caracter
	result = recog(arr)

	# Verifica se sequencia da lista criptografada faz parte da string resultante do áudio analisado
	for e, en in enumerate(encrypted):
		if en in result:
			print("Canal {} -> Comando: {}".format(canal,decrypted[e]))

