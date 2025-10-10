
import math
import copy
import json

import femm


def number_of_turns(w, h, d):
    w_t = math.floor(w/d)
    h_t = math.floor(h/d)
    return w_t * h_t

def weight_coil(ro, d_wire, n_turns, h_leg, ch, cv, depth):
    area_wire = n_turns * math.pi * (d_wire * d_wire / 4)
    area_solid = ch * cv
    fill_coef = area_wire / area_solid
    area_solid_cs = ( ((h_leg + (2*ch)) * (depth+ 2*ch)) - (h_leg * depth) )
    area_wire_cs = area_solid_cs * fill_coef
    weight = area_wire_cs * cv * ro / 1000
    print(f"weight coil solid: {area_solid_cs * cv * ro / 1000}, for 12: {12 * area_solid_cs * cv * ro / 1000}")
    print(f"weight coil turns: {weight}, for 12: {12 * weight}")

    return weight


def c_block_geometry(V, H, h_leg, v_leg, gv, gh, h_mid, cv, ch, mh, mv, gap, gap_m):
    # In local coordinates, origin - left bottom
    core = [
        (0, 0),                     # 1
        (0, V),                     # 2
        (H, V),                     # 3
        (H, 0),                     # 4
        (H - h_leg, 0),             # 5
        (H - h_leg, v_leg),         # 6
        (h_leg, v_leg),             # 7    
        (h_leg, 0),                 # 8
    ]
    coil = [
        (0, 0),    # 1
        (0, cv),   # 2
        (ch, cv),  # 3
        (ch, 0),   # 4
    ]
    magn = [
        (0, 0),    # 1
        (0, mv),   # 2
        (mh, mv),  # 3
        (mh, 0),   # 4
    ]
    air = [
        (- ((H/2) + ch) * 3 * 1.5, - (mv + gap + V) * 3)
    ]
    air.append((air[0][0], abs(air[0][1])))
    air.append((abs(air[0][0]), abs(air[0][1])))
    air.append((abs(air[0][0]), air[0][1]))

    # move and locate: magnets
    magn_left = [(x[0] - mh - (gap_m/2), x[1] - (mv/2)) for x in magn]
    magn_right = [(x[0] + mh + gap_m, x[1]) for x in magn_left]

    # move and locate: cores
    h_move = H / 2
    core_top = [(x[0] - h_move, x[1] + gap + (mv/2)) for x in core]
    core_bttm = [(x[0], - x[1]) for x in core_top]

    # move and locate: coils
    gv_bttm = v_leg - cv - gv
    coil_top_1 = [(x[0] - h_move - ch - gh, x[1] + gap + (mv/2) + gv_bttm) for x in coil]
    coil_top_2 = [(x[0] + ch + (2*gh) + h_leg, x[1]) for x in coil_top_1]
    coil_top_3 = [(x[0] + h_mid - (2*gh) - ch, x[1]) for x in coil_top_2]
    coil_top_4 = [(x[0] + ch + (2*gh) + h_leg, x[1]) for x in coil_top_3]

    coil_bttm_1 = [(x[0], -x[1]) for x in coil_top_1]
    coil_bttm_2 = [(x[0], -x[1]) for x in coil_top_2]
    coil_bttm_3 = [(x[0], -x[1]) for x in coil_top_3]
    coil_bttm_4 = [(x[0], -x[1]) for x in coil_top_4]

    # material labels
    magn_left_label = (magn_left[0][0] + (mh/2), magn_left[0][1] + (mv/2))
    magn_right_label = (magn_right[0][0] + (mh/2), magn_right[0][1] + (mv/2))

    core_top_label = (core_top[0][0] + (h_leg/2), core_top[0][1] + (V/2))
    core_bttm_label = (core_bttm[0][0] + (h_leg/2), core_bttm[0][1] - (V/2))


    coil_top_1_label = (coil_top_1[0][0] + (ch/2), coil_top_1[0][1] + (cv/2))
    coil_top_2_label = (coil_top_2[0][0] + (ch/2), coil_top_2[0][1] + (cv/2))
    coil_top_3_label = (coil_top_3[0][0] + (ch/2), coil_top_3[0][1] + (cv/2))
    coil_top_4_label = (coil_top_4[0][0] + (ch/2), coil_top_4[0][1] + (cv/2))

    coil_bttm_1_label = (coil_bttm_1[0][0] + (ch/2), coil_bttm_1[0][1] - (cv/2))
    coil_bttm_2_label = (coil_bttm_2[0][0] + (ch/2), coil_bttm_2[0][1] - (cv/2))
    coil_bttm_3_label = (coil_bttm_3[0][0] + (ch/2), coil_bttm_3[0][1] - (cv/2))
    coil_bttm_4_label = (coil_bttm_4[0][0] + (ch/2), coil_bttm_4[0][1] - (cv/2))

    air_label = (air[0][0] + ch, air[0][1] + cv)

    return {
        "air": air,
        "core_top": core_top,
        "core_bttm": core_bttm,
        "magn_left": magn_left,
        "magn_right": magn_right,

        "coil_top_1": coil_top_1,
        "coil_top_2": coil_top_2,
        "coil_top_3": coil_top_3,
        "coil_top_4": coil_top_4,

        "coil_bttm_1": coil_bttm_1,
        "coil_bttm_2": coil_bttm_2,
        "coil_bttm_3": coil_bttm_3,
        "coil_bttm_4": coil_bttm_4,

        "air_label": air_label,

        "core_top_label": core_top_label,
        "core_bttm_label": core_bttm_label,

        "magn_left_label": magn_left_label,
        "magn_right_label": magn_right_label,

        "coil_top_1_label": coil_top_1_label,
        "coil_top_2_label": coil_top_2_label,
        "coil_top_3_label": coil_top_3_label,
        "coil_top_4_label": coil_top_4_label,

        "coil_bttm_1_label": coil_bttm_1_label,
        "coil_bttm_2_label": coil_bttm_2_label,
        "coil_bttm_3_label": coil_bttm_3_label,
        "coil_bttm_4_label": coil_bttm_4_label,
    }


