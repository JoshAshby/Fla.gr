modalTmplPre = """
    <div id="requestModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labeledby="requestModal" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true"><i class="icon-remove"></i></button>
            <h3 class="text-{{textColor}}"><i class="icon-{{icon}}"></i> {{modalTitle}}</h3>
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
    ###
    $('#requestModal').on 'hidden', ->
        $("modal").html ""

@modalDelete = (title, text) ->
    modalData =
        "btnText": "Delete"
        "ModalTitle": title
        "btnColor": "danger"
        "textColor": "error"
        "text": text
        "icon": "trash"
        "btnLoadingText": "Deleting..."
    makeModal modalData


@modalEdit = (title, text) ->
    modalData =
        "btnText": "Edit"
        "modalTitle": title
        "btnColor": "primary"
        "textColor": ""
        "text": text
        "icon": "edit"
        "btnLoadingText": "Updating..."
    makeModal modalData


@modalGrant = (title, text) ->
    modalData =
        "btnText": "Grant"
        "modalTitle": title
        "btnColor": "success"
        "textColor": "success"
        "text": text
        "icon": "ok"
        "btnLoadingText": "Granting..."
    makeModal modalData


@modalNew = (title, text) ->
    modalData =
        "btnText": "Create"
        "modalTitle": title
        "btnColor": "info"
        "textColor": "info"
        "text": text
        "icon": "ok"
        "btnLoadingText": "Creating..."
    makeModal modalData


@editForm = (action, value) ->
    jsonVal = $.toJSON value
    $("#editFormInput").val jsonVal
    $("#editForm").attr 'action', action


