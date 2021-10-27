const setScheme = scheme => document.documentElement.className = scheme;

const schemeHeading = document.querySelector('#scheme-name')

const numSchemes = 5;
const schemes = [
	['ayu-mirage', 'ayu mirage'],
	['gruvbox-material', 'gruvbox material'],
	['sonokai-andromeda', 'sonokai andromeda'],
	['everforest', 'everforest'],
	['tokyonight', 'tokyonight'],
];

let schemeIdx = 0;

const mod = (num, den) => {
	if (num >= 0)
		return num % den;
	return den - (-num % den);
}

const nextScheme = f => {
	schemeIdx = mod(f(schemeIdx), numSchemes)

	const [className, schemeName] = schemes[schemeIdx];
	console.log(`Setting scheme to ${schemeName}...`);

	setScheme(className);
	schemeHeading.textContent = schemeName;
}

this.addEventListener('keypress', key => {
	switch (key.keyCode) {
		case  32:
		case 106: nextScheme(i => i + 1); break;
		case 107: nextScheme(i => i - 1); break;
	}
});
