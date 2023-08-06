$(function(){
    var datavalues = document.getElementById("data");
    var optionValues = document.getElementById("options");
    console.log(datavalues.value);
    new Chart(document.getElementById("barchart"), {
        type: 'bar',
        data: datavalues,
        options: optionValues
    });
});