
window.showNotification = function (message, level) {
    var notification = document.createElement('div');
    notification.className = 'notification ' + level;
    notification.innerText = message;

    // Add the notification to the body
    document.body.appendChild(notification);

    // Add the 'show' class to fade in
    setTimeout(function () {
        notification.style.display = "block";
        notification.classList.add('show'); // fade out
    }, 50); // short delay to allow the initial styles to apply

    // Optionally, remove the notification after a delay
    setTimeout(function () {
        notification.classList.remove('show'); // fade out
        setTimeout(function () {
            notification.style.display = "none";
            notification.remove(); // remove from DOM
        }, 500); // match the transition duration
    }, 3000); // 3-second display time
};
