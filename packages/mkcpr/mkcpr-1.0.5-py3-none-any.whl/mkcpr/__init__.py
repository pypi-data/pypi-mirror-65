'''
mkcpr "Competitive programming reference builder tool"
Copyright (C) 2020  Sergio G. Sanchez V.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''


from os import listdir, getcwd
from os.path import isfile, isdir, join
import re
import json
import sys

codeFolder = "Reference"
templatePath = "ReferenceTemplate.tex"
outputFilePath = "Reference.tex"

excluded = set(['.vscode', '__pycache__'])
numberOfColumns = 2
TextToReplaceInTemplate = "CODE HERE"

sortBefore = set()
sortAfter = set()


output = ""


def printSectionType(sectionName, depth, isFile):
    global output
    vspace = 0
    style = '\\bfseries\\sffamily\\centering'
    if depth == 1:
        sectionType = 'section'
        style += '\\Huge'
        vspace = 2
    elif depth == 2:
        sectionType = 'subsection'
        style += '\\LARGE'
        vspace = 1
    elif depth == 3:
        sectionType = 'subsubsection'
        style += '\\Large'
        vspace = 1
    else:
        sectionType = 'paragraph'
        style += '\\large'
        vspace = 1
    if isFile:
        sectionName = sectionName[:sectionName.rfind('.')]
        style = '\\large\\bfseries\\sffamily\\underline'
        vspace = 0
    sectionName = sectionName.replace("_", " ")
    output += '\\' + sectionType + 'font{' + style + '}\n'
    if vspace:
        output += '\\vspace{' + str(vspace - 1) + 'em}\n'
    output += '\\' + sectionType + '*{' + sectionName + '}\n'
    if depth == 1:
        output += '\\markboth{' + sectionName.upper() + '}{}\n'
    output += '\\addcontentsline{toc}{' + sectionType + '}{' + sectionName + '}\n'
    if vspace:
        output += '\\vspace{' + str(vspace + 1) + 'em}\n'


def needspaceForDepth(depth):
    if depth == 1:
        needspace = 4
    elif depth == 2:
        needspace = 3
    elif depth == 3:
        needspace = 2
    else:
        needspace = 1
    return needspace


def printFile(path, depth, sections):
    global output
    global numberOfColumns

    extension = sections[-1][sections[-1].rfind('.') + 1:]
    if extension == 'tex':
        output += '\\end{multicols*}\n'
        for i in range(len(sections)):
            printSectionType(sections[i], depth -
                             len(sections) + i + 1, i == len(sections) - 1)
        with open(path) as f:
            output += f.read() + '\n'
        output += '\\begin{multicols*}{' + str(numberOfColumns) + '}\n'
        return
    if extension == 'h':
        extension = 'cpp'
    with open(path, 'r') as f:
        content = f.read()
    firstLine = content[:content.find('\n') + 1]
    needspace = 0
    if re.fullmatch(' *(?:#|(?://)) ?[1-9][0-9]*\\n', firstLine):
        content = content[len(firstLine):]
        needspace = int(firstLine.strip()[2:].strip())
    for i in range(len(sections)):
        needspace += needspaceForDepth(depth - i)
    output += '\\needspace{' + str(needspace) + '\\baselineskip}\n'
    for i in range(len(sections)):
        printSectionType(sections[i], depth -
                         len(sections) + i + 1, i == len(sections) - 1)
    content = '\\begin{minted}{' + extension + '}\n' + content
    needspaces = set(re.findall(' *(?:#|(?://)) ?[1-9][0-9]*\\n', content))
    for needspace in needspaces:
        news = ''\
            '\\end{minted}\n'\
            '\\vspace{-12pt}\n'\
            '\\needspace{' + needspace.strip()[2:].strip() + '\\baselineskip}\n'\
            '\\begin{minted}{' + extension + '}\n'
        content = content.replace(needspace, news)
    content += '\n\\end{minted}\n'
    output += content + '\n'


def buildOutput(currPath, depth, sections):
    global excluded
    if len(sections) and sections[-1] in excluded:
        return
    sortedDirs = sorted(
        listdir(currPath),
        key=lambda x: (
            x in sortAfter,
            x not in sortBefore,
            isdir(join(currPath, x)),
            x.split('.')[0].lower()
        )
    )
    isFirst = True
    for dirOrFile in sortedDirs:
        f = join(currPath, dirOrFile)
        if isdir(f):
            if isFirst:
                isFirst = False
                sections.append(dirOrFile)
                buildOutput(f, depth + 1, sections)
            else:
                buildOutput(f, depth + 1, [dirOrFile])
        elif isfile(f) and re.fullmatch('.+\\.(cpp|c|py|java|tex)', dirOrFile):
            if isFirst:
                isFirst = False
                sections.append(dirOrFile)
                printFile(f, depth + 1, sections)
            else:
                printFile(f, depth + 1, [dirOrFile])
                
def outputConfigFile():
	configJson = {}
	configJson["codeFolder"] = "/home/san/Projects/mkcpr/CodeFolderExample"
	configJson["templatePath"] = "/home/san/Projects/mkcpr/template.tex"
	configJson["outputFilePath"] = "/home/san/Projects/mkcpr/output.tex"
	configJson["excluded"] = [".vscode", "__pycache__"]
	configJson["columns"] = 2
	configJson["templatePlaceHolder"] = "CODE HERE"
	configJson["sortBefore"] = ["Data Structures"]
	configJson["sortAfter"] = ["Extras"]
	with open('mkcpr-config.json', 'w') as f:
		json.dump(configJson,f, indent=2)


def main():
    global codeFolder
    global templatePath
    global outputFilePath
    global excluded
    global numberOfColumns
    global TextToReplaceInTemplate
    global sortBefore
    global sortAfter
    global output

    codeFolder = "Reference"
    templatePath = "ReferenceTemplate.tex"
    outputFilePath = "Reference.tex"

    excluded = set(['.vscode', '__pycache__'])
    numberOfColumns = 2
    TextToReplaceInTemplate = "CODE HERE"

    sortBefore = set()
    sortAfter = set()
    output = ""
    if sys.version_info[0] < 3:
        print("Error: Use python 3.5+ to execute this script")
        exit(0)
    configFilePath = join(getcwd(), "mkcpr-config.json")

    if (len(sys.argv) == 2 and sys.argv[1] == "-h"):
        print("Usage:")
        print("\tmkcpr [CONFIG FILE PATH]")
        exit(0)
    if (len(sys.argv) == 2 and sys.argv[1] == "-c"):
        outputConfigFile()
        print("Configuration file written in " + getcwd() + "/mkcpr-config.json")
        exit(0)

    if (len(sys.argv) == 2):
        configFilePath = sys.argv[1]

    try:
        with open(configFilePath, 'r') as f:
            try:
                config = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                print("Error: Malformed configuration file")
                exit(0)
            try:
                codeFolder = config["codeFolder"]
                templatePath = config["templatePath"]
                outputFilePath = config["outputFilePath"]
            except KeyError as e:
                print("Error: Invalid config file. Missing", e, "entry in config file")
                exit(0)
            if "excluded" in config:
                excluded = set(config["excluded"])
            if "columns" in config:
                numberOfColumns = config["columns"]
            if "templatePlaceHolder" in config:
                TextToReplaceInTemplate = config["templatePlaceHolder"]
            if "sortBefore" in config:
                sortBefore = set(config["sortBefore"])
            if "sortAfter" in config:
                sortAfter = set(config["sortAfter"])
    except FileNotFoundError:
        print("Error: Configuration file not found in \"" + configFilePath + "\"")
        print("To create a new configuration file use the -c flag")
        exit(0)
    sections = []
    if not isdir(codeFolder):
        print("Error: Code Folder \"" + codeFolder + "\" not found.")
        exit(0)
    buildOutput(codeFolder, 0, sections)
    try:
        with open(templatePath, 'r') as f:
            template = f.read()
            output = template.replace(TextToReplaceInTemplate, output)
            try:
                with open(outputFilePath, 'w+') as f2:
                    f2.write(output)
                    print("Tex file written in \"" + outputFilePath + "\"")
            except IOError:
                print("Cannot write \"" + outputFilePath + "\"")
                exit(0)
    except FileNotFoundError:
        print("Error: Tex template not found in \"" + templatePath + "\"")
        exit(0)
