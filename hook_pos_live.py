import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ----------------------------
# Hard-coded parameters
# ----------------------------
L_main = 3.0       # length of main boom
L_outer = 1.0      # length of outer boom (without extension)
l_ext = 1.0        # telescopic extension length
R_col = 0.0        # radius/offset of crane column

# initial angles
alpha_A_deg_init = 60
alpha_B_deg_init = -90

# Function to calculate coordinates and r_hook
def calculate_geometry(alpha_A_deg, alpha_B_deg):
    alpha_A = np.radians(alpha_A_deg)
    alpha_B = np.radians(alpha_B_deg)

    x_A, y_A = 0.0, R_col
    x_B = x_A + L_main * np.cos(alpha_A)
    y_B = y_A + L_main * np.sin(alpha_A)
    x_H = x_B + (L_outer + l_ext) * np.cos(alpha_A + alpha_B)
    y_H = y_B + (L_outer + l_ext) * np.sin(alpha_A + alpha_B)
    r_hook = L_main*np.cos(alpha_A) + (L_outer + l_ext)*np.cos(alpha_A + alpha_B) - R_col

    return (x_A, y_A, x_B, y_B, x_H, y_H, r_hook)

# helper: set axis limits so all points are visible and aspect is equal
def set_crane_limits(ax, xs, ys, margin_frac=0.12, min_side=0.5):
    """
    Set ax limits to a square window that contains all points (xs, ys),
    with an additional fractional margin (margin_frac).
    min_side prevents the window from collapsing to zero size.
    """
    min_x, max_x = np.min(xs), np.max(xs)
    min_y, max_y = np.min(ys), np.max(ys)

    width = max_x - min_x
    height = max_y - min_y
    side = max(width, height, min_side)

    # add fractional margin
    side *= (1.0 + margin_frac)

    center_x = 0.5 * (min_x + max_x)
    center_y = 0.5 * (min_y + max_y)

    ax.set_xlim(center_x - side/2, center_x + side/2)
    ax.set_ylim(center_y - side/2, center_y + side/2)

# prepare r_hook vs alpha_A curve
alpha_A_range = np.linspace(0, 80, 1000)  # finer grid

def r_hook_curve(alpha_B):
    return (L_main*np.cos(np.radians(alpha_A_range)) +
            (L_outer + l_ext)*np.cos(np.radians(alpha_A_range) + np.radians(alpha_B)) - R_col)

# Create figure and axes with custom size
fig = plt.figure(figsize=(20, 10))
ax1 = fig.add_axes([0.05, 0.3, 0.6, 0.65])  # larger crane geometry plot
ax2 = fig.add_axes([0.7, 0.3, 0.25, 0.4])   # smaller r_hook plot

# Initial plot
x_A, y_A, x_B, y_B, x_H, y_H, r_hook = calculate_geometry(alpha_A_deg_init, alpha_B_deg_init)

# Crane geometry plot
col_line, = ax1.plot([0, x_A], [0, y_A], 'k-', lw=3, label="Column")
main_boom_line, = ax1.plot([x_A, x_B], [y_A, y_B], 'b-', lw=3, label="Main boom")
outer_boom_line, = ax1.plot([x_B, x_H], [y_B, y_H], 'g-', lw=3, label="Outer + Extension boom")
hook_point, = ax1.plot(x_H, y_H, 'ro', markersize=10, label="Hook")
ax1.axhline(0, color='k', linewidth=0.8)
ax1.axvline(0, color='k', linewidth=0.8)
ax1.set_aspect('equal', adjustable='box')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.set_xlabel("Horizontal distance [m]")
ax1.set_ylabel("Vertical distance [m]")
ax1.set_title("Crane Geometry")
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)

# Set initial axis limits so entire crane is visible
xs_init = np.array([0.0, x_A, x_B, x_H])
ys_init = np.array([0.0, y_A, y_B, y_H])
set_crane_limits(ax1, xs_init, ys_init, margin_frac=0.12, min_side=1.0)

# r_hook vs alpha_A plot
r_hook_values = r_hook_curve(alpha_B_deg_init)
r_hook_line, = ax2.plot(alpha_A_range, r_hook_values, 'b-', lw=2, label="r_hook(αA)")
alphaA_vline = ax2.axvline(alpha_A_deg_init, color='r', linestyle='--')
rhook_hline = ax2.axhline(r_hook, color='g', linestyle='--')
ax2.set_xlabel("αA (deg)")
ax2.set_ylabel("Hook radius r_hook [m]")
ax2.set_title("Hook radius vs Main Boom Angle")
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1)

# Sliders
ax_alpha_A = fig.add_axes([0.15, 0.15, 0.65, 0.03])
ax_alpha_B = fig.add_axes([0.15, 0.1, 0.65, 0.03])
slider_alpha_A = Slider(ax_alpha_A, 'αA (deg)', 0, 80, valinit=alpha_A_deg_init)
slider_alpha_B = Slider(ax_alpha_B, 'αB (deg)', -180, 180, valinit=alpha_B_deg_init)

# Update function
def update(val):
    alpha_A_deg = slider_alpha_A.val
    alpha_B_deg = slider_alpha_B.val
    x_A, y_A, x_B, y_B, x_H, y_H, r_hook = calculate_geometry(alpha_A_deg, alpha_B_deg)

    # Update crane geometry
    col_line.set_data([0, x_A], [0, y_A])
    main_boom_line.set_data([x_A, x_B], [y_A, y_B])
    outer_boom_line.set_data([x_B, x_H], [y_B, y_H])
    hook_point.set_data([x_H], [y_H])

    # Compute bounding box and set square limits so the whole crane is visible
    xs = np.array([0.0, x_A, x_B, x_H])
    ys = np.array([0.0, y_A, y_B, y_H])
    set_crane_limits(ax1, xs, ys, margin_frac=0.12, min_side=1.0)

    # Update r_hook plot
    r_hook_values = r_hook_curve(alpha_B_deg)
    r_hook_line.set_ydata(r_hook_values)
    alphaA_vline.set_xdata(alpha_A_deg)
    rhook_hline.set_ydata(r_hook)
    ax2.legend([r_hook_line, alphaA_vline, rhook_hline],
               ["r_hook(αA)", f"Current αA={alpha_A_deg:.1f}°", f"Current r_hook={r_hook:.2f} m"],
               loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1)

    fig.canvas.draw_idle()

slider_alpha_A.on_changed(update)
slider_alpha_B.on_changed(update)

plt.show()
