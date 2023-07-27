import sys
import requests
import xml.etree.ElementTree as ET


def retrieve_uniprot_entry(entry_id):
    url = f"https://www.uniprot.org/uniprot/{entry_id}.xml"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None


def extract_alternative_names(xml_content):
    root = ET.fromstring(xml_content)
    alternative_names = []
    for protein in root.findall(".//{http://uniprot.org/uniprot}protein"):
        for name in protein.findall("{http://uniprot.org/uniprot}alternativeName/{http://uniprot.org/uniprot}fullName"):
            if name.text:
                alternative_names.append(name.text)
    return alternative_names


def extract_gene_names(xml_content):
    root = ET.fromstring(xml_content)
    gene_names = []

    # Extract gene names from the recommendedName element
    for gene in root.findall(
            ".//{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}recommendedName/{http://uniprot.org/uniprot}fullName"):
        if gene.text:
            gene_names.append(gene.text)
    for name in root.findall(
            ".//{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}SubName/{http://uniprot.org/uniprot}fullName"):
        if name.text:
            gene_names.append(name.text)
    for name in root.findall(
            ".//{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}ID/{http://uniprot.org/uniprot}fullName"):
        if name.text:
            gene_names.append(name.text)
    # Extract gene names from the alternativeName element
    for gene in root.findall(
            ".//{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}alternativeName/{http://uniprot.org/uniprot}fullName"):
        if gene.text:
            gene_names.append(gene.text)

    # Extract gene names from the name element in otherName
    for gene in root.findall(
            ".//{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}otherName/{http://uniprot.org/uniprot}name"):
        if gene.text:
            gene_names.append(gene.text)

    # Extract gene names from the name element in gene
    for gene in root.findall(".//{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}name"):
        if gene.text:
            gene_names.append(gene.text)

    return gene_names


def extract_entry_id(xml_content):
    root = ET.fromstring(xml_content)
    entry_id = ""

    for entry in root.findall(".//{http://uniprot.org/uniprot}entry"):
        entry_id = entry.get("id")
        break

    return entry_id


def extract_protein_name(xml_content):
    root = ET.fromstring(xml_content)
    protein_name = ""

    for name in root.findall(
            ".//{http://uniprot.org/uniprot}protein/{http://uniprot.org/uniprot}submittedName/{http://uniprot.org/uniprot}fullName"):
        if name.text not in " ":
            protein_name = name.text
            break

    if not protein_name:
        for name in root.findall(".//{http://uniprot.org/uniprot}protein/{http://uniprot.org/uniprot}recommendedName/{http://uniprot.org/uniprot}fullName"):
            if name.text not in " ":
                protein_name = name.text
                break

    if not protein_name:
        for name in root.findall(".//{http://uniprot.org/uniprot}protein/{http://uniprot.org/uniprot}recommendedName/{http://uniprot.org/uniprot}shortName"):
            if name.text not in " ":
                protein_name = name.text
                break

    if not protein_name:
        for name in root.findall(".//{http://uniprot.org/uniprot}protein/{http://uniprot.org/uniprot}recommendedName/{http://uniprot.org/uniprot}ecName"):
            if name.text not in " ":
                protein_name = name.text
                break

    if not protein_name:
        for name in root.findall(".//{http://uniprot.org/uniprot}protein/{http://uniprot.org/uniprot}name"):
            if name.text not in " ":
                protein_name = name.text
                break

    return protein_name


def get_protein_name(xml_string):
    root = ET.fromstring(xml_string)
    ns = {'uniprot': 'http://uniprot.org/uniprot'}
    name_element = root.find('.//uniprot:entry/uniprot:protein/uniprot:recommendedName/uniprot:fullName', ns)
    if name_element is not None:
        return name_element.text
    else:
        name_element = root.find('.//uniprot:entry/uniprot:protein/uniprot:submittedName/uniprot:fullName', ns)
        if name_element is not None:
            return name_element.text
        else:
            return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a UniProt entry ID as a command-line argument.")
        sys.exit(1)

    entry_id = sys.argv[1]
    xml_content = retrieve_uniprot_entry(entry_id)

    if xml_content:
        entry_id = extract_entry_id(xml_content)
        protein_name = extract_protein_name(xml_content)
        gene_names = extract_gene_names(xml_content)
        alternative_names = extract_alternative_names(xml_content)

        all_names = [entry_id, protein_name] + gene_names + alternative_names

        if all_names and len(all_names) > 2:
            print("/".join(filter(None, all_names)))
        else:
            protein_name = get_protein_name(xml_content) + "/"
            if protein_name:
                print(protein_name)
            else:
                print("Failed to retrieve protein name.")
    else:
        print("Failed to retrieve XML content.")
