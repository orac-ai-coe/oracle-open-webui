/* Oracle co-branding in the application's existing logo positions. */
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

	const updateLogos = () => {
		document.getElementById('oracle-brand-header')?.remove();
		for (const logo of document.querySelectorAll(
			'#sidebar img.sidebar-new-chat-icon, #auth-page img#logo'
		)) {
			if (logo.getAttribute('src') !== '/static/oracle-openwebui.svg') {
				logo.setAttribute('src', '/static/oracle-openwebui.svg');
				logo.setAttribute('alt', 'Oracle O | Open WebUI');
				logo.classList.add('oracle-sidebar-brand');
				if (logo.closest('#sidebar')) {
					logo.closest('a')?.classList.add('oracle-sidebar-brand-link');
				}
			}
		}
	};
	const start = () => {
		updateLogos();
		// Svelte mounts the sidebar after sign-in and recreates it on navigation.
		new MutationObserver(updateLogos).observe(document.body, {
			childList: true,
			subtree: true,
			attributes: true,
			attributeFilter: ['src']
		});
	};
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', start, { once: true });
	} else {
		start();
	}
})();
