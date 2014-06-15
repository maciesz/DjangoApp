function ContentBuilder() {}

//============================================================================//
//                                                                            //
// Budowniczy Modala.                                                         //
//                                                                            //
//============================================================================//

// Znaczenie parametrów:
// -> data: JSONowe dane zwrócone przez serwer.
// -> room_name: Nazwa pokoju, dla którego dane są aktualizowane.
ContentBuilder.prototype.buildModalContent = function(data, room_name) {
	// Inicjacja zmiennych wewnetrznych
	var counter = 0;
	var str = '<div class="panel-group" id="date_collapse">';
	// Przegladanie danych w postaci JSON
	$.each(data, function(key, value) {
		date = key;
		counter++;
		
		// Budowa wnętrza my_modal
		str += '<div class="panel panel-default">';
		str += '<div class="panel-heading">';// id="date" value="' + date + '">';
		str += '<h4 class="panel-title">';
		str += '<a data-toggle="collapse" data-parent="date_collapse" href="#collapse';
		str += counter + '">';
		str += '<strong>' + counter + '. </strong>' + date;
		str += '</a></h4></div>';
		str += '<div id="collapse' + counter + '" class="panel-collapse collapse';
		str += (counter == 1) ? ' in">' : '">';
		str += '<div class="panel-body">';
		str += '<div class="row">';
		str += '<div class="col-md-6">';
		str += 'Suggested hour intervals are: ';
		str += '<br><br>';
		str += '<ul>';
		$.each(this, function(key, value) {
			str += '<li>' + value[0] + '-' + value[1] + '</li>';
		})
		
		str += '</ul>';
		str += '<br><br>';
		str += '<input name="room" class="form-control" value="' + room_name + '" style="width: 60%;" readonly>';
		str += '<br>';
		str += '<input name="date" class="form-control date" value="' + date + '" style="width: 60%;" readonly>';
		str += '<br>';
		str += '</div>';
		str += '<div class="col-md-6">';
		
		// Budowanie prawej strony rozwijanego modala
		str += '<br>';
		
		str += '<div class="input-group">';
		str += '<span class="input-group-addon">From: </span>';
		str += '<input name="from_hour" class="timepicker from form-control" placeholder="..." readonly/>';
		str += '</div>';
		str += '<br>';
		str += '<div class="input-group">';
		str += '<span class="input-group-addon">To: </span>';
		str += '<input name="to_hour" class="timepicker to form-control"  placeholder="..." readonly/>';
		str += '</div>';
		
		str += '<br/><br/>';
		str += '<center>';
		str += '<input type="submit" class="btn btn-success reserve" value="Reserve" style="width: 100%;"/>';
		str += '</center>';
		str += '</div>';
		str += '</div></div></div>';
	})
	str += '</div></div>';
	
	return str;
}


//============================================================================//
//                                                                            //
// Budowniczy Tabeli rekordów.                                                //
//                                                                            //
//============================================================================//

ContentBuilder.prototype.buildTableContent = function(jsdb) {
	// Ściągnij wartość zapytania z inputa wyszukiwarki.
	var query = this.getUserQuery();
	// Odczytaj wartości capacity ze slidera(min, max).
	var lower_bound = this.setLowerBound()
	var upper_bound = this.setUpperBound();
	// Ściągnij wszystkie wymagania dotyczące sprzętu.
	var attributes = this.collectRoomAttributes();
	attributes.sort();
	// [DEBUG 1]
	this.debugAfterRecvInfo(attributes, lower_bound, upper_bound, query);
	// Na podstawie przekazanych danych zwróć stringa reprezentującego
	// tabelę + paginację.
	var room_collection = jsdb.room_collection.slice();
	/*console.log('---------------------------- Room collection -------------------------');
	for (i = 0; i< room_collection.length; i++) {
		console.log(room_collection[i]);
	}*/
	// Wybierz tylko te pokoje , które spełniają oczekiwania klienta.
	var room_data = 
		this.getRooms(room_collection, query, lower_bound, upper_bound, attributes);
	
	console.log('Po przeparsowaniu..');
	for (i = 0; i< room_data.length; i++)
		console.log(room_data[i]);
	// Bazując na wyżej wybranych pokojach utwórz kontent HTML dla tabeli.
	var tab_n_pag_string = this.fulfillTableContent(room_data);
	// Zwróć wynikowego stringa.
	return tab_n_pag_string;
}

