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
    "v_leg": 25,
    "gv": 1.0,
    "gh": 1.0,
    "h_mid": 35.199999999999996,
    "cv": 23.0,
    "ch": 16.099999999999998,
    "mh": 44,
    "mv": 5,
    "gap": 5,
    "gap_m": 14,
    "air_material": "Air",
    "core_material": "416 Stainless Steel",
    "magnet_material": "N40",
    "coil_material": "0.8mm",
    "n_turns": 560,
    "magnet_density": 0.0075,
    "core_density": 0.0078,
    "coil_mat_density": 0.008960000000000001,
    "coil_mat_specific_heat": 385
}

Results:
{
    "From calculation (Unlimited battery)": {
        "V_drop": 18.27,
        "I": 1.25,
        "P": 22.83,
        "Fx": 75.36,
        "delta T for 60sec 1 coil (vacuum)": 5.95
    },
    "Limited by battery": {
        "V": 48,
        "I": 1.25,
        "P": 60.0,
        "Fx": 198.01,
        "delta T for 60sec 1 coil (vacuum)": 15.62
    },
    "Weights": {
        "magnet_on_wheel_weight (for 32 spokes) (kg)": 1.62,
        "U_core_weight (6 items) (kg)": 3.43,
        "coil_weight (12 items) (kg) calculated as solid block": 7.18,
        "total witout battery (kg)": 12.23
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