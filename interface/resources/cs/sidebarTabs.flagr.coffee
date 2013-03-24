$ ->
    ###
    Activate the tabs
    ###
    $('#sidebarTabs a').click (e) ->
        e.preventDefault()
        $(this).tab 'show'
    $("#sidebarTabs a.btn").click (e) ->
        e.preventDefault()
