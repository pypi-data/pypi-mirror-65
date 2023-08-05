from os.path import dirname, basename, isfile, join
import os
import sys
import glob
import argparse		
import shaonutil
import ast

def show_info(functionNode,ModuleName,classobj=""):
    str_ = ""

    if classobj != "":
    	Parameters = [arg.arg for arg in functionNode.args.args if arg.arg != 'self']
    	classobj = getattr(__import__(ModuleName), classobj.name)
    	funcobj = getattr(classobj,functionNode.name)
    	if funcobj.__doc__ != None:
    		str_ += "&nbsp;&nbsp;&nbsp;&nbsp;Function **"+ functionNode.name +"("+ ','.join(Parameters) +")** -> Description: " + funcobj.__doc__ + "<br>\n"
    	else:
    		str_ += "&nbsp;&nbsp;&nbsp;&nbsp;Function **"+ functionNode.name+"("+ ','.join(Parameters) +")**" + "<br>\n"
    else:
    	Parameters = [arg.arg for arg in functionNode.args.args]
    	funcobj = getattr(__import__(ModuleName), functionNode.name)
    	if funcobj.__doc__ != None:
    		str_ += "Function **" + functionNode.name +"("+ ','.join(Parameters) +")** -> Description: " + funcobj.__doc__ + "<br>\n"
    	else:
    		str_ += "Function **" + functionNode.name +"("+ ','.join(Parameters) +")**" + "<br>\n"
    #import pdb; pdb.set_trace()
    return str_
        

def generateModuleFunctionUsageString(ModuleName):
    with open(ModuleName+".py", encoding="utf8") as file:
        node = ast.parse(file.read())

    functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]

    full_string = ""

    
    for function in functions:
    	full_string += show_info(function,ModuleName)

    for class_ in classes:
        classobj = getattr(__import__(ModuleName), class_.name)
        if classobj.__doc__ != None:
        	full_string += "Class **" + class_.name + "** -> Description: " + classobj.__doc__ + "<br>\n"
        else:
        	full_string += "Class **" + class_.name + "**<br>\n"

        methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
        for method in methods:
            full_string += show_info(method,ModuleName,classobj=class_)

    return full_string

def generateDirFunctionUsageString():
    full_string = ""
    
    modules = glob.glob(join(os.getcwd(), "*.py"))
    __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

    for ModuleName in __all__:
    	if ModuleName != "__init__" and ModuleName+'.py' != basename(__file__):
            #ModuleName = "mysqlDB.py"
            ModuleName = ModuleName.split('.')[0]
            Module = __import__(ModuleName)
            full_string += "### " + str(Module.__doc__) + "\n" + generateModuleFunctionUsageString(ModuleName)
    
    return full_string



def get_members(module):
	return [member for member in dir(module) if callable(getattr(module, member))]

def get_file_description_file(module):
	member_doc_dic = {}
	for member in get_members(module):
		if getattr(module, member).__doc__ != None:
			member_doc_dic[member] = getattr(module, member).__doc__
	return member_doc_dic

def createNewReadme():
	name = input("Project Name:")
	version = input("Project Version:")
	tag = input("Project Tag:")
	author = input("Project Author:")
	contact = input("Project Contact:")
	installation = input("Installation Link/String:")
	
	final_string_to_save = f"""# {name}  - {version}
## {tag}

Stable Version - {version}<br>
Author: {author}<br>
Contact: {contact}

## Area of Utilities

## Installation
<code>{installation}</code>
## Function Usages

Function Usages End


## Versioning 

*major.minor[.maintenance[.build]]* (example: *1.4.3.5249*)

adoption: major.minor.patch.maintenance.status.trials_for_success

The last position

- 0 for alpha (status) 
- 1 for beta (status)
- 2 for release candidate
- 3 for (final) release

For instance:

- 1.2.0.1 instead of 1.2-a1
- 1.2.1.2 instead of 1.2-b2 (beta with some bug fixes)
- 1.2.2.3 instead of 1.2-rc3 (release candidate)
- 1.2.3.0 instead of 1.2-r (commercial distribution)
- 1.2.3.5 instead of 1.2-r5 (commercial distribution with many bug fixes)"""
	return final_string_to_save

def generateFunctionUsagesString(realcurrentpath):
	#list all py modules in current directory
	all_py_files = glob.glob(join(realcurrentpath, "*.py"))
	allmodules = [basename(c)[:-3] for c in all_py_files if isfile(c) and not c.endswith('__init__.py')]

	#get function usages lines
	func_usages_string = ''
	for m in allmodules:
		module_heading = '### '+m+'\n\n'
		module = __import__(m)
		member_doc_dic = get_file_description_file(module)
		func_lines = ''
		for member in member_doc_dic:
			func_lines += member + ' - ' + member_doc_dic[member] + '\n\n'
		func_usages_string += module_heading + func_lines

	return func_usages_string

def init(args):
	printline=True

	realcurrentpath = os.path.realpath('')
	sys.path.append(realcurrentpath)

	if args.output:
		outputfile = args.output
	else:
		outputfile = 'docu.md'

	outputfile = os.path.join(realcurrentpath, outputfile)

	if args.readme == 'bare':
		alllines = createNewReadme()
	else:
		readmefilename = args.readme
		filerealpath = os.path.join(realcurrentpath, readmefilename)
		# read the contents of your README file
		lines = shaonutil.file.read_file(filerealpath)
		alllines = '\n'.join(lines)

	start = '## Function Usages'
	end = 'Function Usages End'

	func_usages_string = start + '\n\n' + generateDirFunctionUsageString() + '\n\n' + end

	
	deductlines = alllines[ alllines.index(start):alllines.index(end)+len(end) ]

	#replacing existing lines with prepared lines
	final_string_to_save = alllines.replace(deductlines,func_usages_string)

	if(printline):print(final_string_to_save)
	shaonutil.file.write_file(outputfile, final_string_to_save,mode="w")

def main():
	parser = argparse.ArgumentParser(description="Automatic Documentation Generator")
	parser.add_argument("--readme", help="input the sample readme file",type=str,required=True)
	parser.add_argument("--output", help="input the outputfile file",type=str)
	args = parser.parse_args()

	try:
		init(args)
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()
