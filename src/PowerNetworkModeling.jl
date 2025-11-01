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
    #include("parser.jl")

    export psspy
    export build_pm_data

end
