# IP Subnet Calculator

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

An interactive **IPv4 addressing and subnetting calculator** built with Python and Flask.
Enter an IP address in CIDR notation — for example `192.168.1.10/24` — and the application
instantly returns the subnet mask, network address, broadcast address, usable host range,
address counts, IP class, and whether the address is public or private. It can also split a
network into equal subnets and display them visually.

## Why subnet calculation matters

Every device on an IP network needs an address, and every network needs boundaries. Subnetting
is how those boundaries are defined: it divides a large address space into smaller, isolated
networks so that addresses are used efficiently, broadcast traffic stays contained, and traffic
between segments can be controlled and routed. Doing these calculations by hand means converting
addresses to binary and applying bitwise logic — which is exactly what this tool automates while
still showing the reasoning behind each result.

## Networking concepts demonstrated

- IPv4 addressing and the 32-bit structure of an address
- The four-octet dotted-decimal notation and its binary equivalent
- Classful addressing (Classes A, B, C, D and E)
- CIDR notation and prefix lengths
- Subnet masks and the network/host bit boundary
- Network and broadcast address derivation using bitwise operations
- Usable host ranges and address capacity
- Public vs. private address space (RFC 1918)
- Subnet splitting and borrowing host bits

---

## Features

| Feature | Description |
| --- | --- |
| **IPv4 address parsing** | Converts dotted-decimal addresses to and from 32-bit integers. |
| **CIDR prefix support** | Accepts any `IP/prefix` input with a prefix between `/0` and `/32`. |
| **Automatic subnet mask generation** | Builds the dotted-decimal mask directly from the CIDR prefix. |
| **Network address calculation** | Computed with a bitwise `AND` between the address and the mask. |
| **Broadcast address calculation** | Computed with a bitwise `OR` against the inverted mask. |
| **First usable host** | The address immediately after the network address. |
| **Last usable host** | The address immediately before the broadcast address. |
| **Total addresses** | The full size of the address block (`2^(32 - prefix)`). |
| **Usable hosts** | Total addresses minus the network and broadcast addresses. |
| **IP class detection** | Identifies Class A, B, C, D or E from the first octet. |
| **Public / private detection** | Flags RFC 1918 ranges and the loopback range as private. |
| **Subnet splitting** | Divides a network into *N* equal subnets by borrowing host bits. |
| **Visual subnet representation** | Renders the split address space as a proportional bar. |
| **Reverse CIDR mode** | Finds the smallest CIDR block containing two given addresses. |
| **User-friendly interface** | A clean, responsive web UI — plus a command-line mode. |

---

## Technologies Used

- **Python 3** — core calculation logic, implemented with pure bitwise operations
- **Flask** — lightweight web framework serving the application
- **HTML** — page templates
- **CSS** — styling and layout
- **JavaScript** — client-side interactivity, including the calculator mode toggle

---

## How It Works

Behind the friendly interface, every result comes from a few simple binary operations.

### 1. Converting the IP address into binary

An IPv4 address is really a single 32-bit number written as four 8-bit octets:

```
192  .  168  .    1  .   10
11000000.10101000.00000001.00001010
```

The calculator shifts each octet into place to build that 32-bit value.

### 2. Converting the CIDR prefix into a subnet mask

The prefix says how many leading bits identify the **network**; the rest identify the **host**.
A `/24` prefix means 24 network bits followed by 8 host bits:

```
/24  ->  11111111.11111111.11111111.00000000  ->  255.255.255.0
```

### 3. Network address — bitwise AND

Comparing the address with the mask bit by bit keeps the network bits and zeroes the host bits:

```
  11000000.10101000.00000001.00001010   192.168.1.10
AND
  11111111.11111111.11111111.00000000   255.255.255.0
= 11000000.10101000.00000001.00000000   192.168.1.0   <- network address
```

### 4. Broadcast address — inverted mask and bitwise OR

Inverting the mask flips it so only the host bits are set. Combining that with the network
address using `OR` sets every host bit to 1:

```
  11000000.10101000.00000001.00000000   192.168.1.0
OR
  00000000.00000000.00000000.11111111   inverted mask
= 11000000.10101000.00000001.11111111   192.168.1.255  <- broadcast address
```

