export var terminal_source_url = "not-found";
export var eventsource_source_url = "not-found";

function pageSpecificFunction() {
    var pageType = document.body.getAttribute('data-page-type');
    // console.log("pageType:", pageType);
    switch (pageType) {
        case 'log_collection':
            terminal_source_url = '/log_collection_terminal_endpoint';
            eventsource_source_url = '/log_collection_endpoint';
            break;
        case 'cleanup':
            terminal_source_url = '/cleanup_terminal_endpoint';
            eventsource_source_url = '/cleanup_endpoint';
            break;
        case 'fqdn':
            terminal_source_url = '/fqdn_terminal_endpoint';
            eventsource_source_url = '/fqdn_endpoint';
            break;
        // ... add more cases for other pages as needed
        default:
            // Default actions or none
            break;
    }
    window.terminal_source_url = terminal_source_url;
    window.eventsource_source_url = eventsource_source_url;
    // console.log("page_specific_urls.js loaded: " + terminal_source_url + " " + eventsource_source_url);
}

// Call the function on page load
pageSpecificFunction()
// document.addEventListener('DOMContentLoaded', pageSpecificFunction);

