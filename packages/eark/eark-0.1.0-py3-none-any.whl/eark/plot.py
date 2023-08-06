"""Plotting utilities for eark

"""


import matplotlib.pyplot as plt


plt.plot(t, s[:, 0], 'r--', label='neutron population', linewidth=2.0)
plt.plot(t, s[:, 1], 'g-', label='Delayed Group 1', linewidth=2.0)
plt.plot(t, s[:, 2], 'y-', label='Delayed Group 2', linewidth=2.0)
plt.plot(t, s[:, 3], 'c-', label='Delayed Group 3', linewidth=2.0)
plt.plot(t, s[:, 4], 'm-', label='Delayed Group 4', linewidth=2.0)
plt.plot(t, s[:, 5], 'k-', label='Delayed Group 5', linewidth=2.0)
plt.plot(t, s[:, 6], 'b-', label='Delayed Group 6', linewidth=2.0)
plt.xlabel("t")
plt.ylabel("Concentration")
plt.legend(["N", "C"])
plt.show()