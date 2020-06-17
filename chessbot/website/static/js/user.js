window.onload = function() {
    let page = window.location.search.replace("?page=", '');
    let selected = document.getElementById("number-"+page);
 
    if (selected) {
        selected.className = 'active';
    } else document.getElementById('number-1').className = 'active';

}