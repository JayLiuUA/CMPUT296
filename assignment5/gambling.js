/*
collaborating student: Yuan Wang
sources:
https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API/Using_Fetch
https://stackoverflow.com/questions/48158190/how-do-i-print-fetch-promise-value-in-reactjs
https://www.mkyong.com/javascript/how-to-access-json-object-in-javascript/
https://developer.mozilla.org/en-US/docs/Web/API/FormData
http://www.w3school.com.cn/ajax/ajax_xmlhttprequest_send.asp
https://www.w3schools.com/jsref/dom_obj_style.asp
*/

class Gambler {
    constructor(url, token) {
        this.url = url;
        this.token = token;

        var money = document.getElementsByTagName("output")[2];
        var session = document.getElementsByTagName("output")[1];
        var status = document.getElementsByTagName("output")[0];

        // requirement 2
        fetch(url).then(function(response) {
            if (response.ok !== true) {
                console.log('Problem in fetching');
                return;
            } else {
                response.text().then(function(data) {
                    console.log(data);
                });
            }
        })

        // requirement 3
        var encoded = encodeURIComponent(token);
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.open("POST", url + 'sit', true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var response = xmlhttp.responseText;
                var json_response = JSON.parse(response);
                // display status
                status.innerText = xmlhttp.status + ' ' + xmlhttp.statusText;
                money.innerText = json_response.money;
                session.innerText = json_response.session;

                // gray out buttons
                document.getElementsByTagName("button")[1].disabled = true;
                document.getElementsByTagName("button")[2].disabled = true;
                document.getElementsByTagName("button")[3].disabled = true;
                document.getElementsByTagName("button")[4].disabled = true;

                console.log(response);
            }
        }
        xmlhttp.send("token=" + encoded);
    }

    bet(amount) {
        var amount_encoded = encodeURIComponent(amount);
        var session = document.getElementsByTagName("output")[1];
        var encoded = encodeURIComponent(this.token);
        var money = document.getElementsByTagName("output")[2];
        var dealer_cards = document.getElementsByTagName("output")[3];
        var player_cards = document.getElementsByTagName("output")[4];
        var xmlhttp = new XMLHttpRequest();
        var result = document.getElementsByTagName("output")[5];
        var bet_amount = document.getElementsByTagName("output")[6];
        var won = document.getElementsByTagName("output")[7];

        xmlhttp.open("POST", this.url + session.innerText + '/bet', true);

        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var response = xmlhttp.responseText;
                console.log(response);
                var json_response = JSON.parse(response);

                try {
                    money.innerText = json_response.money;
                    var changed1 = changeCards(json_response.game.dealer_hand);
                    dealer_cards.innerText = changed1;
                    var changed2 = changeCards(json_response.game.player_hand);
                    player_cards.innerText = changed2;
                    result.innerText = ' ';
                    bet_amount.innerText = json_response.game.bet;
                    won.innerText = '0';
                    // gray out buttons
                    document.getElementsByTagName("button")[0].disabled = true;
                    document.getElementsByTagName("button")[1].disabled = false;
                    document.getElementsByTagName("button")[2].disabled = false;
                    document.getElementsByTagName("button")[3].disabled = false;
                    document.getElementsByTagName("button")[4].disabled = false;
                } catch (error) {
                    money.innerText = json_response.money;
                    var changed1 = changeCards(json_response.last_game.dealer_hand);
                    dealer_cards.innerText = changed1;
                    var changed2 = changeCards(json_response.last_game.player_hand);
                    player_cards.innerText = changed2;
                    result.innerText = json_response.last_game.result;
                    bet_amount.innerText = json_response.last_game.bet;
                    won.innerText = json_response.last_game.won;
                    effect(result);
                    setTimeout(function() {
                        result.style.fontSize = '42px'
                    }, 600);
                    // gray out buttons
                    document.getElementsByTagName("button")[0].disabled = false;
                    document.getElementsByTagName("button")[1].disabled = true;
                    document.getElementsByTagName("button")[2].disabled = true;
                    document.getElementsByTagName("button")[3].disabled = true;
                    document.getElementsByTagName("button")[4].disabled = true;
                }
            }
        }

        xmlhttp.send("token=" + encoded + "&" + "amount=" + amount_encoded);

    }

    stand() {
        var session = document.getElementsByTagName("output")[1];
        var encoded = encodeURIComponent(this.token);
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.open("POST", this.url + session.innerText + '/stand', true);

        // gray out buttons
        document.getElementsByTagName("button")[0].disabled = false;
        document.getElementsByTagName("button")[1].disabled = true;
        document.getElementsByTagName("button")[2].disabled = true;
        document.getElementsByTagName("button")[3].disabled = true;
        document.getElementsByTagName("button")[4].disabled = true;

        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var response = xmlhttp.responseText;
                console.log(response);
                var json_response = JSON.parse(response);
                // display money
                var money = document.getElementsByTagName("output")[2];
                money.innerText = json_response.money;
                // display cards
                var dealer_cards = document.getElementsByTagName("output")[3];
                var changed1 = changeCards(json_response.last_game.dealer_hand);
                dealer_cards.innerText = changed1;
                var player_cards = document.getElementsByTagName("output")[4];
                var changed2 = changeCards(json_response.last_game.player_hand);
                player_cards.innerText = changed2;
                // display result
                var result = document.getElementsByTagName("output")[5];
                result.innerText = json_response.last_game.result;
                effect(result);
                setTimeout(function() {
                    result.style.fontSize = '42px'
                }, 600);
                var bet_amount = document.getElementsByTagName("output")[6];
                bet_amount.innerText = json_response.last_game.bet;
                var won = document.getElementsByTagName("output")[7];
                won.innerText = json_response.last_game.won;
            }
        }

        xmlhttp.send("token=" + encoded);
    }

    hit() {
        var session = document.getElementsByTagName("output")[1];
        var encoded = encodeURIComponent(this.token);
        var money = document.getElementsByTagName("output")[2];
        var dealer_cards = document.getElementsByTagName("output")[3];
        var player_cards = document.getElementsByTagName("output")[4];
        var result = document.getElementsByTagName("output")[5];
        var bet_amount = document.getElementsByTagName("output")[6];
        var won = document.getElementsByTagName("output")[7];


        var xmlhttp = new XMLHttpRequest();

        xmlhttp.open("POST", this.url + session.innerText + '/hit', true);

        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var response = xmlhttp.responseText;
                console.log(response);
                var json_response = JSON.parse(response);
                try {
                    money.innerText = json_response.money;
                    var changed1 = changeCards(json_response.last_game.dealer_hand);
                    dealer_cards.innerText = changed1;
                    var changed2 = changeCards(json_response.last_game.player_hand);
                    player_cards.innerText = changed2;
                    result.innerText = json_response.last_game.result;
                    effect(result);
                    setTimeout(function() {
                        result.style.fontSize = '42px'
                    }, 600);
                    bet_amount.innerText = json_response.last_game.bet;
                    won.innerText = json_response.last_game.won;
                    // gray out buttons
                    document.getElementsByTagName("button")[0].disabled = false;
                    document.getElementsByTagName("button")[1].disabled = true;
                    document.getElementsByTagName("button")[2].disabled = true;
                    document.getElementsByTagName("button")[3].disabled = true;
                    document.getElementsByTagName("button")[4].disabled = true;
                } catch (error) {
                    money.innerText = json_response.money;
                    if (typeof json_response.game.won != 'undefined') {
                        won.innerText = json_response.game.won;
                        result.innerText = json_response.game.result;
                    }
                    won.innerText = ' ';
                    result.innerText = ' ';
                    var changed1 = changeCards(json_response.game.dealer_hand);
                    dealer_cards.innerText = changed1;
                    var changed2 = changeCards(json_response.game.player_hand);
                    player_cards.innerText = changed2;
                    bet_amount.innerText = json_response.game.bet;
                    // gray out buttons
                    document.getElementsByTagName("button")[0].disabled = true;
                    document.getElementsByTagName("button")[1].disabled = false;
                    document.getElementsByTagName("button")[2].disabled = false;
                    document.getElementsByTagName("button")[3].disabled = false;
                    document.getElementsByTagName("button")[4].disabled = true;
                }
            }
        }

        xmlhttp.send("token=" + encoded);
    }

    double_down() {
        var session = document.getElementsByTagName("output")[1];
        var encoded = encodeURIComponent(this.token);
        var xmlhttp = new XMLHttpRequest();
        var money = document.getElementsByTagName("output")[2];
        var dealer_cards = document.getElementsByTagName("output")[3];
        var player_cards = document.getElementsByTagName("output")[4];
        var result = document.getElementsByTagName("output")[5];
        var bet_amount = document.getElementsByTagName("output")[6];
        var won = document.getElementsByTagName("output")[7];


        xmlhttp.open("POST", this.url + session.innerText + '/double_down', true);
        // gray out buttons
        document.getElementsByTagName("button")[0].disabled = false;
        document.getElementsByTagName("button")[1].disabled = true;
        document.getElementsByTagName("button")[2].disabled = true;
        document.getElementsByTagName("button")[3].disabled = true;
        document.getElementsByTagName("button")[4].disabled = true;

        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var response = xmlhttp.responseText;
                console.log(response);
                var json_response = JSON.parse(response);
                money.innerText = json_response.money;
                var changed1 = changeCards(json_response.last_game.dealer_hand);
                dealer_cards.innerText = changed1;
                var changed2 = changeCards(json_response.last_game.player_hand);
                player_cards.innerText = changed2;
                result.innerText = json_response.last_game.result;
                effect(result);
                setTimeout(function() {
                    result.style.fontSize = '42px'
                }, 600);
                bet_amount.innerText = json_response.last_game.bet;
                won.innerText = json_response.last_game.won;
            }
        }

        xmlhttp.send("token=" + encoded);
    }

    surrender() {
        var session = document.getElementsByTagName("output")[1];
        var encoded = encodeURIComponent(this.token);
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.open("POST", this.url + session.innerText + '/surrender', true);

        // gray out buttons
        document.getElementsByTagName("button")[0].disabled = false;
        document.getElementsByTagName("button")[1].disabled = true;
        document.getElementsByTagName("button")[2].disabled = true;
        document.getElementsByTagName("button")[3].disabled = true;
        document.getElementsByTagName("button")[4].disabled = true;

        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var response = xmlhttp.responseText;
                console.log(response);
                var json_response = JSON.parse(response);
                // display money
                var money = document.getElementsByTagName("output")[2];
                money.innerText = json_response.money;
                // display cards
                var dealer_cards = document.getElementsByTagName("output")[3];
                var changed1 = changeCards(json_response.last_game.dealer_hand);
                dealer_cards.innerText = changed1;
                var player_cards = document.getElementsByTagName("output")[4];
                var changed2 = changeCards(json_response.last_game.player_hand);
                player_cards.innerText = changed2;
                // display result
                var result = document.getElementsByTagName("output")[5];
                result.innerText = json_response.last_game.result;
                effect(result);
                setTimeout(function() {
                    result.style.fontSize = '42px'
                }, 600);
                var bet_amount = document.getElementsByTagName("output")[6];
                bet_amount.innerText = json_response.last_game.bet;
                var won = document.getElementsByTagName("output")[7];
                won.innerText = json_response.last_game.won;
            }
        }
        xmlhttp.send("token=" + encoded);
    }
}

function changeCards(cards) {
    var i;
    for (i = 0; i < cards.length; i++) {
        if (cards[i] == 1) {
            cards[i] = 'Ace';
        } else if (cards[i] == 11) {
            cards[i] = 'J';
        } else if (cards[i] == 12) {
            cards[i] = 'Q';
        } else if (cards[i] == 13) {
            cards[i] = 'K';
        }
    }
    return cards
}

function effect(result) {
    var text = result.innerText;
    result.style.fontSize = '150%';
    if (text == 'win') {
        result.style.color = 'red';
    } else if (text == 'lose') {
        result.style.color = 'gray';
    } else if (text == 'tie') {
        result.style.color = 'green';
    } else if (text == 'blackjack') {
        result.style.color = 'purple';
    } else if (text == 'bust') {
        result.style.color = 'blue';
    } else if (text == 'surrender') {
        result.style.color = 'orange';
    }
}
