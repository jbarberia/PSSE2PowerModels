using PowerNetworkModeling
using JuMP
using Test

using Ipopt


@testset "package" begin
    # Dummy test to check package
    @test true
end

@testset "parser" begin
    psspy.progress_output(6)

    @testset "read case" begin
        PowerNetworkModeling.open_psse("WSCC 9 bus.raw")
        psspy.fnsl()
        @test psspy.solved() == 0
    end

    @testset "create bus" begin
        PowerNetworkModeling.open_psse("WSCC 9 bus.raw")
        net = PowerNetworkModeling.Network()
        
        PowerNetworkModeling.add_bus!(net, 1)
        @test length(net.buses) == 1

        bus = net.buses[1]
        @test isapprox(start_value(bus.v_mag), 1.04; rtol=1e-6)
    end

    @testset "create branch" begin
        PowerNetworkModeling.open_psse("WSCC 9 bus.raw")
        net = PowerNetworkModeling.Network()

        PowerNetworkModeling.add_bus!(net, 4)
        PowerNetworkModeling.add_bus!(net, 5)
        PowerNetworkModeling.add_branch!(net, 4, 5, "1")

        @test length(net.branches) == 1        
    end

    @testset "create generators" begin
        PowerNetworkModeling.open_psse("WSCC 9 bus.raw")
        net = PowerNetworkModeling.create_network()
        @test length(net.generators) == 3
        
        gen = PowerNetworkModeling.get_generator(net, 3, "1 ")
        @test isapprox(start_value(gen.p_gen), 0.85; rtol=1e-6)
        
    end
    
    @testset "create network" begin
        PowerNetworkModeling.open_psse("WSCC 9 bus.raw")
        net = PowerNetworkModeling.create_network()
        @test length(net.buses) == 9
        @test length(net.branches) == 9
    end
end

@testset "model" begin
    @testset "case 9 flujo de potencia" begin
        PowerNetworkModeling.open_psse("WSCC 9 bus.raw")
        net = PowerNetworkModeling.create_network()        

        for bus in net.buses
            @constraint(net.model, bus.p_balance == 0)
            @constraint(net.model, bus.q_balance == 0)
        end

        for gen in net.generators
            ierr, type = psspy.busint(gen.ibus, "TYPE")
            type != 3 && fix(gen.p_gen, start_value(gen.p_gen))
        end

        obj = 0
        for gen in net.generators
            ierr, vs = psspy.macdat(gen.ibus, gen.id, "VSCHED")
            bus = PowerNetworkModeling.get_bus(net, gen.ibus)
            obj += (bus.v_mag - vs)^2
        end        
        @objective(net.model, Min, obj)

        set_optimizer(net.model, Ipopt.Optimizer)
        optimize!(net.model)
        @test is_solved_and_feasible(net.model)

        bus = PowerNetworkModeling.get_bus(net, 9)
        @test isapprox(JuMP.value(bus.v_mag), 1.032689; rtol=1e-6)
    end

    @testset "case 9 flujo de potencia con taps fijos" begin
        PowerNetworkModeling.open_psse("WSCC 9 bus taps.raw")
        net = PowerNetworkModeling.create_network()        

        for bus in net.buses
            @constraint(net.model, bus.p_balance == 0)
            @constraint(net.model, bus.q_balance == 0)
        end

        for gen in net.generators
            ierr, type = psspy.busint(gen.ibus, "TYPE")
            type != 3 && fix(gen.p_gen, start_value(gen.p_gen))
        end

        obj = 0
        for gen in net.generators
            ierr, vs = psspy.macdat(gen.ibus, gen.id, "VSCHED")
            bus = PowerNetworkModeling.get_bus(net, gen.ibus)
            obj += (bus.v_mag - vs)^2
        end        
        @objective(net.model, Min, obj)

        set_optimizer(net.model, Ipopt.Optimizer)
        optimize!(net.model)
        @test is_solved_and_feasible(net.model)

        bus = PowerNetworkModeling.get_bus(net, 9)
        @test isapprox(JuMP.value(bus.v_mag), 1.068753; rtol=1e-6)
    end

    @testset "sadi 500kV con shunts" begin
        PowerNetworkModeling.open_psse("V25p_MAX_RED.raw")
        net = PowerNetworkModeling.create_network()        

        for bus in net.buses
            @constraint(net.model, bus.p_balance == 0)
            @constraint(net.model, bus.q_balance == 0)

            ierr, type = psspy.busint(bus.number, "TYPE")
            if type == 3
                fix(bus.v_mag, start_value(bus.v_mag); force=true)
                fix(bus.v_ang, start_value(bus.v_ang); force=true)
            end
        end

        for shunt in net.switched_shunts
            fix(shunt.b, start_value(shunt.b))
        end

        for gen in net.generators
            ierr, type = psspy.busint(gen.ibus, "TYPE")
            type != 3 && fix(gen.p_gen, start_value(gen.p_gen))
        end

        obj = 0
        for gen in net.generators
            ierr, vs = psspy.macdat(gen.ibus, gen.id, "VSCHED")
            bus = PowerNetworkModeling.get_bus(net, gen.ibus)
            obj += (bus.v_mag - vs)^2
        end        


        @objective(net.model, Min, obj)
        set_optimizer(net.model, Ipopt.Optimizer)
        
        optimize!(net.model)
        
        @test is_solved_and_feasible(net.model)
        
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 2000).v_mag), 1.0160; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 2008).v_mag), 1.0090; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 2010).v_mag), 1.0273; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 2011).v_mag), 1.0161; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 2012).v_mag), 1.0165; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 2013).v_mag), 1.0091; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 2049).v_mag), 1.0180; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 2050).v_mag), 1.0180; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 3000).v_mag), 1.0000; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 3002).v_mag), 1.0100; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 3003).v_mag), 1.0060; rtol=1e-4)
        @test isapprox(JuMP.value.(PowerNetworkModeling.get_bus(net, 3004).v_mag), 1.0010; rtol=1e-4)

    end



end
