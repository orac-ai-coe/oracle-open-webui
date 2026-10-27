import json,pathlib,subprocess
root=pathlib.Path('/opt/openwebui-branding/sidebar-20261027')
root.chmod(0o700)
info=json.loads(subprocess.check_output(['docker','inspect','open-webui'],text=True))[0]
p=root/'container-before.json';p.write_text(json.dumps(info,indent=2));p.chmod(0o600)
subprocess.run(['docker','build','--build-arg','BASE_IMAGE='+info['Image'],'-t','oracle-openwebui:sidebar-branding-20261027',str(root)],check=True)
