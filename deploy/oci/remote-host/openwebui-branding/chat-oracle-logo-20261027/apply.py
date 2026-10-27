import json,pathlib,subprocess
root=pathlib.Path('/opt/openwebui-branding/chat-oracle-logo-20261027')
for file in ['custom.css','loader.js']:
    subprocess.run(['docker','cp','open-webui:/app/build/static/'+file,str(root/(file+'.before'))],check=True)
subprocess.run(['docker','build','--build-arg','BASE_IMAGE=oracle-openwebui:sidebar-caption16-20261027','-t','oracle-openwebui:chat-oracle-logo-20261027',str(root)],check=True)
for directory in ['/app/build/static/','/app/backend/open_webui/static/']:
    subprocess.run(['docker','cp',str(root/'assets')+'/.','open-webui:'+directory],check=True)
p=pathlib.Path('/opt/open-webui/start.sh');s=p.read_text();(root/'start.sh.before').write_text(s)
assert 'oracle-openwebui:sidebar-caption16-20261027' in s
p.write_text(s.replace('oracle-openwebui:sidebar-caption16-20261027','oracle-openwebui:chat-oracle-logo-20261027'))
print(json.dumps({'image':'oracle-openwebui:chat-oracle-logo-20261027','chat_welcome_logo':'Oracle O'}))
