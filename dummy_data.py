data =\
{
    'variables':
    {
        'machine_name': 'chicago_main',
        'user': 'maintenance',
        'target_dir': '/data/box'
    },
    'tasks':
    [
        {
            'type': 'copyFile',
            'blk_no': 1,
            'is_enabled': True,
            'params':
            {
                'filePath': './local',
                'to': '/data/remote',
                'ifTrue': 'True'
            }
        },
        {
            'type': 'getFileList',
            'blk_no': 2,
            'is_enabled': True,
            'params':
            {
                'fullPath': './input',
                'ifTrue': 'True',
                'inFolder': '/home/user/zip',
                'includes': 'all',
                'excludes': '*.jpg',
                'recurse': 'NO',
                'assign': 'best'
            }
        },
        {
            'type': 'copyFile',
            'blk_no': 5,
            'is_enabled': False,
            'params':
            {
                'filePath': './local',
                'to': '/data/remote',
                'ifTrue': ''
            }
        }
    ]
}
