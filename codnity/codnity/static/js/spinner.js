// API url 
const api_url = "http://localhost:8000/hacker_news/update_results";

async function getapi() {
    document.getElementById('submit').style.display='none';
    document.getElementById('spinner').style.display='block';
    const response = await fetch(api_url);

    if (response) {
        hideSpinner();
    }
}

function hideSpinner() {
    document.getElementById('spinner').style.display='none';
    document.getElementById('submit').style.display='block';
    location.reload();
}

$(document).ready(function (){
    document.getElementById('spinner').style.display='none';
});