import datetime, json, pathlib, subprocess
root=pathlib.Path('/opt/openwebui-branding/20261027')
root.mkdir(parents=True, exist_ok=True)
root.chmod(0o700)
def run(*args): return subprocess.check_output(args, text=True)
info=json.loads(run('docker','inspect','open-webui'))[0]
(root/'container-before.json').write_text(json.dumps(info,indent=2))
(root/'container-before.json').chmod(0o600)
for source,target in [('/app/backend/open_webui/env.py','env.py'),('/app/backend/open_webui/routers/openai.py','openai.py'),('/app/build/index.html','index.html')]:
    subprocess.run(['docker','cp',f'open-webui:{source}',str(root/target)], check=True)
    (root/(target+'.before')).write_bytes((root/target).read_bytes())
p=root/'env.py'; s=p.read_text()
old="WEBUI_NAME = os.getenv('WEBUI_NAME', 'Open WebUI')\nif WEBUI_NAME != 'Open WebUI':"
assert old in s
p.write_text(s.replace(old,"WEBUI_NAME = os.getenv('WEBUI_NAME', 'Oracle - OpenWebUI')\nif 'openwebui' not in WEBUI_NAME.lower().replace(' ', ''):"))
p=root/'index.html'; s=p.read_text(); assert '<title>Open WebUI</title>' in s
p.write_text(s.replace('<title>Open WebUI</title>','<title>Oracle - OpenWebUI</title>'))
# Preserve static source and served files for rollback before staging the overlay.
subprocess.run(['docker','exec','open-webui','sh','-c','mkdir -p /app/backend/data/backups/branding-20261027 && cp /app/build/static/loader.js /app/backend/data/backups/branding-20261027/loader.js && cp /app/build/static/custom.css /app/backend/data/backups/branding-20261027/custom.css'],check=True)
subprocess.run(['docker','build','--build-arg','BASE_IMAGE='+info['Image'],'-t','oracle-openwebui:branding-20261027',str(root)],check=True)
print(json.dumps({'image':'oracle-openwebui:branding-20261027','base':info['Image'],'backup':str(root)}))
