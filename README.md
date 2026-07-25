# IP Address & Subnet Calculator

A Python-based **IPv4 addressing and subnetting toolkit** with both a command-line
interface and a clean Flask web UI. It performs classic subnet calculations using
low-level bitwise operations, splits networks into equal subnets with a visual
representation of the address space, and includes a **Reverse CIDR** mode that finds
the smallest CIDR block containing two given IP addresses.

---

## Features

- **IPv4 address parsing** — convert dotted-decimal addresses to/from 32-bit integers.
- **CIDR calculation** — derive network details from an `IP/prefix` input (e.g. `192.168.1.50/24`).
- **Subnet mask generation** — build the subnet mask from a CIDR prefix.
- **Network address calculation** — via bitwise `AND` of the IP and mask.
- **Broadcast address calculation** — via the inverted mask.
- **First and last usable host** — usable host range for the network.
- **IP class detection** — Class A / B / C / D / E.
- **Public / Private IP detection** — RFC 1918 range detection.
- **Subnet splitting** — divide a network into N equal subnets, with a **visual bar** of the split.
- **Reverse CIDR mode** — find the smallest CIDR block that contains two IP addresses (using XOR + bitwise logic).
- **Flask web interface** — a responsive HTML/CSS UI on top of the core logic.

---

## Technologies Used

- **Python 3** — core calculation logic (bitwise operations, no external networking libs).
- **Flask** — lightweight web framework serving the UI layer.
- **HTML / CSS** — templates and styling (with a small amount of vanilla JavaScript for the mode toggle).

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/LeenMahdi345/IP-Subnet-Calculator.git
cd IP-Subnet-Calculator
```

**2. (Recommended) Create a virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Web interface (Flask)

```bash
python app.py
```

Then open your browser at **http://127.0.0.1:5000**.

### Command-line interface

```bash
python main.py
```

You'll be prompted to choose a mode:

```
Choose mode:
1. Normal subnet calculation
2. Reverse CIDR mode
```

---

## Example Usage

### Normal subnet calculation

**Input:** `192.168.1.50/24`, split into `4` subnets

| Field                  | Value           |
| ---------------------- | --------------- |
| IP Address             | 192.168.1.50    |
| CIDR Prefix            | /24             |
| IP Class               | Class C         |
| Subnet Mask            | 255.255.255.0   |
| Network Address        | 192.168.1.0     |
| Broadcast Address      | 192.168.1.255   |
| First Usable Host      | 192.168.1.1     |
| Last Usable Host       | 192.168.1.254   |
| Total Addresses        | 256             |
| Usable Host Addresses  | 254             |
| Public / Private       | Private         |

**Subnet split:**

```
Subnet 1: 192.168.1.0/26
Subnet 2: 192.168.1.64/26
Subnet 3: 192.168.1.128/26
Subnet 4: 192.168.1.192/26

[ Subnet 1 ][ Subnet 2 ][ Subnet 3 ][ Subnet 4 ]
```

### Reverse CIDR mode

**Input:** `192.168.1.10` and `192.168.1.200`

**Output:**

```
Smallest CIDR Block: 192.168.1.0/24
```

---

## Project Structure

```
IP-Subnet-Calculator/
├── app.py              # Flask web application (UI layer)
├── main.py             # Core calculation logic + CLI
├── requirements.txt    # Python dependencies
├── .gitignore
├── README.md
├── templates/
│   └── index.html      # Web UI template
└── static/
    └── style.css       # Styling for the web UI
```

---

## Future Improvements

- **IPv6 support** — extend parsing and subnetting to 128-bit addresses.
- **Variable Length Subnet Masking (VLSM)** — split into subnets of different sizes.
- **Input validation & error messages** — stricter octet/prefix checks in the UI.
- **Export results** — download results as CSV/JSON.
- **REST API endpoint** — expose calculations as a JSON API.
- **Unit tests** — automated tests for the core calculation functions.

---

## License

This project is available under the MIT License.
