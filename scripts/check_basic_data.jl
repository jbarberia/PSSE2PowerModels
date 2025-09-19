using PowerModels
using JuMP
using Test
using Ipopt

filename = ARGS[1]
data = parse_json(filename)
make_basic_network!(data)
# export_matpower("tmp.m", data)

@testset "verificar mismatch" begin
    Y = calc_basic_admittance_matrix(data)
    S = calc_basic_bus_injection(data)
    V = calc_basic_bus_voltage(data)

    mismatch = S - V .* conj(Y * V)
    indices = sortperm(abs.(mismatch))

    for i in indices[end-5:end] |> reverse
        identification = data["bus"]["$i"]["source_id"][2]    
        mis_p = round(real(mismatch[i]) * 100, digits=2)
        mis_q = round(imag(mismatch[i]) * 100, digits=2)
        println("BUS:\t$(identification)\t$(mis_p)\tMW\t$(mis_q)\tMVAr")
    end

    # 5 barras por encima de un mismatch de 1 pu
    # @test sum( abs.(mismatch) .> 1 ) <= 5
end

@testset "flujo de carga DC" begin
    # prueba flujo de carga en continua
    results = solve_dc_pf(data, Ipopt.Optimizer)
    @test results["termination_status"] == MOI.LOCALLY_SOLVED
end

@testset "flujo de carga AC" begin
    # prueba flujo de carga en alterna - pero con warm start
    for (i, bus) in data["bus"]
        bus["vm_start"] = bus["vm"]
        bus["va_start"] = bus["va"]    
    end

    for (i, gen) in data["gen"]
        gen["pg_start"] = gen["pg"]
        gen["qg_start"] = gen["qg"]
    end

    # corro una iteracion a efectos de inicializar todas las variables
    pm = instantiate_model(data, ACPPowerModel, build_pf);
    set_optimizer(pm.model, Ipopt.Optimizer)
    set_optimizer_attribute(pm.model, "max_iter", 100)
    set_optimizer_attribute(pm.model, "print_level", 5)
    results = optimize_model!(pm)
    @test results["termination_status"] == MOI.LOCALLY_SOLVED
end

# en caso de que falle usar el siguiente bloque para verificar que barra es la que rompe el flujo.
# TOL = 1.5e-2
# #linear = all_constraints(pm.model, JuMP.GenericAffExpr{Float64,JuMP.VariableRef}, MOI.EqualTo{Float64})
# nonlinear = all_constraints(pm.model, JuMP.NonlinearExpr, MOI.EqualTo{Float64});
# for c in nonlinear
#     constr_obj = JuMP.constraint_object(c)
#     lhs = value(constr_obj.func)
#     rhs = constr_obj.set.value
#     if isnan(lhs) || isinf(lhs)
#         @warn "Nonlinear constraint $(c) evaluates to NaN/Inf"
#     elseif abs(lhs - rhs) > TOL
#         @warn "Nonlinear constraint $(c) violated: lhs=$lhs rhs=$rhs residual=$(lhs - rhs)"
#     end
# end


# minimum(value.(var(pm, :vm)))
# data["bus"]["2865"]
# data["bus"]["2868"]






