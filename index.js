/*
https://michael-harris-dr.github.io/fantasy_hockey/
*/
var nameList = []
var tableData = []
var teamGP = []
//TODO improve error handling
const LIVE = true

const API_URL = LIVE ? "https://fantasy-hockey.onrender.com" : "http://127.0.0.1:10000"

$(document).ready(function()
{
	fill_teamGP()

	$("#search_field").on("focus", function()
	{
		if(this.value == '')
		{
			this.placeholder = ''
		}
	});

	$("#search_field").on("focusout", function()
	{
		if(this.value == '')
		{
			this.placeholder = "Enter player surname..."
		}
	});

	$("#search_field").keydown(function(event)
	{
		if(event.keyCode === 13)
		{
			event.preventDefault();
			$("#search_button").click();
		}
	});

	$(document).on('click', '#search_button', function()
	{
		this.blur()

		if(teamGP.length < 1)
		{
			fill_teamGP()
		}

		var field_val = pascalify($('#search_field').val())

		if(!(nameList.includes(field_val)))
		{
			$.ajax({
				type: 'GET',
				dataType: "json",
				url: `${API_URL}/players`,
				headers: {
					"Access-Control-Allow-Origin": "True",
					"x-api-key": "4132"
				},
				data: {
					"Players": JSON.stringify([field_val])
				},
				error: function()
				{
					alert("Error: Failed to connect to backend service, please try again later.")
				},
				success: function(data, status)
				{
					console.log("SUCCESS")
					resp = JSON.parse(data)
					console.log(`${API_URL}/players: `, resp);

					if(Object.keys(data).length > 2) 
					{
						tableData = (resp)
						add_to_table()
					}


					nameList.push(resp[0]["lastName"])
				}
			});
		}

		$("#search_field").val('');
	});

});

$(document).on('click', '#delete_row_button', function()
{
	pid = this.dataset.player_id

	console.log("deleting: ", pid)


	nameList.splice(nameList.indexOf(this.dataset.player_surname), 1)

	console.log(this.dataset.player_surname)
	console.log(nameList)

	$("." + pid).remove();
});

function pascalify(string) 
{
	return string.charAt(0).toUpperCase() + string.substring(1).toLowerCase()
}

function add_to_table()
{
	for(var player in tableData)
	{
		projectedStats = predict_future(tableData[player])
		stats = tableData[player]
		var tableHTML = `<tbody class="player_rows">
							<tr class="table_row ${stats["id"]}">
								<td class="table_pic" rowspan="2"><img class="headshot" src=${stats["headshot"]}></td>
								<td class="table_player_name" rowspan="2">${stats["lastName"]} ${stats["special"]}</td>
								<td class="table_stat stat_type">Current:</td>
								<td class="table_stat">${stats["seasons"]["20232024"]["gp"]}</td>
								<td class="table_stat">${stats["seasons"]["20232024"]["goals"]}</td>
								<td class="table_stat">${stats["seasons"]["20232024"]["assists"]}</td>
								<td class="table_stat">${stats["seasons"]["20232024"]["points"]}</td>
								<td class="table_stat">${(100 * stats["seasons"]["20232024"]["shp"]).toFixed(1)}</td>
								<td class="table_stat">${Number(stats["seasons"]["20232024"]["goals"]) * 3 + 2 * Number(stats["seasons"]["20232024"]["assists"])}</td>
								<td class="delete_btn" rowspan="2">
								<input type="button" id="delete_row_button" value="x" data-player_id="${stats["id"]}" data-player_surname="${stats["lastName"]}"></td>
							</tr>
							<tr class="table_row ${stats["id"]}">
								<td class="table_stat stat_type">Projected:</td>
								<td class="table_stat">${projectedStats["gp"]}</td>
								<td class="table_stat">${projectedStats["goals"]}</td>
								<td class="table_stat">${projectedStats["assists"]}</td>
								<td class="table_stat">${projectedStats["points"]}</td>
								<td class="table_stat">${projectedStats["shp"]}</td>
								<td class="table_stat">${projectedStats["fanPts"]}</td>
							</tr>
						</tbody>`
		document.getElementById("stat_table").innerHTML += tableHTML
	}
}

function predict_future(player)
{
	gpList = []
	sh = []
	relativeWeight = []
	relevantGP = 0


	gamesLeft = 82 - teamGP[player['team']]

	//find current season
	let currentSeason = -1;
	for(let season in player["seasons"])
	{
		if(season > currentSeason)
		{
			currentSeason = season
		}
	}

	currentAssistsPerGame = player["seasons"][currentSeason]["assists"] / player["seasons"][currentSeason]["gp"]
	currentShp = player["seasons"][currentSeason]["shp"]
	currentG = player["seasons"][currentSeason]["goals"]
	currentSpg = (currentG / currentShp) / player["seasons"][currentSeason]["gp"]

	//find most recent three seasons
	let relevantSeasons = []
	for(let season in player["seasons"])
	{
		if((currentSeason - season) < 40000 && (currentSeason - season) != 0)
		{
			relevantSeasons.push(season)
		}
	}

	for(let season in player["seasons"])
	{
		if(relevantSeasons.includes(season))
		{
			gpList.push(player["seasons"][season]["gp"])
			sh.push(player["seasons"][season]["shp"])
			relevantGP += player["seasons"][season]["gp"]
		}
	}

	let projPct = 0.0

	if(relevantSeasons.length < 3)
	{
		gpList.push(player["seasons"][currentSeason]["gp"])
		sh.push(player["seasons"][currentSeason]["shp"])
		relevantGP += player["seasons"][currentSeason]["gp"]
	}

	for(season in gpList)
	{
		projPct += sh[season] * gpList[season] / relevantGP
	}

	projGoals = gamesLeft * (currentSpg * projPct)
	projApps = gamesLeft * (currentAssistsPerGame)
	projFP = 3 * projGoals + 2 * projApps

	return {
		"goals": projGoals.toFixed(1),
		"assists": projApps.toFixed(1),
		"gp": gamesLeft,
		"shp": (100 * projPct).toFixed(1),
		"points": (projGoals + projApps).toFixed(1),
		"fanPts": (projGoals * 3 + 2 * projApps).toFixed(1)
	}
}

function fill_teamGP()
{
	console.log("Populating teamGP...")
	$.ajax({
		type: 'GET',
		dataType: "json",
		url: `${API_URL}/teams`,
		headers: {
			"Access-Control-Allow-Origin": "True",
			"x-api-key": "4132"
		},
		data: {
		},
		success: function(data, status)
		{
			teamGP = JSON.parse(data)
			console.log(`${API_URL}/teams: `, teamGP);
		}
	});
}
