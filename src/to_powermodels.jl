

function bus_to_pm()
    intstr = ["NUMBER", "TYPE", "AREA", "ZONE", "OWNER"]
    charstr = ["NAME"]
    realstr = ["PU", "ANGLE", "BASE", "NVLMHI", "NVLMLO"]

    ierr, nb = psspy.abuscount(-1, flag=2)
    ierr, intarr = psspy.abusint(-1, flag=2, string=intstr)
    ierr, chararr = psspy.abuschar(-1, flag=2, string=charstr)
    ierr, realarr = psspy.abusreal(-1, flag=2, string=realstr)

    arr = vcat(intarr, chararr, realarr)
    k = vcat(intstr, charstr, realstr)
    bus = Dict{String,Any}(k[i] => @view arr[i, :] for i in eachindex(k))

    data = Vector{Dict{String,Any}}(undef, nb)
    for i in 1:nb
        data[i] = Dict{String,Any}(
            "bus_i" => bus["NUMBER"][i],
            "source_id" => ["BU", bus["NUMBER"][i]],
            "bus_type" => bus["TYPE"][i],
            "base_kv" => bus["BASE"][i],
            "vm" => bus["PU"][i],
            "va" => bus["ANGLE"][i],
            "area" => bus["AREA"][i],
            "zone" => bus["ZONE"][i],
            "owner" => bus["OWNER"][i],
            "vmin" => bus["NVLMLO"][i],
            "vmax" => bus["NVLMHI"][i],
        )
    end

    return data
end


function non_transformer_branch_to_pm()
    intstr = ["FROMNUMBER", "TONUMBER", "TYPE", "STATUS"]
    charstr = ["ID"]
    realstr = ["RATEA", "CHARGING"]
    cplxstr = ["RX", "FROMSHNT", "TOSHNT"]

    ierr, nb = psspy.abrncount(-1, flag=2)
    ierr, intarr = psspy.abrnint(-1, flag=2, string=intstr)
    ierr, chararr = psspy.abrnchar(-1, flag=2, string=charstr)
    ierr, realarr = psspy.abrnreal(-1, flag=2, string=realstr)
    ierr, cplxarr = psspy.abrncplx(-1, flag=2, string=cplxstr)

    arr = vcat(intarr, chararr, realarr, cplxarr)
    k = vcat(intstr, charstr, realstr, cplxstr)
    brn = Dict{String,Any}(k[i] => @view arr[i, :] for i in eachindex(k))

    data = Vector{Dict{String,Any}}(undef, nb)
    for i in 1:nb
        data[i] = Dict{String,Any}(
            "f_bus" => brn["FROMNUMBER"][i],
            "t_bus" => brn["TONUMBER"][i],
            "source_id" => [
                brn["TYPE"][i] > 0 ? "SYS" : "LII",
                brn["FROMNUMBER"][i],
                brn["TONUMBER"][i],
                brn["ID"][i]
            ],
            "br_status" => brn["STATUS"][i],
            "br_r" => brn["RX"][i] |> real,
            "br_x" => brn["RX"][i] |> imag,
            "b_fr" => brn["CHARGING"][i] / 2 + imag(brn["FROMSHNT"][i]),
            "b_to" => brn["CHARGING"][i] / 2 + imag(brn["TOSHNT"][i]),
            "g_fr" => 0.0,
            "g_to" => 0.0,
            "tap" => 1.0,
            "shift" => 0.0,
            "transformer" => false,
            "switch" => brn["TYPE"][i] > 0,
        )
    end

    return data
end


