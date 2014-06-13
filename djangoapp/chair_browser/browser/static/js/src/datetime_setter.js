function DateTime() {
	this.setter = new Date();
	this.date_separator = "-";
	this.time_separator = ":";
}

DateTime.prototype.getDate = function() {
	// Domyślnie getMonth liczy miesiące od 0 do 11.
	var date =
		setter.getDate() +
		date_separator +
		(setter.getMonth() + 1) +
		date_separator +
		setter.getFullYear();
	
	return date;
}

DateTime.prototype.getCurrentTime = function() {
	// Ustal aktualną godzinę.
	var hours = setter.getHours();
	// Dopasuj format('AM'/'PM').
	var ending = (hours > 12) ? 'PM' : 'AM';
	// Zmodyfikuj odpowiednio format godziny.
	hours = (hours > 12) ? (hours - 12) : hours;
	// Skonstruuj ostateczny napis reprezentujący datę 
	// zgodną z przyjętym formatem.
	var current_time = 
		hours +
		time_separator +
		setter.getMinutes() +
		" " +
		ending;
	
	return current_time;
}
