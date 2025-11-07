"tests if two dicts are equal, up to floating point precision"
function compare_dict(d1, d2; atol=1e-4)
    for (k1,v1) in d1
        if !haskey(d2, k1)
            return false
        end
        v2 = d2[k1]

        if isa(v1, Number)
            if !_compare_numbers(v1, v2, atol)
                return false
            end
        elseif isa(v1, Array)
            if length(v1) != length(v2)
                return false
            end
            for i in 1:length(v1)
                if isa(v1[i], Number)
                    if !_compare_numbers(v1[i], v2[i], atol)
                        return false
                    end
                else
                    if v1[i] != v2[i]
                        return false
                    end
                end
            end
        elseif isa(v1, Dict)
            if !compare_dict(v1, v2; atol=atol)
                return false
            end
        else
            if !isapprox(v1, v2; atol=atol)
                return false
            end
        end
    end
    return true
end


"tests if two numbers are equal, up to floating point precision"
function _compare_numbers(v1, v2, atol=1e-4)
    if isnan(v1)
        #println("1.1")
        if !isnan(v2)
            #println(v1, " ", v2)
            return false
        end
    else
        #println("1.2")
        if !isapprox(v1, v2; atol=atol)
            println(v1, " ", v2, " ", atol)
            return false
        end
    end
    return true
end
