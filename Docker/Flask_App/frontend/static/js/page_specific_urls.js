export var terminal_source_url = "";
export var eventsource_source_url = "";
export var eventsource_action_clear_logs_url = "";
export var terminal_source_stop_url = "";

export var terminal_log_download_source_url = "/download_terminal_log";
window.terminal_log_download_source_url = terminal_log_download_source_url;

export var eventsource_action_stop_url = "/endpoint_stop";
export var eventsource_action_clear_files_url = "/clear_action_files";
export var download_action_files_url = "/file_table_download";
export var action_folder_info_url = "/folder_info";



function pageSpecificFunction() {
    var pageType = document.body.getAttribute('data-page-type');
    // console.log("pageType:", pageType);
    switch (pageType) {
        case 'log_collection':
            terminal_source_url = '/log_collection_terminal_endpoint';
            eventsource_source_url = '/log_collection_endpoint';
            eventsource_action_clear_logs_url = "/clear_Log_Collection_Log_Files";
            terminal_source_stop_url = "/log_collection_stop_endpoint";
            break;
        case 'cleanup':
            terminal_source_url = '/cleanup_terminal_endpoint';
            eventsource_source_url = '/cleanup_endpoint';
            eventsource_action_clear_logs_url = "";
            terminal_source_stop_url = "/cleanup_stop_endpoint";
            break;
        case 'fqdn':
            terminal_source_url = '/fqdn_terminal_endpoint';
            eventsource_source_url = '/fqdn_endpoint';
            eventsource_action_clear_logs_url = "";
            terminal_source_stop_url = "/fqdn_stop_endpoint";
            break;
        case 'backup':
            terminal_source_url = '/backup_terminal_endpoint';
            eventsource_source_url = '/backup_endpoint';
            eventsource_action_clear_logs_url = "";
            terminal_source_stop_url = "/backup_stop_endpoint";
            break;
        default:
            terminal_source_url = '/not-found';
            eventsource_source_url = '/not-found';
            terminal_log_download_source_url = '/not-found';
            eventsource_action_clear_logs_url = "";
            terminal_source_stop_url = "/not-found";
            break;
    }
}

// Call the function on page load
pageSpecificFunction()
// document.addEventListener('DOMContentLoaded', pageSpecificFunction);

