const setScheme = scheme => document.documentElement.className = scheme;
const schemeHeading = document.querySelector('#scheme-name');
const schemes = [
  [
    "Everforest",
    "everforest",
    [
      "dark"
    ]
  ],
  [
    "Catppuccin",
    "catppuccin",
    [
      "default"
    ]
  ],
  [
    "Gruvbox",
    "gruvbox",
    [
      "material"
    ]
  ],
  [
    "Tokyonight",
    "tokyonight",
    [
      "default"
    ]
  ],
  [
    "Nightfox",
    "nightfox",
    [
      "night"
    ]
  ],
  [
    "Nightfly",
    "nightfly",
    [
      "default"
    ]
  ],
  [
    "Ros\u00e9 Pine",
    "ros\u00e9-pine",
    [
      "main"
    ]
  ],
  [
    "Sonokai",
    "sonokai",
    [
      "andromeda"
    ]
  ],
  [
    "Kanagawa",
    "kanagawa",
    [
      "default"
    ]
  ],
  [
    "Ayu",
    "ayu",
    [
      "mirage"
    ]
  ]
];
const numSchemes = schemes.length;
let schemeIdx = 0;

function mod(num, deno) {
	return ((num % deno) + deno) % deno;
}

function nextScheme(f) {
	schemeIdx = mod(f(schemeIdx), numSchemes);

	const [schemeName, hyphenatedName, variants] = schemes[schemeIdx];
	const className = `${hyphenatedName}-${variants[0]}`;

	console.log(`Setting scheme to ${schemeName} (${className})...`);

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
