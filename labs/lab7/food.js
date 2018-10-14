function askForFavouriteFood() {
    var faveFood = prompt('What is your favourite food?');
    faveFood = faveFood.toLowerCase();
    faveFood = faveFood.trim();
    if (faveFood === 'papasas') {
        alert('Yay! Pupusas are my favourite too!');
    }
    else {
        alert(faveFood);
    }
}