



################################################################################
mutable struct Bus
    number
    name
    v_mag
    v_ang
    p_balance
    q_balance
end

################################################################################
abstract type Branch end

struct ACBranch <: Branch
    ibus
    jbus
    ckt
    p_from
    q_from
    p_to
    q_to
end

struct ZeroImpedanceLine <: Branch
    ibus
    jbus
    ckt
end

################################################################################
struct Generator
    ibus
    id
    p_gen
    q_gen
end


################################################################################
struct Load
    ibus
    id
end

################################################################################
struct SwitchedShunt
    ibus
    b
end


################################################################################
struct Network
    model::JuMP.Model
    buses::Array{Bus}
    generators::Array{Generator}
    loads::Array{Load}
    branches::Array{Branch}
    switched_shunts::Array{SwitchedShunt}
    bus2idx::Dict{Int32, Int32}
    gen2idx::Dict{Any, Any}
    load2idx::Dict{Any, Any}
end

function Network()
    Network(
        JuMP.Model(),
        Bus[],
        Generator[],
        Load[],
        ACBranch[],
        SwitchedShunt[],
        Dict{Int32, Int32}(),
        Dict{Any, Int32}(),
        Dict{Any, Int32}()
    )
end

################################################################################
function add_bus!(net::Network, number)    
    ierr, name = psspy.notona(number)
    
    ierr, v_mag_act = psspy.busdat(number, "PU")
    ierr, v_ang_act = psspy.busdat(number, "ANGLE")
    
    v_mag = @variable(net.model, base_name="v_mag", start=v_mag_act, upper_bound=1.5, lower_bound=0.5)
    v_ang = @variable(net.model, base_name="v_mag", start=v_ang_act)
    
    p_balance = 0#@expression(net.model, 0)
    q_balance = 0#@expression(net.model, 0)

    bus = Bus(number, name, v_mag, v_ang, p_balance, q_balance)
    push!(net.buses, bus)
    
    net.bus2idx[number] = length(net.buses)
end

function get_bus(net::Network, number)
    net.buses[net.bus2idx[number]]
end

################################################################################
function add_branch!(net, ibus, jbus, kbus, ickt)
    if kbus == 0
        add_branch!(net, ibus, jbus, ickt)
    else
        # TODO escribir para tres arrollamientos
    end
end

function add_branch!(net::Network, ibus, jbus, ickt)
    ierr, rx = psspy.brndt2(ibus, jbus, ickt, "RX")
    zero_impedance = abs(imag(rx)) < 0.0001

    if zero_impedance
        _add_branch_zi!(net, ibus, jbus, ickt)
    else
        _add_branch_ac!(net, ibus, jbus, ickt)
    end

end


function _add_branch_ac!(net::Network, ibus, jbus, ickt)
    ierr, char = psspy.brndat(ibus, jbus, ickt, "CHARG")
    ierr, rx = psspy.brndt2(ibus, jbus, ickt, "RX")

    # Taps de trafos de dos arrollamientos
    ierr, ti = psspy.xfrdat(ibus, jbus, ickt, "RATIO")    
    ierr, tj = psspy.xfrdat(ibus, jbus, ickt, "RATIO2")
    ierr, tapped = psspy.xfrint(ibus, jbus, ickt, "TAPPED")
    if ierr != 3
        if ibus == tapped
            ti, tj = ti, tj
        else
            ti, tj = tj, ti # permuto por estar en el otro arrollamiento
        end
    else
        ti = tj = 1
    end

    # Parametros serie
    r = real(rx)
    x = imag(rx)
    
    g = real(1/rx)
    b = imag(1/rx)

    # Parametros derivacion
    ierr, yi = psspy.brndt2(ibus, jbus, ickt, "ISHNT")
    gi = real(yi)
    bi = imag(yi)
    
    ierr, yj = psspy.brndt2(ibus, jbus, ickt, "JSHNT")
    gj = real(yj)
    bj = imag(yj)
    
    # Variables
    vi_mag = get_bus(net, ibus).v_mag
    vj_mag = get_bus(net, jbus).v_mag
    
    vi_ang = get_bus(net, ibus).v_ang
    vj_ang = get_bus(net, jbus).v_ang
    dw = vi_ang - vj_ang

    p_from = @expression(net.model,           (g + gi) * (vi_mag / ti)^2 - vi_mag * vj_mag / ti / tj * (g * cos( dw) + b * sin( dw)))
    q_from = @expression(net.model, -(b + bi + char/2) * (vi_mag / ti)^2 - vi_mag * vj_mag / ti / tj * (g * sin( dw) - b * cos( dw)))
    p_to   = @expression(net.model,           (g + gj) * (vj_mag / tj)^2 - vi_mag * vj_mag / ti / tj * (g * cos(-dw) + b * sin(-dw)))
    q_to   = @expression(net.model, -(b + bj + char/2) * (vj_mag / tj)^2 - vi_mag * vj_mag / ti / tj * (g * sin(-dw) - b * cos(-dw)))

    get_bus(net, ibus).p_balance -= p_from
    get_bus(net, ibus).q_balance -= q_from
    get_bus(net, jbus).p_balance -= p_to
    get_bus(net, jbus).q_balance -= q_to

    branch = ACBranch(
        ibus,
        jbus,
        ickt,
        p_from,
        q_from,
        p_to,
        q_to
    )
    push!(net.branches, branch)
