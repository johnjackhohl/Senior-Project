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
		opt.value = hero;
		opt.textContent = hero;
		heroSelect.appendChild(opt);
	});	
}

document.addEventListener('DOMContentLoaded', function () {
    const rosterSelects = document.getElementsByClassName('roster-select');
    const roleSelects = document.getElementsByClassName('role-select');

    // Function to update role and attach event listener
    const setupRosterSelect = (rosterSelect, index) => {
        updateRole(index);
        rosterSelect.addEventListener('change', () => updateRole(index));
    };

    // Function to update heroes and attach event listener
    const setupRoleSelect = (roleSelect, index) => {
        updateHeroes(index);
        roleSelect.addEventListener('change', () => updateHeroes(index));
    };

    // Attach event listeners to all roster selects
    for (let i = 0; i < rosterSelects.length; i++) {
        setupRosterSelect(rosterSelects[i], i);
    }

    // Attach event listeners to all role selects
    for (let i = 0; i < roleSelects.length; i++) {
        setupRoleSelect(roleSelects[i], i);
    }
});
