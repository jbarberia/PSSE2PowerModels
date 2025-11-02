
function merge_zi_connected_buses!(data; threshold=0.0001)
    bus_sets = Dict{Int,Set{Int}}()

    for (i, branch) in data["branch"]
        branch["br_status"] == 0 && continue
        abs(branch["br_x"]) > threshold && continue
        
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
