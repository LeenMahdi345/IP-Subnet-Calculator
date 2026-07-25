import math


def ip_to_int(ip):
    parts = ip.split(".")

    result = 0

    for part in parts:
        result = (result << 8) + int(part)

    return result


def int_to_ip(number):
    return ".".join([
        str((number >> 24) & 255),
        str((number >> 16) & 255),
        str((number >> 8) & 255),
        str(number & 255)
    ])


def mask_to_int(mask):
    parts = mask.split(".")

    result = 0

    for part in parts:
        result = (result << 8) + int(part)

    return result


# CIDR مثل 24 إلى Subnet Mask
def cidr_to_mask(prefix):
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

    return int_to_ip(mask)


# حساب Broadcast
def calculate_broadcast(network_int, mask_int):
    inverted_mask = (~mask_int) & 0xFFFFFFFF

    broadcast_int = network_int | inverted_mask

    return broadcast_int


# تحديد IP Class
def get_ip_class(ip):
    first_octet = int(ip.split(".")[0])

    if 1 <= first_octet <= 126:
        return "Class A"

    elif 128 <= first_octet <= 191:
        return "Class B"

    elif 192 <= first_octet <= 223:
        return "Class C"

    elif 224 <= first_octet <= 239:
        return "Class D"

    elif 240 <= first_octet <= 255:
        return "Class E"

    else:
        return "Invalid IP"


# تقسيم الشبكة إلى Subnets
def split_subnets(network_int, prefix, subnet_count):

    # عدد الـ bits التي نحتاج استعارتها
    bits_needed = math.ceil(math.log2(subnet_count))

    # الـ prefix الجديد
    new_prefix = prefix + bits_needed

    # حجم كل subnet
    subnet_size = 2 ** (32 - new_prefix)

    subnets = []

    current_network = network_int

    for i in range(subnet_count):

        subnet_address = int_to_ip(current_network)

        subnets.append(
            f"Subnet {i + 1}: {subnet_address}/{new_prefix}"
        )

        current_network += subnet_size

    return subnets



# Reverse CIDR: أصغر CIDR block يحتوي عنوانين
def reverse_cidr(ip1, ip2):

    # تحويل العنوانين إلى Integer
    ip1_int = ip_to_int(ip1)

    ip2_int = ip_to_int(ip2)

    # XOR لإيجاد البتات المختلفة
    diff = ip1_int ^ ip2_int

    # حساب عدد الـ host bits (عدد البتات المشتركة من الأعلى)
    host_bits = 0

    while diff > 0:
        diff >>= 1

        host_bits += 1

    # طول الـ prefix المشترك
    prefix = 32 - host_bits

    # إنشاء الـ subnet mask
    mask_int = (0xFFFFFFFF << host_bits) & 0xFFFFFFFF

    # تصفير الـ host bits للحصول على Network Address
    network_int = ip1_int & mask_int

    network_address = int_to_ip(network_int)

    return f"{network_address}/{prefix}"


# ---------------- MAIN ----------------

if __name__ == "__main__":

    # قائمة الاختيار
    print("Choose mode:")
    print("1. Normal subnet calculation")
    print("2. Reverse CIDR mode")

    mode = input("Enter choice (1/2): ").strip()

    if mode == "2":
        # Reverse CIDR mode
        ip1 = input("Enter first IP: ")

        ip2 = input("Enter second IP: ")

        cidr_block = reverse_cidr(ip1, ip2)

        print("\n--- Result ---")

        print("Smallest CIDR block containing both:", cidr_block)

        raise SystemExit

    ip_cidr = input("Enter IP/CIDR: ")

    # فصل IP عن CIDR
    ip, prefix = ip_cidr.split("/")

    prefix = int(prefix)


    # تحويل CIDR إلى Mask
    mask = cidr_to_mask(prefix)


    # تحويل IP و Mask إلى Integer
    ip_int = ip_to_int(ip)

    mask_int = mask_to_int(mask)


    # Network Address
    network_int = ip_int & mask_int

    network_address = int_to_ip(network_int)


    # Broadcast Address
    broadcast_int = calculate_broadcast(network_int, mask_int)

    broadcast_address = int_to_ip(broadcast_int)


    # First and Last usable host
    first_host_int = network_int + 1

    last_host_int = broadcast_int - 1


    first_host = int_to_ip(first_host_int)

    last_host = int_to_ip(last_host_int)


    # IP Class
    ip_class = get_ip_class(ip)


    # Split Subnets
    subnet_count = int(input("\nHow many subnets do you want? "))

    subnets = split_subnets(
        network_int,
        prefix,
        subnet_count
    )


    # Output
    print("\n--- Result ---")

    print("IP:", ip)

    print("CIDR Prefix:", prefix)

    print("Subnet Mask:", mask)

    print("Network Address:", network_address)

    print("Broadcast Address:", broadcast_address)

    print("First Usable Host:", first_host)

    print("Last Usable Host:", last_host)

    print("IP Class:", ip_class)


    print("\n--- Subnets ---")

    for subnet in subnets:
        print(subnet)