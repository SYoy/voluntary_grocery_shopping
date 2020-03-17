/* query slected location listing*/
$("#location").change(function (e) {
    e.preventDefault();
    // get the nickname
    var location = $(this).val();
    // GET AJAX request
    $.ajax({
        type: 'GET',
        url: "{% url 'query_listings_blackboard' %}",
        data: {"location": location,
                "status": $("#status").val()},

        success: function (response) {
            // if not valid user, alert the user
            if(response["valid"]){
                console.log("You selected location:" + response["selected_loc"]);
                console.log(response["data"])
            }
        },
        error: function (response) {
            console.log(response)
        }
    })
})

/* query slected location listing*/
$("#status").change(function (e) {
    e.preventDefault();
    // get the nickname
    var status = $(this).val();
    // GET AJAX request
    $.ajax({
        type: 'GET',
        url: "get/ajax/listings'",
        data: {"location": $("#location").val(),
                "status": status},

        success: function (response) {
            // if not valid user, alert the user
            if(response["valid"]){
                console.log("You selected status:" + response["selected_status"]);
                console.log(response["data"])
            }
        },
        error: function (response) {
            console.log(response)
        }
    })
})