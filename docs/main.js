const setScheme = scheme => document.documentElement.className = scheme;
const schemeHeading = document.querySelector('#scheme-name');
const numSchemes = 6;

const schemes = [
	['ayu-mirage', 'ayu mirage'],
	['gruvbox-material', 'gruvbox material'],
	['sonokai-andromeda', 'sonokai andromeda'],
	['everforest', 'everforest'],
	['tokyonight', 'tokyonight'],
	['nightfly', 'nightfly'],
];

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
