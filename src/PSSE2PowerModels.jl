module PSSE2PowerModels
    using PowerModels
    using PyCall

    const psspy = PyNULL()
    function __init__()
        Sys.WORD_SIZE == 32 && pyimport("psse34")
        Sys.WORD_SIZE == 64 && pyimport("psse3606")
        copy!(psspy, pyimport("psspy"))        
    end
    
    include("to_powermodels.jl")
    include("to_psse.jl")
    include("pm_nw_procesor.jl")

    export psspy
    export build_pm_data
    export build_psse_data

    export merge_zi_connected_buses!
    export correct_pv_bus_type!

end
