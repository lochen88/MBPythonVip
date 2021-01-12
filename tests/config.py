# -*- coding:utf-8 -*-
from pathlib import Path
current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)

icon_path=f'{current_folder}/testjs/images/logo.ico'

mb_path=f'{father_folder}/mb.dll'
node_path=f'{father_folder}/node.dll'#vip-32bit名称必须固定node.dll

# mb_path=f'{father_folder}/mb_x64.dll'
# node_path=f'{father_folder}/miniblink_x64.dll'#vip-64bit名称必须固定miniblink_x64.dll
