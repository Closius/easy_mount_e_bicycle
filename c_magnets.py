
import math
import femm
import matplotlib.pyplot as plt


def number_of_turns(w, h, d):
    w_t = math.floor(w/d)
    h_t = math.floor(h/d)
    return w_t * h_t


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
        (- ((H/2) + ch) * 2.5, - (mv + gap + V) * 2.5)
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


def main():
    depth = 30
    I = 9
    V = 40
    H = 80
    h_leg = H / 3
    v_leg = 25
    gv = 0.5
    gh = 0.5
    h_mid = H - (2 * h_leg)
    cv = v_leg - (2*gv)
    ch = (h_mid - (3*gh)) / 2
    mh = (H + (4*ch) + (6*gh)) / 2  
    mv = 5
    gap = 3
    gap_m = gh

    n_turns = number_of_turns(ch, cv, 0.315)


    # The package must be initialized with the openfemm command.
    femm.openfemm()

    # We need to create a new Magnetostatics document to work on.
    femm.newdocument(0)

    # Define the problem type.  Magnetostatic; Units of mm; Axisymmetric; 
    # Precision of 10^(-8) for the linear solver; a placeholder of 0 for 
    # the depth dimension, and an angle mesh constraint of 30 degrees
    femm.mi_probdef(0, 'millimeters', 'planar', 1e-8, depth, 30)

    femm.mi_getmaterial("Air")      
    femm.mi_getmaterial("416 Stainless Steel")
    femm.mi_getmaterial("N52")
    femm.mi_getmaterial("0.315mm")

    # mi_addcircprop(’circuitname’, i, circuittype) adds a new 
    # circuit property with name
    # ’circuitname’ with a prescribed current. The circuittype 
    # parameter is 0 for a parallelconnected circuit and 1 for a 
    # series-connected circuit.
    femm.mi_addcircprop('icoil', I, 1)

    cbg = c_block_geometry(V, H, h_leg, v_leg, gv, gh, h_mid, cv, ch, mh, mv, gap, gap_m)

    make_femm_geometry(cbg)

    femm.mi_selectlabel(*cbg["air_label"])
    femm.mi_setblockprop("Air", 0, 1, '<None>', 0, 0, 0)
    femm.mi_clearselected()

    femm.mi_selectlabel(*cbg["core_top_label"])
    femm.mi_selectlabel(*cbg["core_bttm_label"])
    femm.mi_setblockprop("416 Stainless Steel", 0, 1, '<None>', 0, 0, 0)
    femm.mi_clearselected()

    femm.mi_selectlabel(*cbg["magn_left_label"])
    femm.mi_setblockprop("N52", 0, 1, '<None>', 0, 0, 0)
    femm.mi_clearselected()

    femm.mi_selectlabel(*cbg["magn_right_label"])
    femm.mi_setblockprop("N52", 0, 1, '<None>', 180, 0, 0)
    femm.mi_clearselected()

    femm.mi_selectlabel(*cbg["coil_top_1_label"])
    femm.mi_selectlabel(*cbg["coil_top_4_label"])
    femm.mi_selectlabel(*cbg["coil_bttm_2_label"])
    femm.mi_selectlabel(*cbg["coil_bttm_3_label"])
    femm.mi_setblockprop("0.315mm", 0, 1, 'icoil', 0, 0, n_turns)
    femm.mi_clearselected()

    femm.mi_selectlabel(*cbg["coil_top_2_label"])
    femm.mi_selectlabel(*cbg["coil_top_3_label"])
    femm.mi_selectlabel(*cbg["coil_bttm_1_label"])
    femm.mi_selectlabel(*cbg["coil_bttm_4_label"])
    femm.mi_setblockprop("0.315mm", 0, 1, 'icoil', 0, 0, - n_turns)
    femm.mi_clearselected()


    # Now, the finished input geometry can be displayed.
    femm.mi_zoomnatural()

    # We have to give the geometry a name before we can analyze it.
    femm.mi_saveas('c_magnets.fem');


    # Now,analyze the problem and load the solution when the analysis is finished
    femm.mi_analyze()
    femm.mi_loadsolution()

    # # If we were interested in the flux density at specific positions, 
    # # we could inquire at specific points directly:
    # b0=femm.mo_getb(0,0);
    # print('Flux density at the center of the bar is %g T' % b0[1]);
    # b1=femm.mo_getb(0,50);
    # print('Flux density at r=0,z=50 is %g T' % b1[1]);

    # # The program will report the terminal properties of the circuit:
    # # current, voltage, and flux linkage 
    # vals = femm.mo_getcircuitproperties('icoil');

    # # [i, v, \[Phi]] = MOGetCircuitProperties["icoil"]

    # # If we were interested in inductance, it could be obtained by
    # # dividing flux linkage by current
    # L = 1000*vals[2]/vals[0];
    # print('The self-inductance of the coil is %g mH' % L);

    # # Or we could, for example, plot the results along a line using 
    # zee=[]
    # bee=[]
    # for n in range(-100,101):
    #     b=femm.mo_getb(0,n);
    #     zee.append(n)
    #     bee.append(b[1]);

    # plt.plot(zee,bee)
    # plt.ylabel('Flux Density, Tesla')
    # plt.xlabel('Distance along the z-axis, mm')
    # plt.title('Plot of flux density along the axis')
    # plt.show()

    # When the analysis is completed, FEMM can be shut down.
    femm.closefemm()



if __name__ == "__main__":
    main()