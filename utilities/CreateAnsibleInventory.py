"""
This is a utility to accept IP pool and write
ansible inventory file.
"""

import jinja2
import os

POLICY_RANDOM_ALL = 1
POLICY_SATISFY = 2
POLICY_AVERAGE = 3

node_type = [
    "quanta_t41",
    "quanta_d51",
    "s2600kp",
    "s2600tp",
    "s2600wtt",
    "dell_r730xd",
    "dell_r730",
    "dell_r630",
    "dell_c6320"
]


# Find template from test/doc/template_ansible_inventory
path_template = os.sep.join(
    # ../doc/template_ansible_inventory
    os.path.abspath(__file__).split(os.sep)[:-2]
    +["doc", "template_ansible_inventory"])


def load_ip_pool(filepath=""):
    list_ip_pool = [
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.3",
        "192.168.1.4",
        "192.168.1.5",
        "192.168.1.6",
        "192.168.1.7",
        "192.168.1.8",
        "192.168.1.9",
        "192.168.1.10",
        "192.168.1.11",
        "192.168.1.12",
        "192.168.1.13",
        "192.168.1.14",
        "192.168.1.15",
        "192.168.1.16",
        "192.168.1.17"
    ]

    return list_ip_pool


def assign_ip_pool(list_ip_pool, policy=POLICY_AVERAGE):
    """
    Give an IP pool and policy, put them into a dict,
    with node type as key, IP list as value.

    POLICY_RANDOM_ALL, random on any type
    POLICY_SATISFY, at least one of a kind, then random assign
    POLICY_AVERAGE, average on each type
    """
    dict_assignment = {}

    # Guarantee at least one node of a type
    if policy == POLICY_RANDOM_ALL:
        print "Not implement yet."
    elif policy == POLICY_SATISFY:
        print "Not implement yet."
    elif policy == POLICY_AVERAGE:
        type_ct = len(node_type)
        for i in range(type_ct):
            dict_assignment[node_type[i]] = list_ip_pool[i::type_ct]
    else:
        pass

    return dict_assignment


def write_inventory(assignment, path="inventory"):
    ip_string = {}
    for key, value in assignment.items():
        ip_string[key] = "\n".join(value)

    with open(path_template, "r") as fp:
        inventory_template = fp.read()
    template = jinja2.Template(inventory_template)
    inventory = template.render(ip_string)
    with open(path, "w") as fp:
        fp.write(inventory)


if __name__ == "__main__":
    ip_pool = load_ip_pool()
    ip_assignment = assign_ip_pool(ip_pool)
    write_inventory(ip_assignment)
