$ ->
    deleteModalTmplPre = """
        <div id="requestDeleteModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labeledby="tmplDeleteModal" aria-hidden="true">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true"><i class="icon-remove"></i></button>
                <h3 class="text-error"><i class="icon-trash"></i> Delete request by `{{email}}`?</h3>
            </div>
            <div class="modal-body">
                <p class="text-error">You're about to delete this invite request?</p>
                <p class="text-error">Are you sure you want to do this? Do you really want to crush their soul? Are you really that horrible? Maybe I should take away your lemons...</p>
            </div>
            <div class="modal-footer">
                <form action="/admin/requests/{{id}}/delete" method="POST">
                    <div class="btn-group">
                        <a class="btn" data-dismiss="modal" aria-hidden="true">Close</a>
                        <button class="btn btn-danger" type="submit" id="deleteButton" data-loading-text="Deleting..."><i class="icon-trash"></i> Delete</button>
                    </div>
                </form>
            </div>
        </div>
    """
    grantModalTmplPre = """
        <div id="requestGrantModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labeledby="tmplDeleteModal" aria-hidden="true">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true"><i class="icon-remove"></i></button>
                <h3 class="text-success"><i class="icon-trash"></i> Grant request by `{{email}}`?</h3>
            </div>
            <div class="modal-body">
                <p class="text-success">Yay! You're granting someones invite request and letting them have a stab at fla.gr and using it! Good for you, you deserve more lemons.</p>
            </div>
            <div class="modal-footer">
                <form action="/admin/requests/{{id}}/edit" method="POST">
                    <div class="btn-group">
                        <a class="btn" data-dismiss="modal" aria-hidden="true">Close</a>
                        <button class="btn btn-success" type="submit" id="grantButton" data-loading-text="Granting..."><i class="icon-ok"></i> Grant</button>
                    </div>
                    <input type="hidden" value="grant" name="grant">
                </form>
            </div>
        </div>
    """

    deleteModalTmpl = Handlebars.compile deleteModalTmplPre
    grantModalTmpl = Handlebars.compile grantModalTmplPre


    ###
    Theres probably a much much better and DRY way to do this, but heres a quick
    hack instead...
    ###

    ###
    When the user presses the delete button, generate the modal, throw it into
    the page and hope for the best.
    ###
    $(".requestDeleteButton").click ->
        email = $(this).data "email"
        id = $(this).data "id"
        $("#modal").html deleteModalTmpl {"email": email, "id": id}
        $("#requestDeleteModal").modal()
        $("#requestDeleteModal").modal 'show'

        $("#requestDeleteModal").on 'shown', ->
            $("#deleteButton").button()

            $("#deleteButton").click ->
                $(this).button 'loading'

        ###
        Clear the HTML we threw into the page after the modal is gone,
        not sure if this is needed since the page probably will redirect
        to /admin/templates if I'm correct...
        ###
        $('#requestDeleteModal').on 'hidden', ->
            $("modal").html ""

    ###
    When the user presses the grant button, generate the modal, throw it into
    the page and hope for the best. Just like deletes
    ###
    $(".requestGrantButton").click ->
        email = $(this).data "email"
        id = $(this).data "id"
        $("#modal").html grantModalTmpl {"email": email, "id": id}
        $("#requestGrantModal").modal()
        $("#requestGrantModal").modal 'show'

        $("#requestGrantModal").on 'shown', ->
            $("#grantButton").button()

            $("#grantButton").click ->
                $(this).button 'loading'

        ###
        Clear the HTML we threw into the page after the modal is gone,
        not sure if this is needed since the page probably will redirect
        to /admin/templates if I'm correct...
        ###
        $('#requestGrantModal').on 'hidden', ->
            $("modal").html ""
