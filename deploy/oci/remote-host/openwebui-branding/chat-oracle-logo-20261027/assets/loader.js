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
			'#sidebar img.sidebar-new-chat-icon'
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
		// The welcome model icon sits above the composer. Scope the replacement
		// to this area so message avatars and model-menu images keep their behavior.
		for (const logo of document.querySelectorAll(
			'#chat-welcome img.oracle-chat-welcome-logo, #chat-pane .translate-y-6 img[aria-hidden="true"][draggable="false"][class~="size-9"]'
		)) {
			if (logo.getAttribute('src') !== '/static/oracle-o.png') {
				logo.setAttribute('src', '/static/oracle-o.png');
				logo.setAttribute('alt', 'Oracle');
			}
			logo.classList.add('oracle-chat-welcome-logo');
		}
		const sidebarName = document.getElementById('sidebar-webui-name');
		if (sidebarName && sidebarName.textContent !== 'Oracle-OpenWebUI') {
			sidebarName.textContent = 'Oracle-OpenWebUI';
		}
		const heading = document.querySelector('#auth-login-card form > div:first-child > div');
		if (heading) {
			heading.classList.toggle(
				'oracle-login-heading',
				heading.textContent.trim() === 'Sign in to Oracle - OpenWebUI'
			);
		}
	};
	const start = () => {
		updateLogos();
		// Svelte mounts the sidebar after sign-in and recreates it on navigation.
		new MutationObserver(updateLogos).observe(document.body, {
			childList: true,
			subtree: true,
			attributes: true,
			attributeFilter: ['src', 'id'],
			characterData: true
		});
	};
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', start, { once: true });
	} else {
		start();
	}
})();
