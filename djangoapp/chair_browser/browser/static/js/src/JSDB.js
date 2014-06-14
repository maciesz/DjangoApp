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
	
	// Iterowanie po słowniku.
	$.each(data, function(model_dict, values) {
		// Wypisz nazwę klucza.
		console.log('Klucz: ' + model_dict);
		console.log('Wartości: ' + values[0]);
		// W zależności od klucza.
		switch (model_dict) {
			case this.attribute_key:
				this.attribute_collection.push(new Attribute(values[1]));
				break;
			case this.room_key:
				this.room_collection.push(new Room(
						values[1], // name
						values[2], // capacity
						values[3], // description
						values[4]  // attributes_list
					)
				);
				break;
			case this.term_key:
				this.term_collection.push(new Term(
						values[1], // booking_date
						values[2], // from
						values[3], // to
						values[4]  // room_name
					)
				);
				break;
		}
	})
}
	
