$ ->
    ###
    When the user presses the delete button, generate the modal, throw it into
    the page and hope for the best.
    ###
    $("#tmplDeleteButton").click ->
        tmplTitle = $(this).data "title"
        id = $(this).data "id"
        text = "Are you sure you want to delete this template? It could be used by other systems within fla.gr and cause things to break..."
        title = "Delete `#{ tmplTitle  }`?"

        mod = new deleteModal title, text
        mod.make()
        editForm "/admin/templates/delete/#{ id  }", []

        $("#modalButton").click ->
            $("#editForm").submit()