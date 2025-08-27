import matplotlib.pyplot as plt

def calc_ramp(rope_length, rmp_start, rmp_end, spd_red, spdkor_not=32767):
    if rope_length > rmp_start and rope_length < rmp_end:
        del_alpha_akt = rmp_end - rope_length
        range_ = rmp_end - rmp_start
        if range_ <= 0 or del_alpha_akt < 0 or del_alpha_akt > range_:
            set_speed = spdkor_not
        else:
            set_speed = int((del_alpha_akt * 0x7FFF) / range_)
        if set_speed < spd_red:
            set_speed = spd_red
        return set_speed
    else:
        return spdkor_not

rmp_start = 1000
rmp_end = 1500
spd_red = 8000

rope_lengths = range(900, 1600, 10)
speeds = [calc_ramp(rl, rmp_start, rmp_end, spd_red) for rl in rope_lengths]

plt.plot(rope_lengths, speeds)
plt.xlabel('Rope Length')
plt.ylabel('Allowed Speed')
plt.title('Linear Ramp Calculation')
plt.grid(True)
plt.show()
