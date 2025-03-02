function showMessage() {
    alert("wassssssaaaaaaaaaaaap");
}

// To attach the function dynamically (alternative to using inline onclick)
document.addEventListener("DOMContentLoaded", function () {
    let button = document.getElementById("myButton");
    if (button) {
        button.addEventListener("click", showMessage);
    }
});
