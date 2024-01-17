function updateRole(element_num) {
	var rosterSelect = document.getElementById('id_player-'+element_num+'-roster_id');
    var selectedRosterId = rosterSelect.value;
	var roles = rosterData[selectedRosterId];
	console.log(selectedRosterId);
	console.log(element_num);

    var roleSelect = document.getElementById('id_player-'+element_num+'-role');
	roleSelect.innerHTML = ''; // Clear existing options

	var opt = document.createElement('option');
	var opt2 = document.createElement('option');
	var opt3 = document.createElement('option');
	if (roles.toLowerCase() == "support") {
		opt.value = 'Support';
		opt.textContent = 'Support';
		opt2.value = 'Tank';
		opt2.textContent = 'Tank';
		opt3.value = 'DPS';
		opt3.textContent = 'DPS';
	} else if (roles.toLowerCase() == "tank") {
		opt.value = 'Tank';
		opt.textContent = 'Tank';
		opt2.value = 'DPS';
		opt2.textContent = 'DPS';
		opt3.value = 'Support';
		opt3.textContent = 'Support';
	} else if (roles.toLowerCase() == "dps") {
		opt.value = 'DPS';
		opt.textContent = 'DPS';
		opt2.value = 'Tank';
		opt2.textContent = 'Tank';
		opt3.value = 'Support';
		opt3.textContent = 'Support';
	} else {
		opt.value = 'Tank';
		opt.textContent = 'Tank';
		opt2.value = 'Support';
		opt2.textContent = 'Support';
		opt3.value = 'DPS';
		opt3.textContent = 'DPS';
	}
	roleSelect.appendChild(opt);
	roleSelect.appendChild(opt2);
	roleSelect.appendChild(opt3);
	updateHeroes(element_num);
}

function updateHeroes(element_num) {
	var roleSelect = document.getElementById('id_player-'+element_num+'-role');
	var role = roleSelect.value;
	console.log(role);
	console.log(element_num);
	var heroes = [];
	
	var heroSelect = document.getElementById('id_player-'+element_num+'-hero');
	heroSelect.innerHTML = ''; // Clear existing options
	
	if (role.toLowerCase() == "tank") {
		heroes = tankData;
	} else if (role.toLowerCase() == "support") {
		heroes = supportData;
	} else {
		heroes = dpsData;
	}
	
	heroes.forEach(function(hero) {
		var opt = document.createElement('option');
		opt.value = hero.hero_name;
		opt.textContent = hero.hero_name;
		heroSelect.appendChild(opt);
	});	
}

/* document.addEventListener('DOMContentLoaded', function () {
	var rosterSelect = document.getElementById('id_player-0-roster_id');
	
	// Call updateSubMaps initially to populate sub-maps for the default selection
	updateRole(0);

	// Add event listener for change event
	rosterSelect.addEventListener('change', (event) => {
		updateRole(0);
	});
});


document.addEventListener('DOMContentLoaded', function () {
	var roleSelect = document.getElementById('id_player-0-role');

	updateHeroes(0);

	roleSelect.addEventListener('change', (event) => {
		updateHeroes(0);
	});
}); */

var rosterSelects = document.getElementsByClassName('roster-select');
var roleSelects = document.getElementsByClassName('role-select');

console.log(rosterSelects.item(0));