function transformer_branch_to_pm()
    intstr = ["FROMNUMBER", "TONUMBER", "WIND1NUMBER", "WIND2NUMBER", "STATUS"]
    charstr = ["ID"]
    realstr = ["RATEA", "RATIO", "RATIO2", "ANGLE"]
    cplxstr = ["RXACT", "YMAG"]

    ierr, nb = psspy.atrncount(-1, flag=2)
    ierr, intarr = psspy.atrnint(-1, flag=2, string=intstr)
    ierr, chararr = psspy.atrnchar(-1, flag=2, string=charstr)
    ierr, realarr = psspy.atrnreal(-1, flag=2, string=realstr)
    ierr, cplxarr = psspy.atrncplx(-1, flag=2, string=cplxstr)

    arr = vcat(intarr, chararr, realarr, cplxarr)
    k = vcat(intstr, charstr, realstr, cplxstr)
    trn = Dict{String,Any}(k[i] => @view arr[i, :] for i in eachindex(k))

    data = Vector{Dict{String,Any}}(undef, nb)
    for i in 1:nb
        data[i] = Dict{String,Any}(
            "f_bus" => trn["WIND1NUMBER"][i],
            "t_bus" => trn["WIND2NUMBER"][i],
            "source_id" => ["TR", trn["WIND1NUMBER"][i], trn["WIND2NUMBER"][i], trn["ID"][i]],
            "br_status" => trn["STATUS"][i],
            "br_r" => (trn["RXACT"][i] * trn["RATIO2"][i]^2) |> real,   # POM 4.6 Tap Changing Transformers
            "br_x" => (trn["RXACT"][i] * trn["RATIO2"][i]^2) |> imag,   # POM 4.6 Tap Changing Transformers
            "b_fr" => trn["YMAG"][i] |> imag,
            "b_to" => 0.0,
            "g_fr" => trn["YMAG"][i] |> real,
            "g_to" => 0.0,
            "tap" => trn["RATIO"][i] / trn["RATIO2"][i],
            "shift" => trn["ANGLE"][i] * pi / 180,
            "transformer" => true,            
        )
    end

    return data
end


