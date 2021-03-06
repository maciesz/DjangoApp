// Klasy definiujące poszczególne modele
//
// W wersji pierwszej umownej przyjmujemy,
// że nazwa pokoju jest unikalna i to właśnie ona jest kluczem dla terminu.
function Room(name, capacity, description, attributes) {
	this.name = name;
	this.capacity = capacity;
	this.description = description;
	this.attribute_list = attributes;
}

function Term(room_name, booking_date, from, to) {
	this.room_name = room_name;
	this.booking_date = booking_date;
	this.from = from;
	this.to = to;
}

function Attribute(name) {
	this.name = name;
}
