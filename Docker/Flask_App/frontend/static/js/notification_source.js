import { notification_source_url } from './page_specific_urls.js';
import { showNotification } from './notification.js';



export var notification_source;



function notification_EventSource_Start() {
    if (notification_source) {
        notification_source.close();
    }

    var pageType = document.body.getAttribute('data-page-type');
    notification_source = new EventSource(notification_source_url);

    notification_source.onerror = function (error) {
        console.error("EventSource ", pageType, " failed:", error);
        showNotification('Connection Lost: ' + pageType, "error");
        notification_source.close(); // close the connection if an error occurs
    };

    notification_source.onmessage = function (event) {
        let correctedData = event.data.replace(/'/g, '"');
        let notification_json = JSON.parse(correctedData);

        showNotification(notification_json["message"], notification_json["status"]);
    };
}

function notification_EventSource_Stop() {
    if (notification_source) {
        notification_source.close();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    notification_EventSource_Start();
});


