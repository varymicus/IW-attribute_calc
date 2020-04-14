import math

inputs = []
with open('inputs.txt') as f:
    for line in f:
        inputs.append(line[line.find(":")+2:-1])

print(inputs)

# INPUTS
attribute_cap = int(inputs[0]) #200
free_points = int(inputs[1]) #1000
myst_power = float(inputs[2]) #0.04
void_profit = float(inputs[3]) #0.16
achievements = int(inputs[4]) #782
achievement_points = int(inputs[5]) #14790
upgrades = int(inputs[6]) #1209
ve_collected = float(inputs[7]) #2E4
ve_lifetime = float(inputs[8]) #5.19E7
ve_spawnrate = float(inputs[9]) #4.84E6
spells_cast = float(inputs[10]) #1E10
accumulated_casts = float(inputs[11]) #1E6
shards_collected = float(inputs[12]) #1E17
evocation_casts = float(inputs[13]) #1E9
shards_per_sec = float(inputs[14]) #2E24
autoclicks = float(inputs[15]) #1E6
sources = int(inputs[16]) #86400
idle_time = float(inputs[17]) #5E4
green_catalyst_power = float(inputs[18]) #1.025
hero_level = int(inputs[19]) #175
pet_level = int(inputs[20]) #225
pet_time = float(inputs[21]) #5E4


# Scaling Power Values
myst_scale = 1.00
profit_scale = 1.00
shard_scale = 1.35
pet_ap_scale = 1.28
char_ap_scale = 1.00
cap_growth_scale = 1.7
idle_scale = 1.00
vp_scale = 1.00
ve_scale = 1.00
autoclick_scale = 0.00
evo_scale = 1.00
inc_scale = 6.6
crit_scale = 0

i_scale = 1.02 ** myst_scale
n_scale = 1.022 ** ve_scale
s_scale = 1.03 ** evo_scale
w_scale = 1.02 ** shard_scale
d_scale = 1.029 ** autoclick_scale
p_scale = 1.03 ** idle_scale
m_scale = 1.018 ** char_ap_scale
e_scale = 1.018 ** pet_ap_scale

debug = 0

def optimize(i_min, i_add, n_min, n_add, s_min, s_add, w_min, w_add, d_min, d_add, p_min, p_add, m_min, m_add, e_min, e_add):

    multiplier = 1.00
    ptsSpent = 0
    spread = [i_min + i_add, n_min + n_add, s_min + s_add, w_min + w_add, d_min + d_add, p_min + p_add, m_min + m_add, e_min + e_add]
    print(spread)

    for i in range (i_min + i_add, attribute_cap + 1, 25):
        ptsSpent = i - i_add
        if ptsSpent <= free_points:
            i_mult = calc_i_mult(i)
            for n in range (n_min + n_add, attribute_cap + 1, 5):
                ptsSpent = i + n - i_add - n_add
                if ptsSpent <= free_points:
                    n_mult = calc_n_mult(n)
                    for s in range (s_min + s_add, attribute_cap + 1, 25):
                        ptsSpent = i + n + s - i_add - n_add - s_add
                        if ptsSpent <= free_points:
                            s_mult = calc_s_mult(s)
                            for w in range (w_min + w_add, attribute_cap + 1, 25):
                                ptsSpent = i + n + s + w - i_add - n_add - s_add - w_add
                                if ptsSpent <= free_points:
                                    w_mult = calc_w_mult(w)
                                    for d in range (d_min + d_add, attribute_cap + 1, 25):
                                        ptsSpent = i + n + s + w + d - i_add - n_add - s_add - w_add - d_add
                                        if ptsSpent <= free_points:
                                            d_mult = calc_d_mult(d)
                                            for p in range (p_min + p_add, attribute_cap + 1, 25):
                                                ptsSpent = i + n + s + w + d + p - i_add - n_add - s_add - w_add - d_add - p_add
                                                if ptsSpent <= free_points:
                                                    p_mult = calc_p_mult(p)
                                                    for m in range (m_min + m_add, attribute_cap + 1, 25):
                                                        ptsSpent = i + n + s + w + d + p + m - i_add - n_add - s_add - w_add - d_add - p_add - m_add
                                                        if ptsSpent <= free_points:
                                                            m_mult = calc_m_mult(m)
                                                            for e in range (e_min + e_add, attribute_cap + 1, 25):
                                                                ptsSpent = i + n + s + w + d + p + m + e - i_add - n_add - s_add - w_add - d_add - p_add - m_add - e_add
                                                                if ptsSpent <= free_points:
                                                                    e_mult = calc_e_mult(e)
                                                                    temp = i_mult * n_mult * s_mult * w_mult * d_mult * p_mult * m_mult * e_mult
                                                                    if temp > multiplier:
                                                                        multiplier = temp
                                                                        spread = [i,n,s,w,d,p,m,e]
    print("{:.2e}, {:.2e}, {:.2e}, {:.2e}, {:.2e}, {:.2e}".format(calc_i_mult(spread[0]), calc_n_mult(spread[1]), calc_s_mult(spread[2]), calc_w_mult(spread[3]), calc_d_mult(spread[4]), calc_p_mult(spread[5])))
    return spread

