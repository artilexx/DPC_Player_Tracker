function filterFunction() {
    var input, filter, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("dropdown-content");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
      txtValue = a[i].textContent || a[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
    input.addEventListener("keypress", function(event) {
      event.preventDefault
      if (event.key === "Enter") {
        document.getElementById("enter-button").click()
      }
    });
}

function inputplayer() {
  input = document.getElementById("myInput")
  window.location.href = input.value;
}

function enterlisten(){
  var input = document.getElementById("myInput");
  input.addEventListener("keypress", function(event) {
    event.preventDefault
    if (event.key === "Enter") {
      document.getElementById("enter-button").click()
    }
  });
}
