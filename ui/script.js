

fetch('header.html')
    .then(response => response.text())
    .then(data => {
        document.querySelector('.header').innerHTML = data;
    })
    .catch(error => console.error('Error loading header.html:', error));


function getDataOfMonth(data,month, year){
    const monthData = data.filter(entry => {
        const entryDate = moment(entry.DateTime);
        return entryDate.month() === month && entryDate.year() === year;
    });
    console.log(monthData, "monthData");

    const historyContainer = document.querySelector('.history_weather_container');
    let monthlyHTML = `<h3>${moment.months(month)} ${year}</h3>`;
    let weather_icon = "https://www.awxcdn.com/adc-assets/images/weathericons/6.svg";
    monthData.forEach(entry => {
        const date = moment(entry.DateTime).format('MM-DD');
        monthlyHTML += `
            <div class="monthly_forecast_card">
                <div class="date">
                    <h3><strong>${getDayOfWeek(date)}</strong></h3>
                    <p>${truncate_date(date)}</p>
                </div>
                <div class="min_max_temp">
                    <img src="${weather_icon}" alt="Weather Icon" class="weather_icon">
                    <h3><strong>${entry['Temp']}°C</strong></h3>
                </div>
            </div>
        `;
    });
    monthlyHTML += '</div>';
    historyContainer.innerHTML = monthlyHTML;
}



function fetchdata() {
    fetch('../data/weather_cleaned.csv')
        .then(response => response.text())
        .then(text => {
            const rows = text.trim().split('\n').slice(1);

            const data = rows.map(row => {
                const cols = row.split(',');
                return {
                    Date: cols[0],
                    Time: cols[1],
                    Weather: cols[2],
                    'Temp': parseFloat(cols[3]),
                    'Rain': parseFloat(cols[4]),
                    'Cloud': parseFloat(cols[5]),
                    'Pressure': parseFloat(cols[6]),
                    'Wind': parseFloat(cols[7]).toFixed(2),
                    'Gust': parseFloat(cols[8]),
                    DateTime: moment(`${cols[0]} ${cols[1]}`, 'YYYY-MM-DD HH:mm')
                };
            });

            const now = moment();

            // Find the closest time
            const closest = data.reduce((prev, curr) => {
                return Math.abs(curr.DateTime.diff(now)) < Math.abs(prev.DateTime.diff(now)) ? curr : prev;
            });

            // Display the matched data
            document.querySelector('.current_temp').innerText = `🌡️ Temp: ${closest['Temp']}°C`;
            document.querySelector('.current_wind').innerText = `💨 Wind: ${closest['Wind']} km/h`;
            document.querySelector('.current_rain').innerText = `🌧️ Rain: ${closest['Rain']} mm`;
            console.log( "data");
            // Optional: show current time
            document.querySelector('.current_time').innerText = `${now.format('YYYY-MM-DD HH:mm')}`;
            get_hourly_weather();
            get_weekly_weather(data);
            drawAreaChart(data);
            drawLineChart(data);
            getDataOfMonth(data,2, 2025);


        })
        .catch(error => {
            console.error('Error reading CSV:', error);
        });
}
fetchdata();
setInterval(function () {
    fetchdata();
}, 2 * 60 * 60 * 1000);

function checkInternetConnection() {
    if (navigator.onLine) {
        console.log("✅ You are online.");
    } else {
        console.log("❌ You are offline.");
    }
}

// Run the check
checkInternetConnection();

// Optionally, listen for changes
window.addEventListener('online', () => alert("✅ You are back online."));
window.addEventListener('offline', () => alert("❌ You are offline."));

setInterval(() => {
    let currentTime = moment().format('YYYY-MM-DD HH:mm');
    document.querySelector('.current_time').innerText = `${currentTime}`;
}, 1000);


async function fectchAPI() {
    const rs = await fetch('https://pbl7-weather-forecast-app-iqe3.onrender.com/api/predict/sarima')
    const data = await rs.json();
    console.log(data.predictions, "data");
    return data.predictions;
}


