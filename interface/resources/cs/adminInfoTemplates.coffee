$ ->
    modalTmplPre = """
        <div id="tmplDeleteModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labeledby="tmplDeleteModal" aria-hidden="true">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true"><i class="icon-remove"></i></button>
                <h3 class="text-error"><i class="icon-trash"></i> Delete `{{title}}`?</h3>
            </div>
            <div class="modal-body">
                <p class="text-error">You're about to delete the template `{{title}}`</p>
                <p class="text-error">Are you sure you want to do this? The template will be gone forever if you delete it, and anything which uses it will break. You could be responsible for a fire if you do this.</p>
            </div>
            <div class="modal-footer">
                <form action="/admin/templates/{{id}}/delete" method="POST">
                    <div class="btn-group">
                        <a class="btn" data-dismiss="modal" aria-hidden="true">Close</a>
                        <button class="btn btn-danger" type="submit" id="deleteButton" data-loading-text="Deleting..."><i class="icon-trash"></i> Delete</button>
                    </div>
                </form>
            </div>
        </div>
    """

    modalTmpl = Handlebars.compile modalTmplPre

    ###
    Activate the tabs
    ###
    $('#tmplInfoTabs a').click (e) ->
        e.preventDefault()
        $(this).tab 'show'

    ###
    When the user presses the delete button, generate the modal, throw it into
    the page and hope for the best.
    ###
    $("#tmplDeleteButton").click ->
        title = $(this).data "title"
        id = $(this).data "id"
        $("#modal").html modalTmpl {"title": title, "id": id}
        $("#tmplDeleteModal").modal()
        $("#tmplDeleteModal").modal 'show'

        $("#tmplDeleteModal").on 'shown', ->
            $("#deleteButton").button()

            $("#deleteButton").click ->
                $(this).button 'loading'

        ###
        Clear the HTML we threw into the page after the modal is gone,
        not sure if this is needed since the page probably will redirect
        to /admin/templates if I'm correct...
        ###
        $('#tmplDeleteModal').on 'hidden', ->
            $("modal").html ""
