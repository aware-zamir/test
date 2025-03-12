document.getElementById("redButton").addEventListener("click", function() {
    let randomNumber = Math.floor(Math.random() * 10) + 1; 
    document.getElementById("numberDisplay").textContent = randomNumber;
});
