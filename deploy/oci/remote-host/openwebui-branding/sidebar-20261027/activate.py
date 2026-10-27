import json,pathlib,subprocess,time,urllib.request
root=pathlib.Path('/opt/openwebui-branding/sidebar-20261027')
info=json.loads((root/'container-before.json').read_text())
def run(*args): return subprocess.check_output(args,text=True).strip()
env=dict(item.split('=',1) for item in info['Config']['Env'])
env['WEBUI_NAME']='Oracle - OpenWebUI'
assert all('\n' not in value for value in env.values()), 'Multiline environment requires a different transfer format'
p=root/'runtime.env'; p.write_text('\n'.join(k+'='+v for k,v in env.items())+'\n'); p.chmod(0o600)
args=['docker','create','--name','open-webui-sidebar-branding-stage','--restart','unless-stopped','--env-file',str(p)]
for key,bindings in info['HostConfig']['PortBindings'].items():
    for bind in bindings:
        args+=['-p',bind['HostIp']+':'+bind['HostPort']+':'+key]
for m in info['Mounts']:
    assert m['Type']=='volume',m['Type']
    args+=['-v',m['Name']+':'+m['Destination']+('' if m['RW'] else ':ro')]
for value in info['HostConfig'].get('ExtraHosts') or []: args+=['--add-host',value]
for k,v in (info['Config'].get('Labels') or {}).items(): args+=['--label',k+'='+v]
args+=['--user',info['Config']['User'],'--workdir',info['Config']['WorkingDir'],'oracle-openwebui:sidebar-branding-20261027']
args+=info['Config']['Cmd'] or []
run(*args)
old='open-webui-before-sidebar-branding-20261027'
run('docker','stop','-t','30','open-webui')
run('docker','rename','open-webui',old)
run('docker','update','--restart=no',old)
try:
    run('docker','rename','open-webui-sidebar-branding-stage','open-webui')
    run('docker','start','open-webui')
    for attempt in range(90):
        try:
            with urllib.request.urlopen('http://127.0.0.1:3000/api/config',timeout=3) as response: config=json.load(response)
            if config.get('name')=='Oracle - OpenWebUI': break
        except Exception: pass
        time.sleep(2)
    else: raise RuntimeError('New container did not return the requested application name')
except Exception:
    run('docker','stop','open-webui')
    run('docker','rename','open-webui','open-webui-sidebar-branding-failed-20261027')
    run('docker','rename',old,'open-webui')
    run('docker','update','--restart=unless-stopped','open-webui')
    run('docker','start','open-webui')
    raise
# Keep the server's recreation helper aligned with the active, patched image.
p=pathlib.Path('/opt/open-webui/start.sh'); original=p.read_text()
(root/'start.sh.before').write_text(original)
original=original.replace('docker pull ghcr.io/open-webui/open-webui:v0.12.0','docker image inspect oracle-openwebui:sidebar-branding-20261027 >/dev/null')
original=original.replace('ghcr.io/open-webui/open-webui:v0.12.0','oracle-openwebui:sidebar-branding-20261027')
original=original.replace('oracle-openwebui:branding-20261027','oracle-openwebui:sidebar-branding-20261027')
p.write_text(original)
p=pathlib.Path('/opt/open-webui/webui.env'); original=p.read_text()
(root/'webui.env.before').write_text(original); (root/'webui.env.before').chmod(0o600)
p.write_text((root/'runtime.env').read_text())
(root/'result.json').write_text(json.dumps({'image':'oracle-openwebui:sidebar-branding-20261027','name':config['name'],'rollback_container':old},indent=2))
print((root/'result.json').read_text())
