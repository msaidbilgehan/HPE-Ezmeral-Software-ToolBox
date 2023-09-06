import { terminal_source_url, endpoint_stop_url } from './page_specific_urls.js';

export var terminal_source;

function terminal_EventSource_Start() {
    clear_Terminal();

    var contentDiv = document.getElementById('stream_content');
    if (terminal_source) {
        terminal_source.close();
    }
    var pageType = document.body.getAttribute('data-page-type');
    terminal_source = new EventSource(terminal_source_url + "/" + pageType); // use the URL with the IP addresses
    
    terminal_source.onerror = function (error) {
        console.error("EventSource failed:", error);
        showNotification('EventSource failed: ' + error, "error");
        terminal_source.close(); // close the connection if an error occurs
    };

    terminal_source.onmessage = function (event) {
        // console.info("EventSource:", event.data);
        contentDiv.innerHTML += event.data + "<br>"; // append each new log line to the content div

        // Check if the user is at or near the bottom of the container
        var container = document.querySelector('.fakeScreen');
        if (container.scrollTop + container.clientHeight >= container.scrollHeight - 50) { // 50px tolerance
            // Scroll to the bottom
            container.scrollTop = container.scrollHeight;
        }
    };
}

function terminal_EventSource_Stop() {
    if (terminal_source) {
        terminal_source.close();
    }
}

function clear_Terminal() {
    var contentDiv = document.getElementById('stream_content');
    contentDiv.innerHTML = ""; // clear the content div
}

function stop_Action() {
    var pageType = document.body.getAttribute('data-page-type');
    fetch(endpoint_stop_url + "/" + pageType)
        .then(response => response.json())
        .then(data => {
            // document.getElementById('output').innerText = data.message;
            showNotification(data.message, "info");
        })
        .catch(error => {
            console.error('An error occurred:', error);
            showNotification('An error occurred: ' + error, "error");
        });
}

document.addEventListener('DOMContentLoaded', function () {
    terminal_EventSource_Start();
});



window.clear_Terminal = clear_Terminal;
window.terminal_EventSource_Stop = terminal_EventSource_Stop;
window.terminal_EventSource_Start = terminal_EventSource_Start;
window.stop_Action = stop_Action;