async function get_hourly_weather() {
    const hourly_data_api = await fectchAPI();
    const hourlyContainer = document.querySelector('.hourly_forecast_cards');
    let weather_icon = "https://www.awxcdn.com/adc-assets/images/weathericons/6.svg";
    let hourlyHTML = '';
    // hourlyHTML += `<button class="arrow-left" onclick="leftScroll()">${icon_arrow_left}</button>`;
    hourly_data_api.forEach(entry => {
        const dateObj = new Date(entry.datetime);
        const hours = String(dateObj.getHours()).padStart(2, '0');
        const minutes = String(dateObj.getMinutes()).padStart(2, '0');
        const formattedTime = `${hours}:${minutes}`;

        hourlyHTML += `
            <div class="hourly_forecast_card">
                <h3><strong>${formattedTime}</strong></h3>
                <img src="${weather_icon}" alt="Weather Icon" class="weather_icon">
                <p>${entry.temperature} °C</p>
            </div>
        `;
    });
    // hourlyHTML += `<button class="arrow-right" onClick="rightScroll()">${icon_arrow_right}</button>`;
    hourlyHTML += '</div>';
    hourlyContainer.innerHTML = hourlyHTML;
}

function getDayOfWeek(date) {
    return moment(date).format('dddd');
}

function truncate_date(date) {
    return moment(date).format('MM-DD');
}

function get_weekly_weather(data) {
    const now = moment("2025-03-24");
    const current_date = now.format('YYYY-MM-DD');
    const next_week = now.clone().add(7, 'days').format('YYYY-MM-DD');

    const weekly_data = data.filter(entry => {
        const entryDate = moment(entry.DateTime).format('YYYY-MM-DD');
        return entryDate > current_date && entryDate <= next_week;
    });

    const min_max_data = weekly_data.reduce((acc, entry) => {
        const date = moment(entry.DateTime).format('YYYY-MM-DD');
        if (!acc[date]) {
            acc[date] = { min: entry['Temp'], max: entry['Temp'] };
        } else {
            acc[date].min = Math.min(acc[date].min, entry['Temp']);
            acc[date].max = Math.max(acc[date].max, entry['Temp']);
        }
        return acc;
    }, {});


    const weeklyContainer = document.querySelector('.weekly_forecast_cards');
    let weeklyHTML = ``;
    let weather_icon = "https://www.awxcdn.com/adc-assets/images/weathericons/6.svg";
    for (const [date, temps] of Object.entries(min_max_data)) {
        weeklyHTML += `
        <div class="weekly_forecast_card">
            <div class="date">
            <h3><strong>${getDayOfWeek(date)}</strong></h3>
            <p>${truncate_date(date)}</p>
            </div>
            <div class="min_max_temp">
            <img src="${weather_icon}" alt="Weather Icon" class="weather_icon">
            <h3><strong>${temps.max}°C</strong></h3>
            <p>${temps.min}°C</p>
            </div>
        </div>
        `;
    }
    weeklyHTML += '</div>';
    weeklyContainer.innerHTML = weeklyHTML;
}

function drawAreaChart(data) {
    const ctx = document.getElementById('AreaChart').getContext('2d');
    const now = moment("2021-09-24");
    const current_date = now.format('YYYY-MM-DD');
    const next_week = now.clone().add(7, 'days').format('YYYY-MM-DD');

    const weekly_data = data.filter(entry => {
        const entryDate = moment(entry.DateTime).format('YYYY-MM-DD');
        return entryDate > current_date && entryDate <= next_week;
    });
    const groupedData = weekly_data.reduce((acc, entry) => {
        const date = moment(entry.DateTime).format('MM-DD');
        if (!acc[date]) {
            acc[date] = { min: entry['Temp'], max: entry['Temp'] };
        } else {
            acc[date].min = Math.min(acc[date].min, entry['Temp']);
            acc[date].max = Math.max(acc[date].max, entry['Temp']);
        }
        return acc;
    }, {});


    // Extract labels (dates) and datasets (min and max temperatures)
    const labels = Object.keys(groupedData);
    const minTemps = labels.map(date => groupedData[date].min);
    const maxTemps = labels.map(date => groupedData[date].max);

    // Chart.js configuration
    const chartData = {
        labels: labels,
        datasets: [
            {
                label: 'Min Temperature (°C)',
                data: minTemps,
                borderColor: 'blue',
                backgroundColor: 'rgba(234, 255, 0, 0.2)',
                fill: '+1',
                tension: 0.4
            },
            {
                label: 'Max Temperature (°C)',
                data: maxTemps,
                borderColor: 'red',
                backgroundColor: 'rgba(255, 0, 0, 0.2)',
                fill: '+2',
                tension: 0.4
            }
        ]
    };

    const myChart = new Chart(ctx, {
        type: 'line', // Area chart is a filled line chart
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Min & Max Temperatures Weekly',
                    font: {
                        size: 24
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            size: 14
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Temp',
                        font: {
                            size: 14
                        }
                    },
                    beginAtZero: false,
                    min: 15,
                    max: 45
                }
            }
        }
    });

}

