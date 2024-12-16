import os
import requests
import tarfile

base_url_server = "https://collector.torproject.org/archive/relay-descriptors/server-descriptors/server-descriptors-{month}.tar.xz"
base_url_consensus = "https://collector.torproject.org/archive/relay-descriptors/consensuses/consensuses-{month}.tar.xz"

months_of_interest = ["2024-10", "2024-11"]  # Add the months for which tor data needs to be downloaded
output_dir = "./Tor_consensus"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


for month in months_of_interest:
    print(f"Processing data for {month}...")
    folder_name = month.replace("-", "_")
    month_folder_path = os.path.join(output_dir, folder_name)
    if not os.path.exists(month_folder_path):
        os.makedirs(month_folder_path)

    consensus_folder = os.path.join(month_folder_path, f"consensuses-{month}")
    server_descriptors_folder = os.path.join(month_folder_path, f"server-descriptors-{month}")

    os.makedirs(consensus_folder, exist_ok=True)
    os.makedirs(server_descriptors_folder, exist_ok=True)

    server_file_url = base_url_server.format(month=month)
    consensus_file_url = base_url_consensus.format(month=month)

    server_file_path = os.path.join(month_folder_path, f"server-descriptors-{month}.tar.xz")
    consensus_file_path = os.path.join(month_folder_path, f"consensuses-{month}.tar.xz")

    response = requests.get(server_file_url, stream=True)
    with open(server_file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    with tarfile.open(server_file_path, "r:xz") as tar:
        for member in tar.getmembers():
            member.name = os.path.basename(member.name)  # Avoid nested folders
            tar.extract(member, server_descriptors_folder)
    os.remove(server_file_path)
    print("Server-descriptors downloaded and extracted successfully.")


    response = requests.get(consensus_file_url, stream=True)
    with open(consensus_file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    with tarfile.open(consensus_file_path, "r:xz") as tar:
        for member in tar.getmembers():
            member.name = os.path.basename(member.name)  # Avoid nested folders
            tar.extract(member, consensus_folder)
    os.remove(consensus_file_path)
    print("Consensuses downloaded and extracted successfully.")

print("All data processed successfully.")
