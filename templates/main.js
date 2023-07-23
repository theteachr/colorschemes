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

const inc = i => i + 1
const dec = i => i - 1

this.addEventListener('keypress', key => {
	switch (key.key) {
		case " ":
		case "j": nextScheme(inc); break;
		case "k": nextScheme(dec); break;
		case "h": nextVariant(dec); break;
		case "l": nextVariant(inc); break;
	}
});

this.addEventListener('click', _ => nextScheme(inc))
