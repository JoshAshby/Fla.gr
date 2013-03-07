$ ->
    labels = []
    labelsTemplate = """ <span class="label">{{label}}</span> """
    labelsCompiledTemplate = Handlebars.compile labelsTemplate
    ###
    The hidden label may have labels preloaded, so we need to make sure
    those labels get into the array and the div list
    ###
    base = $("#labels").val() or ""
    if base isnt ""
        base = $("#labels").split ","
        for label in base
            labels.push label
            $("#dynamicLabels").append labelsCompiledTemplate {"label": label}

    ###
    Refresh the labels array and adding anything in the
    input box to the span
    ###
    refreshLabels = ->
        input = $("#labelInput").val()
        if input isnt ""
            labels_string = ""
            labels_string += (label + ", ") for label in labels
            labels_input_break = input.replace /\s+/g, ''
            labels_input_break = labels_input_break.split ","
            for label in labels_input_break
                labels.push label

                $("#dynamicLabels").append labelsCompiledTemplate {"label": label}
                labels_string += (label + ",")
            labels_string = labels_string.substring 0, (labels_string.length - 2)
            $("#labels").val labels_string
            $("#labelInput").val ""


    ###
    When the add button is clicked then add the labels to the
    div list, the array and the hidden value, before finally
    clearing the field
    ###
    $("#addLabels").click ->
        refreshLabels()

    ###
    Prevent the form from submitting if the enter key is pressed
    Instead, add the tags that are in the input
    ###
    $("#labelInput").keypress (event) =>
        if event.which is 13
            event.preventDefault()
            refreshLabels()

    ###
    Bind the click even to all labels
    When a click happens then remove that element
    from both the DOM and the array of labels and the hidden input
    ###
    $(document).on "click", "#dynamicLabels>span.label", ->
        labels.splice labels.indexOf($(this).text()), 1
        labels_string = ""
        labels_string += (label + ", ") for label in labels
        $("#labels").val labels_string
        $(this).remove()
