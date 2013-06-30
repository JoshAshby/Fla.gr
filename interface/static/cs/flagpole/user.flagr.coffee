$ ->
    $("#userToggleButton").click ->
        form = $(this).parents("form")
        input = form.find('input[name="disable"]')

        if input.val is "False"
            action = "disable"
            val = "true"
        else
            action = "enable"
            val = "false"

        title = "Are you sure?"
        text = "You are about to #{ action } this user. Are you sure you want to do this?"

        callback = () ->
            input.val val
            form.submit()

        mod = new toggleModal title, text, callback
        mod.make()
