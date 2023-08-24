function get_activity(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState ==4 && this.status == 200) {
            document.getElementById("data").innerHTML = this.responseText;
        }
    }
    xhttp.open("POST", `/speedapp/_show_activity/${id}`, true);
    xhttp.send();
}