function three_winding_branch_to_pm()
    intstr = ["WNDBUSNUMBER", "WIND1NUMBER", "WIND2NUMBER", "WIND3NUMBER", "WNDNUM", "STATUS"]
    charstr = ["ID"]
    realstr = ["RATEA", "RATIO", "ANGLE"]
    cplxstr = ["RXACT"]

    ierr, nb = psspy.awndcount(-1, flag=3, entry=2)
    ierr, intarr = psspy.awndint(-1, flag=3, entry=2, string=intstr)
    ierr, chararr = psspy.awndchar(-1, flag=3, entry=2, string=charstr)
    ierr, realarr = psspy.awndreal(-1, flag=3, entry=2, string=realstr)
    ierr, cplxarr = psspy.awndcplx(-1, flag=3, entry=2, string=cplxstr)

    # se suman numeros starbus
    starbus = []
    for i in 1:Int(size(intarr)[2] / 3)
        push!(starbus, 1_000_000 + i)
        push!(starbus, 1_000_000 + i)
        push!(starbus, 1_000_000 + i)
    end

    arr = vcat(intarr, chararr, realarr, cplxarr)
    arr = [arr; starbus']
    k = vcat(intstr, charstr, realstr, cplxstr, ["STARBUSNUMBER"])
    tr3 = Dict{String,Any}(k[i] => @view arr[i, :] for i in eachindex(k))

    brn_data = Vector{Dict{String,Any}}(undef, nb)
    for i in 1:nb

        # transformer no load losses
        if tr3["WNDNUM"][i] == 1
            ierr, ymagnt = psspy.tr3dt2(
                tr3["WIND1NUMBER"][i],
                tr3["WIND2NUMBER"][i],
                tr3["WIND3NUMBER"][i],
                tr3["ID"][i],
                "YMAGNT")                
        else
            ymagnt = 0 + 0im
        end

        brn_data[i] = Dict{String,Any}(
            "f_bus" => tr3["WNDBUSNUMBER"][i],
            "t_bus" => tr3["STARBUSNUMBER"][i],
            "source_id" => [
                "T3",
                tr3["WIND1NUMBER"][i],
                tr3["WIND2NUMBER"][i],
                tr3["WIND3NUMBER"][i],
                tr3["ID"][i],
                tr3["WNDNUM"][i]
            ],
            "br_status" => tr3["STATUS"][i],
            "br_r" => tr3["RXACT"][i] |> real,
            "br_x" => tr3["RXACT"][i] |> imag,
            "b_fr" => ymagnt |> imag,
            "b_to" => 0.0,
            "g_fr" => ymagnt |> real,
            "g_to" => 0.0,
            "tap" => tr3["RATIO"][i],
            "shift" => tr3["ANGLE"][i] * pi / 180,
            "transformer" => true,
        )
    end

    nt = Int(nb / 3)
    bus_data = Vector{Dict{String,Any}}(undef, nt)
    
    for j in 1:nt
        i = 3*(j - 1) + 1

        ibus = tr3["WIND1NUMBER"][i]
        jbus = tr3["WIND2NUMBER"][i]
        kbus = tr3["WIND3NUMBER"][i]
        ickt = tr3["ID"][i]
        
        ierr, vm = psspy.tr3dat(ibus, jbus, kbus, ickt, "VMSTAR")
        ierr, va = psspy.tr3dat(ibus, jbus, kbus, ickt, "ANSTAR")
        ierr, area = psspy.busint(ibus, "AREA")
        ierr, zone = psspy.busint(ibus, "ZONE")
        ierr, owner = psspy.busint(ibus, "OWNER")
            
        bus_data[j] = Dict{String,Any}(
            "bus_i" => tr3["STARBUSNUMBER"][i],
            "source_id" => [
                "STARBUS",
                tr3["WIND1NUMBER"][i],
                tr3["WIND2NUMBER"][i],
                tr3["WIND3NUMBER"][i],
                tr3["ID"][i],
            ],
            "bus_type" => 1,
            "base_kv" => 1.0,
            "vm" => vm,
            "va" => va * pi / 180,
            "area" => area,
            "zone" => zone,
            "owner" => owner,
            "vmin" => 0.5,
            "vmax" => 2.0,
        )
    end

    return brn_data, bus_data
end


function machine_to_pm()
    baseMVA = psspy.sysmva()
    
    intstr = ["NUMBER", "STATUS"]
    charstr = ["ID"]
    realstr = ["PGEN", "QGEN", "PMAX", "PMIN", "QMAX", "QMIN"]
    cplxstr = ["ZSORCE"]

    ierr, nb = psspy.amachcount(-1, flag=2)
    ierr, intarr = psspy.amachint(-1,  flag=2, string=intstr)
    ierr, chararr = psspy.amachchar(-1, flag=2, string=charstr)
    ierr, realarr = psspy.amachreal(-1, flag=2, string=realstr)
    ierr, cplxarr = psspy.amachcplx(-1, flag=2, string=cplxstr)

    arr = vcat(intarr, chararr, realarr, cplxarr)
    k = vcat(intstr, charstr, realstr, cplxstr)
    mach = Dict{String,Any}(k[i] => @view arr[i, :] for i in eachindex(k))

    data = Vector{Dict{String,Any}}(undef, nb)
    for i in 1:nb
        ibus = mach["NUMBER"][i]
        id = mach["ID"][i]
        
        ierr, vs = psspy.macdat(ibus, id, "VSCHED")
        ierr, ireg = psspy.macint(ibus, id, "IREG")

        data[i] = Dict(
            "gen_bus" => mach["NUMBER"][i],            
            "source_id" => ["ME", mach["NUMBER"][i], mach["ID"][i]],
            "pg" => mach["PGEN"][i] / baseMVA,
            "qg" => mach["QGEN"][i] / baseMVA,
            "pmin" => mach["PMIN"][i] / baseMVA,
            "pmax" => mach["PMAX"][i] / baseMVA,
            "qmin" => mach["QMIN"][i] / baseMVA,
            "qmax" => mach["QMAX"][i] / baseMVA,
            "vg" => vs,
            "vg_bus" => ireg,
            "gen_status" => mach["STATUS"][i],
        )
    end

    return data
end


function load_to_pm()
    baseMVA = psspy.sysmva()

    intstr = ["NUMBER", "AREA", "ZONE", "OWNER", "SCALE", "STATUS"]
    charstr = ["ID"]    
    cplxstr = ["MVANOM"]

    ierr, nb = psspy.aloadcount(-1, flag=1)
    ierr, intarr = psspy.aloadint(-1,  flag=1, string=intstr)
    ierr, chararr = psspy.aloadchar(-1, flag=1, string=charstr)    
    ierr, cplxarr = psspy.aloadcplx(-1, flag=1, string=cplxstr)

    arr = vcat(intarr, chararr, cplxarr)
    k = vcat(intstr, charstr, cplxstr)
    load = Dict{String,Any}(k[i] => @view arr[i, :] for i in eachindex(k))

    data = Vector{Dict{String,Any}}(undef, nb)
    for i in 1:nb
        data[i] = Dict(
            "load_bus" => load["NUMBER"][i],            
            "source_id" => ["LO", load["NUMBER"][i], load["ID"][i]],
            "pd" => load["MVANOM"][i] / baseMVA |> real ,
            "qd" => load["MVANOM"][i] / baseMVA |> imag ,            
            "scalable" => load["SCALE"][i],
            "status" => load["STATUS"][i],
        )
    end

    return data
end


function sw_shunt_to_pm()
    baseMVA = psspy.sysmva()

    intstr = ["NUMBER", "AREA", "ZONE", "OWNER", "STATUS"]    
    realstr = ["BSWNOM"]    

    ierr, nb = psspy.aswshcount(-1, flag=1)
    ierr, intarr = psspy.aswshint(-1,  flag=1, string=intstr)
    ierr, realarr = psspy.aswshreal(-1, flag=1, string=realstr)    

    arr = vcat(intarr, realarr)
    k = vcat(intstr, realstr)
    shunt = Dict{String,Any}(k[i] => @view arr[i, :] for i in eachindex(k))

    data = Vector{Dict{String,Any}}(undef, nb)
    for i in 1:nb
        bus = Int(shunt["NUMBER"][i])
        data[i] = Dict(
            "shunt_bus" => bus,      
            "source_id" => ["SWS", bus],
            "gs" => 0.0,
            "bs" => shunt["BSWNOM"][i] / baseMVA,             
            "status" => shunt["STATUS"][i] |> Int,
        )
    end

    return data
end


function fx_shunt_to_pm()
    baseMVA = psspy.sysmva()

    intstr = ["NUMBER", "STATUS"]   
    charstr = ["ID"]        
    cplxstr = ["SHUNTNOM"]    

    ierr, nb = psspy.afxshuntcount(-1, flag=1)
    ierr, intarr = psspy.afxshuntint(-1, flag=1, string=intstr)
    ierr, chararr = psspy.afxshuntchar(-1, flag=1, string=charstr)
    ierr, cplxarr = psspy.afxshuntcplx(-1, flag=1, string=cplxstr)    

    arr = vcat(intarr, chararr, cplxarr)
    k = vcat(intstr, charstr, cplxstr)
    shunt = Dict{String,Any}(k[i] => @view arr[i, :] for i in eachindex(k))

    data = Vector{Dict{String,Any}}(undef, nb)
    for i in 1:nb
        data[i] = Dict(
            "shunt_bus" => shunt["NUMBER"][i],            
            "source_id" => ["FXS", shunt["NUMBER"][i], shunt["ID"][i]],
            "gs" => shunt["SHUNTNOM"][i] / baseMVA |> real,
            "bs" => shunt["SHUNTNOM"][i] / baseMVA |> imag,
            "status" => shunt["STATUS"][i],
        )
    end

    return data
end


function dcline_to_pm()
    baseMVA = psspy.sysmva()

    intstr = ["FROMNUMBER", "TONUMBER"]   
    charstr = ["DCNAME"]
    cplxstr = ["PQAC_R", "PQAC_I"]    

    ierr, nb = psspy.a2trmdccount(-1, flag=1)
    ierr, intarr = psspy.a2trmdcint(-1, flag=1, string=intstr)
    ierr, chararr = psspy.a2trmdcchar(-1, flag=1, string=charstr)
    ierr, cplxarr = psspy.a2trmdccplx(-1, flag=1, string=cplxstr)    

    arr = vcat(intarr, chararr, cplxarr)
    k = vcat(intstr, charstr, cplxstr)
    hvdc = Dict{String,Any}(k[i] => @view arr[i, :] for i in eachindex(k))

    data = Vector{Dict{String,Any}}(undef, nb)
    for i in 1:nb        
        data[i] = Dict(
            "f_bus" => hvdc["FROMNUMBER"][i],
            "t_bus" => hvdc["TONUMBER"][i],
            "pf" => hvdc["PQAC_R"][i] / baseMVA |> real,
            "pt" => hvdc["PQAC_I"][i] / baseMVA |> real,
            "vf" => 1.0,
            "vt" => 1.0,
            "pminf" => hvdc["PQAC_R"][i] / baseMVA |> real,
            "pmaxf" => hvdc["PQAC_R"][i] / baseMVA |> real,
            "qminf" => hvdc["PQAC_R"][i] / baseMVA |> imag,
            "qmaxf" => hvdc["PQAC_R"][i] / baseMVA |> imag,
            "pmint" => hvdc["PQAC_I"][i] / baseMVA |> real,
            "pmaxt" => hvdc["PQAC_I"][i] / baseMVA |> real,
            "qmint" => hvdc["PQAC_I"][i] / baseMVA |> imag,
            "qmaxt" => hvdc["PQAC_I"][i] / baseMVA |> imag,
            "loss0" => 0.0,
            "loss1" => 0.0,
            "br_status" => 1,            
            "source_id" => ["DC", hvdc["DCNAME"][i]],
        )
    end
    return data
end


function build_pm_data()
    baseMVA = psspy.sysmva()

    pm_data = Dict{String, Any}(
        "name"     => "",
        "title"    => "",
        "baseMVA"  => baseMVA,
        "per_unit" => true,
        "storage"  => Dict{String, Any}(),
        "switch"   => Dict{String, Any}(),
        "bus"      => Dict{String, Any}(),
        "branch"   => Dict{String, Any}(),
        "load"     => Dict{String, Any}(),
        "gen"      => Dict{String, Any}(),
        "shunt"    => Dict{String, Any}(),
        "dcline"   => Dict{String, Any}(),
    )

    # topology
    buses = bus_to_pm()
    lines = non_transformer_branch_to_pm()
    xfmr_2w = transformer_branch_to_pm()
    xfmr_3w, starbuses = three_winding_branch_to_pm()

    # components
    machines = machine_to_pm()
    loads = load_to_pm()
    sw_shunts = sw_shunt_to_pm()
    fx_shunts = fx_shunt_to_pm()    
    dclines = dcline_to_pm()

    # buses
    for bus in [buses..., starbuses...]
        i = bus["bus_i"]
        bus["index"] = bus["bus_i"]
        pm_data["bus"][string(i)] = bus
    end
    
    # branches
    sw_idx = 1
    br_idx = 1
    for brn in [lines..., xfmr_2w..., xfmr_3w...]
        #if get(brn, "switch", false)
        #    brn["psw"] = 0.0
        #    brn["qsw"] = 0.0
        #    brn["state"] = brn["br_status"]
        #    brn["status"] = 1
        #    brn["index"] = sw_idx
        #    brn["source_id"][1] = "SYS"
        #    pm_data["switch"][string(sw_idx)] = brn
        #    sw_idx += 1
        #else
            brn["index"] = br_idx
            brn["angmin"] = -pi / 6
            brn["angmax"] =  pi / 6
            pm_data["branch"][string(br_idx)] = brn
            br_idx += 1
        #end

    end
    
    for (i, dcline) in enumerate(dclines)
        dcline["index"] = i
        pm_data["dcline"][string(i)] = dcline
    end

    # components
    for (i, mach) in enumerate(machines)
        mach["index"] = i
        pm_data["gen"][string(i)] = mach
    end
    
    for (i, load) in enumerate(loads)
        load["index"] = i
        pm_data["load"][string(i)] = load
    end
    
    for (i, shunt) in enumerate([sw_shunts..., fx_shunts...])
        shunt["index"] = i
        pm_data["shunt"][string(i)] = shunt
    end



    return pm_data
end

