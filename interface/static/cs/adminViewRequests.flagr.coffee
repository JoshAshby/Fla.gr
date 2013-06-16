$ ->
    ###
    When the user presses the delete button, generate the modal, throw it into
    the page and hope for the best.
    ###
    $(".requestDeleteButton").click ->
        email = $(this).data "email"
        id = $(this).data "id"
        text = "You're about to delete a persons one chance at getting into the fla.gr system! Just kidding, go a head and delete them, but don't expect anymore lemons after this!"
        title = "Delete request by `#{ email }`?"

        mod = new deleteModal title, text
        mod.make()
        editForm '/admin/requests/delete', [id]

        $("#modalButton").click ->
            $("#editForm").submit()


    ###
    When the user presses the grant button, generate the modal, throw it into
    the page and hope for the best. Just like deletes
    ###
    $(".requestGrantButton").click ->
        email = $(this).data "email"
        id = $(this).data "id"
        text = "Congrats! You're granting one persons dream of getting to use fla.gr while it's still closed! Good for you, you deserve more lemons!"
        title = "Grant request by `#{ email }`?"

        mod = new grantModal title, text
        mod.make()
        editForm '/admin/requests/grant', [id]

        $("#modalButton").click ->
            $("#editForm").submit()


    $("#deleteButton").click ->
        values = []
        for box in $(".bulkCheckbox:checked")
            values.push $(box).val()

        text = "You're about to delete all of these requests! Are you sure you want to take this oppertunity away from all of these poor souls?"
        title = "Delete all of these?"

        mod = new deleteModal title, text
        mod.make()
        editForm '/admin/requests/delete', values

        $("#modalButton").click ->
            $("#editForm").submit()


    $("#grantButton").click ->
        values = []
        for box in $(".bulkCheckbox:checked")
            values.push $(box).val()

        text = "You're about to grant all of these requests, which will send each and every person a specialized email for each one will be sent and they will all have an oppertunity to register for a closed trial account. Continue?"
        title = "Grant all of these?"

        mod = new grantModal title, text
        mod.make()
        editForm '/admin/requests/grant', values

        $("#modalButton").click ->
            $("#editForm").submit()