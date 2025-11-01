using PowerNetworkModeling
using PowerModels
using JuMP
using Ipopt
using Test


optimizer = Ipopt.Optimizer

function test_voltage()
    psspy.fnsl(
        options1=0,
        options2=0,
        options3=0,
        options4=1,
        options5=0,
        options6=0,
        options7=0,
        options8=0,
    )
    data = build_pm_data()
    results = solve_ac_pf(data, optimizer)

    for (i, res_bus) in results["solution"]["bus"]
        ibus = parse(Int, i)
        ierr, vm = psspy.busdat(ibus, "PU")
        ierr, va = psspy.busdat(ibus, "ANGLE")
        
        ierr, type = psspy.busint(ibus, "TYPE")        
        
        @test isapprox(res_bus["vm"], vm, atol=1e-4)
        @test isapprox(res_bus["va"], va, atol=1e-4)
    end    
end


@testset failfast = true "WSCC9" begin
    psspy.read(0,"data/WSCC 9 bus.raw")
    test_voltage()
end


@testset failfast = true "IEEE118" begin
    psspy.read(0,"data/IEEE 118 Bus.raw")
    test_voltage()
end


# @testset failfast = true "Texas66" begin
#     psspy.read(0,"data/Base_Texas_66GW.raw")
#     test_voltage()
# end
