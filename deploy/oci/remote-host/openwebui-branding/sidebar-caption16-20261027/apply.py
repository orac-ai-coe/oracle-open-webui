import json,pathlib,subprocess
root=pathlib.Path('/opt/openwebui-branding/sidebar-caption16-20261027')
subprocess.run(['docker','cp','open-webui:/app/build/static/custom.css',str(root/'custom.css.before')],check=True)
subprocess.run(['docker','build','--build-arg','BASE_IMAGE=oracle-openwebui:sidebar-caption-20261027','-t','oracle-openwebui:sidebar-caption16-20261027',str(root)],check=True)
for directory in ['/app/build/static/','/app/backend/open_webui/static/']:
    subprocess.run(['docker','cp',str(root/'assets/custom.css'),'open-webui:'+directory+'custom.css'],check=True)
p=pathlib.Path('/opt/open-webui/start.sh');s=p.read_text();(root/'start.sh.before').write_text(s)
assert 'oracle-openwebui:sidebar-caption-20261027' in s
p.write_text(s.replace('oracle-openwebui:sidebar-caption-20261027','oracle-openwebui:sidebar-caption16-20261027'))
print(json.dumps({'image':'oracle-openwebui:sidebar-caption16-20261027','font_size':'16px','line_height':'20px'}))
