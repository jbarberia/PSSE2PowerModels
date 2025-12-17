
@testset failfast = true "verificacion_taps_3W" begin
    psspy.read(0,"data/ver2526pid.raw")
    data = build_pm_data()
    merge_zi_connected_buses!(data)
    correct_pv_bus_type!(data)
    
    source2idx = Dict(brn["source_id"] => i for (i, brn) in data["branch"])
    
    # modify tap of 3W transformer T7EZ
    index_T7EZ = source2idx[["T3", 3000, 3110, 3702, "7 ", 2]]
    old_t7_tap = data["branch"][index_T7EZ]["tap"]     
    new_t7_tap = data["branch"][index_T7EZ]["tap"] = data["branch"][index_T7EZ]["tm_min"]
    
    build_psse_data(data)
    ierr, t7_tap = psspy.wnddat(3110, 3702, 3000, "7 ", "RATIO")

    @test t7_tap != old_t7_tap
    @test isapprox(t7_tap, new_t7_tap, atol=1e-4)


    # 500 kV is not tapped
    index_T7EZ = source2idx[["T3", 3000, 3110, 3702, "7 ", 1]]
    w1 = data["branch"][index_T7EZ]
    @test isapprox(w1["tap"], w1["tm_min"], atol=1e-4)
    @test isapprox(w1["tap"], w1["tm_max"], atol=1e-4)
end


@testset failfast = true "verificacion_taps_2W" begin
    psspy.read(0,"data/ver2526pid.raw")
    data = build_pm_data()
    merge_zi_connected_buses!(data)
    correct_pv_bus_type!(data)
    
    source2idx = Dict(brn["source_id"] => i for (i, brn) in data["branch"])

    # modify tap of 2W
    index_mesespi = source2idx[["TR", 478, 477, "1 "]]
    old_mesespi_tap = data["branch"][index_mesespi]["tap"]     
    new_mesespi_tap = data["branch"][index_mesespi]["tap"] = data["branch"][index_mesespi]["tm_min"]
    
    build_psse_data(data)
    ierr, mesespi_tap = psspy.xfrdat(477, 478, "1 ", "RATIO")
    
    @test mesespi_tap != old_mesespi_tap
    @test isapprox(mesespi_tap, new_mesespi_tap, atol=1e-4)
end


@testset failfast = true "verificacion_taps_3W_approx" begin
    # off step turn ratio - T7EZ has 233 kV nominal voltage
    # it sets to 220 kV so PSSE force to 219 kV.
    psspy.read(0,"data/ver2526pid.raw")
    data = build_pm_data()
    merge_zi_connected_buses!(data)
    correct_pv_bus_type!(data)
    
    source2idx = Dict(brn["source_id"] => i for (i, brn) in data["branch"])
    
    # modify tap of 3W transformer T7EZ
    index_T7EZ = source2idx[["T3", 3000, 3110, 3702, "7 ", 2]]
    old_t7_tap = data["branch"][index_T7EZ]["tap"]     
    new_t7_tap = data["branch"][index_T7EZ]["tap"] = 1.0
    
    build_psse_data(data)
    ierr, t7_tap = psspy.wnddat(3110, 3702, 3000, "7 ", "RATIO")

    @test t7_tap != old_t7_tap
    @test t7_tap != new_t7_tap
    @test isapprox(t7_tap, 219/220, atol=1e-4)
end


@testset failfast = true "verificacion_control_con_zi" begin
    psspy.read(0,"data/ver2526pid.raw")
    data = build_pm_data()
    merge_zi_connected_buses!(data)
    correct_pv_bus_type!(data)
    
    source2idx = Dict(brn["source_id"] => i for (i, brn) in data["branch"])
    
    # En olavarria los controles van a barras por separado
    index_T1OL = source2idx[["T3", 2008, 2296, 2505, "1 ", 1]]
    index_T2OL = source2idx[["T3", 2008, 2298, 2506, "2 ", 1]]
    T1OL = data["branch"][index_T1OL]
    T2OL = data["branch"][index_T2OL]
    @test T1OL["control_bus"] == T2OL["control_bus"]
    
    # En campana los controles van a la misma barra
    index_T1CA = source2idx[["T3", 2002, 2292, 2804, "1 ", 1]]
    index_T2CA = source2idx[["T3", 2002, 2294, 2823, "2 ", 1]]
    T1CA = data["branch"][index_T1CA]
    T2CA = data["branch"][index_T2CA]
    @test T1CA["control_bus"] == T2CA["control_bus"]
end


@testset failfast=true "verificacion shunt" begin
    # a proposito se setea el shunt a -40 MVAR para verificar que el PSSE
    # lo redondea al valor nominal
    # esto sucede luego de correr el flujo con todo bloqueado
    psspy.read(0,"data/ver2526pid.raw")
    data = build_pm_data()
    merge_zi_connected_buses!(data)
    correct_pv_bus_type!(data)

    source2idx = Dict(sh["source_id"] => i for (i, sh) in data["shunt"])
    index_zn = source2idx[["SWS", 12]]
    shunt_zn = data["shunt"][index_zn]

    old_b = shunt_zn["bs"]
    new_b = shunt_zn["bs"] = -0.4

    build_psse_data(data)
    psspy.fnsl(options1=0, options5=0)
    ierr, binit = psspy.swsdt1(12, "BINIT")

    @test isapprox(binit, -50.0, atol=1e-4)
    @test old_b != new_b
end
