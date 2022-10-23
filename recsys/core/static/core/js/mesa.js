$(document).ready(function () {
  $("#test").CreateMultiCheckBox({ width: '230px',
             defaultText : 'Select Below', height:'250px' });
});

window.addEventListener('DOMContentLoaded', event => {

    console.log("Entrou na função certo");

    let squads_text = document.getElementById("squads").textContent;

    console.log("pegou as squads");
    console.log(squads_text);

    const squads = squads_text.split(",");

    console.log(squads);

    squads.forEach(myFunction);

    function myFunction(item, index) {
        const datatablesSimple = document.getElementById('table'+item);
        if (datatablesSimple) {
            new simpleDatatables.DataTable(datatablesSimple);
        }
    }
});