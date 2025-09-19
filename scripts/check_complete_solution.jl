
using PowerModels
using PyCall
using JuMP
using Ipopt
using Test

# cargo red en psse
psse34 = pyimport("psse34")
psspy = pyimport("psspy")
psspy.psseinit()
psspy.case(ARGS[1])
psspy.fnsl(
    options1=1,
    options2=0,
    options3=0,
    options4=0,
    options5=1,
    options6=0,
    options7=0,
    options8=0,
)
@test psspy.solved() == 0

# cargo red en powermodels
filename = ARGS[2]
data = parse_json(filename)
make_basic_network!(data)
for (i, bus) in data["bus"]
    bus["vm_start"] = bus["vm"]
    bus["va_start"] = bus["va"]    
end
for (i, gen) in data["gen"]
    gen["pg_start"] = gen["pg"]
    gen["qg_start"] = gen["qg"]
end
results = solve_ac_pf(data, Ipopt.Optimizer)
update_data!(data, results["solution"])
flows = calc_branch_flow_ac(data)
update_data!(data, flows)
@test results["termination_status"] == MOI.LOCALLY_SOLVED


@testset "barras" begin
    for (i, bus) in data["bus"]  
        "STARPOINT" in bus["source_id"] && continue                
        bus["bus_type"] == 4 && continue

        busi = bus["source_id"][2]
        ierr, vm = psspy.busdat(busi, "PU") 
        ierr, va = psspy.busdat(busi, "ANGLE") 
        
        if ierr == 0            
            @test isapprox(bus["vm"], vm; rtol=0.100) # 10 %
            @test isapprox(bus["va"], va; atol=0.100) # 5 grados
        end
    end
end

@testset "generadores" begin
    for (i, gen) in data["gen"]  
        gen["gen_status"] == 0 && continue
        data["bus"][string(gen["gen_bus"])]["bus_type"] == 3 && continue

        bus, id = gen["source_id"][2:end]
        ierr, pg = psspy.macdat(bus, id, "P") 
        ierr, qg = psspy.macdat(bus, id, "Q") 
        
        if ierr == 0                        
            @test isapprox(gen["pg"], pg / 100.0; atol=0.01) # 1 MW
            @test isapprox(gen["qg"], qg / 100.0; atol=0.50) # 50 MVAr
        end
    end
end

@testset "lineas" begin
    for (i, branch) in data["branch"]
        # filtro lineas superiores a 220 kV
        f_bus = branch["f_bus"]
        data["bus"]["$f_bus"]["base_kv"] <= 220 && continue
        branch["source_id"][1] != "LII" && continue

        fbus, tbus, ckt = branch["source_id"][2:end]
        ierr, flow = psspy.brnflo(fbus, tbus, ckt)

        if ierr == 0
            @test isapprox(branch["pf"], real(flow) / 100; atol=0.50) # 50 Mw
        end
    end
end



