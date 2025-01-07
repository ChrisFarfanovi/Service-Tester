# region Init

import os, ipaddress, sys, paramiko

# Set Working directory to file directory
os.chdir(os.path.dirname(__file__))
# region Variables

port_schema = str
service_schema = {}
target_ip = str
target_Pis = []
ssh_results = {}
http_results = {}

# endregion

# endregion

# region Functions

# region Fetching


def fetch_file(filepath):  # Call to fetch a file from a specific filepath
    contents = open(str(filepath), "r").read()
    return contents


def fetch_schema():  # Call to fetch schema from storage
    global port_schema, service_schema
    print("================================\nFetching schema...")
    port_schema = fetch_file("schema/ports.txt")
    print(f"\n__Port Schema fetched:__\n| {port_schema}")
    var = fetch_file("schema/services.txt").split("\n")
    for x in range(len(var)):
        var[(x - 1)] = var[(x - 1)].split(" = ")  # type: ignore
    for x in range(len(var)):
        service_schema.update({var[(x - 1)][0]: var[(x - 1)][1]})
    print(f"\n__Service Schema fetched:__\n|[key]:[service]")
    for service in service_schema:
        print(f"|  {service_schema[service]}  : {service}")
    print("All schema fetched!")


# endregion

# region Inputs


def y_n(text):
    varstr = "x"
    while varstr[0] not in ["y", "n"]:
        varstr = input(f"\n{text}\n\n>>> ").lower() + "x"
    if varstr[0] == "y":
        return True
    else:
        return False


def check_ip(ip_to_check):
    print(f"\nChecking IP address: {ip_to_check}")
    try:
        ipaddress.ip_address(ip_to_check)
        print("\nIP is valid")
        return True
    except ValueError:
        print("\nIP Address/Netmask is invalid.")
        return False
    except:
        print("\nUnknown error in check_ip()")
        return False


def take_ip():
    global target_ip
    varstr = input(
        "\n================================\nPlease enter the host IP address that you would like to check\n\n>>> "
    )
    while check_ip(varstr) == False:
        varstr = input(
            "\nPlease enter the host IP address that you would like to check:\n\n>>> "
        )
    target_ip = varstr


def take_Pis():
    global target_Pis
    print("\n================================")
    target_Pis = []
    resolved = False
    while resolved == False:
        var = input("\nEnter the range of Pis you'd like to check:\n\n>>> ")
        if any(
            character not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "-", ","]
            for character in var
        ):
            print("\nPlease only use integers, '-' and ','.")
        else:
            for item in var.split(","):
                if "-" in item:
                    bottom, top = item.split("-")
                    target_Pis.extend(range(int(bottom), int(top) + 1))
                else:
                    target_Pis.append(int(item))
            target_Pis = list(set(target_Pis))
            resolved = True


def confirm_vars():
    print(
        f"\n================================\nVerifying information:\n\nPort schema: {port_schema}\n\nService schema:\n[key] : [service]"
    )
    for service in service_schema:
        print(f"  {service_schema[service]}  : {service}")
    print(f"\nHost IP:\n{target_ip}\n\nPis to check:{target_Pis}\n")
    match y_n("Are these details correct?"):
        case True:
            return True
        case False:
            if (
                y_n(
                    "Would like to ammend the information you entered?\n(Answering 'no' will restart the program, refreshing the schema)"
                )
                == True
            ):
                return False
            else:
                print("Refreshing")
                os.execv(__file__, sys.argv)


# endregion

# region Services


def ssh_check():
    global ssh_results
    print("\nStarting SSH Check...")
    username = input("\nSSH User:\n\n>>>")
    password = input("\nSSH Password:\n\n>>>")
    service_key = service_schema["ssh"]
    ssh_results = {}
    print("Generating Client...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Attempting connections now:")
    for Pi in target_Pis:
        port = str(port_schema.replace("[pi]", str(Pi))).replace("[service]", str(service_key))  # type: ignore
        print(f"Attempting Pi {Pi}...")
        try:
            ssh.connect(str(target_ip), int(port), username, password)
            print("  SUCCESS")
            ssh_results.update({Pi: [port, " UP "]})
        except:
            print("  FAILURE")
            ssh_results.update({Pi: [port, "DOWN"]})
        ssh.close()


def http_check():
    global http_results
    print("\nStarting SSH Check...")
    username = "cn-01"
    password = "C0d3!Nat10n"
    service_key = service_schema["ssh"]
    ssh_results = {}
    print("Generating Client...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Attempting connections now:")
    for Pi in target_Pis:
        port = str(port_schema.replace("[pi]", str(Pi))).replace("[service]", str(service_key))  # type: ignore
        print(f"Attempting Pi {Pi}...")
        try:
            ssh.connect(str(target_ip), int(port), username, password)
            print("  SUCCESS")
            ssh_results.update({Pi: [port, " UP "]})
        except:
            print("  FAILURE")
            ssh_results.update({Pi: [port, "DOWN"]})
        ssh.close()


def report():
    print("Not written reporting function yet")


# endregion

# region Main


def main():
    fetch_schema()
    confirmed = False
    while confirmed == False:
        take_ip()
        take_Pis()
        if confirm_vars() == True:
            confirmed = True
    ssh_check()
    http_check()
    report()

    #     os.execv(__file__, sys.argv)
    #     sys.exit()


# endregion

# endregion

# region Run

main()

# endregion
