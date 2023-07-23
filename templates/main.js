const setScheme = scheme => document.documentElement.className = scheme;

const schemeHeading = document.querySelector('#scheme-name');
const schemeVariant = document.querySelector('#scheme-variant');

const schemes = '<schemes>';
const numSchemes = schemes.length;

let schemeIdx = 0;
let variantIdx = 0;

function mod(num, deno) {
	return ((num % deno) + deno) % deno;
}

function nextScheme(f) {
	variantIdx = 0;
	schemeIdx = mod(f(schemeIdx), numSchemes);

	const [schemeName, hyphenatedName, variants] = schemes[schemeIdx];
	const variant = variants[0];
	const className = `${hyphenatedName}-${variant}`;

	console.log(`Setting scheme to ${schemeName} (${className})...`);

	setScheme(className);
	schemeHeading.textContent = schemeName;
	schemeVariant.textContent = variant;
}

function nextVariant(f) {
	const [schemeName, hyphenatedName, variants] = schemes[schemeIdx];
	variantIdx = mod(f(variantIdx), variants.length);
	console.log(variantIdx);
	const variant = variants[variantIdx];
	const className = `${hyphenatedName}-${variant}`;

	console.log(`Setting scheme to ${schemeName} (${className})...`);

	setScheme(className);
	schemeHeading.textContent = schemeName;
	schemeVariant.textContent = variant;
}


this.addEventListener('keypress', key => {
	switch (key.key) {
		case " ":
		case "j": nextScheme(i => i + 1); break;
		case "k": nextScheme(i => i - 1); break;
		case "h": nextVariant(i => i - 1); break;
		case "l": nextVariant(i => i + 1); break;
	}
});