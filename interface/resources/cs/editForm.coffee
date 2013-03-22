@editForm = (action, value) ->
    jsonVal = $.toJSON value
    $("#editFormInput").val jsonVal
    $("#editForm").attr 'action', action
