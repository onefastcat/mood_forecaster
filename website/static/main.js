
// will need to change the latitude and longitude based on what address user provides

const api_url = "https://api.open-meteo.com/v1/forecast?hourly=temperature_2m,precipitation,surface_pressure&temperature_unit=fahrenheit"

const options = {
    enableHighAccuracy: true,
    maximumAge: 86400000
};


async function getPosition() {
    return new Promise((resolve, reject) =>
        navigator.geolocation.getCurrentPosition(resolve, reject, options)
    );
}


async function getTodaysData() {

    const date = new Date();
    today = date.toISOString().slice(0,10);
    let position;

    try {
        position = await getPosition();
    } catch(e) {
        alert('Error: ' + e.message);
    }

    url = api_url + "&latitude=" + position.coords.latitude + "&longitude=" + position.coords.longitude + '&start_date=' + today + '&end_date=' + today;

    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    }
    catch(e) {
        alert('Error: ' + e.message)
    }
}

async function getForecast() {
    const date = new Date();
    let next_week = new Date();
    let tomorrow = new Date();

    next_week.setDate(date.getDate() + 7);
    tomorrow.setDate(date.getDate() + 1)

    next_week = next_week.toISOString().slice(0,10);
    tomorrow = tomorrow.toISOString().slice(0,10);

    const forecast_api_url = api_url.concat(`&start_date=${tomorrow}&end_date=${next_week}`);

    let response = await fetch(forecast_api_url);
    let data = await response.json();
    console.log(forecast_api_url)

    return data;
}
// perhaps refactor this and the previous two methods, so that only use one method for all 3 situations
async function getPrevData() {
    const date = new Date();
    let prev_week = new Date();
    let yesterday = new Date();

    prev_week.setDate(date.getDate() - 7);
    yesterday.setDate(date.getDate() - 1)

    prev_week = prev_week.toISOString().slice(0,10);
    yesterday = yesterday.toISOString().slice(0,10);

    const forecast_api_url = api_url.concat(`&start_date=${prev_week}&end_date=${yesterday}`);

    let response = await fetch(forecast_api_url);
    let data = await response.json();

    return data;
}


addEventListener('DOMContentLoaded', async (event) => {

    let data = await getTodaysData();


    const average = arr => arr.reduce( ( p, c ) => p + c, 0 ) / arr.length;
    const sum = arr => arr.reduce( (accum, cur) => accum + cur, 0);

    const container = document.getElementsByClassName('data')[0];

    // + removes the last zeroes at the end of floats
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
    const mood_prediction_btn = document.getElementById('mood_forecast');



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

        window.location.href = '/';


    });

    mood_prediction_btn.addEventListener('click', async(event) => {

        event.preventDefault();

        const forecast = await getForecast();

        const average_pressures = hourly_to_averages(forecast.hourly.surface_pressure);
        const average_temps = hourly_to_averages(forecast.hourly.temperature_2m);
        const average_precip = hourly_to_sums(forecast.hourly.precipitation);
        // get historical data from last 7 days
        const prev_data = await getPrevData();

        const historical_average_pressures = hourly_to_averages(prev_data.hourly.surface_pressure);
        const historical_average_temps = hourly_to_averages(prev_data.hourly.temperature_2m);
        const historical_average_precip = hourly_to_sums(prev_data.hourly.precipitation);


        let response = await fetch('/mood-forecast', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                            pressure: average_pressures,
                            temp: average_temps,
                            precip: average_precip,
                            historical_pressure: historical_average_pressures,
                            historical_precip: historical_average_precip,
                            historical_temp: historical_average_temps
            })
        });

        if(response.status == 200){
            window.location.href='/mood-forecast'
        }


    });

    function hourly_to_averages(dataArr) {
        let sum = 0;
        let arr_averages = [];

        for( let i = 0; i < dataArr.length; i++){
            // console.log(i)
            sum += dataArr[i];
            //adds a sum of pressures for 24 hours (1 day)
            //resets the sum for further calculation for next 24 hour period
            if(i % 24 === 23 && i !== 1){
                let daily_average = +(sum/24).toFixed(5);
                arr_averages.push(daily_average);
                sum = 0;
            }
        }

        return arr_averages;
    }

    function hourly_to_sums(dataArr) {
        let sum = 0;
        let arr_sums = [];

        for( let i = 0; i < dataArr.length; i++){
            // console.log(i)
            sum += dataArr[i];
            //adds a sum of pressures for 24 hours (1 day)
            //resets the sum for further calculation for next 24 hour period
            if(i % 24 === 23 && i !== 1){
                arr_sums.push(sum);
                sum = 0;
            }
        }

        return arr_sums;
    }




});
