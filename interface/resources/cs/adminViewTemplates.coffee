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


    $("#deleteButton").click ->
        values = []
        for box in $(".bulkCheckbox:checked")
            values.push $(box).val()

        jsonVal = $.toJSON values
        $("#editFormInput").val jsonVal
        $("#editForm").attr 'action', '/admin/templates/delete'

        text = "You're about to delete all of these templates! Are you sure you want to take the chance of setting fire to all of fla.gr by deleting possibly used templates?"
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


    $("#bulkCheckButton").click ->
        if $("#bulkCheckButton").hasClass 'active'
            $(".bulkCheckbox").prop 'checked', false
        else
            $(".bulkCheckbox").prop 'checked', true


    ###
    Activate the tabs
    ###
    $('#sidebarTabs a').click (e) ->
        e.preventDefault()
        $(this).tab 'show'
