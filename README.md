# 🧩 prosub

**prosub** is a simple CLI tool that retrieves subdomains from the [Profundis](https://profundis.io) API.  



## ⚙️ Installation

```
git clone https://github.com/badcrack3r/prosub.git
cd prosub
chmod +x prosub.py
```

## required package


```
pip install requests

```

🚀 Usage

1. Get your profundis.io API key from https://profundis.io/profile

2. Set your Profundis API key

```
export PROFUNDIS_API_KEY="your_api_key"
```

3. Fetch subdomains



Example usage: 

```

# Single -d domain

python3 prosub.py -d example.com

# Multiple -d domains
python3 prosub.py -d example.com -d sub-domain.com

# Domains from a file
python3 prosub.py -f domains.txt



```
