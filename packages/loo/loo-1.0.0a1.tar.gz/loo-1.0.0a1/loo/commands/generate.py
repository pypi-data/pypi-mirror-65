import os
import click

from ..cli import main

@click.command(name='g', help='Generate react component including test and styles files')
@click.argument('componentname')
@click.option('--skiptest', is_flag=True, help='Skip test file')
@click.option('--skipstyles', is_flag=True, help='Skip style file')
def generate(componentname, skiptest, skipstyles):
    folderExists = os.path.exists(componentname)

    if folderExists == False:
        os.mkdir(componentname)
        os.chdir(componentname)
        _createComponentFile(componentname)

        if skiptest == False:
            _createTestFile(componentname)

        if skipstyles == False:
            _createStylesFile(componentname)

        print(componentname + " generated")
    else:
        print("Component already exists!")

main.add_command(generate)

def _createComponentFile(name):
    file = open(name + ".tsx", "w")
    file.writelines([
        "import React from 'react';",
        "\n",
        "\nconst " + name + " = () => {",
        "\n  return (",
        "\n    <div>" + name + "</div>",
        "\n  );",
        "\n}",
        "\n",
        "\nexport default " + name
    ])
    
    file.close()

def _createTestFile(name):
    file = open(name + ".test.tsx", "w")
    file.write("Test")
    file.close()

def _createStylesFile(name):
    file = open(name + ".styles.tsx", "w")
    file.write("Styles")
    file.close()
