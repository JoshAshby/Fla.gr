$ ->
    $("#deleteButton").click ->
        values = []
        for box in $(".bulkCheckbox:checked")
            values.push $(box).val()

        text = "You're about to delete all of these templates! Are you sure you want to take the chance of setting fire to all of fla.gr by deleting possibly used templates?"

        modalDelete "Delete all of these?", text
        editForm '/admin/templates/delete', values

        $("#modalButton").click ->
            $("#editForm").submit()
