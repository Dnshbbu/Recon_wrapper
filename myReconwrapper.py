from subprocess import *
import argparse
import sys
import os
import sublist3r
from datetime import date
from datetime import datetime #need to be removed later
import pexpect
import re

parser = argparse.ArgumentParser(description='myAutomate recon script')

parser.add_argument('-f','--file', dest='file',help="input file")
parser.add_argument('-d','--domain', dest='domain',help="domain name")
#parser.add_argument('-n', type=int, default=2,metavar='integers',choices=[1, 2, 3], help="define the number of random integers")
#parser.add_argument('--name', required=True)

def recon(domain):
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d-%m-%Y-%H:%M:%S")
    workingdir = domain+"_"+d1#"_"+dt_string
    # os.mkdir(workingdir)
    os.makedirs(workingdir, exist_ok=True)
    # if not os.path.exists(os.path.dirname(workingdir)):
    #     os.makedirs(os.path.dirname(workingdir))
    # Create target Directory if don't exist
    # if not os.path.exists(workingdir):
    #     os.mkdir(workingdir)
    #     print("[*] Directory \'"+workingdir+"\' Created ")
    # else:    
    #     workingdir = domain+"_"+d1+"_"+dt_string
    #     os.mkdir(workingdir)
    #     print("[*] Directory \'"+workingdir+"\' already exists")
    
    os.chdir(workingdir) #move to working directory

    '''All the functions are below'''
    subdomains_res = SubdomainEnumeration(workingdir, domain)
    #httpprobe_res = httpprobedomain(workingdir,domain)
    screenshots_res = HttpProbesAndScreenshots(workingdir,domain)
    #portscan_res = PortScan(workingdir,domain)
    directorysearch_res = DirectorySearch(domain)

def SubdomainEnumeration(workingdir,domain): 
    print("=======================\n[+] Running sublist3r for "+domain+"\n=======================")
    subdomains = sublist3r.main(domain, 50,'sublister_subdomains.txt', ports= None,silent=False, verbose= True, enable_bruteforce= False, engines=None)
    ####subdomains = sublist3r.main(domain, no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines)

    print("=======================\n[+] Running amass for "+domain+"\n=======================")
    #amass_command = "amass enum -d "+domain+" --passive -o amass_subdomains.txt"
    #amass_command = "amass enum -d "+domain+" -active -o amass_subdomains.txt"
    #active & brute ->provides more active domains
    amass_command = "amass enum -d "+domain+" -active -brute -o amass_subdomains.txt"
    os.system(amass_command)

    print("=======================\n[+] Running assetfinder for "+domain+"\n=======================")
    assetfinder_command = "assetfinder -subs-only "+domain+"| tee assetfinder_subdomains.txt"
    #os.system(assetfinder_command)

    print("=======================\n[+] Subdomains cleanup for "+domain+"\n=======================")
    merge_command = "cat amass_subdomains.txt sublister_subdomains.txt assetfinder_subdomains.txt >> all_subdomains.txt"
    os.system(merge_command)
    uniq_command = "sort all_subdomains.txt |uniq > uniq_subdomains.txt"
    os.system(uniq_command)
    #cat uniq_subdomains.txt |wc -l

    return "success"


def HttpProbesAndScreenshots(workingdir,domain):  
    # test_command = "pwd"       
    # os.system(test_command)
    # os.chdir(workingdir)
    print("=======================\n[+] Running httprobe for "+domain+"\n=======================")
    httprobe_command = "cat uniq_subdomains.txt| httprobe >> subdomains.httpprobed"
    os.system(httprobe_command)

    print("=======================\n[+] Running Eyewitness & Aquatone for "+domain+"\n=======================")
    if not os.path.exists("Eyewitness-output"):        
        eyewitness_command = "eyewitness -f subdomains.httpprobed -d Eyewitness-output --timeout 10 --threads 20"
        aquatone_command  = "cat uniq_subdomains.txt | aquatone  -out Aqua-output" #-chrome-path /usr/bin/chromium : didtn work well
        os.system(aquatone_command)
        #gowitness file -s subdomains.httpprobed --threads 20 -d  Gowitness-output
        p = os.popen(eyewitness_command, "w")
        p.write("y\n")
        p.close()
        #p.write('\x03')
        #p.send_signal(signal.SIGINT)
        #p.stdout.close()
        #sys.exit()
        #print("[*] Screenshots taken. Find at "+workingdir+"/Eyewitness-output")
    else:    
        print("[*] Screens folder already exists")
    return "success"

