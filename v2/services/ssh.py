import paramiko
from getpass import getpass


def main(
    target_ip: str,
    target_devices_parsed: list[int],
    service_schema: dict[str, str],
    port_schema: str,
):
    print("\nStarting SSH Check...")
    # Take username and pass
    username = input("\nSSH User:\n\n>>>")
    password = getpass("\nSSH Password:\n\n>>>")
    # If not in schema, say so and return. Otherwise, fetch the key.
    if "ssh" not in service_schema.keys():
        print("\nSSH not found in `service_schema`.\nAdd SSH to the schema to continue")
        return
    else:
        service_key = service_schema["ssh"]
    # Create Client object
    print("Generating Client...")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # For each device, attempt to make the connection.
    print("Attempting connections now:")
    ssh_results = {}
    for device in target_devices_parsed:
        port = str(port_schema.replace("[device]", str(device))).replace(
            "[service]", str(service_key)
        )
        print(f"Attempting device {device}...")
        try:
            ssh_client.connect(str(target_ip), int(port), username, password)
            print("  SUCCESS")
            ssh_results.update({device: [port, " UP "]})
        except:
            print("  FAILURE")
            ssh_results.update({device: [port, "DOWN"]})
        ssh_client.close()
    # TODO Print results
    print()
