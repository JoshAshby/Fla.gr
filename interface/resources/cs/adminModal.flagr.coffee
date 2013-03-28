###
Provides a basic interface for making a general modal dynamically, using Handlebars.js
and jQuery.
###
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
    constructor: (@title, @text) ->
        ###
        :param title: The title for the modal
        :param text: The text which will be included in the modals body
        ###

    make: (data) ->
        ###
        Please note all `*Color` properties should not include the prefix  
            eg: For a red button do `danger` and not `btn-danger`  
  
        If your @text which you passed in into the constructor has {{}} such as defined by
        the mustache templating language, you can also pass those properties with `data`  
  
        :param data: An object containing the pieces
            * btnText - The text which should be included on the action button of the modal
            * btnColor - The bootstrap button color name to use for the action button
            * textColor - The bootstrap text color name to use of the modal's text
            * icon - The fontawesome icon name, without the `icon-` prefix
            * btnLoadingText - The text to display once the action button has been clicked
        ###
        data["text"] = @text
        data["modalTitle"] = @title
        $("#modal").html modalTmpl data
        $("#requestModal").modal()
        $("#requestModal").modal 'show'

        $("#requestModal").on 'shown', ->
            $("#modalButton").button()

            $("#modalButton").click ->
                $(this).button 'loading'

        #In case they close it without taking action, remove the HTML from the
        #div.
        $('#requestModal').on 'hidden', ->
            $("modal").html ""


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
