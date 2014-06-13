function ContentBuilder() {}

// Znaczenie parametrów:
// -> data: JSONowe dane zwrócone przez serwer.
// -> room_name: Nazwa pokoju, dla którego dane są aktualizowane.
ContentBuilder.prototype.buildContent = function(data, room_name) {
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
