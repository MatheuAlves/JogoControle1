import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, impulse

# Defina os valores dos polos e zeros diretamente
poles = [10 + 0j, 1 + 0j]  # Exemplo com dois polos complexos conjugados
zeros = [10]  # Exemplo com um zero

# Cria a função de transferência com base nos polos e zeros fornecidos
numerator = np.poly(zeros)
denominator = np.poly(poles)

sys = TransferFunction(numerator, denominator)

# Calcula a resposta ao impulso
t, y = impulse(sys)

# Plota a resposta ao impulso
plt.plot(t, y)
plt.xlabel('Tempo')
plt.ylabel('Resposta ao Impulso')
plt.title('Resposta ao Impulso da Função de Transferência')
plt.grid(True)
plt.show()
