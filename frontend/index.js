nameList = []

$(document).ready(function () {

    $("#search_field").keydown(function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            $("#search_button").click();
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
                    $('#player_name').append('\n' + field_val)
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
                    $('#player_name').append('\n' + field_val);
                }
            }
        });
    });

});

function pascalify(string) 
{
    return string.charAt(0).toUpperCase() + string.substring(1).toLowerCase()
}