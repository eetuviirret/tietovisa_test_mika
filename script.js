//Muuttujat HTML-sivun alueille
const kysymysalue = document.getElementById("kysymysalue");
const vastausalue = document.getElementById("vastausalue");

//Pelimuuttuja
const game = {
    //Alustetaan muuttujia peliin
    kysymys: [],
    kierros: 0,
    score: 1,
    olki1: 1,
    olki2: 1,
    olki3: 1,

    //Init -funktio käynnistää pelin
    async init(name) {
        //Haetaan kysymys
        this.kysymys = await kysymyshaku(this.kierros);
        //Tallennetaan pelaajan nimi
        this.player_name = name;
        //Printataan pelaajan nimi
        this.printUsername();
        this.exit();
        //Printataan kysymys
        this.kysymysfunktio();
        //Printataan kysymysnumero
        this.printScore();

    },
    //Printataan pelaajan nimi
    printUsername() {
        document.getElementById("username").innerHTML = "Username:<br>"  + this.player_name;
    },
    printScore(){
        document.getElementById("kysymysnro").innerHTML = "NRO/" + this.score;
    },
    exit(){
         const exit_button = document.createElement("button");

         exit_button.textContent = 'EXIT';
         exit_button.id = "exit";

         //Event listener jokaiselle napille
        exit_button.addEventListener("click", () => {refresh();
        });
        document.getElementById("exit").appendChild(exit_button);



    },

    money() {

    },

    kysymysfunktio() {
        //Tarkastetaan kysymyksen muoto ja printataan se
        if (this.kysymys["kysymysteksti"][0] === "What is the distance between " || this.kysymys["kysymysteksti"][0] === "How many kilotons of CO2 emmission are produced on a flight between ") {
            kysymysalue.innerHTML = '';
            kysymysalue.innerHTML += this.kysymys["kysymysteksti"][0];
            kysymysalue.innerHTML += this.kysymys["kysymys"][0][0] +" and "+this.kysymys["kysymys"][1][0];
            kysymysalue.innerHTML += this.kysymys["kysymysteksti"][1]
        }
        else {
            kysymysalue.innerHTML = '';
            kysymysalue.innerHTML += this.kysymys["kysymysteksti"][0];
            kysymysalue.innerHTML += this.kysymys["kysymys"][0];
            kysymysalue.innerHTML += this.kysymys["kysymysteksti"][1]
        }

    //Tyhjennetään vastausalue
    vastausalue.innerHTML = "";

    //Luodaan jokaiselle vastaukselle painike
    for (let i = 1; i < 5; i++) {
        const button = document.createElement("button");

        button.textContent = this.kysymys[`vastaus${i}`][1];
        button.value = this.kysymys[`vastaus${i}`][0];
        button.id = "vastausnappi";

        //Event listener jokaiselle napille jos niitä painaa
        button.addEventListener("click", () => {
            //Ajetaan vastauksen tarkistus
            this.handleAnswer(this.kysymys[`vastaus${i}`][2]);
        });

        //Printataan painike
        vastausalue.appendChild(button);
    }

    //Ajetaan oljenkorsi-funktio
    this.oljenkorsifunktio()

    },

    //Määritetään oljenkorsi-funktio
    oljenkorsifunktio() {
        if (this.olki1 === 1 || this.olki2 === 1 || this.olki3 === 1) {
            const lifelineArea = document.createElement("div")
            lifelineArea.id = "oljenkorsialue";

            const linebreak = document.createElement("br");
            vastausalue.appendChild(linebreak);
            vastausalue.appendChild(lifelineArea)

            const lifelineButton = document.createElement("button");

            lifelineButton.textContent = "Lifelines";
            lifelineButton.id = "oljenkorsinappi";

            lifelineButton.addEventListener("click", () => {
                //Näytetään lifelinet
                lifelineArea.removeChild(lifelineButton);

                //Kysy yleisöltä
                if (this.olki1 === 1) {
                    const askAudienceButton = document.createElement("button");

                    askAudienceButton.textContent = "Ask the Audience"
                    askAudienceButton.id = "oljenkorsinappi"
                    askAudienceButton.value = "olki1"

                    askAudienceButton.addEventListener("click", () => {
                        //Oljenkorsi käytetty
                        this.olki1 = 0;

                        //ASK AUDIENCE KOODI
                        let yleiso = {
                            A: Math.floor(Math.random() * 60) + 1,
                            B: Math.floor(Math.random() * 60) + 1,
                            C: Math.floor(Math.random() * 60) + 1,
                            D: Math.floor(Math.random() * 60) + 1
                        }
                        //Tarkistetaan oikea, ja annetaan sille mahdollisuus saada enemmän ääniä
                        for (let i = 1; i < 5; i++) {
                            if (this.kysymys[`vastaus${i}`][2] === 1) {
                                if (this.kysymys[`vastaus${i}`][0] === "A") {
                                    yleiso.A = Math.floor(Math.random() * 90) + 1;
                                }
                                else if (this.kysymys[`vastaus${i}`][0] === "B") {
                                    yleiso.B = Math.floor(Math.random() * 90) + 1;
                                }
                                else if (this.kysymys[`vastaus${i}`][0] === "C") {
                                    yleiso.C = Math.floor(Math.random() * 90) + 1;
                                }
                                else if (this.kysymys[`vastaus${i}`][0] === "D") {
                                    yleiso.D = Math.floor(Math.random() * 90) + 1;
                                }
                            }
                        }
                        //Tarkistetaan onko elementti jo olemassa
                        //Jos on, muokataan sitä
                        if (document.getElementById("vihjealue") != null) {
                          document.getElementById("vihjealue").innerHTML = `The audience has voted:<br><ul><li>A: ${yleiso.A} votes</li><li>B: ${yleiso.B} votes</li><li>C: ${yleiso.C} votes</li><li>A: ${yleiso.D} votes</li></ul>`
                        }
                        //Jos ei, luodaan se
                        else {
                            const hintArea = document.createElement("div")
                            hintArea.id = "vihjealue"
                            hintArea.innerHTML = `The audience has voted:<br><ul><li>A: ${yleiso.A} votes</li><li>B: ${yleiso.B} votes</li><li>C: ${yleiso.C} votes</li><li>D: ${yleiso.D} votes</li></ul>`

                            kysymysalue.appendChild(hintArea)
                        }


                        lifelineArea.innerHTML = "";

                        if (this.olki1 === 1 || this.olki2 === 1 || this.olki3 === 1) {
                            lifelineArea.appendChild(lifelineButton)
                        }


                    });

                    lifelineArea.appendChild(askAudienceButton)
                }

                //Eliminoi puolet vääristä vastauksista
                if (this.olki2 === 1) {
                    const fiftyFiftyButton = document.createElement("button");

                    fiftyFiftyButton.textContent = "50/50"
                    fiftyFiftyButton.id = "oljenkorsinappi"
                    fiftyFiftyButton.value = "olki2"

                    fiftyFiftyButton.addEventListener("click", () => {
                        //Oljenkorsi käytetty
                        this.olki2 = 0;

                        lifelineArea.innerHTML = "";

                        //FIFTY FIFTY KOODI
                        let piilotettavat = []

                        for (let i = 1; i < 5; i++) {
                            if (this.kysymys[`vastaus${i}`][2] === 0) {
                                let selected = document.querySelector(`button[value=${this.kysymys[`vastaus${i}`][0]}]`)
                                console.log(selected)
                                piilotettavat.push(selected)
                            }
                        }

                        piilotettavat.slice(0, 2).forEach(i => i.classList.add('hidden'));

                        //Tarkistetaan onko elementti jo olemassa
                        //Jos on, muokataan sitä
                        if (document.getElementById("vihjealue") != null) {
                          document.getElementById("vihjealue").textContent = "TÄMÄ ON FIFTY FIFTY PALAUTUS"
                        }
                        //Jos ei, luodaan se
                        else {
                            const hintArea = document.createElement("div")
                            hintArea.id = "vihjealue"
                            hintArea.textContent = "TÄMÄ ON FIFTY FIFTY PALAUTUS"

                            kysymysalue.appendChild(hintArea)
                        }

                        if (this.olki1 === 1 || this.olki2 === 1 || this.olki3 === 1) {
                            lifelineArea.appendChild(lifelineButton)
                        }
                    });


                    lifelineArea.appendChild(fiftyFiftyButton)
                }

                //Kysy kaverilta
                if (this.olki3 === 1) {
                    const callFriendButton = document.createElement("button");

                    callFriendButton.textContent = "Call a Friend"
                    callFriendButton.id = "oljenkorsinappi"
                    callFriendButton.value = "olki3"

                    callFriendButton.addEventListener("click", () => {
                        //Oljenkorsi käytetty
                        this.olki3 = 0;

                        //CALL FRIEND KOODI
                        let kaveri = "";
                        let errormargin = Math.floor(Math.random() * 100) + 1

                        if (errormargin <= 50) {
                            for (let i = 1; i < 5; i++) {
                                if (this.kysymys[`vastaus${i}`][2] === 1) {
                                    kaveri = this.kysymys[`vastaus${i}`][1]
                                }
                            }
                        }
                        else {
                            for (let i = 1; i < 5; i++) {
                                if (this.kysymys[`vastaus${i}`][2] === 0) {
                                    kaveri = this.kysymys[`vastaus${i}`][1]
                                }
                            }
                        }

                        //Tarkistetaan onko elementti jo olemassa
                        //Jos on, muokataan sitä
                        if (document.getElementById("vihjealue") != null) {
                          document.getElementById("vihjealue").textContent = `I think the answer is ${kaveri}`
                        }
                        //Jos ei, luodaan se
                        else {
                            const hintArea = document.createElement("div")
                            hintArea.id = "vihjealue"
                            hintArea.textContent = `I think the answer is ${kaveri}`

                            kysymysalue.appendChild(hintArea)
                        }

                        lifelineArea.innerHTML = "";

                        if (this.olki1 === 1 || this.olki2 === 1 || this.olki3 === 1) {
                            lifelineArea.appendChild(lifelineButton)
                        }
                    });


                    lifelineArea.appendChild(callFriendButton)
                }
            });
            //Rivinvaihto


            //Printataan oljenkorsinappi
            lifelineArea.appendChild(lifelineButton);


        }
    },

    //Vastauksen tarkistus
    handleAnswer(selectedIndex) {
        //Jos valitun vastauksen arvo oli 1, se on oikein
        if (selectedIndex === 1) {
            //Lisätään score ja kierros
            this.score++;
            this.kierros++;

            //Uusi kierros, jos kierrokset ovat täynnä, lopetetaan peli
            if (this.kierros < 16) {
                this.questionright()
                //TÄMÄ KOODI KUTSUU UUDEN KYSYMYKSEN, SE KORVATAAN
                //LUO UUSI FUNKTIO JOKA TYHJENTÄÄ KYSYMYSALUEEN
                //JA PRINTTAA SIIHEN "VOITTAJA" -KUVAN SEKÄ NAPIN JOKA KUTSUU TUOTA YLLÄ OLEVAA INIT-FUNKTIOTA
            } else {
                //TÄMÄ KOHTA ON KUN PELAAJA VOITTAA PELIN
                //LUO UUSI FUNKTIO JOKA ON SAMANLAINEN KUIN GAME OVER, MUTTA ILMOITTAA PELAAJALLE VOITOSTA
                this.gameover();
            }
        }
        //Jos valitun vastauksen arvo oli 0, lopetetaan peli
        else {
            //TÄMÄ AJETAAN KUN PELAAJA VASTAA VÄÄRIN
            this.gameover();
        }
    },
    questionright() {
        const right_image = document.createElement('img');
        right_image.src= 'gif/private_plane_right_gif.gif';
        right_image.id="right_image";

        kysymysalue.textContent = "Right!";
        kysymysalue.appendChild(right_image);
        kysymysalue.innerHTML += `<br><button class='continue_button' onclick='game.init("${this.player_name}")'>Next</button>`
        vastausalue.innerHTML = "";
    },

    //Printataan lopputulos
    gameover() {
         const game_over_image = document.createElement('img');
        game_over_image.src= 'gif/private_plane_game_over_gif.gif';
        game_over_image.id="game_over_image";

        kysymysalue.textContent = "GAME OVER! "+this.player_name+`'s Quiz finished! Score: ${this.score}`;
        kysymysalue.appendChild(game_over_image);
        kysymysalue.innerHTML += "<br><button class='continue_button' onclick='refresh()'>Try again?</button> "
        vastausalue.innerHTML = "";
    }
};


//API -haku
async function kysymyshaku(kierros) {
    const response = await fetch(`http://127.0.0.1:3000/${kierros}`);
    return response.json();
}


//Printataan nimikenttä ja aloitusnappi
vastausalue.innerHTML = "<form id='start_game'><input id='namebox' name='namebox' placeholder='Enter name...' type='text'><input type='submit' value='Start game'></form>";
const start_game = document.querySelector('#start_game');

//Lisätään aloitusnappiin async event listener
start_game.addEventListener('submit', async function(evt){
    evt.preventDefault();
    const player_name = document.querySelector('input[name=namebox]').value;
    game.init(player_name);
});

//Kun haluaa aloittaa pelin uudelleen
function refresh(){
        window.location.reload("Refresh")
}
