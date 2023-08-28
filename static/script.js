function get_activity(id) {
    document.getElementById("data").innerHTML = "<p class='no_data_text'> Fetching Activity... <\p>"
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState ==4){
            if( this.status == 200){
                document.getElementById("data").innerHTML = this.responseText;
            }else{
                document.getElementById("data").innerHTML = "<p class='no_data_text'> No Speed Data for this Activity!<\p>"
            }
        }
    }
    xhttp.open("POST", `/speedapp/_show_activity/${id}`, true);
    xhttp.send();
}