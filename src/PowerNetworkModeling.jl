module PowerNetworkModeling
    using PowerModels
    using PyCall
    using Graphs

    const psspy = PyNULL()
    function __init__()
        pyimport("psse34")
        copy!(psspy, pyimport("psspy"))
        psspy.psseinit()
    end
    
    include("to_powermodels.jl")
    include("pm_nw_procesor.jl")
    #include("parser.jl")

    export psspy
    export build_pm_data

    export merge_zi_connected_buses!
    export correct_pv_bus_type!

end
