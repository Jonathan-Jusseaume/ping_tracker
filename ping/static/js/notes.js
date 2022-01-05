window.onload = init;
let isActive = false;
let crsfToken;

function init() {
    crsfToken = document.getElementById('form-container').innerHTML;
    document.getElementById('add').addEventListener("click", addForm);
}

function addForm() {
    if (!isActive) {
        isActive = true;
        document.getElementById('form-container').innerHTML +=
            '<div class="form-group">' +
            '<span class="error hidden" id="note-error">Votre commentaire doit être compris entre 5 et 500 caractères</span>' +
            '<textarea placeholder="Rentrez votre commentaire..." maxlength="500" id="note" name="note"></textarea>' +
            '</div>' +
            '<div class="actions">' +
            '<input type="reset" value="EFFACER"/>' +
            '<input type="submit" value="VALIDER"/>' +
            '</div>';
        document.getElementById('form-container').classList.add("active-form")
        document.getElementById('add').innerHTML = "ANNULER";
    } else {
        isActive = false;
        document.getElementById('form-container').innerHTML = crsfToken;
        document.getElementById('form-container').classList.remove("active-form")
        document.getElementById('add').innerHTML = "AJOUTER";
    }

}

function checkForm() {
    const textArea = document.getElementById('note')
    document.getElementById('note-error').classList.add('hidden');
    document.getElementById('note').classList.remove('error-form');
    if (textArea.value.length < 5 || textArea.value > 500) {
        document.getElementById('note').classList.add('error-form');
        document.getElementById('note-error').classList.remove('hidden');
        return false;
    }
    return true;
}