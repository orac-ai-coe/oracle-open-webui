import json,pathlib,subprocess
root=pathlib.Path('/opt/openwebui-branding/equal-logos-20261027')
info=json.loads(subprocess.check_output(['docker','inspect','open-webui'],text=True))[0]
subprocess.run(['docker','cp','open-webui:/app/build/static/oracle-openwebui.svg',str(root/'oracle-openwebui.svg.before')],check=True)
subprocess.run(['docker','build','--build-arg','BASE_IMAGE='+info['Image'],'-t','oracle-openwebui:equal-logos-20261027',str(root)],check=True)
for target in ['/app/build/static/oracle-openwebui.svg','/app/backend/open_webui/static/oracle-openwebui.svg']:
    subprocess.run(['docker','cp',str(root/'assets/oracle-openwebui.svg'),'open-webui:'+target],check=True)
p=pathlib.Path('/opt/open-webui/start.sh');s=p.read_text();(root/'start.sh.before').write_text(s)
assert 'oracle-openwebui:sidebar-branding-20261027' in s
p.write_text(s.replace('oracle-openwebui:sidebar-branding-20261027','oracle-openwebui:equal-logos-20261027'))
print(json.dumps({'image':'oracle-openwebui:equal-logos-20261027','applied':'live and startup static assets','icon_size':'32 x 32 for both'}))