def PortScan(workingdir,domain):  
    # test_command = "pwd"       
    # os.system(test_command)
    # os.chdir(workingdir)
    print("=======================\n[+] Running Nmap for All Subdomains of "+domain+"\n=======================")
    os.system("pwd")
    #nmap_command ="nmap -Pn -A -vvv -iL uniq_subdomains.txt -oA Nmap-results/nmap_results -p 80,443" 
    #Options to add:
    #-p0-65535,--top-ports
    #nmap_command ="nmap -sS -sV -Pn -vvv -iL uniq_subdomains.txt -oA nmap_results -p 80,443"
    nmap_command ="nmap -sS -sV -p0-65535 -Pn -vvv -iL uniq_subdomains.txt -oA nmap_results"
    os.system(nmap_command)
    convert_to_html = "xsltproc nmap_results.xml -o nmap_results.html"
    os.system(convert_to_html)
    os.mkdir("Nmap-output")
    move_to_nmap_folder = "mv nmap* Nmap-output/" #move all nmap files to Nmap-output folder
    os.system(move_to_nmap_folder)
    os.system("pwd")
    return "success"
    #nmap -Pn -A -vvv -iL uniq_subdomains.txt -oA nmap_results --top-ports
    #xsltproc nmap_results_1.xml -o nmapnew.html 
    #-p0-65535 
    #masscan -iL uniq_subdomains.txt ‐‐top-ports 100 -oX massresults ‐‐echo > scan.txt !!!!ONly ip addresses can be given as input!!!!!
    
    #proc.stdin.write("y\n")
    #output = proc.communicate("y")  # send 1 to test.exe 
    #print(output) 

def DirectorySearch(domain):
    os.system("pwd")
    os.mkdir("ffuf-output")
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    with open("subdomains.httpprobed", "r") as httpprobedfile:
        for each_url_unstriped in httpprobedfile:
            each_url = each_url_unstriped.strip()
            url = each_url+"/FUZZ"
            m = re.search('https?://([A-Za-z_0-9.-]+).*', each_url) #to get the host part in url
            #gobuster_command = "gobuster dir -w "+wordlist+" -t 40 -e -o gobuster_"+m.group(1)+".txt -u "+each_url
            ffuf_command= "ffuf -w "+wordlist+" -u "+url+" -of html -o ffuf-output/"+m.group(1)+".html"
            print(ffuf_command)
            #p = os.popen(gobuster_command, "w")
            p = os.popen(ffuf_command, "w")
            #p.write("y\n")
            p.close()            
            print(ffuf_command)
            #os.system(gobuster_command)
    return "success"



def main():
    args = parser.parse_args()
    if (args.domain):
        domain = args.domain
        print("=======================\n[+] Recon started for  "+domain+"\n=======================")
        recon(domain)

    if (args.file):
        with open(args.file, "r") as domainfile:
            for domain in domainfile:
                DomainStriped = domain.strip()
                print("=======================\n[+] Recon started for  "+DomainStriped+"\n=======================")
                recon(DomainStriped)
                os.chdir("..") # go to the root directory /AutomateRecon
                



if __name__=="__main__":
    main()

# n = args.n

# for i in range(n):
#     print(random.randint(-100, 100))



# if args.output:
#     print("This is some output")
# print(args.name)
