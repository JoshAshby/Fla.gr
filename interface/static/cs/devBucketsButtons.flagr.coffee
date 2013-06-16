$ ->
    $(".modal-options-btn").click ->
        elem = $(this)
        bucket = elem.data "bucket"
        $.post "/admin/dev/buckets", json: "{\"bucket\": \"" + bucket+"\"}", (data) ->
            if data["status"]
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
                $("#"+bucket+"Modal").modal('hide')
