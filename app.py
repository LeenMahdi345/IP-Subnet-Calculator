from flask import Flask, render_template, request

# Reuse the existing, unmodified calculation logic from main.py
from main import (
    ip_to_int,
    int_to_ip,
    mask_to_int,
    cidr_to_mask,
    calculate_broadcast,
    get_ip_class,
    split_subnets,
    reverse_cidr,
)

app = Flask(__name__)


def is_private_ip(ip):
    """Return 'Private' or 'Public' based on RFC 1918 ranges (UI-layer helper)."""
    octets = [int(p) for p in ip.split(".")]
    first, second = octets[0], octets[1]

    if first == 10:
        return "Private"
    if first == 172 and 16 <= second <= 31:
        return "Private"
    if first == 192 and second == 168:
        return "Private"
    if first == 127:
        return "Private"  # loopback
    return "Public"


def calculate(ip_cidr, subnet_count=None):
    """Drive the existing functions from main.py and gather all display values."""
    ip, prefix = ip_cidr.strip().split("/")
    prefix = int(prefix)

    if not 0 <= prefix <= 32:
        raise ValueError("CIDR prefix must be between 0 and 32.")

    # Existing logic
    mask = cidr_to_mask(prefix)
    ip_int = ip_to_int(ip)
    mask_int = mask_to_int(mask)

    network_int = ip_int & mask_int
    network_address = int_to_ip(network_int)

    broadcast_int = calculate_broadcast(network_int, mask_int)
    broadcast_address = int_to_ip(broadcast_int)

    first_host = int_to_ip(network_int + 1)
    last_host = int_to_ip(broadcast_int - 1)

    ip_class = get_ip_class(ip)

    # UI-layer derived values (do not touch core functions)
    total_addresses = 2 ** (32 - prefix)
    usable_hosts = max(total_addresses - 2, 0)

    results = {
        "IP Address": ip,
        "CIDR Prefix": "/" + str(prefix),
        "IP Class": ip_class,
        "Subnet Mask": mask,
        "Network Address": network_address,
        "Broadcast Address": broadcast_address,
        "First Usable Host": first_host,
        "Last Usable Host": last_host,
        "Total Addresses": total_addresses,
        "Usable Host Addresses": usable_hosts,
        "Public / Private": is_private_ip(ip),
    }

    subnets = None
    if subnet_count:
        subnets = split_subnets(network_int, prefix, int(subnet_count))

    return results, subnets


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    subnets = None
    error = None
    ip_cidr = ""
    subnet_count = ""
    mode = "normal"
    ip1 = ""
    ip2 = ""
    reverse_result = None

    if request.method == "POST":
        mode = request.form.get("mode", "normal")

        if mode == "reverse":
            # Reverse CIDR mode
            ip1 = request.form.get("ip1", "").strip()
            ip2 = request.form.get("ip2", "").strip()
            try:
                reverse_result = reverse_cidr(ip1, ip2)
            except Exception as exc:
                error = f"Invalid input: {exc}"
        else:
            # Normal calculator (unchanged behavior)
            ip_cidr = request.form.get("ip_cidr", "")
            subnet_count = request.form.get("subnet_count", "").strip()
            try:
                results, subnets = calculate(
                    ip_cidr,
                    subnet_count if subnet_count else None,
                )
            except Exception as exc:
                error = f"Invalid input: {exc}"

    return render_template(
        "index.html",
        results=results,
        subnets=subnets,
        error=error,
        ip_cidr=ip_cidr,
        subnet_count=subnet_count,
        mode=mode,
        ip1=ip1,
        ip2=ip2,
        reverse_result=reverse_result,
    )


if __name__ == "__main__":
    app.run(debug=True)
