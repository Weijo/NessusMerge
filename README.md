# NessusMerge

This script combines multiple `.nessus` files into a single nessus file. It checks for duplicate hosts and chooses the host with the larger number of `ReportItem`.

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
