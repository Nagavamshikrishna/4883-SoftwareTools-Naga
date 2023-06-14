import csv
import random

def create_dot_file(data):
    dot_content = "digraph FamilyTree {\n"
    dot_content += 'node [shape=box, fontname="Arial", fontsize=12, penwidth=2]\n'
    dot_content += 'edge [penwidth=2]\n'
    dot_content += 'rankdir="TB"\n'  # Arrange generations from top to bottom

    # Add nodes (individuals) with their attributes
    for person in data:
        pid = person["pid"]
        name = person["name"]
        gender = person["gender"]
        clan_id = person["clan"]
        birthdate = person["byear"]
        deathdate = person["dyear"]
        age = person["dage"]
        if age == "100+":
            age = str(random.randint(30, 100))
        fillcolor = ""
        shape = ""
        if clan_id == "1":
            fillcolor = "lightcoral"
            clan_name = "Parent Clan"
        elif clan_id == "2":
            fillcolor = "green"
            clan_name = "Child Clan"
        elif clan_id == "3":
            fillcolor = "lightyellow"
            clan_name = "Beard Clan"
        elif clan_id == "4":
            fillcolor = "lightpink"
            clan_name = "Mustache Clan"
        elif clan_id == "5":
            fillcolor = "lightblue"
            clan_name = "Water Clan"
        elif clan_id == "6":
            fillcolor = "orange"
            clan_name = "Fire Clan"
        else:
            fillcolor = "white"
            clan_name = "Unknown Clan"
        generation = int(person["generation"])
        if gender == "M":
            shape = "square"
        elif gender == "F":
            shape = "circle"
        else:
            shape = "box"
        node_content = f'{pid} [label="{name}\\nAge: {age}\\nbdate:{birthdate}\\nddate: {deathdate}\\ngender: {gender}\\nClan: {clan_name}\\nGeneration: {generation}", shape="{shape}", style="filled", fillcolor="{fillcolor}", color="black"]\n'
        dot_content += node_content

    # Add edges (parent-child relationships)
    for person in data:
        pid = person["pid"]
        parentId1 = person["parentId1"]
        parentId2 = person["parentId2"]
        relation1 = person.get("relation1", "")
        relation2 = person.get("relation2", "")
        if parentId1:
            edge_content = f'{parentId1} -> {pid} [label="Child"]\n'
            dot_content += edge_content
        if parentId2:
            edge_content = f'{parentId2} -> {pid} [label="Child"]\n'
            dot_content += edge_content

        # Add husband-wife relationships
        spouse_id = person.get("spouseId")
        if spouse_id:
            if gender == "M":
                edge_content = f'{pid} -> {spouse_id} [label="Husband-Wife"]\n'
            else:
                edge_content = f'{spouse_id} -> {pid} [label="Husband-Wife"]\n'
            dot_content += edge_content

            # Add invisible edge to position husband and wife nodes side by side
            invisible_edge_content = f'{pid} -> {spouse_id} [style=invis, weight=10]\n'
            dot_content += invisible_edge_content

    dot_content += "}\n"

    # Write the DOT content to a file
    with open("family_tree.dot", "w") as file:
        file.write(dot_content)


# Read data from CSV file
def read_csv_file(file_path):
    with open(file_path, "r") as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)
    return data


# Example usage
file_path = "family_data.csv"
family_data = read_csv_file(file_path)

create_dot_file(family_data)
