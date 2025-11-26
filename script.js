const kysymysalue = document.getElementById("kysymysalue");
const vastausalue = document.getElementById("vastausalue");

vastausalue.innerHTML = "<form id='choose_name'><input id='namebox' name='namebox' type='text'><input type='submit' value='Confirm name'></form>"

const choose_name = document.querySelector('#choose_name')

choose_name.addEventListener('submit', async function(evt){
    evt.preventDefault();

    let player_name = document.querySelector('input[name=namebox]').value;
    kysymysalue.innerHTML = "Player name: "+player_name;

    vastausalue.innerHTML = "<form id='start_game'><input type='submit' value='Start game'></form>";

    const start_game = document.querySelector('#start_game');
    let round = 1;
    let money = 0;

    start_game.addEventListener('submit', async function(evt){
        evt.preventDefault();


        try {
            const response = await fetch(`http://127.0.0.1:3000/${round}`);
            const jsonData = await response.json();
            console.log(jsonData);

            if (jsonData["kysymysteksti"][0] === "What is the distance between " || jsonData["kysymysteksti"][0] === "How many kilotons of CO2 emmission are produced on a flight between ") {
                kysymysalue.innerHTML = '';
                kysymysalue.innerHTML += jsonData["kysymysteksti"][0];
                kysymysalue.innerHTML += jsonData["kysymys"][0][0] +" and "+jsonData["kysymys"][1][0];
                kysymysalue.innerHTML += jsonData["kysymysteksti"][1]
            }
            else {
                kysymysalue.innerHTML = '';
                kysymysalue.innerHTML += jsonData["kysymysteksti"][0];
                kysymysalue.innerHTML += jsonData["kysymys"][0];
                kysymysalue.innerHTML += jsonData["kysymysteksti"][1]
            }

            vastausalue.innerHTML = '';
            vastausalue.innerHTML += "<button name='vastaus1' value='A'>Vastausteksti</button>";
            vastausalue.innerHTML += "<button name='vastaus2' value='B'>Vastausteksti</button>";
            vastausalue.innerHTML += "<button name='vastaus3' value='C'>Vastausteksti</button>";
            vastausalue.innerHTML += "<button name='vastaus4' value='D'>Vastausteksti</button>";
            vastausalue.innerHTML += "<br><button name='oljenkorsi' value='E'>Use a lifeline</button>";

            let vastaus1 = document.querySelector('button[name=vastaus1]');
            let vastaus2 = document.querySelector('button[name=vastaus2]');
            let vastaus3 = document.querySelector('button[name=vastaus3]');
            let vastaus4 = document.querySelector('button[name=vastaus4]');

            vastaus1.innerHTML = jsonData["vastaus1"][0]+": "+jsonData["vastaus1"][1];
            vastaus2.innerHTML = jsonData["vastaus2"][0]+": "+jsonData["vastaus2"][1];
            vastaus3.innerHTML = jsonData["vastaus3"][0]+": "+jsonData["vastaus3"][1];
            vastaus4.innerHTML = jsonData["vastaus4"][0]+": "+jsonData["vastaus4"][1];
        }
        catch (error) {
        console.log(error.message);
        }
    });
});
