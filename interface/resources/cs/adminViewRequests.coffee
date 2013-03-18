$ ->
    modalTmplPre = """
        <div id="requestModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labeledby="requestModal" aria-hidden="true">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true"><i class="icon-remove"></i></button>
                <h3 class="text-{{textColor}}"><i class="icon-{{icon}}"></i> {{modalTitle}}?</h3>
            </div>
            <div class="modal-body">
            <p class="text-{{textColor}}">{{{text}}}</p>
            </div>
            <div class="modal-footer">
                <div class="btn-group">
                    <a class="btn" data-dismiss="modal" aria-hidden="true">Close</a>
                    <button class="btn btn-{{btnColor}}" type="submit" id="modalButton" data-loading-text="{{btnLoadingText}}"><i class="icon-{{icon}}"></i> {{btnText}}</button>
                </div>
            </div>
        </div>
    """


    modalTmpl = Handlebars.compile modalTmplPre


    makeModal = (data) ->
        $("#modal").html modalTmpl data
        $("#requestModal").modal()
        $("#requestModal").modal 'show'

        $("#requestModal").on 'shown', ->
            $("#modalButton").button()

            $("#modalButton").click ->
                $(this).button 'loading'

        ###
        Clear the HTML we threw into the page after the modal is gone,
        not sure if this is needed since the page probably will redirect
        to /admin/templates if I'm correct...
        ###
        $('#requestModal').on 'hidden', ->
            $("modal").html ""


    ###
    When the user presses the delete button, generate the modal, throw it into
    the page and hope for the best.
    ###
    $(".requestDeleteButton").click ->
        email = $(this).data "email"
        id = $(this).data "id"
        text = "You're about to delete a persons one chance at getting into the fla.gr system! Just kidding, go a head and delete them, but don't expect anymore lemons after this!"
        modalData =
            "btnText": "Delete"
            "modalTitle": "Delete request by `#{ email }`?"
            "btnColor": "danger"
            "textColor": "error"
            "text": text
            "icon": "trash"
            "btnLoadingText": "Deleting..."
        jsonVal = $.toJSON [id]
        $("#editFormInput").val jsonVal
        $("#editForm").attr 'action', '/admin/requests/delete'
        makeModal modalData
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
        modalData =
            "btnText": "Grant"
            "modalTitle": "Grant request by `#{ email }`?"
            "btnColor": "success"
            "textColor": "success"
            "text": text
            "icon": "ok"
            "btnLoadingText": "Granting..."
        jsonVal = $.toJSON [id]
        $("#editFormInput").val jsonVal
        $("#editForm").attr 'action', '/admin/requests/grant'
        makeModal modalData
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

        jsonVal = $.toJSON values
        $("#editFormInput").val jsonVal
        $("#editForm").attr 'action', '/admin/requests/delete'

        text = "You're about to delete all of these requests! Are you sure you want to take this oppertunity away from all of these poor souls?"
        modalData =
            "btnText": "Delete"
            "modalTitle": "Delete all of these?"
            "btnColor": "danger"
            "textColor": "error"
            "text": text
            "icon": "trash"
            "btnLoadingText": "Deleting..."
        makeModal modalData
        $("#modalButton").click ->
            $("#editForm").submit()


    $("#grantButton").click ->
        values = []
        for box in $(".bulkCheckbox:checked")
            values.push $(box).val()

        jsonVal = $.toJSON values
        $("#editFormInput").val jsonVal
        $("#editForm").attr 'action', '/admin/requests/grant'

        text = "You're about to grant all of these requests, which will send each and every person a specialized email for each one will be sent and they will all have an oppertunity to register for a closed trial account. Continue?"
        modalData =
            "btnText": "Grant"
            "modalTitle": "Grant all of these?"
            "btnColor": "success"
            "textColor": "success"
            "text": text
            "icon": "ok"
            "btnLoadingText": "Granting..."
        makeModal modalData
        $("#modalButton").click ->
            $("#editForm").submit()


    $("#newRequestButton").click ->
        text = """So you want to make a new request? Great! Please note that this person won't be notified until you grant the request however.<br><input id="emailInput" type="email" placeholder="email...">"""
        modalData =
            "btnText": "Create"
            "modalTitle": "Creating a new request..."
            "btnColor": "info"
            "textColor": "info"
            "text": text
            "icon": "ok"
            "btnLoadingText": "Creating..."
        $("#editForm").attr 'action', '/admin/requests/new'
        makeModal modalData

        $("#modalButton").click ->
            email = $("#emailInput").val()
            $("#editFormInput").val email
            $("#editForm").submit()
