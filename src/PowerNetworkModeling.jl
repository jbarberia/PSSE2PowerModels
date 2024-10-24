module PowerNetworkModeling
    using JuMP

    using PyCall
    const psspy = PyNULL()
    function __init__()
        pyimport("psse34")
        copy!(psspy, pyimport("psspy"))
        psspy.psseinit()
    end
    
    # Write your package code here.

    include("struct.jl")
    include("parser.jl")

    export psspy

end
