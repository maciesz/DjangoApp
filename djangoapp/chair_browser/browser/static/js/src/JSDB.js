function JSDB() {
	// Kolekcje dla poszczególnych modeli w bazie.
	this.attribute_collection = new Array();
	this.room_collection = new Array();
	this.term_collection = new Array();
	// Stałe podające dokładną nazwę klucza
	// dla poszczególnych słowników konkretnych modeli.
	// Wykorzystywane w momencie ściągania danych z bazy(offline).
	this.attribute_key = 'Attribute';
	this.room_key = 'Room';
	this.term_key = 'Term';
}

// 'data' jest to plik JSONowy,
// w którym mieści się zawartość nieco zmodyfikowanej bazy pierwotnej.
JSDB.prototype.updateContent = function(data) {
	// Czyszczenie tablic.
	// Ustalając długość tablicy na 0,
	// wywołujemy domyślnie destruktor dla każdego obiektu.
	// To zabiera(podobno) trochę więcej czasu niż arr=[],
	// ale zwalnianie pamięci ,,na bieżąco'' w przypadku
	// przeglądarki ,,offline'' wydaje się być sensowne.
	this.attribute_collection.length = 0;
	this.room_collection.length = 0;
	this.term_collection.length = 0;
	
	// Tablice pomocnicze.
	var attr_col = new Array();
	var r_col = new Array();
	var t_col = new Array();
	// Kolejne indeksy.
	var attr_idx = 0;
	var r_idx = 0;
	var t_idx = 0;
	// Iterowanie po słowniku.
	$.each(data, function(model_dict, values) {
		var mod_dict = String(model_dict);
		switch (mod_dict) {
			case 'Attribute':
				for (var next in values) {
					attr_col[attr_idx] = new Attribute(values[attr_idx]);
					attr_idx++;
				}
				break;
			case 'Room':
				for (var next in values) {
					r_col[r_idx] = new Room(
							values[r_idx][0], // name
							values[r_idx][1], // capacity
							values[r_idx][2], // description
							values[r_idx][3]  // attributes_list
						);
					r_idx++;
				}
				break;
			case 'Term':
				for (var next in values) {
					t_col[t_idx] = new Term(
							values[t_idx][0], // booking_date
							values[t_idx][1], // from
							values[t_idx][2], // to
							values[t_idx][3]  // room_name
						);
					t_idx++;
				}
				break;
		}
	})
	// Przenieś zawartość tablic pomocniczych
	// do buforów po stronie klienta.
	this.attribute_collection = attr_col.slice();
	this.room_collection = r_col.slice();
	this.term_collection = t_col.slice();
	// Wyczyść tablice pomocnicze.
	attr_col.length = 0;
	r_col.length = 0;
	t_col.length = 0;
}

JSDB.prototype.debugAfterUpdate = function() {
	// [DEBUG] Sprawdź kontent po aktualizacji danych.
	console.log("---------------------- Atrybuty -----------------------");
	for (i = 0; i< this.attribute_collection.length; i++)
		console.log(this.attribute_collection[i]);
	console.log("---------------------- Pokoje -------------------------");
	for (i = 0; i< this.room_collection.length; i++) {
		console.log(this.room_collection[i]);
	}
	console.log("---------------------- Terminy ------------------------");
	for (i = 0; i< this.term_collection.length; i++) {
		console.log(this.term_collection[i]);
	}
}
