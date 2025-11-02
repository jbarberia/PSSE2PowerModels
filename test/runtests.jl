using PowerNetworkModeling
using PowerModels
using JuMP
using Ipopt
using Test


psspy.progress_output(6) # No output

optimizer = JuMP.optimizer_with_attributes(
    Ipopt.Optimizer,
    "tol"=>1e-6,
    "print_level"=>0,
)


function solve()
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
    resolve_swithces!(data)
    results = solve_ac_pf(data, optimizer)
    
    # postprocess
    update_data!(data, results["solution"])
    flows = calc_branch_flow_ac(data)
    update_data!(data, flows)

    return data
end


function test_voltage(data; vm_atol=1e-4, va_atol=1e-4)
    for (i, res_bus) in data["bus"]
        ibus = parse(Int, i)
        ibus >= 100_000 && continue
        ierr, vm = psspy.busdat(ibus, "PU")
        ierr, va = psspy.busdat(ibus, "ANGLE")
        # @show ibus
        @test isapprox(res_bus["vm"], vm, atol=vm_atol)
        @test isapprox(res_bus["va"], va, atol=va_atol)
    end    
end


function test_powerflow(data; p_atol=1e-4, q_atol=1e-4)
    baseMVA = psspy.sysmva()
    for (i, brn) in data["branch"]        
        if brn["source_id"][1] == "LII"
            ibus, jbus, ckt = brn["source_id"][2:end]
            ierr, flow = psspy.brnflo(ibus, jbus, ckt)            
            pf = flow / baseMVA |> real
            qf = flow / baseMVA |> imag
            # @show (ibus, jbus, ckt)
            @test(isapprox(brn["pf"], pf, atol=p_atol))
            @test(isapprox(brn["qf"], qf, atol=q_atol))
        end        
    end    
end


@testset failfast = true "WSCC9" begin
    psspy.read(0,"data/WSCC 9 bus.raw")
    data = solve()
    test_voltage(data)
    test_powerflow(data)
end


@testset failfast = true "IEEE118" begin    
    psspy.read(0,"data/IEEE 118 Bus.raw")
    data = solve()
    test_voltage(data)
    test_powerflow(data)
end


@testset failfast = true "IEEE300" begin    
    psspy.read(0,"data/IEEE300Bus.raw")
    data = solve()
    test_voltage(data; vm_atol=1e-3, va_atol=1e-2)
    test_powerflow(data; p_atol=1e-3, q_atol=1e-2)
end


@testset failfast = true "RAWEO" begin    
    psspy.read(0,"data/RAWEO.raw")
    data = solve()
    test_voltage(data)
    test_powerflow(data)
end


@testset failfast = true "SIP" begin
    psspy.read(0,"data/SIP.raw")
    data = solve()
    test_voltage(data; vm_atol=1e-3, va_atol=1e-2)
    test_powerflow(data; p_atol=1e-3, q_atol=1e-2)
end




# @testset failfast = true "Texas66" begin
#     psspy.read(0,"data/Base_Texas_66GW.raw")
#     data = solve()
#     test_voltage(data)
# end
