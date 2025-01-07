# import config file
from importlib import import_module
import importlib
from operator import contains
from struct import pack
from schema import *

# import libraries
# `os` - interacting with the os
# `sys` - interacting with the system
# `ipaddress` - for verifying that the IP is valid
# `paramiko` - for interacting with SSH
import os, sys, ipaddress, paramiko


def y_n(text: str) -> bool:
    """Provides a prompt from the given input, outputting `True` if the first letter is a `y` and `False` if the first letter is an `n`. Will ask until one option is chosen."""
    option = "x"
    while option[0] not in ["y", "n"]:
        option = input(f"\n{text}\n\n>>> ").lower() + "x"
    return True if option[0] == "y" else False


def check_ip(ip_to_check: str) -> bool:
    """Takes an IP address and outputs `True` if the IP is valid, otherwise outputs `False`"""
    # print(f"\nChecking IP address: {ip_to_check}")
    try:
        ipaddress.ip_address(ip_to_check)
        # print("\nIP is valid")
        return True
    except ValueError:
        # print("\nIP Address is invalid - Please check your input.")
        return False
    except:
        # print("\nUnknown error in check_ip()")
        return False


def take_ip() -> str:
    """Takes the chosen IP from the user and validates it. Returns a `str` containing the validated IP."""
    chosen_ip = input(
        "\nPlease enter the host IP address that you would like to check\n\n>>> "
    )
    while check_ip(chosen_ip) == False:
        chosen_ip = input(
            "\nIP Address is invalid - Please check your input and try again.\n\n>>> "
        )
    return chosen_ip


def take_devices() -> dict[str, str | list[int]]:
    """
    Prompts the user to enter which devices they want to check the services of. Rejects invalid inputs.

    Can use `-` to denote ranges and `,` to separate numbers

    Returns a `dict` where the key is the original input and the value is the parsed list of device numbers.
    """
    while True:
        chosen_devices = input(
            "\nEnter the device numbers you'd like to check:\n\n>>> "
        )
        output_list = []
        if any(
            character not in device_parse_characters for character in chosen_devices
        ):
            print("\nPlease only use integers, '-' and ','.")
        else:
            for item in chosen_devices.split(","):  # split groups of device numbers
                if "-" in item:  # Extend ranges to contain each device number.
                    left, right = item.split("-")
                    left, right = int(left), int(right)
                    if left < right:
                        output_list.extend(range(left, right + 1))
                    else:
                        output_list.extend(range(right, left + 1))
                else:
                    output_list.append(int(item))
            return {"devices": chosen_devices, "parsed": sorted(output_list)}


def confirm_vars() -> bool:
    """Prompts the user with a list of the current configurations.
    Returns `True` if the configuration is correct.
    Returns `False` if incorrect, but user is willing to reconfigure.
    Exits otherwise."""
    services = ""
    for service, key in service_schema.items():
        services += f"\n{key: ^5}: {service}"
    print(
        f"""
Verifying information:

Port Schema: {port_schema}

Service Schema:
[key] : [service]
{services}

Host IP: {target_ip}

Devices to check:
{target_devices["devices"]}
{target_devices["parsed"]}
"""
    )
    if y_n("Are these details correct?") == True:
        return True
    elif (
        y_n("Would you like to amend your entries?\n(If not, the program will close.)")
        == True
    ):
        return False
    else:
        print("Closing...")
        sys.exit()


if __name__ == "__main__":
    # Set working directory to current directory
    os.chdir(os.path.dirname(__file__))
    # Init Variables
    device_parse_characters: tuple = (
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "-",
        ",",
    )
    # Take user input
    target_ip: str = take_ip()
    target_devices: dict[str, str | list[int]] = take_devices()
    while confirm_vars() == False:
        target_ip = take_ip()
        target_devices = take_devices()
    # Run services modules
    service_modules = {}
    for service in os.listdir("./services"):
        name = service.replace(".py", "")
        if len(service) > len(name):
            module = importlib.import_module(name=f"services.{name}", package=None)
            print(name, module)
            module.main(
                target_ip, list(target_devices.values())[0], service_schema, port_schema
            )
