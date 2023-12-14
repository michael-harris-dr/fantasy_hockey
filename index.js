var nameList = []
var tableData = []

//changes to the following HTML should be reflected in index.html
const staticTableHTML = `        <colgroup>
									<col class="picture_col">
									<col class="player_col">
									<col class="gp_col num">
									<col class="g_col num">
									<col class="a_col num">
									<col class="p_col num">
									<col class="shp_col num">
								</colgroup>
									<tr id="headers" class="heads">
										<th colspan="2" class = "table_player_name">Player</th>
										<th class = "table_stat">GP</th>
										<th class = "table_stat">G</th>
										<th class = "table_stat">A</th>
										<th class = "table_stat">P</th>
										<th class = "table_stat">SH%</th>
									</tr>`

$(document).ready(function () {

	$('#stat_table').html(staticTableHTML)

	$("#search_field").keydown(function (event) {
		if (event.keyCode === 13) {
			event.preventDefault();
			$("#search_button").click();
			console.log("CLICK!")
		}
	});

	$(document).on('click', '#search_button', async function () {

		console.log("CLICKED SEARCH BUTTON")

		var field_val = pascalify( $('#search_field').val() )

		$.ajax({
			type: 'GET',
			dataType: "json",
			url: 'http://127.0.0.1:8000/validatePlayer',
			headers: {
				"Access-Control-Allow-origin": "True",
				"x-api-key": "temp120681689"
			},
			data: {
				"Player": field_val
			},
			success: function (data, status) {
				console.log('http://127.0.0.1:8000/validatePlayer: ', data)

				if (data && !(nameList.includes(field_val))) //if player exists API returns TRUE and player name isn't already in the list of names
				{
					nameList.push(field_val)
					console.log('nameList: ', nameList)
					update_list()
				}
			}
		});
	});

	$(document).on('click', '#call_api', function () {
		console.log("CLICKED API BUTTON");

		console.log(nameList)
		$.ajax({
			type: 'GET',
			dataType: "json",
			url: 'http://127.0.0.1:8000/players',
			headers: {
				"Access-Control-Allow-origin": "True",
				"x-api-key": "4132"
			},
			data: {
				"Players": JSON.stringify(nameList)
			},
			success: function (data, status) {
				console.log('http://127.0.0.1:8000/players: ', JSON.parse(data));

				if (Object.keys(data).length > 2) 
				{
					tableData = (JSON.parse(data))
					update_table()
				}
			}
		});
	});

});

function pascalify(string) 
{
	return string.charAt(0).toUpperCase() + string.substring(1).toLowerCase()
}

function update_list()
{
	let nameString = ""
	for (const name of nameList)
	{
		nameString += name + '\n'
	}

	$('#player_name').html(nameString);
}


function update_table()
{
	console.log("tableData: ", tableData)
	let tableHTML = staticTableHTML
	for (var player in tableData)
	{
		stats = tableData[player]
		console.log(stats)
		console.log(player)
		tableHTML +=    `<tr id="${stats["id"]}_row" class="table_row">
						<td class = table_pic><img class="headshot" src=${stats["headshot"]}></td>
						<td class = "table_player_name">${stats["lastName"]} ${stats["special"]}</td>
						<td class = "table_stat">${stats["seasons"]["20232024"]["gp"]}</td>
						<td class = "table_stat">${stats["seasons"]["20232024"]["goals"]}</td>
						<td class = "table_stat">${stats["seasons"]["20232024"]["assists"]}</td>
						<td class = "table_stat">${stats["seasons"]["20232024"]["points"]}</td>
						<td class = "table_stat">${(100 * stats["seasons"]["20232024"]["shp"]).toFixed(1)}</td>
						</tr>`
	}
	$('#stat_table').html(tableHTML)
}