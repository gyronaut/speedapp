function get_activity(id) {
    document.getElementById("data").innerHTML = "<p class='no_data_text'> Fetching Activity... <\p>"
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState ==4 && this.status == 200) {
            document.getElementById("data").innerHTML = this.responseText;
        }
    }
    xhttp.open("POST", `/speedapp/_show_activity/${id}`, true);
    xhttp.send();
}