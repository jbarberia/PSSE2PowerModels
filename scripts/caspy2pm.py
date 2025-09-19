import os
import sys
import psse34
import caspy
import math
import json
import time


def zero_impedance_conections(sav, ZTHRS=0.0001):
    siz = sav.psssiz
    brn = sav.pssbrn

    brn_rx = brn["RX"]
    brn_fbus = brn["FRMBUS"]
    brn_tbus = brn["TOBUS"]
    brn_stat = brn["STAT"]

    # Union-Find helpers
    parent = {}

    def find(x):
        # Path compression
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px

    # Inicializa cada bus en su propio conjunto
    for i in range(siz["NLIN"]):
        if abs(brn_rx[i].imag) <= ZTHRS and brn_rx[i].real == 0.0:
            if brn_stat[i] == 0:
                continue
            fbus, tbus = brn_fbus[i], brn_tbus[i]
            if fbus not in parent:
                parent[fbus] = fbus
            if tbus not in parent:
                parent[tbus] = tbus
            union(fbus, tbus)

    # Construye los grupos
    groups = {}
    for bus in parent:
        root = find(bus)
        if root not in groups:
            groups[root] = []
        groups[root].append(bus)

    return list(groups.values())


def lookup_connections(sav):
    ext2int = {}
    zi_connections = zero_impedance_conections(sav)

    for zi_connected_buses in zi_connections:
        con_bus = min(zi_connected_buses)
        for bus in zi_connected_buses:
            ext2int[bus] = con_bus

    for bus in sav.pssbus["NUM"]:
        if not bus in ext2int:
            ext2int[bus] = bus

    return ext2int


def _bus2pm(sav, bus2idx):
    msc = sav.pssmsc
    hibus = msc["HIBUS"]

    bus = sav.pssbus
    bus_num   = bus["NUM"]
    bus_baskv = bus["BASKV"]
    bus_ide   = bus["IDE"]
    bus_vm    = bus["VM"]
    bus_va    = bus["VA"]
    bus_nminv = bus["NMINV"]
    bus_nmaxv = bus["NMAXV"]

    unique_bus = set(bus2idx.values())
    indices = [i for i, bus in enumerate(bus_num) if bus in unique_bus]

    bus_dict = {}
    for i in indices:
        num = bus_num[i]
        source_id = ["STARPOINT"] if num > hibus else ["BU", num]
        bus_dict[str(num)] = {
            "index": num,
            "bus_i": num,
            "source_id": source_id,
            "base_kv": bus_baskv[i],
            "bus_type": bus_ide[i],
            "vm": bus_vm[i],
            "va": bus_va[i] * math.pi / 180,
            "vmin": bus_nminv[i],
            "vmax": bus_nmaxv[i],
        }

    return bus_dict


def _branch2pm(sav, bus2idx):
    siz = sav.psssiz
    
    brn = sav.pssbrn
    brn_fbus = brn["FRMBUS"]
    brn_tbus = brn["TOBUS"]
    
    trn = sav.psstrn
    tr3 = sav.pss3wt

    brn_dict = {}

    for i in range(siz["NLIN"]):
        source_id = _get_branch_source_id(i, brn, trn, tr3)
        
        entry = {
            "index": i+1,
            "f_bus": bus2idx[brn_fbus[i]],
            "t_bus": bus2idx[brn_tbus[i]],
            "source_id": source_id
        }

        if source_id[0] in ["TR", "T3"]:
            param = _get_branch_entry_trn(i, sav)
        else:
            param = _get_branch_entry_brn(i, sav)

        brn_dict[str(i+1)] = dict(**entry, **param)
    
    return brn_dict


def _get_branch_source_id(i, brn, trn, tr3):
    brn_indx2w  = brn["INDX2W"]
    brn_indxswd = brn["INDXSWD"]
    brn_fbus = brn["FRMBUS"]
    brn_tbus = brn["TOBUS"]
    brn_ckt  = brn["CKT"]
    
    trn_indx3w = trn["INDX3W"]
    
    tr3_bus1st = tr3["BUS1ST"]
    tr3_bus2nd = tr3["BUS2ND"]
    tr3_bus3rd = tr3["BUS3RD"]
    tr3_ckt    = tr3["CKT"]
    
    if brn_indx2w[i] != 0: # is xfmr        
        j = brn_indx2w[i] - 1
        if trn_indx3w[j] != 0: # is 3 winding
            k = trn_indx3w[j] - 1
            w1 = tr3_bus1st[k] 
            w2 = tr3_bus2nd[k] 
            w3 = tr3_bus3rd[k]
            ckt = tr3_ckt[k]
            
            wnum = {
                w1: 1,
                w2: 2,
                w3: 3,  
            }[brn_fbus[i]]
            return ["T3", w1, w2, w3, ckt, wnum]
        else: # is 2 winding
            return ["TR", brn_fbus[i], brn_tbus[i], brn_ckt[i]]
    
    elif brn_indxswd[i] != 0:
        return ["SWD", brn_fbus[i], brn_tbus[i], brn_ckt[i]]
    else:
        return ["LII", brn_fbus[i], brn_tbus[i], brn_ckt[i]]


