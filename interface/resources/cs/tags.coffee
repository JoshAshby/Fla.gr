$ ->
    tags = []
    ###
    The hidden tag may have tags preloaded, so we need to make sure
    those tags get into the array and the div list
    ###
    base = $("#tags_hidden").val().split ", "
    for tag in base
        tags.push tag
        $("#tag_list").append ("""
    <span class="label">
        <a href="#tag_link">""" + tag + """</a>
    </span>""")

    ###
    When the add button is clicked then add the tags to the
    div list, the array and the hidden value, before finally
    clearing the field
    ###
    $("#add_tag_btn").click ->
        input = $("#tag_input").val()
        if input isnt ""
            tags_string = ""
            tags_string += (tag + ", ") for tag in tags
            tags_input_break = input.split ", "
            for tag in tags_input_break
                tags.push tag
                $("#tag_list").append ("""
            <span class="label">
                <a href="#tag_link">""" + tag + """</a>
            </span>""")
                tags_string += (tag + ", ")
            tags_string = tags_string.substring 0, (tags_string.length - 2)
            $("#tags").val tags_string
            $("#tag_input").val ""

    ###
    Bind the click even to all labels
    When a click happens then remove that element
    from both the DOM and the array of tags and the hidden input
    ###
    $(document).on "click", "span.label>a", ->
        $(this).parent().remove()
        tags.splice tags.indexOf($(this).text()), 1
        tags_string = ""
        tags_string += (tag + ", ") for tag in tags
        $("#tags").val tags_string
