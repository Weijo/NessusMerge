"""
Recursively searches given directory to find .nessus files.
Checks each file for duplicate elements and insert the host 
with more vulnerabilities found.

Default name exported is `merged_report.nessus`

Run it as such:
```bash
python3 nessusMerge.py -d nessus_directory
```

Specify the output name:
```bash
python3 nessusMerge.py -d nessus_directory -o new_name.nessus
```

Change the report name:
```bash
python3 nessusMerge.py -d nessus_directory -n report_name
```

Change report and output name:
```bash
python3 nessusMerge.py -d nessus_directory -n report_name -o new_name.nessus
```
"""
import argparse, os
import xml.etree.ElementTree as ET

def merge_report(mainTree, tree):
    """ 
    Merges mainTree and tree.
    
    Checks ReportHost on each tree and combine them.    
    The larger duplicate ReportHost tree will be combined.
    """
    mainReportElement = mainTree.findall('.//Report')[0]
    for host in tree.findall('.//ReportHost'):
        # Check for duplicate        
        hostname = host.attrib['name']
        existingHosts = mainTree.findall(f".//ReportHost[@name='{hostname}']")
        if existingHosts:            
            # Check which element is larger, replace the larger else do nothing
            if len(host.findall('.//ReportItem')) > len(existingHosts[0].findall('.//ReportItem')):
                mainReportElement.remove(existingHosts[0])
                mainReportElement.append(host)
            else:
                mainReportElement.append(host)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()    
    parser.add_argument('-d', '--directory', help='Directory that contains the nessus files', required=True)
    parser.add_argument('-o', '--output', help='Output file name', default='merged_report.nessus')    
    parser.add_argument('-n', '--name', help='Name of merged report')

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print('[!] Cannot find specified directory')       
        exit()

    nessusFiles = [os.path.join(args.directory, file) for file in os.listdir(args.directory) if file.endswith('.nessus')]
    if len(nessusFiles) == 0:
        print('[!] No .nessus files found!')        
        exit()
    else:         
        print(f'[*] Found {len(nessusFiles)} nessus files!')
    
    mainTree = None
    for file in nessusFiles:
        # Set first file as the main tree
        if not mainTree:            
            print(f'[*] Setting {file} as main file')
            mainTree = ET.parse(file)       
        else:
            print(f'[*] Merging {file}')            
            tree = ET.parse(file)
            merge_report(mainTree, tree)  


    if args.name:       
        print(f"[*] Setting report name to {args.name}")
        mainReportElement = mainTree.findall('.//Report')[0]        
        mainReportElement.attrib['name'] = args.name
        
    mainTree.write(args.output, encoding='utf-8', xml_declaration=True)    
    print(f'[+] Merged into {args.output}')
