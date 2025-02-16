document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('#redButton');
    
    // Add click event listener to the button
    button.addEventListener('click', function() {
        alert('Button clicked!');
    });
});

// Note: Make sure you have this HTML in your idk.html file:
/*
<button id="redButton" style="background-color: red; color: white; padding: 10px 20px; border: none; cursor: pointer;">
    Click Me
</button>
*/