
function merge_zi_connected_buses!(data; threshold=0.0001)
    bus_sets = Dict{Int,Set{Int}}()

    for (i, branch) in data["branch"]
        branch["br_status"] == 0 && continue
        branch["source_id"][1] != "LII" && continue
        abs(branch["br_x"]) > threshold && continue
        abs(branch["b_fr"]) != 0.0 && continue
        abs(branch["b_to"]) != 0.0 && continue
        
        f_bus, t_bus = branch["f_bus"]::Int, branch["t_bus"]::Int
        if !haskey(bus_sets, f_bus)
            bus_sets[f_bus] = Set{Int}(f_bus)
        end
        if !haskey(bus_sets, t_bus)
            bus_sets[t_bus] = Set{Int}(t_bus)
        end
        merged_set = union(bus_sets[f_bus], bus_sets[t_bus])
        for bus in merged_set
            bus_sets[bus] = merged_set
        end    
    end

    bus_id_map = Dict{Int,Int}()
    for bus_set in Set(values(bus_sets))
        bus_min = minimum(bus_set)
        @info("merged zero impedance connected buses $(join(bus_set, ",")) in to bus $(bus_min)")

        bus_type = maximum(data["bus"]["$i"]["bus_type"] for i in bus_set)
        # There should not be any inactive buses at this point.
        @assert 1 <= bus_type <= 3

        for i in bus_set
            data["bus"]["$i"]["bus_type"] = bus_type
            if i != bus_min
                bus_id_map[i] = bus_min
            end
        end
    end

    update_bus_ids!(data, bus_id_map, injective=false)
    
    for (equiv_bus, retained_bus) in bus_id_map
        data["bus"][string(retained_bus)]["source_id"][1] = "GROUPEDBUS" 
        data["bus"][string(retained_bus)]["source_id"][2] = retained_bus        
        push!(data["bus"][string(retained_bus)]["source_id"], equiv_bus)
    end
    
    for (i, branch) in data["branch"]
        if branch["f_bus"] == branch["t_bus"]
            @info("zero impedance connection of branch $(i) - $(branch["source_id"]) has same from and to buses: $(branch["f_bus"]), deactivating branch")
            branch[pm_component_status["branch"]] = pm_component_status_inactive["branch"]
        end
    end
    
    for (i, dcline) in data["dcline"]
        if dcline["f_bus"] == dcline["t_bus"]
            @info("zero impedance connection of dcline $(i) - $(branch["source_id"]) has same from and to buses: $(dcline["f_bus"]), deactivating dcline")
            branch[pm_component_status["dcline"]] = pm_component_status_inactive["dcline"]
        end
    end

    correct_branch_directions!(data)
end


function correct_pv_bus_type!(data)    
    # map buses -> generators
    bus_gens = Dict{Int, Vector{String}}()
    bus_gens_status = Dict{Int, Vector{Int}}()

    for (i, bus) in data["bus"]
        bus_gens[bus["index"]] = Int[]
        bus_gens_status[bus["index"]] = Int[]
    end

    for (i, gen) in data["gen"]
        bus_id = gen["gen_bus"]
        gen_status = gen["gen_status"]

        push!(bus_gens[bus_id], i)
        push!(bus_gens_status[bus_id], gen_status)
    end

    # correct bus codes
    for (bus_i, machine_statuses) in bus_gens_status
        bus_key = string(bus_i)
        !haskey(data["bus"], bus_key) && continue
        
            
        bus = data["bus"][bus_key]
        all_oos = isempty(machine_statuses) || sum(machine_statuses) == 0
        
        # PV Buses without Generators
        if all_oos && bus["bus_type"] == 2
            data["bus"][bus_key]["bus_type"] = 1
            @info "setting bus $bus_i from type 2 to type 1 - No generators connected"
        end
        
        # Generators in PQ Buses
        if !all_oos && bus["bus_type"] == 1
            if haskey(bus_gens, bus_i)
                for gen_i in bus_gens[bus_i]        
                    data["gen"][gen_i]["gen_status"] = 0
                    @info "setting gen $gen_i out of service, it is connected to type 1 bus"
                end
            end
        end
    end
end
