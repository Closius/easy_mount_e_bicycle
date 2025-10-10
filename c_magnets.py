
import math
import copy
import json

import femm

import geometry


def get_data():
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

    data["n_turns"] = 900 # geometry.number_of_turns(data["ch"], data["cv"], data["coil_diameter"]) # 900


    data["magnet_density"] = 7.5 / 1000
    data["core_density"] = 7.8 / 1000  # ferrite
    # data["core_density"] = 2.7 / 1000  # aluminium
    # data["coil_mat_density"] = 2.7 / 1000  # aluminium
    data["coil_mat_density"] = 8.96 / 1000  # copper
    # data["coil_mat_specific_heat"] = 910 # Dj/(kg*K)   Aluminium
    data["coil_mat_specific_heat"] = 385 # Dj/(kg*K)   Copper

    return data


def main():
    data = get_data()

    geom_data = geometry.femm_geometry(data)

    result = geometry.calculate(*geom_data)


    return result


if __name__ == "__main__":
    result = main()
