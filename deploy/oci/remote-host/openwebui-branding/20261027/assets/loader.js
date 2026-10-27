/* Oracle co-branding. Keep the original Open WebUI name, logos and attribution. */
(() => {
	if (!localStorage.getItem('oracle-theme-v1')) {
		localStorage.setItem('theme', 'dark');
		localStorage.setItem('oracle-theme-v1', 'true');
	}
	document.documentElement.classList.add('oracle-theme');
	if (localStorage.getItem('theme') === 'dark') {
		document.documentElement.classList.remove('light');
		document.documentElement.classList.add('dark');
	}

	const mountBrand = () => {
		if (document.getElementById('oracle-brand-header')) return;
		const header = document.createElement('header');
		header.id = 'oracle-brand-header';
		header.setAttribute('aria-label', 'Oracle - OpenWebUI');
		const name = document.createElement('span');
		name.className = 'oracle-app-name';
		name.textContent = 'Oracle - OpenWebUI';
		const logos = document.createElement('div');
		logos.className = 'oracle-brand-logos';
		const oracle = document.createElement('img');
		oracle.src = '/static/oracle-o.png';
		oracle.alt = 'Oracle';
		oracle.className = 'oracle-o-logo';
		const pipe = document.createElement('span');
		pipe.className = 'oracle-brand-pipe';
		pipe.textContent = '|';
		pipe.setAttribute('aria-hidden', 'true');
		const webui = document.createElement('img');
		webui.src = '/static/favicon.png';
		webui.alt = 'Open WebUI';
		webui.className = 'oracle-webui-logo';
		const label = document.createElement('span');
		label.textContent = 'OpenWebUI';
		logos.append(oracle, pipe, webui, label);
		header.append(name, logos);
		document.body.append(header);
	};
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', mountBrand, { once: true });
	} else {
		mountBrand();
	}
})();
