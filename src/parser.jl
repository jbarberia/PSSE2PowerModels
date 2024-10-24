function open_psse(filename)
    if endswith(filename, ".sav")
        psspy.case(filename)
    elseif endswith(filename, ".raw")
        psspy.read(0, filename)
    end

end


function create_network()
    net = Network()

    # buses
    ierr = psspy.inibus(0)
    while ierr == 0
        ierr, ibus, cval = psspy.nxtbus()
        ierr != 0 && continue

        ierr, type = psspy.busint(ibus, "TYPE")
        type == 4 && continue

        add_bus!(net, ibus)
    end

    # branches
    for ibus in map(x -> x.number, net.buses)
        ierr = psspy.inibrn(ibus, 1)
        while ierr == 0
            ierr, jbus, kbus, ickt = psspy.nxtbrn3(ibus)
            ierr != 0 && continue
            
            if kbus == 0
                ierr, status = psspy.brnint(ibus, jbus, ickt, "STATUS")
            else
                status = 0 # TODO detectar trafos en servicio
            end
            status == 0 && continue
            

            add_branch!(net, ibus, jbus, kbus, ickt)  
        end
    end
    
    # loads
    for ibus in map(x -> x.number, net.buses)
        ierr = psspy.inilod(ibus)
        while ierr == 0
            ierr, id = psspy.nxtlod(ibus)
            ierr != 0 && continue
            add_load!(net, ibus, id)
        end
    end

    # machines
    for ibus in map(x -> x.number, net.buses)
        ierr = psspy.inimac(ibus)
        while ierr == 0
            ierr, id = psspy.nxtmac(ibus)
            ierr != 0 && continue
            add_generator!(net, ibus, id)
        end
    end

    # shunts



    return net
end