### 5. Determining the usable host range

The network address and the broadcast address are reserved, so the hosts you can actually
assign sit between them:

```
First usable host = network address + 1   ->  192.168.1.1
Last usable host  = broadcast address - 1 ->  192.168.1.254
Total addresses   = 2^(32 - 24) = 256
Usable hosts      = 256 - 2 = 254
```

### 6. Splitting into subnets

To create more networks, bits are *borrowed* from the host portion. Splitting a `/24` into
4 subnets borrows 2 bits (`2^2 = 4`), producing four `/26` networks of 64 addresses each:

```
192.168.1.0/26    192.168.1.64/26    192.168.1.128/26    192.168.1.192/26
```

---

## Project Structure

```
IP-Subnet-Calculator/
│
├── app.py              # Flask web application: routes, form handling, result formatting
├── main.py             # Core calculation logic (bitwise helpers) + command-line interface
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
│
├── templates/
│   └── index.html      # Main page template: input form and results display
│
└── static/
    └── style.css       # Stylesheet for the web interface
```

| Path | Responsibility |
| --- | --- |
| `app.py` | Starts the Flask server, handles `GET`/`POST` requests, calls the calculation functions and passes results to the template. |
| `main.py` | Contains all subnetting logic — address conversion, mask generation, network and broadcast calculation, class detection, subnet splitting and reverse CIDR — and can be run standalone as a CLI. |
| `requirements.txt` | Lists the packages needed to run the project. |
| `templates/` | Jinja2 HTML templates rendered by Flask. |
| `static/` | Static assets served directly by Flask (CSS, and any images or scripts). |

---

## Installation and Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/LeenMahdi345/IP-Subnet-Calculator.git
```

### 2. Navigate to the project folder

```bash
cd IP-Subnet-Calculator
```

### 3. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

The development server starts on **http://127.0.0.1:5000** — open that address in your browser.

To use the command-line version instead:

```bash
python main.py
```

---

## Usage

1. Start the application and open **http://127.0.0.1:5000**.
2. Enter an IPv4 address in CIDR notation, for example:

   ```
   192.168.1.10/24
   ```

3. Optionally enter the number of subnets you want the network divided into.
4. Submit the form to see the full breakdown.

The application displays:

- **IP class** — A, B, C, D or E
- **Subnet mask** — in dotted-decimal notation
- **Network address**
- **Broadcast address**
- **First usable host**
- **Last usable host**
- **Number of addresses** in the block
- **Number of usable hosts**
- **Public / private status**

### Example result for `192.168.1.10/24`

| Field | Value |
| --- | --- |
| IP Address | 192.168.1.10 |
| CIDR Prefix | /24 |
| IP Class | Class C |
| Subnet Mask | 255.255.255.0 |
| Network Address | 192.168.1.0 |
| Broadcast Address | 192.168.1.255 |
| First Usable Host | 192.168.1.1 |
| Last Usable Host | 192.168.1.254 |
| Total Addresses | 256 |
| Usable Hosts | 254 |
| Public / Private | Private |

If a subnet count of `4` is supplied, the network is also split into:

```
Subnet 1: 192.168.1.0/26
Subnet 2: 192.168.1.64/26
Subnet 3: 192.168.1.128/26
Subnet 4: 192.168.1.192/26
```

---

## Screenshots

*(Add application screenshots here)*

<!--
![Home page](static/screenshots/home.png)
![Calculation results](static/screenshots/results.png)
![Subnet split view](static/screenshots/subnets.png)
-->

---

## Future Improvements

- **IPv6 support** — extend parsing and subnetting to 128-bit addresses
- **Advanced subnet visualization** — interactive charts of address-space allocation
- **Reverse subnet calculation** — expanded tooling around deriving prefixes from address ranges
- **Network planning tools** — VLSM support for subnets of differing sizes
- **Export calculation results** — download results as CSV, JSON or PDF
- **More networking utilities** — wildcard masks, binary breakdown views and a REST API endpoint
- **Automated tests** — unit tests covering the core calculation functions

---

## License

This project is released under the **MIT License**. You are free to use, modify and distribute
it with attribution.

---

**Author:** Leen Mahdi — [@LeenMahdi345](https://github.com/LeenMahdi345)
