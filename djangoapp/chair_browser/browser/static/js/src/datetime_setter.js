function DateTime() {
	this.setter = new Date();
	this.date_separator = "-";
	this.time_separator = ":";
}

DateTime.prototype.getDate = function() {
	// Domyślnie getMonth liczy miesiące od 0 do 11.
	var date =
		this.setter.getFullYear() +
		this.date_separator +
		(this.setter.getMonth() + 1) +
		this.date_separator +
		this.setter.getDay() + 1;
	// [DEBUG] Wypisz efekt.
	//console.log("Utworzyłem datę: " + date);
	return date;
}

DateTime.prototype.getCurrentTime = function() {
	var current_time = 
		this.setter.getHours() +
		this.time_separator +
		this.setter.getMinutes();
	// [DEBUG] Wypisz efekt.
	//console.log("Utworzyłem czas: " + current_time);
	return current_time;
}
