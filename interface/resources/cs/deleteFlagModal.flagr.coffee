$ ->
    modalTmplPre = """
        <div id="flagDeleteModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labeledby="flagDeleteModal" aria-hidden="true">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true"><i class="icon-remove"></i></button>
                <h3 class="text-error"><i class="icon-trash"></i> Delete `{{title}}`?</h3>
            </div>
            <div class="modal-body">
                <p class="text-error">You're about to delete your flag `{{title}}`</p>
                <p class="text-error">Are you sure you want to do this? The flag will be gone forever if you delete it</p>
            </div>
            <div class="modal-footer">
                <form action="/flags/{{id}}/delete" method="POST">
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
    When a delete button is pressed, grab the id and title of the flag
    from the data-id and data-title attributes of the button, then use
    the compiled Handlebars template from above to generate the modal
    and finally put it into the page and display it
    ###
    $(".flagDeleteButton").click ->
        title = $(this).data "title"
        id = $(this).data "id"
        $("#modal").html modalTmpl {"title": title, "id": id}
        $("#flagDeleteModal").modal()
        $("#flagDeleteModal").modal 'show'

        $("#flagDeleteModal").on 'shown', ->
            $("#deleteButton").button()

            $("#deleteButton").click ->
                $(this).button 'loading'

        ###
        Clear the HTML we threw into the page after the modal is gone,
        not sure if this is needed since the page probably will redirect
        to /your/flags if I'm correct...
        ###
        $('#flagDeleteModal').on 'hidden', ->
            $("modal").html ""
