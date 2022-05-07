const setScheme = scheme => document.documentElement.className = scheme;
const schemeHeading = document.querySelector('#scheme-name');
const numSchemes = 7;
const schemes = [['ayu-mirage', 'Ayu Mirage'], ['everforest', 'Everforest'], ['gruvbox-material', 'Gruvbox Material'], ['catppuccin', 'Catppuccin'], ['sonokai-andromeda', 'Sonokai Andromeda'], ['tokyonight', 'Tokyonight'], ['nightfly', 'Nightfly']];
let schemeIdx = 0;

function mod(num, deno) {
	return ((num % deno) + deno) % deno;
}

function nextScheme(f) {
	schemeIdx = mod(f(schemeIdx), numSchemes)

	const [className, schemeName] = schemes[schemeIdx];
	console.log(`Setting scheme to ${schemeName}...`);

	setScheme(className);
	schemeHeading.textContent = schemeName;
}

this.addEventListener('keypress', key => {
	switch (key.key) {
		case " ":
		case "j": nextScheme(i => i + 1); break;
		case "k": nextScheme(i => i - 1); break;
	}
});
