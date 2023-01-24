const api_url = "https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.01&hourly=temperature_2m,precipitation,surface_pressure,cloudcover&temperature_unit=fahrenheit"

async function getData() {

    const date = new Date();
    today = date.toISOString().slice(0,10);
    console.log(today)

    const current_api_url = api_url.concat(`&start_date=${today}&end_date=${today}`);

    const response = await fetch(current_api_url);
    const data = await response.json();

    return data;
}


addEventListener('DOMContentLoaded', async (event) => {

    let data = await getData();

    console.log(data)

    const average = arr => arr.reduce( ( p, c ) => p + c, 0 ) / arr.length;
    const sum = arr => arr.reduce( (accum, cur) => accum + cur, 0);

    const container = document.getElementsByClassName('data')[0];

    const pressure = +average(data.hourly.surface_pressure).toFixed(5);
    const temperature = +average(data.hourly.temperature_2m).toFixed(5);
    const precipitation = +sum(data.hourly.precipitation).toFixed(5);

    const temp_element = document.createElement('div');
    const pressure_element = document.getElementById('pressure');
    const precipitation_element = document.createElement('div');

    temp_element.name = 'temperature';
    //pressure_element.name = 'pressure';
    precipitation_element.name = 'precipitation';

    temp_element.data = temperature;
    pressure_element.data = pressure;
    precipitation_element.data = precipitation;

    temp_element.innerText = temperature;
    pressure_element.innerText = pressure;
    precipitation_element.innerText = precipitation;

    container.appendChild(temp_element);
    container.appendChild(pressure_element);
    container.appendChild(precipitation_element);



    const form = document.getElementById('form');

    form.addEventListener('submit', async (event) => {

        let mood = parseInt(document.getElementById('mood-slider').value);
        let energy = parseInt(document.getElementById('energy-slider').value);

        event.preventDefault();

        let response = await fetch('/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ temperature: temperature,
                                   pressure: pressure,
                                   precipitation: precipitation,
                                   mood: mood,
                                   energy: energy })
        });

    });

});
