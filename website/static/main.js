const api_url = "https://api.open-meteo.com/v1/forecast?hourly=temperature_2m,precipitation,surface_pressure&temperature_unit=fahrenheit"

const options = {
    enableHighAccuracy: false,
    timeout: 10000,
    maximumAge: 1000500,
};

function getPosition() {
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, options);
    });
}

async function getTodaysData(latitude, longitude) {

    const date = new Date();
    today = date.toISOString().slice(0,10);

    try {
        url = api_url + "&latitude=" + latitude + "&longitude=" + longitude + '&start_date=' + today + '&end_date=' + today;
        const response = await fetch(url);
        const data = await response.json();
        console.log(data.hourly.precipitation)
        return data;

    } catch(e) {
        alert('Error: ' + e.message);
    }

}

async function getForecast(latitude, longitude) {

    console.log('getting forecast')


    const date = new Date();
    let next_week = new Date();

    next_week.setDate(date.getDate() + 6);

    next_week = next_week.toISOString().slice(0,10);
    let today = date.toISOString().slice(0,10);

    const forecast_api_url = api_url + "&latitude=" + latitude + "&longitude=" + longitude + `&start_date=${today}&end_date=${next_week}`;

    let response = await fetch(forecast_api_url);
    let data = await response.json();
    console.log(forecast_api_url)

    return data;
}
// perhaps refactor this and the previous two methods, so that only use one method for all 3 situations
async function getPrevData(latitude, longitude) {
    const date = new Date();
    let prev_week = new Date();
    let yesterday = new Date();

    prev_week.setDate(date.getDate() - 7);
    yesterday.setDate(date.getDate() - 1)


    prev_week = prev_week.toISOString().slice(0,10);
    yesterday = yesterday.toISOString().slice(0,10);

    const forecast_api_url = api_url + "&latitude=" + latitude + "&longitude=" + longitude + `&start_date=${prev_week}&end_date=${yesterday}`;

    let response = await fetch(forecast_api_url);
    let data = await response.json();

    return data;
}


document.addEventListener('DOMContentLoaded', async (event) => {


    console.log('before get position')
    let position = await getPosition();
    console.log('after get position')

    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;
    let data = await getTodaysData(latitude, longitude);

    // const submit_button = document.getElementById('submit-form-btn');
    // const

    // if (submit_button.classList.contains('active')) button.disabled = "false";
    // else button.disabled = "false"

    // let days = document.getElementsByClassName('days')[0];

    // days.classList.add('data')

    // let position = await getPosition();
    // let latitude = position.coords.latitude;
    // let longitude = position.coords.longitude;
    // let data = await getTodaysData(latitude, longitude);

    // const average = arr => arr.reduce( ( p, c ) => p + c, 0 ) / arr.length;
    // const sum = arr => arr.reduce( (accum, cur) => accum + cur, 0);

    // const container = document.getElementsByClassName('data')[0];

    // const temp_element = document.getElementById('temp');
    // const pressure_element = document.getElementById('pressure');
    // const precipitation_element = document.getElementById('precip');

    console.log('before awaiting data')

    let pressure_arr = await data.hourly.surface_pressure;
    let temp_arr = await data.hourly.temperature_2m;
    let precip_arr = await data.hourly.precipitation;
    console.log('after awaiting data')


    // temp_element.data = temperature;
    // pressure_element.data = pressure;
    // precipitation_element.data = precipitation;

    // temp_element.innerText = temperature;
    // pressure_element.innerText = pressure;
    // precipitation_element.innerText = precipitation;

    // container.appendChild(temp_element);
    // container.appendChild(pressure_element);
    // container.appendChild(precipitation_element);

    const form = document.getElementById('energy-mood-form');
    const mood_prediction_btn = document.getElementById('mood-forecast-btn');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        console.log('inside submit data')
        console.log('check if data is here. temp array must display')
        console.log(temp_arr)

        let mood = parseInt(document.getElementById('mood-slider').value);
        let energy = parseInt(document.getElementById('energy-slider').value);

        let response = await fetch('/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ temperature: temp_arr,
                                   pressure: pressure_arr,
                                   precipitation: precip_arr,
                                   mood: mood,
                                   energy: energy })
        });


        if (response.status == 200){
            window.location.href = '/';
        }

        if (response.status == 401){
            console.log('unauthorized')
            window.location.href = '/login';
        }

    });

    mood_prediction_btn.addEventListener('click', async (event) => {

        event.preventDefault();

        const forecast = await getForecast(latitude, longitude);

        const average_pressures = hourly_to_averages(forecast.hourly.surface_pressure);
        const average_temps = hourly_to_averages(forecast.hourly.temperature_2m);
        const average_precip = hourly_to_sums(forecast.hourly.precipitation);
        // get historical data from last 7 days
        const prev_data = await getPrevData(latitude, longitude);

        const historical_average_pressures = hourly_to_averages(prev_data.hourly.surface_pressure);
        const historical_average_temps = hourly_to_averages(prev_data.hourly.temperature_2m);
        const historical_average_precip = hourly_to_sums(prev_data.hourly.precipitation);

        // for (let i=0; i < days.length; i++){
        //     let date = new Date();
        //     days[i].innerText = date.setDate(date.getDate() + i);

        //     console.log('in days')
        // }



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

        if(response.status == 401){
            window.location.href='/login'
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
