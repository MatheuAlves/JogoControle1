import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parâmetros do sistema discreto (você pode ajustar conforme necessário)
numerator = [1.0]  # Coeficientes do numerador da função de transferência discreta
denominator = [1.0, 1.0, 100.0]  # Coeficientes do denominador da função de transferência discreta

# Tempo de simulação discreto
time_discrete = np.arange(0, 20, 1)  # Tempo discreto de 0 a 20 com passo 1

# Criar a função de transferência discreta
system_discrete = signal.dlti(numerator, denominator, dt=1.0)  # dt é o intervalo de amostragem

# Gerar resposta ao degrau discreto
time_discrete, response_discrete = signal.dstep(system_discrete)

# Ajustar o shape da resposta ao degrau
response_discrete = np.squeeze(response_discrete)

# Plotar a resposta ao degrau discreto
plt.stem(time_discrete, response_discrete)
plt.title('Resposta ao Degrau Discreto')
plt.xlabel('Tempo discreto')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()
