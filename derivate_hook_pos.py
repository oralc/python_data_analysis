
import numpy as np
import matplotlib.pyplot as plt


L_main = 3.0       # length of main boom
L_outer = 1.0      # length of outer boom (without extension)
l_ext = 1.0        # telescopic extension length
R_col = 0.0        # radius/offset of crane column

alpha_B_deg_init = -90
alpha_A_deg_init = 60

alpha_A_range = np.linspace(0, 80, 1000)  # degrees
alpha_A_rad = np.radians(alpha_A_range)
alpha_B_rad = np.radians(alpha_B_deg_init)

# r_hook as function of alpha_A (radians)
r_hook = L_main * np.cos(alpha_A_rad) + (L_outer + l_ext) * np.cos(alpha_A_rad + alpha_B_rad) - R_col

# Differentiate r_hook with respect to alpha_A
#dr_hook_dalpha_A = sp.diff(r_hook, alpha_A)


# analytical derivative w.r.t alpha_A (radians)
# dr/dalphaA = -L_main*sin(alpha_A) - (L_outer + l_ext)*sin(alpha_A + alpha_B)
dr_dalphaA = -L_main * np.sin(alpha_A_rad) - (L_outer + l_ext) * np.sin(alpha_A_rad + alpha_B_rad)


dr_dalphaA_per_deg = dr_dalphaA * (np.pi / 180.0)

plt.figure(figsize=(8,4))
plt.plot(alpha_A_range, r_hook, linewidth=2)
plt.axvline(alpha_A_deg_init, linestyle='--')
current_r = (L_main*np.cos(np.radians(alpha_A_deg_init)) + 
             (L_outer + l_ext)*np.cos(np.radians(alpha_A_deg_init) + np.radians(alpha_B_deg_init)) - R_col)
plt.axhline(current_r, linestyle='--')
plt.xlabel("αA (deg)")
plt.ylabel("r_hook [m]")
plt.title("r_hook vs αA")
plt.grid(True, linestyle='--', alpha=0.6)

# plot 2: derivative dr/dalpha_A (per rad) and per degree
plt.figure(figsize=(8,4))
plt.plot(alpha_A_range, dr_dalphaA, linewidth=2, label="dr/dαA (per rad)")
plt.plot(alpha_A_range, dr_dalphaA_per_deg, linewidth=1.5, linestyle=':', label="dr/dαA (per deg)")
# mark current alpha_A
current_idx = np.argmin(np.abs(alpha_A_range - alpha_A_deg_init))
plt.axvline(alpha_A_deg_init, linestyle='--')
plt.scatter([alpha_A_deg_init], [dr_dalphaA[current_idx]])
plt.xlabel("αA (deg)")
plt.ylabel("Derivative of r_hook")
plt.title("Derivative of r_hook w.r.t αA")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# print analytic formulas and current values
print("Analytic derivative (radians): dr/dαA = -L_main*sin(αA) - (L_outer + l_ext)*sin(αA + αB)")
print("Value at current αA = {:.1f}°: dr/dαA = {:.4f} m/rad".format(alpha_A_deg_init, dr_dalphaA[current_idx]))
print("Equivalent per degree: dr/dαA_deg = {:.6f} m/deg".format(dr_dalphaA_per_deg[current_idx]))

plt.show()