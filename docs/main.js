const setTheme = theme => document.documentElement.className = theme;

document.getElementById('scheme-selector').addEventListener('change', function () {
	console.log(`Setting theme to "${this.value}"`);
	setTheme(this.value);
});