# -*- coding:utf-8 -*-
import os
import sys
from pathlib import Path
current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))
sys.path.append(father_folder)


from MBPythonVip import miniblink 

from config import node_path,mb_path
mbpython=miniblink.Miniblink
mb=mbpython.init(node_path,mb_path)
wke=mbpython(mb)

def test():   
    if mb==0:return
    window=wke.window
    callback=wke.callback
    network=wke.network

    webview=window.mbCreateWebWindow(0,0,0,0,860,760)
    callback.mbOnDestroy(webview)
    network.mbLoadURL(webview,'https://www.baidu.com/')
    window.mbMoveToCenter(webview)
    window.mbShowWindow(webview)
    window.message_loop()

if __name__=='__main__':
    test()
    ...
