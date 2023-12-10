var nameList = []
var tableData = []

//changes to the following HTML should be reflected in index.html
const staticTableHTML = '        <colgroup>												\
									<col class="player_col">							\
									<col class="gp_col num">							\
									<col class="g_col num">								\
									<col class="a_col num">								\
									<col class="p_col num">								\
									<col class="shp_col num">							\
								</colgroup>												\
									<tr id="headers" class="heads">						\
										<th>Player</th class = "table_player_name">		\
										<th>gp</th class = "table_stat">				\
										<th>g</th class = "table_stat">					\
										<th>a</th class = "table_stat">					\
										<th>p</th class = "table_stat">					\
										<th>sh%</th class = "table_stat">				\
									</tr>'

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
		console.log(field_val);

		$.ajax({
			type: 'GET',
			dataType: "json",
			url: 'http://127.0.0.1:8000/validatePlayer',
			headers: {
				"Access-Control-Allow-origin": "True"
			},
			data: {
				"Player": field_val
			},
			success: function (data, status) {
				console.log('data: ', data);
				console.log('status: ', status);

				const obj = JSON.parse(data);
				console.log(obj == true);

				if (obj && !(nameList.includes(field_val))) //if player exists API returns TRUE and player name isn't already in the list of names
				{
					console.log(nameList, field_val)
					update_list()
					nameList.push(field_val)
				}
			}
		});
	});

	$(document).on('click', '#call_api', function () {
		console.log("CLICKED API BUTTON");

		var field_val = $('#search_field').val()
		console.log(nameList)
		$.ajax({
			type: 'GET',
			dataType: "json",
			url: 'http://127.0.0.1:8000/players',
			headers: {
				"Access-Control-Allow-origin": "True"
			},
			data: {
				"Players": JSON.stringify(nameList)
			},
			success: function (data, status) {
				console.log('data: ', JSON.parse(data));
				console.log('status: ', status);

				if (Object.keys(data).length > 2) 
				{
					tableData = (JSON.parse(data))
					console.log("TABLEDATA NOW ", tableData)
					update_list()
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
	console.log("SFJA:")
	let nameString = ""
	for (const name of nameList)
	{
		nameString += name + '\n'
	}

	$('#player_name').html(nameString);
}


function update_table()
{
	console.log("TABLEDATA: ", tableData)
	let tableHTML = staticTableHTML
	for (var player in tableData)
	{
		console.log(player)
		tableHTML +=    '<tr id="headers" class="heads">		\
						<th>'+tableData[player]["lastName"]+" "+tableData[player]["special"]+'</th class = "table_player_name">   \
						<th>gp</th class = "table_stat">        \
						<th>g</th class = "table_stat">         \
						<th>a</th class = "table_stat">         \
						<th>p</th class = "table_stat">         \
						<th>sh%</th class = "table_stat">       \
						</tr>'
	}
	$('#stat_table').html(tableHTML)
}