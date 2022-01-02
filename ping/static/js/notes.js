window.onload = init;
let isActive = false;

function init() {
    console.log('toto');
    document.getElementById('add').addEventListener("click", addForm);

}

function addForm() {
    if (!isActive) {
        isActive = true;
        document.getElementById('form-container').innerHTML +=
            '<textarea placeholder="Rentrez votre commentaire..." id="note" name="note"></textarea>' +
            '<input type="submit" value="VALIDER"/>';
    }

}