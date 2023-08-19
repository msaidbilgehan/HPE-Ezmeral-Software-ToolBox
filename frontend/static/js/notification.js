

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

    addNotificationToNavbar(message, level);
    addNotificationToCache(message, level);
};

// Function to add a notification
function addNotificationToNavbar(message, small_message) {
    // Find the dropdown menu
    var dropdownMenu = document.querySelector('.dropdown-menu');

    // Create a new dropdown item for the notification
    var notificationItem = document.createElement('a');
    notificationItem.href = '#';
    notificationItem.className = 'dropdown-item';

    // Add the notification message
    var messageElement = document.createElement('h6');
    messageElement.className = 'fw-normal mb-0';
    messageElement.textContent = message;
    notificationItem.appendChild(messageElement);

    // Add the time ago
    var timeElement = document.createElement('small');
    timeElement.textContent = small_message;
    notificationItem.appendChild(timeElement);

    // Append the new notification item to the dropdown menu
    // Insert before the "See all notifications" link
    var seeAllLink = document.querySelector('.dropdown-item.text-center');
    dropdownMenu.insertBefore(notificationItem, seeAllLink);
}

function addNotificationToCache(message, level) {
    // Read the existing notifications
    var notifications = readNotificationsFromCache();

    // Create a notification object
    var notification = { message: message, level: level };

    // Add the new notification object
    notifications.push(notification);

    // Limit to the last 5 notifications
    notifications = notifications.slice(-5);

    // Write the updated notifications to cache
    writeNotificationsToCache(notifications);
}

function writeNotificationsToCache(notifications) {
    // Convert the notifications to a JSON string
    var notificationsString = JSON.stringify(notifications);

    // Write the JSON string to localStorage
    localStorage.setItem('notifications', notificationsString);
}

function readNotificationsFromCache() {
    // Read the JSON string from localStorage
    var notificationsString = localStorage.getItem('notifications');

    // If there are no notifications, return an empty array
    if (!notificationsString) return [];

    // Parse the JSON string to an array of notifications
    return JSON.parse(notificationsString);
}

function clearNotificationsFromCache() {
    localStorage.removeItem('notifications');
}

// Read the notifications from cache
var cache_notifications = readNotificationsFromCache()
for (var i = 0; i < cache_notifications.length; i++) {
    var notification = cache_notifications[i];
    addNotificationToNavbar(notification.message, notification.level);
}
