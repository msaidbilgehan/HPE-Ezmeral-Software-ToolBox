import { eventsource_action_clear_files_url } from './page_specific_urls.js';


function clear_Action_Files() {
    var pageType = document.body.getAttribute('data-page-type');
    fetch(eventsource_action_clear_files_url + "/" + pageType)
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
window.clear_Action_Files = clear_Action_Files


function download_Action_Files() {
    var pageType = document.body.getAttribute('data-page-type');
    fetch(eventsource_action_clear_files_url + "/" + pageType)
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
window.download_Action_Files = download_Action_Files


// function clear_Action_Logs() {
//     var contentDiv = document.getElementById('stream_content');
//     contentDiv.innerHTML = ""; // clear the content div

//     fetch(eventsource_action_clear_files_url)
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
// window.clear_Action_Logs = clear_Action_Logs
