function updateSubMaps() {
    var mapSelect = document.getElementById('id_map_name');
    var selectedMapId = mapSelect.value;
    var subMaps = subMapsData[selectedMapId];

    var subMapSelect = document.getElementById('id_map_sub_name');
    subMapSelect.innerHTML = ''; // Clear existing options

    subMaps.forEach(function(subMap) {
        var opt = document.createElement('option');
        opt.value = subMap.sub_map_name;
        opt.textContent = subMap.sub_map_name;
        subMapSelect.appendChild(opt);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    var mapSelect = document.getElementById('id_map_name');
    
    // Call updateSubMaps initially to populate sub-maps for the default selection
    updateSubMaps();

    // Add event listener for change event
    mapSelect.addEventListener('change', updateSubMaps);
});