// Wyciągnij zestaw pożądanych atrybutów z DOMa.
ContentBuilder.prototype.collectRoomAttributes = function() {
	var attributes = new Array();
	var iterator = 0;
	$('.attribute').each(function(index) {
		console.log($(this).attr('name'));//val());
		if ($(this).prop('checked')) {
			var room_attribute = $(this).attr('name');
			attributes[iterator++] = room_attribute;
		}
	});
	
	return attributes;
}

// Zwróć minimalną pojemność pokoju ustaloną przez klienta.
ContentBuilder.prototype.setLowerBound = function() {
	return $('#slider-range').slider('values')[0];
}

// Zwróć maksymalną pojemność pokoju ustaloną przez klienta.
ContentBuilder.prototype.setUpperBound = function() {
	// -> maksymalna pojemność pokoju.
	return $('#slider-range').slider('values')[1];
}

// Zwróć frazę poszukiwana przez klienta.
ContentBuilder.prototype.getUserQuery = function() {
	return $('#id_query').val();
}

//============================================================================//
// Wybór pokoi na podstawie preferencji gracza.                               //
//============================================================================//
ContentBuilder.prototype.getRooms = function(
	room_collection, query, lower_bound, upper_bound, attributes) {
	var rooms = new Array(); // Tablica list reprezentująca konkretne pokoje.
	var idx = 0; // Liczba pokoi.
	var name; // Nazwa pokoju.
	var capacity; // Pojemność..
	var description; // Opis..
	var room_attrs; // Atrybuty..
	//console.log('********************* Ilość rumów: ' + room_collection.length + ' ************************');
	//console.log('Przykład: ' + room_collection[2].name);
	for (i = 0; i< room_collection.length; i++) {
		//console.log('Oto jest room, który dał nam Pan ;-): ' + room_collection[i]);
		var room = room_collection[i];
		// .slice() - kopia.
		//console.log('Oto jest room, który dał nam Pan ;-): ' + room_collection[i]);
		name = room.name;
		cap = room.capacity;
		desc = room.description;
		room_attrs = room.attribute_list;
		// [DEBUG] 
		console.log('--------------------------------------');
		console.log('Name: ' + name);
		console.log('Capacity: ' + cap);
		console.log('Description: ' + desc);
		console.log('Room_attrs: ' + room_attrs);
		console.log('Requirements: ' + attributes);
		var browser_condition = this.checkInclusion(name, cap, desc, query);
		var capacity_condition = this.checkCapacity(cap, lower_bound, upper_bound); 
		var attribute_condition = this.checkAttributes(attributes, room_attrs);
		console.log('Browser condition: ' + browser_condition);
		console.log('Capacity condition: ' + capacity_condition);
		console.log('Attribute condition: ' + attribute_condition);
		// Jeżeli każdy z powyższych warunków jest spełniony.
		if (browser_condition && capacity_condition && attribute_condition)
			rooms[idx++] = [name, cap, desc];
	}
	
	console.log('Kończę..');
	
	return rooms;
}

// Sprawdź warunek zawierania frazy wpisanej do wyszukiwarki przez model pokoju.
ContentBuilder.prototype.checkInclusion = function(
	name, capacity, description, query) {
	var inc_name = (name.toLowerCase().indexOf(query.toLowerCase()) >= 0);
	var inc_cap = (String(capacity).indexOf(query) >= 0);
	var inc_desc = (description.toLowerCase().indexOf(query.toLowerCase()) >= 0);
	
	return (inc_name || inc_cap || inc_desc) ? true : false;
}

// Sprawdź, czy pojemność konkretnego pokoju jest zgodna z oczekiwaniami klienta.
ContentBuilder.prototype.checkCapacity = function(
	capacity, lower_bound, upper_bound) {
	return (capacity >= lower_bound && capacity <= upper_bound) ? true : false;
}

