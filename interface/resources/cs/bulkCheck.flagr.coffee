$ ->
    $("#bulkCheckButton").click ->
        if $("#bulkCheckButton").hasClass 'active'
            $(".bulkCheckbox").prop 'checked', false
        else
            $(".bulkCheckbox").prop 'checked', true