def make_femm_geometry(cbg):
    for name, obj in cbg.items():
        if not name.endswith("_label"):
            for p1, p2 in [[obj[i], obj[(i + 1) % len(obj)]] for i in range(len(obj))]:
                femm.mi_drawline(*p1,*p2)
        else:
            femm.mi_addblocklabel(*obj)


def create_material(name, properties: dict):
    femm.mi_addmaterial(name, *properties)


def main(data):
    """
        data = {}
        data["battery_I"] = 15
        data["battery_V"] = 48
        data["battery_P"] = data["battery_I"] * data["battery_V"]

        data["depth"] = 30
        data["V"] = 40
        data["H"] = 80
        data["h_leg"] = data["H"] / 3
        data["v_leg"] = 25
        data["gv"] = 0.5
        data["gh"] = 0.5
        data["h_mid"] = data["H"] - (2 * data["h_leg"])
        data["cv"] = data["v_leg"] - (2*data["gv"])
        data["ch"] = (data["h_mid"] - (3*data["gh"])) / 2
        data["mh"] = (data["H"] + (4*data["ch"]) + (6*data["gh"])) / 2  
        data["mv"] = 5
        data["gap"] = 3
        data["gap_m"] = data["gh"]

        data["air_material"] = "Air"
        data["core_material"] = "416 Stainless Steel"
        data["magnet_material"] = "N52"
        data["coil_material"] = "0.315mm"

        data["n_turns"] = number_of_turns(data["ch"], data["cv"], 0.315)
    """


    # The package must be initialized with the openfemm command.
    femm.openfemm()

    # We need to create a new Magnetostatics document to work on.
    femm.newdocument(0)

    # Define the problem type.  Magnetostatic; Units of mm; Axisymmetric; 
    # Precision of 10^(-8) for the linear solver; a placeholder of 0 for 
    # the depth dimension, and an angle mesh constraint of 30 degrees
    femm.mi_probdef(0, 'millimeters', 'planar', 1e-8, data["depth"], 30)

    femm.mi_getmaterial(data["air_material"])
    femm.mi_getmaterial(data["core_material"])
    femm.mi_getmaterial(data["magnet_material"])

    if isinstance(data["coil_material"], str):
        femm.mi_getmaterial(data["coil_material"])
        mat_coil_name = data["coil_material"]
    else:
        create_material(*data["coil_material"])
        mat_coil_name = data["coil_material"][0]

    # mi_addcircprop(’circuitname’, i, circuittype) adds a new 
    # circuit property with name
    # ’circuitname’ with a prescribed current. The circuittype 
    # parameter is 0 for a parallelconnected circuit and 1 for a 
    # series-connected circuit.
    femm.mi_addcircprop('icoil', data["battery_I"], 1)

    cbg = c_block_geometry(data["V"], data["H"], data["h_leg"], data["v_leg"], data["gv"], data["gh"], 
        data["h_mid"], data["cv"], data["ch"], data["mh"], data["mv"], data["gap"], data["gap_m"])

    make_femm_geometry(cbg)

    femm.mi_selectlabel(*cbg["air_label"])
    femm.mi_setblockprop(data["air_material"], 0, 1, '<None>', 0, 0, 0)
    femm.mi_clearselected()

    femm.mi_selectlabel(*cbg["core_top_label"])
    femm.mi_selectlabel(*cbg["core_bttm_label"])
    femm.mi_setblockprop(data["core_material"], 0, 1, '<None>', 0, 0, 0)
    femm.mi_clearselected()

    femm.mi_selectlabel(*cbg["magn_left_label"])
    femm.mi_setblockprop(data["magnet_material"], 0, 1, '<None>', 0, 0, 0)
    femm.mi_clearselected()

    femm.mi_selectlabel(*cbg["magn_right_label"])
    femm.mi_setblockprop(data["magnet_material"], 0, 1, '<None>', 180, 0, 0)
    femm.mi_clearselected()

    femm.mi_selectlabel(*cbg["coil_top_1_label"])
    femm.mi_selectlabel(*cbg["coil_top_4_label"])
    femm.mi_selectlabel(*cbg["coil_bttm_2_label"])
    femm.mi_selectlabel(*cbg["coil_bttm_3_label"])
    femm.mi_setblockprop(mat_coil_name, 0, 1, 'icoil', 0, 0, - data["n_turns"])
    femm.mi_clearselected()

    femm.mi_selectlabel(*cbg["coil_top_2_label"])
    femm.mi_selectlabel(*cbg["coil_top_3_label"])
    femm.mi_selectlabel(*cbg["coil_bttm_1_label"])
    femm.mi_selectlabel(*cbg["coil_bttm_4_label"])
    femm.mi_setblockprop(mat_coil_name, 0, 1, 'icoil', 0, 0, data["n_turns"])
    femm.mi_clearselected()


    # mirror objects

    x_m = ((data["H"]/2) + data["ch"] + (1.5 * data["gh"]))
    y_m = (data["mv"] / 2) + data["gap"] + data["V"] + data["gv"]

    femm.mi_selectrectangle(- x_m,y_m,x_m,- y_m,4)
    femm.mi_mirror2(x_m, - y_m, x_m, y_m,1)
    femm.mi_clearselected()
    femm.mi_selectrectangle(- x_m,y_m,x_m,- y_m,4)
    femm.mi_mirror2(x_m, - y_m, x_m, y_m,2)
    femm.mi_clearselected()

    femm.mi_selectrectangle(- x_m,y_m,x_m,- y_m,4)
    femm.mi_mirror2(- x_m, - y_m, - x_m, y_m,1)
    femm.mi_clearselected()
    femm.mi_selectrectangle(- x_m,y_m,x_m,- y_m,4)
    femm.mi_mirror2(- x_m, - y_m, - x_m, y_m,2)
    femm.mi_clearselected()

    # Now, the finished input geometry can be displayed.
    femm.mi_zoomnatural()

    # We have to give the geometry a name before we can analyze it.
    femm.mi_saveas('c_magnets.fem');

    # femm.mi_createmesh()
    femm.mi_analyze(0)
    femm.mi_loadsolution()


    # The program will report the terminal properties of the circuit:
    # current, voltage, and flux linkage 
    vals = femm.mo_getcircuitproperties('icoil')
    result = {}
    V_drop = vals[1]
    I_out = vals[0]
    P_out = V_drop * I_out
    battery_P = data["battery_V"] * I_out

    femm.mo_seteditmode("area")

    femm.mo_clearblock()

    femm.mo_selectblock(*cbg["magn_left_label"])
    femm.mo_selectblock(*cbg["magn_right_label"])

    m_right_1 = list(copy.deepcopy(cbg["magn_right_label"]))
    m_right_1[0] = x_m + (x_m - m_right_1[0])
    femm.mo_selectblock(*m_right_1)
    m_right_2 = list(copy.deepcopy(cbg["magn_left_label"]))
    m_right_2[0] = x_m + x_m + abs(m_right_2[0])
    femm.mo_selectblock(*m_right_2)

    m_left_1 = copy.deepcopy(m_right_1)
    m_left_1[0] = - m_left_1[0]
    femm.mo_selectblock(*m_left_1)
    m_left_2 = copy.deepcopy(m_right_2)
    m_left_2[0] = - m_left_2[0]
    femm.mo_selectblock(*m_left_2)


    Fx = femm.mo_blockintegral(18)  # x-direction force
    battery_Fx =  (data["battery_V"] * Fx) / V_drop
    magnet_on_wheel_weight =  data["depth"] * data["mh"] * data["mv"] * data["magnet_density"] / 1000
    U_core_weight =  ((data["depth"] * data["V"] * data["H"]) - 
        (data["depth"] * data["v_leg"] * data["h_mid"])) * data["core_density"] / 1000

    coil_weight = weight_coil(ro=data["coil_mat_density"], 
        d_wire=data["coil_diameter"], 
        n_turns=data["n_turns"], 
        h_leg=data["h_leg"], 
        ch=data["ch"],
        cv=data["cv"],
        depth=data["depth"])

    # temp of coil in 1 seconds
    delta_T_1sec_P_out = (P_out / (coil_weight * data["coil_mat_specific_heat"]))
    delta_T_1sec_battery_P = (battery_P / (coil_weight * data["coil_mat_specific_heat"]))



    def _round_floats(obj):
        if isinstance(obj, float):
            return round(obj, 2)
        elif isinstance(obj, dict):
            return {k: _round_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [_round_floats(elem) for elem in obj]
        else:
            return obj


    result["From calculation (Unlimited battery)"] = {
        "V_drop": V_drop,
        "I": I_out,
        "P": P_out,
        "Fx": Fx,
        "delta T for 60sec 1 coil (vacuum)": delta_T_1sec_P_out * 60,
    }
    result["Limited by battery"] = {
        "V": data["battery_V"],
        "I": data["battery_I"],
        "P": data["battery_P"],
        "Fx": battery_Fx,
        "delta T for 60sec 1 coil (vacuum)": delta_T_1sec_battery_P * 60
    }
    result["Weights"] = {
        "magnet_on_wheel_weight (for 32 spokes) (kg)": magnet_on_wheel_weight * (32 - 1),
        "U_core_weight (6 items) (kg)": U_core_weight * 6,
        "coil_weight (12 items) (kg) calculated by turns": coil_weight * 12,
        "total witout battery (kg)": (magnet_on_wheel_weight * (32 - 1)) + (U_core_weight * 6) + (coil_weight * 12)
    }

    # When the analysis is completed, FEMM can be shut down.
    femm.closefemm()

    print("Input data:")
    print(json.dumps(data, indent=4))
    print("")
    print("Results:")
    print(json.dumps(_round_floats(result), indent=4))
    print("")
    print("")
    print("                     Regular torque      Medium torque                   High torque")
    print("Measurements         40-60Nm             60-80Nm                         80Nm+")
    print("Force (28\", rim)    148-222             222-296                         296+")
    print("Feel                 Normal              Punchy                          POWERRR!!")
    print("Battery impact       Normal              Minimal impact over normal      Higher, but battery spec compensates")
    print("Best for             Commuting, leisure  More oomph,heavier work         Off-roading, cargo, fun")


    return result


if __name__ == "__main__":
    data = {}
    data["battery_I"] = 15/12
    data["battery_V"] = 48
    data["battery_P"] = data["battery_I"] * data["battery_V"]

    data["depth"] = 31.7
    data["V"] = 40
    data["H"] = 79.8
    data["h_leg"] = 22.3 # (data["H"] / 4)
    data["v_leg"] = 35
    data["gv"] = 1.0
    data["gh"] = 1.0
    data["h_mid"] = data["H"] - (2 * data["h_leg"])
    data["cv"] = data["v_leg"] - (2*data["gv"])
    data["ch"] = (data["h_mid"] - (3*data["gh"])) / 2
    data["mh"] = 44
    data["mv"] = 10
    data["gap"] = 5
    data["gap_m"] = 14 # data["gh"]

    data["air_material"] = "Air"
    data["core_material"] = "416 Stainless Steel"
    # data["core_material"] = "Aluminum, 1100"
    data["magnet_material"] = "N52"
    # data["magnet_material"] = "N40"
    # data["magnet_material"] = "N30"
    # data["coil_material"] = "0.25mm"
    # data["coil_material"] = "0.315mm"
    # data["coil_material"] = "0.4mm"
    # data["coil_material"] = "0.5mm"
    data["coil_material"] = "0.63mm"
    data["coil_diameter"] = 0.63
    # data["coil_material"] = "0.8mm"
    # data["coil_material"] = "1mm"
    # data["coil_material"] = "1.25mm"
    # data["coil_material"] = "1.6mm"

    # data["coil_material"] = ["Aluminium 0.8mm", [
    #                     1,  # mu x, 1 for non-magnetic
    #                     1,  # mu y, 1 for non-magnetic
    #                     0,  # coercivity (Hc), 0 for non-magnetic
    #                     10, # J Applied source current density in Amps/mm2
    #                     35,  # Cduct Electrical conductivity of the material in MS/m.
    #                     0.03,  # lam_d (for lamination, 0 if not laminated)
    #                     0,  # Phi hmax Hysteresis lag angle in degrees, used for nonlinear BH curves
    #                     0,  # Lam fill Fraction of the volume occupied per lamination that is actually filled with iron (Note
    #                         # that this parameter defaults to 1 in the femm preprocessor dialog box because, by default,
    #                         # iron completely fills the volume)
    #                     3,  # Lamtype Set to
    #                             # ∗ 0 – Not laminated or laminated in plane
    #                             # ∗ 1 – laminated x or r
    #                             # ∗ 2 – laminated y or z
    #                             # ∗ 3 – magnet wire
    #                             # ∗ 4 – plain stranded wire
    #                             # ∗ 5 – Litz wire
    #                             # ∗ 6 – square wire
    #                     0, # Phi hx Hysteresis lag in degrees in the x-direction for linear problems.
    #                     0, # Phi hy Hysteresis lag in degrees in the y-direction for linear problems.
    #                     1, # nstr Number of strands in the wire build. Should be 1 for Magnet or Square wire.
    #                     0.8, # dwire Diameter of each of the wire’s constituent strand in millimeters.
    # ]]

    data["n_turns"] = 900 # number_of_turns(data["ch"], data["cv"], data["coil_diameter"]) # 900


    data["magnet_density"] = 7.5 / 1000
    data["core_density"] = 7.8 / 1000  # ferrite
    # data["core_density"] = 2.7 / 1000  # aluminium
    # data["coil_mat_density"] = 2.7 / 1000  # aluminium
    data["coil_mat_density"] = 8.96 / 1000  # copper
    # data["coil_mat_specific_heat"] = 910 # Dj/(kg*K)   Aluminium
    data["coil_mat_specific_heat"] = 385 # Dj/(kg*K)   Copper

    result = main(data)

    # r = {}

    # for wire_d in [0.25, 0.315, 0.4, 0.5, 0.63, 0.8, 1, 1.25, 1.6]:
    #     data["coil_material"] = f"{wire_d}mm"
    #     data["n_turns"] = number_of_turns(data["ch"], data["cv"], wire_d)
    #     result = main(data)
    #     r[wire_d] = {"Fx": min([result["Fx"], result["battery_Fx"]]),
    #     "P": min([result["P_out"], result["battery_P"]])}

    # print("")
    # print("Total Results:")
    # print(json.dumps(r, indent=4))
