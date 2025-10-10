easy_mount_e_bicycle
====================

![general idea](./idea.jpg)

Parametric calculation of the rim based linear engine for turning normal bicycle to e-bicycle

`c_magnets.py` uses following dimentions:

![parametric task](./dimentions_points.png)


Results
=======


```
Input data:
{
    "battery_I": 1.25,
    "battery_V": 48,
    "battery_P": 60.0,
    "depth": 31.7,
    "V": 40,
    "H": 79.8,
    "h_leg": 22.3,
    "v_leg": 35,
    "gv": 1.0,
    "gh": 1.0,
    "h_mid": 35.199999999999996,
    "cv": 33.0,
    "ch": 16.099999999999998,
    "mh": 44,
    "mv": 10,
    "gap": 5,
    "gap_m": 14,
    "air_material": "Air",
    "core_material": "416 Stainless Steel",
    "magnet_material": "N52",
    "coil_material": "0.63mm",
    "coil_diameter": 0.63,
    "n_turns": 900,
    "magnet_density": 0.0075,
    "core_density": 0.0078,
    "coil_mat_density": 0.008960000000000001,
    "coil_mat_specific_heat": 385
}

Results:
{
    "From calculation (Unlimited battery)": {
        "V_drop": 47.34,
        "I": 1.25,
        "P": 59.17,
        "Fx": 252.08,
        "delta T for 60sec 1 coil (vacuum)": 21.28
    },
    "Limited by battery": {
        "V": 48,
        "I": 1.25,
        "P": 60.0,
        "Fx": 255.59,
        "delta T for 60sec 1 coil (vacuum)": 21.58
    },
    "Weights": {
        "magnet_on_wheel_weight (for 32 spokes) (kg)": 3.24,
        "U_core_weight (6 items) (kg)": 2.91,
        "coil_weight (12 items) (kg) calculated by turns": 5.2,
        "total witout battery (kg)": 11.35
    }
}


                     Regular torque      Medium torque                   High torque
Measurements         40-60Nm             60-80Nm                         80Nm+
Force (28", rim)    148-222             222-296                         296+
Feel                 Normal              Punchy                          POWERRR!!
Battery impact       Normal              Minimal impact over normal      Higher, but battery spec compensates
Best for             Commuting, leisure  More oomph,heavier work         Off-roading, cargo, fun
```


![definition](./results/definition.png)

![fields](./results/field.png)