end


function _add_branch_zi!(net::Network, ibus, jbus, ickt)
    bus_i = get_bus(net, ibus)
    bus_j = get_bus(net, jbus)

    @constraint(net.model, bus_i.v_mag == bus_j.v_mag)
    @constraint(net.model, bus_i.v_ang == bus_j.v_ang)

    # Variables auxiliares para pasar potencia de una barra a otra para cumplir
    # con balance de potencia en ambas.
    p = @variable(net.model)
    q = @variable(net.model)

    get_bus(net, ibus).p_balance -= p
    get_bus(net, ibus).q_balance -= q
    get_bus(net, jbus).p_balance += p
    get_bus(net, jbus).q_balance += q

    branch = ZeroImpedanceLine(
        ibus,
        jbus,
        ickt
    )
    push!(net.branches, branch)
end




################################################################################
function add_generator!(net::Network, ibus, id)
    ierr, p_gen_act = psspy.macdat(ibus, id, "P")
    ierr, q_gen_act = psspy.macdat(ibus, id, "Q")
    ierr, q_min = psspy.macdat(ibus, id, "QMIN")
    ierr, q_max = psspy.macdat(ibus, id, "QMAX")

    p_gen_act /= psspy.sysmva()
    q_gen_act /= psspy.sysmva()
    q_min /= psspy.sysmva()
    q_max /= psspy.sysmva()

    pg = @variable(net.model, base_name="pg", start=p_gen_act)
    qg = @variable(net.model, base_name="qg", start=q_gen_act, upper_bound=q_max, lower_bound=q_min)

    get_bus(net, ibus).p_balance += pg
    get_bus(net, ibus).q_balance += qg

    gen = Generator(
        ibus,
        id,
        pg,
        qg
    )
    push!(net.generators, gen)

    net.gen2idx[(ibus, id)] = length(net.generators) 
end

function get_generator(net, ibus, id)
    return net.generators[net.gen2idx[(ibus, id)]]
end


################################################################################
function add_load!(net::Network, ibus, id)
    ierr, s = psspy.loddt2(ibus, id, "MVA", "ACT")
    p = real(s) / psspy.sysmva()
    q = imag(s) / psspy.sysmva()
    
    get_bus(net, ibus).p_balance -= p
    get_bus(net, ibus).q_balance -= q

    load = Load(
        ibus,
        id,
    )
    push!(net.loads, load)
    net.load2idx[(ibus, id)] = length(net.generators) 
end

function get_load(net, ibus, id)
    return net.loads[net.load2idx[(ibus, id)]]
end

################################################################################
function add_shunt!(net::Network, ibus)
    ierr, binit = swsdt1(ibus, "BINIT")
    binit /= psspy.sysmva()
    
    b = @variable(net.model,  base_name="b", start=binit)

    bus = get_bus(net, ibus)
    get_bus(net, ibus).q_balance += b * bus.v_mag^2
    
    shunt = SwitchedShunt(ibus, b)
    push!(net.switched_shunts, shunt)
end


