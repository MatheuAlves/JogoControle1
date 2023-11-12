import numpy as np
import matplotlib.pyplot as plt
import control.matlab as clt
import random

choice = random.choice(['1', '2'])

lower_limit = 0.0
upper_limit = 10.0

if choice == '1':
    rd_num_c1 = random.uniform(lower_limit, upper_limit)
    num = np.array([rd_num_c1])
    rd_den_c1 = random.uniform(lower_limit, upper_limit)
    den = np.array([1, rd_den_c1])
elif choice == '2':
    rd_num_c1 = random.uniform(lower_limit, upper_limit)
    rd_num_c2 = random.uniform(lower_limit, upper_limit)
    num = np.array([rd_num_c1, rd_num_c2])
    rd_den_c1 = random.uniform(lower_limit, upper_limit)
    rd_den_c2 = random.uniform(lower_limit, upper_limit)
    den = np.array([1, rd_den_c1, rd_den_c2])

H_continous = clt.tf(num, den)
print(H_continous)

sample_time = 0.01
H_discrete = clt.sample_system(H_continous, sample_time, method='zoh')

total_time = 10.0
time_interval = np.arange(0, total_time + sample_time, sample_time)

yout, T = clt.step(H_discrete, time_interval)

plt.stem(T, yout, basefmt='b', linefmt='r', markerfmt='r.')
plt.title('Step Response')
plt.xlabel('Time')
plt.ylabel('Response')
plt.grid(True)
plt.show()
