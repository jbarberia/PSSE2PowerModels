
@testset failfast=true "SADI invierno" begin
    # se lleva el SADI de horas resto a horas pico

    # caso de pico para obtener valores iniciales
    psspy.read(0,"data/inv25pi.raw")
    data_1 = build_pm_data()    
    merge_zi_connected_buses!(data_1)
    correct_pv_bus_type!(data_1)
    
    # llevo el caso de resto a pico - verifico su convergencia
    psspy.read(0,"data/inv25hr.raw")
    build_psse_data(data_1)    
    @testset "covergencia" begin    
        psspy.fnsl(
            options1=0,
            options2=0,
            options3=0,
            options4=0,
            options5=0,
            options6=0,
            options7=0,
            options8=0,
        )
        @test psspy.solved() == 0
    end

    psspy.save("foo.sav")

    # datos finales a comparar
    data_2 = build_pm_data()    
    merge_zi_connected_buses!(data_2)
    correct_pv_bus_type!(data_2)

    @testset "comparacion de casos" begin 
        for (i, bus) in data_1["bus"]
            parse(Int, i) > 1_000_000 && continue
            @show i          
            @test compare_dict(data_1["bus"][i], data_2["bus"][i], atol=1e-4)
        end        
        # @test compare_dict(data_1["gen"], data_1["gen"], atol=5e-3)
    end
end

