import json,pathlib,subprocess
root=pathlib.Path('/opt/openwebui-branding/sidebar-caption-20261027')
info=json.loads(subprocess.check_output(['docker','inspect','open-webui'],text=True))[0]
for file in ['custom.css','loader.js']:
    subprocess.run(['docker','cp','open-webui:/app/build/static/'+file,str(root/(file+'.before'))],check=True)
subprocess.run(['docker','build','--build-arg','BASE_IMAGE='+info['Image'],'-t','oracle-openwebui:sidebar-caption-20261027',str(root)],check=True)
for directory in ['/app/build/static/','/app/backend/open_webui/static/']:
    subprocess.run(['docker','cp',str(root/'assets')+'/.','open-webui:'+directory],check=True)
p=pathlib.Path('/opt/open-webui/start.sh');s=p.read_text();(root/'start.sh.before').write_text(s)
assert 'oracle-openwebui:login-heading-20261027' in s
p.write_text(s.replace('oracle-openwebui:login-heading-20261027','oracle-openwebui:sidebar-caption-20261027'))
print(json.dumps({'image':'oracle-openwebui:sidebar-caption-20261027','caption':'Oracle-OpenWebUI','font':'Oracle Sans','font_size':'7pt (9.333px)'}))
