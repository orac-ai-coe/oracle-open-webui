import json,pathlib,subprocess
root=pathlib.Path('/opt/openwebui-branding/login-heading-20261027')
info=json.loads(subprocess.check_output(['docker','inspect','open-webui'],text=True))[0]
for file in ['custom.css','loader.js','oracle-openwebui.svg']:
    subprocess.run(['docker','cp','open-webui:/app/build/static/'+file,str(root/(file+'.before'))],check=True)
subprocess.run(['docker','build','--build-arg','BASE_IMAGE='+info['Image'],'-t','oracle-openwebui:login-heading-20261027',str(root)],check=True)
for file in ['custom.css','loader.js','oracle-openwebui.svg']:
    for directory in ['/app/build/static/','/app/backend/open_webui/static/']:
        subprocess.run(['docker','cp',str(root/'assets'/file),'open-webui:'+directory+file],check=True)
p=pathlib.Path('/opt/open-webui/start.sh');s=p.read_text();(root/'start.sh.before').write_text(s)
assert 'oracle-openwebui:equal-logos-20261027' in s
p.write_text(s.replace('oracle-openwebui:equal-logos-20261027','oracle-openwebui:login-heading-20261027'))
print(json.dumps({'image':'oracle-openwebui:login-heading-20261027','applied':'live and startup static assets'}))