def calc_i_mult(i):
    mult = i_scale ** i
    if i >= 25: mult *= ((0.02 + myst_power) / myst_power) ** myst_scale
    if i >= 50: mult *= ((0.04 + myst_power) / (0.02 + myst_power)) ** myst_scale
    if i >= 100: mult *= ((0.07 + myst_power) / (0.04 + myst_power)) ** myst_scale
    if i >= 125: mult *= ((0.12 + myst_power) / (0.07 + myst_power)) ** myst_scale
    if i >= 150: mult *= ((0.0035 * free_points) + 1) ** profit_scale
    if i >= 175: mult *= ((0.22 + myst_power) / (0.12 + myst_power)) ** myst_scale
    if i >= 200: mult *= ((0.015 * achievements) + 1) ** profit_scale
    if i >= 225: mult *= ((0.32 + myst_power) / (0.22 + myst_power)) ** myst_scale
    if i >= 250: mult *= ((0.0065 * upgrades) + 1) ** profit_scale
    return mult

def calc_n_mult(n):
    mult = n_scale ** n
    if n >= 25: mult *= ((0.12 + void_profit) / void_profit) ** vp_scale
    if n >= 50: mult *= 1.1 ** vp_scale
    if n >= 75: mult *= ((0.27 + void_profit) / (0.12 + void_profit)) ** vp_scale
    if n >= 125: mult *= 4 ** vp_scale
    if n >= 150: mult *= (1 + 0.8 * math.log10(ve_collected + 1)) ** profit_scale
    if n >= 175: mult *= 1.2 ** vp_scale
    if n >= 200: mult *= (1 + 2.5 * math.log10(ve_lifetime + 1)) ** ve_scale
    if n >= 225: mult *= 1.2 ** vp_scale
    if n >= 250: mult *= (1 + 2.5 * math.log10(ve_spawnrate + 1)) ** ve_scale
    return mult

def calc_s_mult(s):
    mult = s_scale ** s
    if s>= 50: mult *= 1.15 ** inc_scale
    if s>= 100: mult *= 1.20 ** inc_scale
    if s>= 150: mult *= (1 + 0.5 * math.log10(spells_cast + 1)) ** profit_scale
    if s>= 175: mult *= 1.25 ** inc_scale
    if s>= 200: mult *= (1 + 1.5 * math.log10(accumulated_casts + 1)) ** evo_scale
    if s>= 225: mult *= 1.25 ** inc_scale
    if s>= 250: mult *= (1 + math.log10(spells_cast + 1) ** 1.05) ** profit_scale
    return mult

def calc_w_mult(w):
    mult = w_scale ** w
    if w >= 150: mult *= (1 + 1.5 * math.log10(shards_collected + 1) ** 1.1) ** profit_scale
    if w >= 200: mult *= (1 + 0.15 * math.log(evocation_casts + 1) ** 1.2) ** inc_scale
    if w >= 250: mult *= (1 + 1.25 * math.log10(shards_per_sec + 1) ** 1.1) ** profit_scale
    return mult
    
def calc_d_mult(d):
    mult = d_scale ** d
    if d >= 25: mult *= 2 ** crit_scale
    if d >= 75: mult *= 2.5 ** crit_scale
    if d >= 125: mult *= 6 ** autoclick_scale
    if d >= 150: mult *= (1 + 0.4 * math.log10(autoclicks + 1)) ** profit_scale
    if d >= 175: mult *= 3.5 ** crit_scale
    if d >= 200: mult *= (1 + 1.78 * math.log10(autoclicks + 1)) ** crit_scale
    if d >= 225: mult *= 2 ** crit_scale
    if d >= 250: mult *= (1 + 0.8 * math.log10(autoclicks + 1) ** 1.05) ** profit_scale
    return mult

def calc_p_mult(p):
    mult = p_scale ** p
    if p >= 150: mult *= (1 + 0.000085 * sources) ** profit_scale
    if p >= 200: mult *= (1 + math.log(1 + 0.00025 * idle_time, 1.6)) ** idle_scale
    if p >= 225: mult *= ((1 + 0.25 + green_catalyst_power) / (1 + green_catalyst_power)) ** profit_scale
    if p >= 250: mult *= (1 + 0.00017 * sources) ** profit_scale
    return mult

def calc_m_mult(m):
    mult = m_scale ** m
    if m >= 25: mult *= 1.25 ** cap_growth_scale
    if m >= 100: mult *= 1.5 ** cap_growth_scale
    if m >= 150: mult *= (1 + 0.015 * hero_level) ** profit_scale
    if m >= 200: mult *= (1 + 0.00075 * achievement_points) ** cap_growth_scale
    if m >= 250: mult *= (1 + 0.03 * hero_level) ** profit_scale
    return mult

def calc_e_mult(e):
    mult = e_scale ** e
    if e >= 150: mult *= (1 + 0.0125 * pet_level) ** profit_scale
    if e >= 200: mult *= (1 + math.log(1 + 0.0005 * pet_time, 1.6)) ** pet_ap_scale
    if e >= 250: mult *= (1 + 0.025 * pet_level) ** profit_scale
    return mult

print((optimize(150, 0, 50, 40, 150, 0, 0, 0, 0, 0, 100, 0, 50, 0, 0, 75,)))
