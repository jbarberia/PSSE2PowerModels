


function bus_to_psse(bus, ibus)    
    psspy.bus_chng_4(
        ibus, 0,
        intgar1 = bus["bus_type"],
        realar2 = bus["vm"],
        realar3 = bus["va"] * 180 / pi,
    )     
end


function starbus_to_psse(bus)
    ibus, jbus, kbus, ickt = bus["source_id"][2:end]
    psspy.three_wnd_imped_chng_4(ibus, jbus, kbus, ickt,
        realari16=bus["vm"],
        realari17=bus["va"] * 180 / pi,
    )
end


function branch_to_psse(branch)
    ibus, jbus, ickt = branch["source_id"][2:end]
    ierr, type_ibus = psspy.busint(ibus, "TYPE")
    ierr, type_jbus = psspy.busint(jbus, "TYPE")
    status = Bool(branch["br_status"]) && type_ibus != 4 && type_jbus != 4
    psspy.branch_chng_3(ibus, jbus, ickt, 
        intgar1=status
    )
end


function switch_to_psse(branch)
    ibus, jbus, ickt = branch["source_id"][2:end]
    ierr, type_ibus = psspy.busint(ibus, "TYPE")
    ierr, type_jbus = psspy.busint(jbus, "TYPE")
    status = Bool(branch["br_status"]) && type_ibus != 4 && type_jbus != 4
    psspy.system_swd_chng(ibus, jbus, ickt,
        intgar1=status
    )
end


function xfmr_2w_to_psse(branch)
    bus1, bus2, ickt = branch["source_id"][2:end]            
    ierr, cw = psspy.xfrint(bus1, bus2, ickt, "CW")
    ierr, tapped = psspy.xfrint(bus1, bus2, ickt, "TAPPED")
    ierr, ratio  = psspy.xfrdat(bus1, bus2, ickt, "RATIO")
    ierr, ratio2 = psspy.xfrdat(bus1, bus2, ickt, "RATIO2")
    
    t1 = t2 = 1.0
    if tapped == bus1
        t1 = branch["tap"] * ratio2
        t2 = ratio2        
    elseif tapped == bus2
        t1 = ratio
        t2 = branch["tap"]
    end
    
    if cw == 2
        ierr, base1 = psspy.busdat(bus1, "BASE")
        ierr, base2 = psspy.busdat(bus2, "BASE")
        t1 *= base1
        t2 *= base2
    elseif cw == 3
        ierr, base_t1 = psspy.xfrdat(bus1, bus2, ickt, "NOMV1")
        ierr, base_t2 = psspy.xfrdat(bus1, bus2, ickt, "NOMV2")
        ierr, base_u1 = psspy.busdat(bus1, "BASE")
        ierr, base_u2 = psspy.busdat(bus2, "BASE")
        t1 *= (base_u1 / base_t1)
        t2 *= (base_u2 / base_t2)
    end
        
    psspy.two_winding_chng_6(bus1, bus2, ickt, 
        intgar1=branch["br_status"],
        realari4=t1,    
        realari7=t2,    
    )
end


function xfmr_3w_to_psse(branch)
    # Generalmente o esta todo en servicio o esta todo fuera de servicio
    ibus, jbus, kbus, ickt, warg = branch["source_id"][2:end]    
    psspy.three_wnd_imped_chng_4(ibus, jbus, kbus, ickt, 
        intgar8=branch["br_status"],   
    )
    ierr, base1 = psspy.busdat(ibus, "BASE")
    ierr, base2 = psspy.busdat(jbus, "BASE")
    ierr, base3 = psspy.busdat(kbus, "BASE")
    ierr, cw = psspy.tr3int(ibus, jbus, kbus, ickt, "CW")
    base = cw != 2 ? 1.0 : [base1, base2, base3][warg]
    psspy.three_wnd_winding_data_5(ibus, jbus, kbus, ickt, warg,
        realari1 = branch["tap"] * base
    )
end


function machine_to_psse(gen)
    baseMVA = psspy.sysmva()
    ibus, id = gen["source_id"][2:end]
    psspy.machine_chng_2(ibus,id,
        intgar1=gen["gen_status"],
        realar1=gen["pg"] * baseMVA,
        realar2=gen["qg"] * baseMVA,
    )
    ierr, vm = psspy.busdat(ibus, "PU")
    psspy.plant_data_4(ibus, 0, intgar1=0, realar1=vm)
    ierr, bus_type = psspy.busint(ibus, "TYPE")    
    if gen["gen_status"] == 1 && bus_type < 2
        psspy.bus_chng_4(
            ibus, 0,
            intgar1=2,
        )
    end
end


function load_to_psse(load)
    baseMVA = psspy.sysmva()
    ibus, id = load["source_id"][2:end]
    psspy.load_data_5(ibus, id, 
        intgar1=load["status"],
        realar1=load["pd"] * baseMVA,
        realar2=load["qd"] * baseMVA,
    )
end


function fixed_shunt_to_psse(shunt)
    baseMVA = psspy.sysmva()
    ibus, id = shunt["source_id"][2:end]    
    psspy.shunt_chng(ibus, id,
        intgar1=shunt["status"],
        realar1=shunt["gs"] * baseMVA,
        realar2=shunt["bs"] * baseMVA,
    )
end


function switched_shunt_to_psse(shunt)
    baseMVA = psspy.sysmva()
    ibus = shunt["source_id"][2]
    psspy.switched_shunt_chng_4(ibus,
        intgar12=shunt["status"],
        realar11=shunt["bs"] * baseMVA,
    )
end

    
function build_psse_data(data::Dict)
    
    # Buses
    for (i, bus) in data["bus"]
        source_id = bus["source_id"]
        if source_id[1] == "BU"
            bus_to_psse(bus, source_id[2])
            
        elseif source_id[1] == "GROUPEDBUS"
            for ibus in source_id[2:end]
                bus_to_psse(bus, ibus)
            end
        
        elseif source_id[1] == "STARBUS"
            starbus_to_psse(bus)
        end
    end
    
    # Branches
    for (i, branch) in data["branch"]
        source_id = branch["source_id"]        
        if source_id[1] == "LII"
            branch_to_psse(branch)
        elseif source_id[1] == "SYS"
            switch_to_psse(branch)
        elseif source_id[1] == "TR"
            xfmr_2w_to_psse(branch)
        elseif source_id[1] == "T3"
            xfmr_3w_to_psse(branch)
        end
    end

    # Add the removed ZI lines    
    for (i, branch) in data["_removed_zi_branches"]
        source_id = branch["source_id"]                   
        if source_id[1] == "LII"
            branch_to_psse(branch)
        elseif source_id[1] == "SYS"
            switch_to_psse(branch)
        end
    end
    
    # Generators
    for (i, gen) in data["gen"]
        source_id = gen["source_id"]
        if source_id[1] == "ME"
            machine_to_psse(gen)
        end
    end

    # Loads
    ierr, buses = psspy.alodbusint(-1, flag=2, string="NUMBER")
    for ibus in buses
        psspy.purgloads(ibus)
    end

    for (i, load) in data["load"]
        source_id = load["source_id"]
        if source_id[1] == "LO"
            load_to_psse(load)
        end
    end

    # Shunt
    for (i, shunt) in data["shunt"]
        source_id = shunt["source_id"]
        if source_id[1] == "FXS"
            fixed_shunt_to_psse(shunt)
        elseif source_id[1] == "SWS"
            switched_shunt_to_psse(shunt)
        end
    end
end
