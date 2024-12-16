# ConsenSGX

ConsenSGX: Scaling Anonymous Communications Networks with Trusted Execution Environments
https://petsymposium.org/2019/files/papers/issue3/popets-2019-0050.pdf

This repository provides the scripts and instructions for recreating the experiments and graphs produced in our paper.

<hr>
<h2>Parsing Tor Consensuses</h2>

This section deals with analysing previous Tor consensus, and the scripts for it are in the subfolder `Tor_consensus`, specifically it reproduces
Figure 2, 3 and 4 of the paper. 

Past Tor consensuses are available to download at the Tor Metrics page:
https://metrics.torproject.org/collector/archive/relay-descriptors/consensuses/

The corresponding relay descriptors for the relays in a consensus are available at:
https://metrics.torproject.org/collector/archive/relay-descriptors/server-descriptors/

To download the necessary consensus and server descriptors for your months of interest, you can either use the `download_tor_data.py` script or manually.
### **Manually**
Gather the consensuses and relay descriptors for the months of interest with which you want to plot the histograms of relay descriptor sizes from the Tor Metrics site into the Tor_conesnsus folder.
For each month, extract the consensus and server descriptors into folders labelled YEAR_MM, which should give you a folder YEAR_MM, with the subfolders
consensuses-YEAR-MM and server-descriptors-YEAR-MM.

The hist_plot.py script produces Fig 3 and 4. As is the script generates this for the first consensus of 2018-09.
Some of the relay descriptors in the consensus for a month aren't available in the server descriptors of that month (these are older descriptors that haven't changed since when they were published).
Hence gather upto 6 months of older server descriptors from the Metrics site, and store them in the same format as mentioned before.
### **Using the download_tor_data.py Script**

This script automates the process of downloading Tor consensus and relay descriptors for the specified months. It creates a folder structure for each year and month in the format `YEAR_MM/consensuses-YEAR-MM` and `YEAR_MM/server-descriptors-YEAR-MM`.

#### **How to use:**
1. **Install Dependencies:**
   - Before running the script, you need to install the required dependencies listed in `requirements.txt`. You can do this by running:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Script:**
   - To download the data for specific months, run the `download_tor_data.py` script as follows:

   ```bash
   python download_tor_data.py
   ```

   The script will download the data for all months defined in the `months_of_interest` list, and organize them into corresponding folders.

#### **Configuring months_of_interest:**
   - You can customize the `months_of_interest` list inside `download_tor_data.py` to specify which months you wish to download data for. Each entry should be in the format `YYYY-MM` (e.g., `2024-11`).

---

### **Generating Plots**

Once the necessary data has been downloaded, you can generate the desired plots as described below.

**1. Histograms of Relay Descriptor Sizes (Figures 3 and 4)**

The `hist_plot.py` script generates Figures 3 and 4 of the paper, which plot the relay descriptor sizes.

To use this script:
- Set the `TARGET_HIST_CONSENSUS` variable to point to the consensus file you want to plot the histogram for.
- Run the script:

```bash
python plot_hist.py
```

This will generate the two graphs:
- `hist_relays.png`
- `hist_relays_pruned.png` (this one has the histogram after pruning the policy and family fields of the relay descriptors as described in the paper).

**2. Bandwidth Curve (Figure 2)**

To generate the bandwidth curve, use the `bandwidth_curve.py` script. Set the `TARGET_CONSENSUS` variable to the consensus file you want to plot the bandwidth curve for, and run the script:

```bash
python bandwidth_curve.py
```

This will produce the bandwidth curve graph as `relays_bws.png`.

---

<hr>

<h2> PIR Experiments </h2>
The experiments for ConsenSGX leverage 3 different PIR systems: 
XPIR, Percy, and ZeroTrace.

Create a working directory, say `CONSENSGX_WD`, which will contain these 3 libraries.

**1) XPIR:**  
Clone the fork of XPIR available at:  
https://github.com/sshsshy/XPIR

Follow the build instructions on the same page.

**2) Percy:**  
Download the source files for Percy available at:  
http://percy.sourceforge.net/download.php

To build the library in the Percy folder:  
First edit the `Makefile` so that the `NTL` directory is `/usr/include/NTL` instead of `/usr/local/include/NTL`.

```bash
make depend
make
```

**3) ZeroTrace:**  
Clone the ZeroTrace library available at:  
https://github.com/sshsshy/ZeroTrace

To build the library in the ZeroTrace folder:

```bash
make clean
make
```

Once `CONSENSGX_WD` has been set up with the above three libraries, clone this repository into a directory for the experiment scripts, say `CONSENSGX_ES`.

The three main scripts are titled `run_experiments_xpir`, `run_experiments_percy.sh`, and `run_experiments_zt.sh`.

To run these scripts in the `CONSENSGX_ES` folder, invoke:

```bash
./run_experiments_XYZ.sh <relays_start> <relays_stop> <increment_additive> <block_size> 
                         <no_of_requests> <bulk_batch_size> <Full_path_to_CONSENSGX_WD>
```

Here:

- `<relays_start>` `<relays_stop>`: Sets the range of relays in a consensus to run experiments with.
- `<increment_additive>`: Sets the increment to iterate from `<relays_start>` to `<relays_stop>`.
- `<block_size>`: Sets the block size used by the PIR scheme. It should be set to the max relay descriptor size.
- `<bulk_batch_size>`: Sets the number of relay descriptors to fetch in a request.

Running any experiment will create a folder called `Results` in the `CONSENSGX_ES` folder, and store the results for the corresponding experiment in `Results/XYZ`.

Once the experiments have been run for the same set of parameters for all 3 PIR schemes, the `generate_graphs.py` script in `CONSENSGX_ES` can generate the graphs corresponding to these experiments by invoking:
```bash
./generate_graphs.py <relays_start> <relays_stop> <increment> <block_size> <no_of_req>
```

The script uses a statically defined list of `bulk_batch_sizes` ([10,50]), which we used for the paper. To try other values, simply redefine it to your required values and run the experiments for those `bulk_batch_sizes` before running the graphing script.

---

### **Requirements**
You will need the following Python packages:

**requirements.txt**  
```txt
requests
numpy
matplotlib
```

To install these dependencies, use:

```bash
pip install -r requirements.txt
```

---