function drawLineChart(data) {
    const ctx = document.getElementById('LineChart').getContext('2d');
    const now = moment("2021-09-24");
    const current_date = now.format('YYYY-MM-DD');
    const next_week = now.clone().add(7, 'days').format('YYYY-MM-DD');

    const weekly_data = data.filter(entry => {
        const entryDate = moment(entry.DateTime).format('YYYY-MM-DD');
        return entryDate > current_date && entryDate <= next_week;
    });
    let labels = [];
    let temp = [];
    let time = [];
    temp_forecast_weely = weekly_data.forEach(entry => {
        labels.push(moment(entry.DateTime).format('MM-DD'));
        temp.push(entry['Temp']);
        time.push(moment(entry.DateTime).format('HH:mm'));
    });

    // Chart.js configuration
    const chartData = {
        labels: labels,
        datasets: [
            {
                label: 'Temperature Forecast (°C)',
                data: temp,
                borderColor: 'blue',
                backgroundColor: 'rgba(0, 0, 255, 0.2)',
                fill: false,
                tension: 0.4
            }
        ]
    };

    const LineChart = new Chart(ctx, {
        type: 'line', // Area chart is a filled line chart
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Temperatures Forecast 7 Days',
                    font: {
                        size: 24
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const index = context.dataIndex; // Get the index of the current data point
                            const date = labels[index]; // Get the date from the labels array
                            const timeValue = time[index]; // Get the time from the time array
                            const tempValue = temp[index]; // Get the temperature from the temp array
                            return `Date: ${date}, Time: ${timeValue}, Temp: ${tempValue}°C`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            size: 14
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Temp',
                        font: {
                            size: 14
                        }
                    },
                    beginAtZero: false,
                    min: 15,
                    max: 45
                }
            },
        }
    });
}


function leftScroll() {
    console.log("leftScroll");
    const scrollCards = document.querySelector(".hourly_forecast_cards");
    scrollCards.scrollBy({
        left: -297,
        behavior: "smooth"
    });
}

function rightScroll() {
    console.log("rightScroll");
    const scrollCards = document.querySelector(".hourly_forecast_cards");
    scrollCards.scrollBy({
        left: 297,
        behavior: "smooth"
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const scrollCards = document.querySelector(".hourly_forecast_cards");
    const scrollLength = scrollCards.scrollWidth - scrollCards.clientWidth;
    const leftButton = document.querySelector(".left");
    const rightButton = document.querySelector(".right");

    if (!scrollCards || !leftButton || !rightButton) {
        console.error("Required elements are missing in the DOM.");
        return;
    }

    function checkScroll() {
        const currentScroll = scrollCards.scrollLeft;
        if (currentScroll === 0) {
            leftButton.setAttribute("disabled", "true");
            rightButton.removeAttribute("disabled");
        } else if (currentScroll === scrollLength) {
            rightButton.setAttribute("disabled", "true");
            leftButton.removeAttribute("disabled");
        } else {
            leftButton.removeAttribute("disabled");
            rightButton.removeAttribute("disabled");
        }
    }

    scrollCards.addEventListener("scroll", checkScroll);
    window.addEventListener("resize", checkScroll);
    checkScroll();

    leftButton.addEventListener("click", leftScroll);
    rightButton.addEventListener("click", rightScroll);
});

