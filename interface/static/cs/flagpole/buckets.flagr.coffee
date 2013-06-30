$ ->
    $(".bucketToggleButton").click ->
        elem = $(this)
        bucket = elem.parent("tr").attr "id"


        callback = () ->
            $.post "/admin/dev/buckets/"+bucket, (data) ->
                if data["status"] and data["success"]
                    if elem.hasClass "btn-inverse"
                        elem.removeClass "btn-inverse"
                        elem.addClass "btn-success"
                        elem.html "<i class=\"icon-bolt\"></i> Enabled"
                    else if elem.hasClass "btn-success"
                        elem.addClass "btn-inverse"
                        elem.removeClass "btn-success"
                        elem.html "<i class=\"icon-off\"></i> Disabled"
                    elem = $("#"+bucket+"ModalButton")
                    if elem.hasClass "btn-inverse"
                        elem.removeClass "btn-inverse"
                        elem.addClass "btn-success"
                        elem.html "<i class=\"icon-bolt\"></i> Enabled"
                    else if elem.hasClass "btn-success"
                        elem.addClass "btn-inverse"
                        elem.removeClass "btn-success"
                        elem.html "<i class=\"icon-off\"></i> Disabled"