def _get_branch_entry_trn(i, sav):
    brn = sav.pssbrn
    brn_stat = brn["STAT"]
    brn_indx2w = brn["INDX2W"]

    j = brn_indx2w[i] - 1
    trn = sav.psstrn
    trn_rxtran = trn["RXTRAN"]
    trn_wind1  = trn["WIND1"]
    trn_wind2  = trn["WIND2"]
    trn_ang1   = trn["ANG1"]
    
    return {
        "br_r": trn_rxtran[j].real,
        "br_x": trn_rxtran[j].imag,
        "b_fr": 0.0,
        "b_to": 0.0,
        "br_status": brn_stat[i],
        "angmin": -math.pi / 6,
        "angmax": math.pi / 6,
        "g_fr": 0.0,
        "g_to": 0.0,
        "tap": trn_wind1[j] / trn_wind2[j],
        "shift": trn_ang1[j] * math.pi / 180,
        "transformer": True,
    }


def _get_branch_entry_brn(i, sav):
    brn = sav.pssbrn
    brn_stat   = brn["STAT"]
    brn_indx2w = brn["INDX2W"]
    brn_b   = brn["B"]
    brn_rx  = brn["RX"]
    brn_gbi = brn["GBI"]
    brn_gbj = brn["GBJ"]

    return {
        "br_r": brn_rx[i].real,
        "br_x": brn_rx[i].imag,
        "b_fr": brn_gbi[i].imag + brn_b[i] / 2,
        "b_to": brn_gbj[i].imag + brn_b[i] / 2,
        "br_status": brn_stat[i],
        "angmin": -math.pi / 6,
        "angmax": math.pi / 6,
        "g_fr": brn_gbi[i].real,
        "g_to": brn_gbj[i].real,
        "tap": 1.0,
        "shift": 0.0,
        "transformer": False,
    }


def _load2pm(sav, bus2idx):
    siz = sav.psssiz
    lod = sav.psslod
    lod_id   = lod["ID"]
    lod_num  = lod["NUM"]
    lod_load = lod["LOAD"]
    lod_stat = lod["STATUS"]

    lod_dict = {}
    for i in range(siz["NLOAD"]):
        lod_dict[str(i + 1)] = {
            "index": i + 1,
            "load_bus": bus2idx[lod_num[i]],
            "status": lod_stat[i],
            "pd": lod_load[i][0].real,
            "qd": lod_load[i][0].imag,
            "source_id": ["LO", lod_num[i], lod_id[i]],
        }
    return lod_dict


def _gen2pm(sav, bus2idx):
    siz = sav.psssiz
    gen = sav.pssgen

    gen_num = gen["NUM"] 
    gen_ide = gen["IDE"] 
    gen_pg = gen["PG"]
    gen_pb = gen["PB"]
    gen_pt = gen["PT"]    
    gen_qg = gen["QG"]
    gen_qb = gen["QB"]
    gen_qt = gen["QT"]
    gen_vs = gen["VS"]
    gen_stat = gen["STAT"]

    gen_dict = {}
    for i in range(siz["NGEN"]):
        gen_dict[str(i + 1)] = {
            "gen_bus": bus2idx[gen_num[i]],
            "index": i + 1,
            "pg": gen_pg[i],
            "qg": gen_qg[i],
            "pmin": gen_pb[i],
            "pmax": gen_pt[i],
            "qmin": gen_qb[i],
            "qmax": gen_qt[i],
            "vg": gen_vs[i],
            "gen_status": gen_stat[i],
            "source_id": ["ME", gen_num[i], gen_ide[i]],
        }        
    return gen_dict


def _shunt2pm(sav, bus2idx):
    siz = sav.psssiz
    
    fsh = sav.pssfsh
    fsh_id    = fsh["ID"]
    fsh_num   = fsh["NUM"]
    fsh_shunt = fsh["SHUNT"]
    fsh_stat  = fsh["STATUS"]
    
    ssh = sav.psswsh
    ssh_num   = ssh["NUM"]
    ssh_stat  = ssh["STAT"]
    ssh_binit = ssh["BINIT"]

    fct       = sav.pssfct
    fct_name  = fct["NAME"]
    fct_sbus  = fct["SBUS"]
    fct_tbus  = fct["TBUS"]    
    fct_qshnt = fct["QSHNT"]

    shn_dict = {}
    
    # fixed shunt
    for i in range(siz["NBUSHN"]):
        shn_dict[str(i + 1)] = {
            "index": i + 1,
            "shunt_bus": bus2idx[fsh_num[i]],
            "gs": fsh_shunt[i].real,
            "bs": fsh_shunt[i].imag,
            "status": fsh_stat[i],
            "source_id": ["FXS", fsh_num[i], fsh_id[i]]
        }

    # switched shunt
    offset = siz["NBUSHN"]
    for i in range(siz["NSHUNT"]):
        shn_dict[str(i + offset + 1)] = {
            "index": i + offset + 1,
            "shunt_bus": bus2idx[ssh_num[i]],
            "gs": 0.0,
            "bs": ssh_binit[i],
            "status": ssh_stat[i],
            "source_id": ["SWS", ssh_num[i]]
        }

    offset += siz["NSHUNT"]
    for i in range(siz["NFACTS"]):

        # skip not statcom components
        if fct_tbus[i] != 0: 
            continue

        shn_dict[str(i + offset + 1)] = {
            "index": i + offset + 1,
            "shunt_bus": bus2idx[fct_sbus[i]],
            "gs": 0.0,
            "bs": -fct_qshnt[i] / 100,
            "status": ssh_stat[i],
            "source_id": ["FD FACTS", fct_name[i]]
        }

    return shn_dict


