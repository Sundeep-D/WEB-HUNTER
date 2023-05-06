![Webhunter](https://github.com/Sundeep-D/WEB-HUNTER/raw/v1.1/bg.png)


# WEB HUNTER

Web Hunter is an automated web reconnaissance tool that utilizes the power of Python programming language to perform a thorough analysis of a target website. This standalone software tool offers comprehensive data on the target website, including header details, Whois information, SSL certificate information, crawler data, DNS enumeration, subdomain enumeration, directory searching, port scanning, and export information in .pdf format.




## Run Locally

Clone the project

```bash
  git clone https://github.com/Sundeep-D/WEB-HUNTER
```
Install dependencies

```bash
  pip install -r requirements.txt
```

Run main file

```bash
  python web-hunter.py
```


## Build executable file

Build with pyinstaller

```bash
  pyinstaller main.spec
```

## Download exe file

This is a stable executable file. Download
[here](https://github.com/Sundeep-D/WEB-HUNTER/releases/download/v2.0/WEB.HUNTER.exe)

*Note: Windows defender will restrict to run this file but bypass and run the file "Run Anyway"*

## Usage/Examples

1. Double-click on the executable file generator in dist folder to launch the application.
2. Enter the target website's URL (For example: www.amazon.in) and click on the "Scan" button.
3. The application will provide a detailed overview of the target website.
4. Click export button on left side to save results in .pdf format 

## Reference
The reference section acknowledges that some of the helper classes used in the development of the tool were sourced from the GitHub repository belonging to thewhiteh4t, namely FinalRecon.