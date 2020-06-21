# Recon_wrapper
This script wraps the multiple tools into the below categories. 
1. Subdomain enumeration
    - sublist3r
    - Amass
    - Assetfinder
2. Http probes and Screenshots
    - httprobe, assetfinder, hakrawler
    - Eyewitness
    - Aquatone
3. Port scan
    - Nmap
4. Directory search
    - gobuster
    - ffuf

## Usage
There are two ways to invoke the script
1. By providing domain name
`./myReconwrapper.py -d <domain-to-test>`
2. By providing a list of domains
`./myReconwrapper.py -f domains.txt`

This script is work in progress. It is lacking lot of clean up and addition of tools.

### !!! Important !!!
This script will produce a lot of traffic. Use it wisely. Feel free to comment out the tools invocation in the script. 
I am not responsible for misuse of this repository. Use at your own risk.

### References:
- [Amass](https://github.com/OWASP/Amass)
- [Assetfinder](https://github.com/tomnomnom/assetfinder)
- [httprobe](https://github.com/tomnomnom/httprobe)
- [hakrawler](https://github.com/hakluke/hakrawler)
- [Eyewitness](https://github.com/FortyNorthSecurity/EyeWitness)
- [Aquatone](https://github.com/michenriksen/aquatone)
- [gobuster](https://github.com/OJ/gobuster)
- [ffuf](https://github.com/ffuf/ffuf)