def _hvdc2pm(sav, bus2idx):
    siz  = sav.psssiz
    
    hvdc = sav.pss2dc
    hvdc_ip   = hvdc["IP"]
    hvdc_pac  = hvdc["PAC"]
    hvdc_qac  = hvdc["QAC"]
    hvdc_mdc  = hvdc["MDC"]
    hvdc_name = hvdc["NAME"]
    
    hvdc_dict = {}

    for i in range(siz["NDCL"]):


        hvdc_dict[str(i + 1)] = {
            "index": i + 1,
            "f_bus": hvdc["IP"][i][0],
            "t_bus": hvdc["IP"][i][1],
            "pf": hvdc["PAC"][i][0],
            "pt": hvdc["PAC"][i][1],
            "vf": 1.0,
            "vt": 1.0,
            "pminf": hvdc["PAC"][i][0],
            "pmaxf": hvdc["PAC"][i][0],
            "qminf": hvdc["QAC"][i][0],
            "qmaxf": hvdc["QAC"][i][0],
            "pmint": hvdc["PAC"][i][1],
            "pmaxt": hvdc["PAC"][i][1],
            "qmint": hvdc["QAC"][i][1],
            "qmaxt": hvdc["QAC"][i][1],
            "loss0": 0.0,
            "loss1": 0.0,
            "br_status": int(hvdc["MDC"][i] > 0),
            "source_id": ["DC", hvdc["NAME"][i]],
        }

    return hvdc_dict


def round_floats(obj):
    if isinstance(obj, float):
        return round(obj, 6)  # deja como número
    elif isinstance(obj, dict):
        return {k: round_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [round_floats(x) for x in obj]
    return obj


def _check_pv_buses(data):
    """
    verifica que los generadores esten conectados a barras PV.
    caso contrario los desconecta o cambia el tipo de barra como el PSSE.
    """
    bus_gens_status = {int(i): [] for i in data["bus"]}
    bus_gens = {}
    for (i, gen) in data["gen"].items():
        bus = gen["gen_bus"]
        gen_status = gen["gen_status"]
        bus_gens_status[bus] = bus_gens_status.get(bus, []) + [gen_status]
        bus_gens[bus] = bus_gens.get(bus, []) + [i]

    for bus_i, machine_status in bus_gens_status.items():
        bus = data["bus"][str(bus_i)]
        all_oos = sum(machine_status) == 0
        
        # si no hay maquinas en un barra PV - se la considera PQ
        if all_oos and bus["bus_type"] == 2:
            data["bus"][str(bus_i)]["bus_type"] = 1

        # La barra PQ no tiene en cuenta los generadores en servicio
        # por este motivo se apagan        
        if not all_oos and bus["bus_type"] == 1:
            for gen_i in bus_gens[bus_i]:
                data["gen"][gen_i]["gen_status"] = 0

    return data


def _check_high_impedance_lines(data):
    """
    Elimina lineas con alta impedancia
    """
    branch2remove = []
    for (i, brn) in data["branch"].items():
        if brn["br_x"] >= 9999:
            branch2remove.append(i)

        elif brn["f_bus"] == brn["t_bus"]:
            branch2remove.append(i)

    for i in branch2remove:        
        del data["branch"][i]
    
    return data


def build_pm(filename):
    """
    Arma una red en powermodels
    """
    sav = caspy.Savecase(filename)
    bus2idx = lookup_connections(sav)

    data = {
        "name": filename.replace(".sav", ""),
        "title": sav.psstit["HEDING"],        
        "baseMVA": sav.pssmsc["SBASE"],
        "per_unit": True,
        "storage": {},
        "switch": {},
        "bus": _bus2pm(sav, bus2idx),
        "branch": _branch2pm(sav, bus2idx),
        "load": _load2pm(sav, bus2idx),
        "gen": _gen2pm(sav, bus2idx),
        "shunt": _shunt2pm(sav, bus2idx),
        "dcline": _hvdc2pm(sav, bus2idx),
    }

    data = _check_pv_buses(data)
    data = _check_high_impedance_lines(data)

    ofile = filename.replace(".sav", ".json")
    with open(ofile, "w") as io:
        json.dump(data, io, indent=4)
    return os.path.abspath(ofile)


if __name__ == "__main__":
    t0 = time.time()
    filename = sys.argv[1]    
    data = build_pm(filename)    
    t1 = time.time()
    print("ET: {:.4f} s".format(t1 - t0))
