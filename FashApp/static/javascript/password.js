function disappear() {
    var x = document.getElementById("hide");
    if (x.type === "password") {
        x.type = "text";
    } else {
    x.type = "password";
    }
}