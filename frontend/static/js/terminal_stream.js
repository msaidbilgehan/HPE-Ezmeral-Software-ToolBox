import { terminal_source_url } from './page_specific_urls.js';

var terminal_source;

function terminal_EventSource_Start(url) {
    clear_Terminal();

    var contentDiv = document.getElementById('stream_content');
    if (terminal_source) {
        terminal_source.close();
    }
    terminal_source = new EventSource(url); // use the URL with the IP addresses
    
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


// function clear_Log_Collection_Log_Files() {
//     var contentDiv = document.getElementById('stream_content');
//     contentDiv.innerHTML = ""; // clear the content div

//     fetch('/clear_Log_Collection_Log_Files')
//         .then(response => response.json())
//         .then(data => {
//             // document.getElementById('output').innerText = data.message;
//             showNotification(data.message, "info");
//         })
//         .catch(error => {
//             console.error('An error occurred:', error);
//             showNotification('An error occurred: ' + error, "error");
//         });
// }

function clear_Terminal() {
    var contentDiv = document.getElementById('stream_content');
    contentDiv.innerHTML = ""; // clear the content div
}


// document.getElementById('listen_logs-btn').addEventListener('click', function () {
//     terminal_EventSource_Start(terminal_source_url);
// });


document.getElementById('stop-btn').addEventListener('click', function () {
    fetch('/log_collection_log_stop_endpoint')
        .then(response => response.json())
        .then(data => {
            // document.getElementById('output').innerText = data.message;
            showNotification(data.message, "info");
        })
        .catch(error => {
            console.error('An error occurred:', error);
            showNotification('An error occurred: ' + error, "error");
        });
});

document.addEventListener('DOMContentLoaded', function () {
    terminal_EventSource_Start(terminal_source_url);
    // console.info("terminal_source_url:" + terminal_source_url);
    // console.info("eventsource_source_url:" + eventsource_source_url);
});



window.clear_Terminal = clear_Terminal;
window.terminal_EventSource_Stop = terminal_EventSource_Stop;
window.terminal_EventSource_Start = terminal_EventSource_Start;

