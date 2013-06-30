modalTmplPre = """
    <div id="flagrModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labeledby="flagrModal" aria-hidden="true">
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
                <button class="btn btn-{{btnColor}}" id="modalButton" data-loading-text="{{btnLoadingText}}"><i class="icon-{{icon}}"></i> {{btnText}}</button>
            </div>
        </div>
    </div>
"""

modalTmpl = Handlebars.compile modalTmplPre


class modalBase
    ###
    Base modal object class

    Takes a title and a modal body text

    methods:
        make(data)
            places the modal into the div #modal
            data is an object with keys
                "btnText": ""
                "btnColor": ""
                "textColor": ""
                "icon": ""
                "btnLoadingText": ""

    ###
    constructor: (@title, @text, @callback) ->

    make: (data) ->
        data["text"] = @text
        data["modalTitle"] = @title
        $("#modal").html modalTmpl data
        $("#requestModal").modal()
        $("#requestModal").modal 'show'

        $("#requestModal").on 'shown', ->
            $("#modalButton").button()

            $("#modalButton").on 'click', ->
                $(this).button 'loading'
                @callback()

        ###
        Clear the HTML we threw into the page after the modal is gone,
        not sure if this is needed since the page probably will redirect
        ###
        $('#requestModal').on 'hidden', ->
            $("modal").html ''
            $("#modalButton").off 'click'


class @deleteModal extends modalBase
    make: ->
        modalData =
            "btnText": "Delete"
            "btnColor": "danger"
            "textColor": "error"
            "icon": "trash"
            "btnLoadingText": "Deleting..."
        super modalData


class @editModal extends modalBase
    make: ->
        modalData =
            "btnText": "Edit"
            "btnColor": "primary"
            "textColor": ""
            "icon": "edit"
            "btnLoadingText": "Updating..."
        super modalData


class @grantModal extends modalBase
    make: ->
        modalData =
            "btnText": "Grant"
            "btnColor": "success"
            "textColor": "success"
            "icon": "ok"
            "btnLoadingText": "Granting..."
        super modalData


class @createModal extends modalBase
    make: ->
        modalData =
            "btnText": "Create"
            "btnColor": "info"
            "textColor": "info"
            "icon": "ok"
            "btnLoadingText": "Creating..."
        super modalData
