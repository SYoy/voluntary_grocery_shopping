function addElement(elementTag, elementId, dict, map) {
    // Adds an element to the document
    var p = document.getElementById("blackboard_elements");
    var newElement = document.createElement(elementTag);
    newElement.setAttribute('id', elementId);
    newElement.innerHTML = dict["nachricht"];

    newElement.className = 'col-md-auto img-rounded';
    newElement.innerHTML = '<p>Nachricht:<br>'+dict["nachricht"]+'<br></p>'+
            '<div class"col-xs-auto img-rounded" style="background: #99aeb5">'+
            '<p>Einkaufswunsch:</p>'+ dict["liste_text"]+'</div> <br>'+
            '<p>Budget: '+ dict["budget"]+'€ Ort:'+ map[dict["user"]] +'</p>';

    // Css styling
    newElement.setAttribute("style", "background: #0f6674; float: left; text-align: " +
        "left; margin-right: 10px; min-width: 10%; max-width: 33%; padding: 5px; margin-bottom: 10px;" +
        "cursor: pointer");
    newElement.setAttribute("id", elementId);
    newElement.setAttribute("onclick","onClickAuftrag(this)");

    p.appendChild(newElement);
}

function clearElements(){
    var element = document.getElementById("blackboard_elements");
    while (element.firstChild) {
      element.removeChild(element.firstChild);
    }
}

function addNoElementsMessage(){
    var p = document.getElementById("blackboard_elements");
    var newElement = document.createElement("div");
    newElement.setAttribute('id', "NoElementsMessage");
    newElement.innerHTML = "Für Ihre Auswahl wurden keine Treffer gefunden, bitte vergrößern Sie Ihren Suchraum.";

    p.appendChild(newElement);
}

function updateBlockboard(e, location, status) {
    e.preventDefault();
    // get the nickname
    // GET AJAX request
    $.ajax({
        type: 'GET',
        url: "{% url 'EinkaufsApp:query_listings_blackboard' %}",
        data: {"location": location,
                "status": status},

        success: function (response) {
            // if not valid user, alert the user
            if(response["valid"]){
                console.log("You selected location:" + response["selected_loc"]);
                console.log(response["data"]);

                var auftraege = JSON.parse(response["data"]);
                if (auftraege.length > 0) {
                    clearElements();
                    auftraege.forEach(function(element) {
                        addElement("div", element["pk"], element["fields"], response["map"]);
                    });
                } else {
                    clearElements();
                    addNoElementsMessage();
                }
            }
        },
        error: function (response) {
            console.log(response)
        }
    })
}