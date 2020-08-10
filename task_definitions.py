# arguments go as
# [
#   name,
#   default value,
#   'O' for optional, or 'M' for mandatory,
#   tooltip
# ]

definitions =\
[
    {
        'name': 'if',
        'arguments':
        [
            ['ifTrue', 'True', 'O', 'condition for task to run'],
            ['condition', '', 'M', 'condition to evaluate']
        ]
    },
    {
        'name': 'for',
        'arguments':
            [
                ['ifTrue', 'True', 'O', 'condition for task to run'],
                ['rangeArgs', '', 'O', 'range of numbers for iteration'],
                ['list', '[]', 'O', 'list of items to iterate thru'],
                ['item', 'item', 'O', 'variable carrying the value of iteration']
            ]
    },
    {
        'name': 'fileExist',
        'arguments':
            [
                ['ifTrue', 'True', 'O', 'condition for task to run'],
                ['filePath', '', 'M', 'path to file or folder'],
                ['assign', '', 'M', 'variable to assign the return']
            ]
    },
    {
        'name': 'copyFile',
        'arguments':
            [
                ['ifTrue', 'True', 'O', 'condition for task to run'],
                ['filePath', '', 'M', 'file to copy from'],
                ['to', '', 'M', 'full path name to copy to']
            ]
    },
    {
        'name': 'readFile',
        'arguments':
            [
                ['ifTrue', 'True', 'O', 'condition for task to run'],
                ['filePath', '', 'M', 'full file path'],
                ['assign', '', 'M', 'variable to hold content of file']
            ]
    },
    {
        'name': 'unzip',
        'arguments':
            [
                ['ifTrue', 'True', 'O', 'condition for task to run'],
                ['zipFilePath', '', 'M', 'full path to zip file'],
                ['toDir', '', 'M', 'folder location to unzip'],
                ['passwd', '', 'O', 'password of zip file']
            ]
    },
    {
        'name': 'getFileList',
        'arguments':
            [
                ['ifTrue', 'True', 'O', 'condition for task to run'],
                ['inFolder', '', 'M', 'folder to get file list'],
                ['includes', '', 'M', 'pattern of files to include'],
                ['excludes', '', 'M', 'pattern of files to exclude'],
                ['recurse', 'NO', 'O', 'recurse thru sub folders'],
                ['fullPath', 'NO', 'O', 'should the response contain full path of filenames'],
                ['assign', '', 'M', 'variable to assign the result']
            ]
    }
]
