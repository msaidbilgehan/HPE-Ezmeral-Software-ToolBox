


export function get_ip_host_addresses(only_ip) {
    var input_ipAddressesHostnames = document.getElementById('input_IP_Addresses_Hostnames').value;

    // Split the IP addresses by a newline or comma
    var ipAddressesHostnames = input_ipAddressesHostnames.split(/\s*[,|\n]\s*/);

    if (only_ip) {
        // You can further validate each IP if needed
        ipAddressesHostnames = ipAddressesHostnames.map(function (entry) {
            var match = entry.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/);
            return match ? match[0] : null;
        }).filter(Boolean);
    }
    else {
        // You can further validate each IP with Hostname if needed
        ipAddressesHostnames = ipAddressesHostnames.filter(function (entry) {
            return /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[-\t\s]+\w+\b/.test(entry);
        });
        ipAddressesHostnames = ipAddressesHostnames.map(function (entry) {
            var parts = entry.split(/[-\t\s]+/);
            return {
                ip: parts[0],
                hostname: parts[1]
            };
        });
    }

    // Encode the IP addresses array into a JSON string
    var ipAddressesHostnamesJson = JSON.stringify(ipAddressesHostnames);

    return ipAddressesHostnamesJson
}