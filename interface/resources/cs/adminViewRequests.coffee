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

        console.log title

        modalDelete title, text
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

        modalGrant title, text
        editForm '/admin/requests/grant', [id]

        $("#modalButton").click ->
            $("#editForm").submit()


    $("#bulkCheckButton").click ->
        if $("#bulkCheckButton").hasClass 'active'
            $(".bulkCheckbox").prop 'checked', false
        else
            $(".bulkCheckbox").prop 'checked', true


    $("#deleteButton").click ->
        values = []
        for box in $(".bulkCheckbox:checked")
            values.push $(box).val()

        text = "You're about to delete all of these requests! Are you sure you want to take this oppertunity away from all of these poor souls?"
        title = "Delete all of these?"

        modalDelete title, text
        editForm '/admin/requests/delete', values

        $("#modalButton").click ->
            $("#editForm").submit()


    $("#grantButton").click ->
        values = []
        for box in $(".bulkCheckbox:checked")
            values.push $(box).val()

        text = "You're about to grant all of these requests, which will send each and every person a specialized email for each one will be sent and they will all have an oppertunity to register for a closed trial account. Continue?"
        title = "Grant all of these?"

        modalGrant title, text
        editForm '/admin/requests/grant', values

        $("#modalButton").click ->
            $("#editForm").submit()


    $("#newRequestButton").click ->
        text = """So you want to make a new request? Great! Please note that this person won't be notified until you grant the request however.<br><input id="emailInput" type="email" placeholder="email...">"""
        title = "Creating a new request..."

        modalNew title, text
        editForm '/admin/requests/new', []

        $("#modalButton").click ->
            email = $("#emailInput").val()
            $("#editFormInput").val email
            $("#editForm").submit()