// Sprawdź, czy dany pokój zawiera wszystkie wymagane atrybuty.
ContentBuilder.prototype.checkAttributes = function(
	attributes, room_attrs) {

	console.log("Attributes size: " + attributes.length);
	// Rozmiary poszczególnych tablic.
	const attrs_length = attributes.length;
	const room_attrs_length = room_attrs.length;
	// Inicjalizacja indeksów startowych.
	var curr_attrs_pos = 0;
	var curr_room_attrs_pos = 0;
	// Trywialny.
	while (curr_attrs_pos < attrs_length && curr_room_attrs_pos < room_attrs_length) {
		if (attributes[curr_attrs_pos] > room_attrs[curr_room_attrs_pos]) {
			curr_room_attrs_pos++;
		} else if (attributes[curr_attrs_pos] == room_attrs[curr_room_attrs_pos]) {
			curr_attrs_pos++;
			curr_room_attrs_pos++;
		} else {
			break;
		}
	}
	
	// Jeżeli pokój posiada wszystkie wymagane atrybuty.. 
	return (curr_attrs_pos == attrs_length) ? true : false;
}

//============================================================================//
// Tworzenie zawartości HTMLowej z pokoi spełniających warunki klienta.       //
//============================================================================//
ContentBuilder.prototype.fulfillTableContent = function(room_data) {
	const rows_per_page = 4;
	const tr_id_beg = 'page';
	const attrs = 3;
	var curr_rows_on_page = 0;
	var curr_page = 1;
	var str = '';
	if (room_data.length > 0) {
		// Określenie wyglądu tabeli.
		str += '<table class="table table-hover table-bordered table-striped"' + 
			'style="margin-bottom:4%;">';
		// Konstrukcja kolumn tytułowych w tabeli.
		str += '<tr>';
		str += '<th><a href="?sort=name">Name</a></th>';
		str += '<th><a href="?sort=capacity">Capacity</a></th>'
		str += '<th>Description</th>'
		str += '<th>Go to form</th>'
		str += '</tr>';
		// Konstrukcja tabeli.
		for (i = 0; i< room_data.length; i+= rows_per_page) {
			// Dodaj unikatowe id dla kolejnej strony.
			str += '<tr id="' + tr_id_beg + ' ' + curr_page + '">';
			// Ustal liczbę pozostałych pokoi.
			var range = Math.min(room_data.length - i, rows_per_page);
			// Dla każdego pokoju na tej stronie..
			for (j = 0; j< range; j++) {
				str += '<tr>';
				// Wypełnij każdą kolumnę(nazwa, pojemność, opis).
				for (k = 0; k< attrs; k++) {
					var vlue = room_data[i+j][k];
					str += '<td>' + vlue + '</td>';
				}
				// Dodaj przycisk umożliwiający rezerwację konkretnego terminu.
				str += '<td>';
				str += '<input type="button" class="btn btn-success query_btn" ';
				var room_name = room_data[i + j][0];
				str += 'id="' + room_name + '" ';
				str += 'name="' + room_name + '" ';
				str += 'value="Book">';
				str += '</td>';
				str += '</tr>';
				curr_rows_on_page++;
			}
			curr_page++;
			
			str += '</tr>';
		}
		str += '</table>';
		
		// Dodanie paginacji... TODO!
	} else {
		str += '<span class="glyphicon glyphicon-warning-sign" ';
		str += 'style="font-size: 1000%;">'
		str += '</span>';
		str += '<br/>'
		str += '<label class="lead" style="margin-top: 3%;">';
		str += 'Any room fulfills Your criteria!</label>';
	}
	
	return str;
}

// Debug po zebraniu informacji.
ContentBuilder.prototype.debugAfterRecvInfo = function(
	attributes, lower_bound, upper_bound, query) {
	// [DEBUG]
	console.log('--------------------- Attributes ----------------------');
	for (i = 0; i< attributes.length; i++) {
		console.log(attributes[i]);
	}
	console.log('------------------- Capacity range --------------------');
	console.log('Lower_bound: ' + lower_bound + ', Upper bound: ' + upper_bound);
	console.log('------------------------ Query ------------------------');
	console.log('Query: ' + query);
}
