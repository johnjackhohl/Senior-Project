
function updateRole() {
    var rosterSelect = document.getElementById('id_roster_id');
    var selectedRosterId = rosterSelect.value;
	var roles = rosterData[selectedRosterId];

    var roleSelect = document.getElementById('id_role');
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
}

document.addEventListener('DOMContentLoaded', function () {
    var rosterSelect = document.getElementById('id_roster_id');

    updateRole();

    rosterSelect.addEventListener('change', updateRole);
});