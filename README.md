# ⚡ ELL URLS - The Most Powerful URL Gathering Tool

### 🔍 Developed by [Tanvir Ahammed](https://www.linkedin.com/in/tanvirahammedpentester/)

## 🚀 Overview

ELL URLS is a powerful Python-based URL gathering tool that integrates multiple passive and active reconnaissance techniques to extract and filter historical and live URLs. Ideal for bug bounty hunters, penetration testers, and OSINT professionals.

## 🛠️ Features

- ✅ Single or batch domain support
- ✅ Extension-based URL filtering (`.zip`, `.pdf`, etc.)
- ✅ Wayback Machine archival URL enumeration
- ✅ Integration with tools like `gau`, `waybackurls`, `hakrawler`, `katana`, `paramspider`, and more
- ✅ Automatically removes duplicates and saves clean output
- ✅ Option to define custom filename for final results


## 📦 Requirements

Make sure the following tools are installed:
```bash
gau
waybackurls
hakrawler
katana
paramspider
waybackpy
python3
pip install requests colorama termcolor pyfiglet
```

## 🚀 Usage

### Clone the Repository

```bash
git clone https://github.com/pentester-tanvir-ahammed/ell-urls.git
cd ell-urls
```

### Install Requirements

Ensure the following tools are installed on your system (if not, install via apt, go, or pip):

```bash
# Install Python dependencies
pip install requests colorama termcolor pyfiglet

# Install required tools (if not already installed)
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/hakluke/hakrawler@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
pip install waybackpy
# Clone ParamSpider separately if needed
```

Make sure all tools are in your `$PATH`.


### Run the Tool

```bash
python3 ellurls.py
```
You're getting the `externally-managed-environment` error because **Kali Linux uses PEP 668** to **protect its system-wide Python environment**. This prevents you from installing Python packages globally using `pip install` unless you explicitly bypass the protection — which is **not recommended** for system stability.

---

### Recommended Fix (Safe Way)

Use a **Python virtual environment** for your tool:

#### Create a virtual environment

```bash
sudo apt install python3-venv -y
python3 -m venv ell-env
```

#### Activate the virtual environment

```bash
source ell-env/bin/activate
```

#### Install Python dependencies *inside the venv*

```bash
pip install requests colorama termcolor pyfiglet
```

You can now safely run `ellurls.py` within the virtual environment without risking your system packages.


### 🧪 Example: Single Domain Mode

```text
Select mode (1: Single Domain, 2: Multiple Domains): 1
Enter the target domain (e.g., example.com): gov.sg
Use custom file extensions or load from extensions.txt? (custom/load): load
```


### 📂 Output

* Filtered URLs by extension saved in `/content/<domain>/`
* Enhanced gathered results saved in `enhanced_output_<domain>.txt`
* All **unique URLs** saved in a user-defined `.txt` file

