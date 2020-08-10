data = {}

data['variables'] = []
data['variables'].append({
    'name': 'machine_name',
    'value': 'chicago_main'
})
data['variables'].append({
    'name': 'user',
    'value': 'maintenance'
})
data['variables'].append({
    'name': 'target_dir',
    'value': '/data/box'
})

data['tasks'] = []
data['tasks'].append({
    'type': 'file_copy',
    'blk_no': 1,
    'is_enabled': True,
    'params': {
        'source': './local',
        'target': '/data/remote',
        'buffer_size': '1024'
    }
})
data['tasks'].append({
    'type': 'unzip',
    'blk_no': 2,
    'is_enabled': True,
    'params': {
        'zipFilePath': './input/words.zip',
        'toDir': './local'
    }
})
data['tasks'].append({
    'type': 'file_copy',
    'blk_no': 3,
    'is_enabled': False,
    'params': {
        'source': './settings',
        'target': '/data/remote/settings',
        'buffer_size': '1024'
    }
})
