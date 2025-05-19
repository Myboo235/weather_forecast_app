window.onload = function () {
  get_weekly_weather("dlinear");
  get_hourly_weather("sarima");
  get_hourly_weather("dlinear");
  drawLineChart("sarima");
  drawAreaChart("sarima");
  onMapTypeChange("windy");

  document.querySelector(".current_temp").innerText = `🌡️29°C`;
  document.querySelector(".current_wind").innerText = `💨 Wind: 30 km/h`;
  document.querySelector(".current_rain").innerText = `🌧️ Rain: 0 mm`;
};

function onModelChange(modelName) {
  get_weekly_weather(modelName);
  drawLineChart(modelName);
  drawAreaChart(modelName);
}

function onMapTypeChange(type) {
  const container = document.getElementById("area_map");
  let iframe = "";

  if (type === "windy") {
    iframe = `<iframe width="100%" height="450"
        src="https://embed.windy.com/embed2.html?lat=16.07&lon=108.22&detailLat=16.07&detailLon=108.22&width=650&height=450&zoom=7&level=surface&overlay=wind"
        frameborder="0" style="border-radius: 12px;"></iframe>`;
  } else if (type === "ventusky") {
    iframe = `<iframe width="100%" height="450"
        src="https://www.ventusky.com/?p=16.1;108.2;6&l=wind-10m"
        frameborder="0" style="border-radius: 12px;"></iframe>`;
  } else if (type === "google") {
    iframe = `<iframe width="100%" height="450"
        src="https://www.google.com/maps/embed/v1/place?key=YOUR_API_KEY&q=Da+Nang,Vietnam"
        frameborder="0" style="border-radius: 12px;"></iframe>`;
  }

  container.innerHTML = iframe;
}

function fetchdata() {
  fetch("../data/weather_cleaned.csv")
    .then((response) => response.text())
    .then((text) => {
      const rows = text.trim().split("\n").slice(1);

      const data = rows.map((row) => {
        const cols = row.split(",");
        return {
          Date: cols[0],
          Time: cols[1],
          Weather: cols[2],
          Temp: parseFloat(cols[3]),
          Rain: parseFloat(cols[4]),
          Cloud: parseFloat(cols[5]),
          Pressure: parseFloat(cols[6]),
          Wind: parseFloat(cols[7]).toFixed(2),
          Gust: parseFloat(cols[8]),
          DateTime: moment(`${cols[0]} ${cols[1]}`, "YYYY-MM-DD HH:mm"),
        };
      });

      const now = moment();

      // Find the closest time
      const closest = data.reduce((prev, curr) => {
        return Math.abs(curr.DateTime.diff(now)) <
          Math.abs(prev.DateTime.diff(now))
          ? curr
          : prev;
      });

      // Display the matched data
      // document.querySelector(
      //   ".current_temp"
      // ).innerText = `🌡️ Temp: ${closest["Temp"]}°C`;
      // document.querySelector(
      //   ".current_wind"
      // ).innerText = `💨 Wind: ${closest["Wind"]} km/h`;
      // document.querySelector(
      //   ".current_rain"
      // ).innerText = `🌧️ Rain: ${closest["Rain"]} mm`;
      // console.log("data");
      // // Optional: show current time
      // document.querySelector(".current_time").innerText = `${now.format(
      //   "YYYY-MM-DD HH:mm"
      // )}`;
      // get_hourly_weather("sarima");
      // get_hourly_weather_dlinear();
      // get_weekly_weather(data);
      // drawAreaChart(data);
      // drawLineChart(data);
    })
    .catch((error) => {
      console.error("Error reading CSV:", error);
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
window.addEventListener("online", () => alert("✅ You are back online."));
window.addEventListener("offline", () => alert("❌ You are offline."));

async function fectchAPI(model) {
  const response = await fetch(
    `https://weather-forecast-app-b74b.onrender.com/api/predict/${model}`
  );
  const data = await rs.json();
  return data.predictions;
}

async function get_hourly_weather(model_name) {
  const hourlyContainer = document.querySelector(
    `.${model_name}_hourly_forecast_cards`
  );
  const weather_icon =
    "https://www.awxcdn.com/adc-assets/images/weathericons/6.svg";
  let hourlyHTML = "";

  try {
    const response = await fetch(`/api/predict/${model_name}`);
    const data = await response.json();
    const predictions = data.predictions;

    if (!Array.isArray(predictions)) {
      throw new Error("Invalid response format");
    }

    predictions.forEach((entry) => {
      const dateObj = new Date(entry.datetime);
      const hours = String(dateObj.getHours()).padStart(2, "0");
      const minutes = String(dateObj.getMinutes()).padStart(2, "0");
      const formattedTime = `${hours}:${minutes}`;

      hourlyHTML += `
        <div class="hourly_forecast_card">
          <h3><strong>${formattedTime}</strong></h3>
          <img src="${weather_icon}" alt="Weather Icon" class="weather_icon">
          <p>${Math.round(entry.temperature)} °C</p>
        </div>
      `;
    });
  } catch (error) {
    console.error(
      `Failed to fetch ${model_name.toUpperCase()} hourly forecast:`,
      error
    );
    hourlyHTML = `
      <div class="error_message">
        <p style="color: red;">⚠️ Failed to load hourly forecast. Please try again later.</p>
      </div>
    `;
  }

  hourlyContainer.innerHTML = hourlyHTML;
}

async function get_hourly_weather_dlinear() {
  const hourly_data_api = await fectchAPI("dlinear");
  const hourlyContainer = document.querySelector(
    ".hourly_forecast_cards_dlinear"
  );
  let weather_icon =
    "https://www.awxcdn.com/adc-assets/images/weathericons/6.svg";
  let hourlyHTML = "";
  hourly_data_api.forEach((entry) => {
    const dateObj = new Date(entry.datetime);
    const hours = String(dateObj.getHours()).padStart(2, "0");
    const minutes = String(dateObj.getMinutes()).padStart(2, "0");
    const formattedTime = `${hours}:${minutes}`;

    hourlyHTML += `
            <div class="hourly_forecast_card">
                <h3><strong>${formattedTime}</strong></h3>
                <img src="${weather_icon}" alt="Weather Icon" class="weather_icon">
                <p>${entry.temperature} °C</p>
            </div>
        `;
  });
  hourlyHTML += "</div>";
  hourlyContainer.innerHTML = hourlyHTML;
}

function getDayOfWeek(date) {
  return moment(date).format("dddd");
}

function truncate_date(date) {
  return moment(date).format("DD/MM");
}

async function get_weekly_weather(model) {
  const weeklyContainer = document.querySelector(".weekly_forecast_cards");
  if (!model) {
    weeklyContainer.innerHTML = `
      <div class="error_message">
        <p style="color: red;">⚠️ No model selected.</p>
      </div>
    `;
    return;
  }

  let weeklyHTML = "";
  try {
    const response = await fetch(
      `/api/predict_next_7_days_stats?model_name=${model}`
    );
    const weekly_forecast_response = await response.json();

    if (
      weekly_forecast_response.status !== 200 ||
      !Array.isArray(weekly_forecast_response.predictions)
    ) {
      throw new Error("Invalid response");
    }

    const weekly_forecast_data = weekly_forecast_response.predictions;
    console.log(weekly_forecast_data);

    const weather_icon =
      "https://www.svgrepo.com/show/194384/thermometer-temperature.svg";

    for (const item of weekly_forecast_data) {
      weeklyHTML += `
        <div class="weekly_forecast_card">
          <div class="date">
            <h3><strong>${getDayOfWeek(item.date)}</strong></h3>
            <p>${truncate_date(item.date)}</p>
          </div>
          <div class="min_max_temp">
            <img src="${weather_icon}" alt="Weather Icon" class="weather_icon">
            <h3><strong>${Math.round(item.max_temp)}°C</strong></h3>
            <p>${Math.round(item.min_temp)}°C</p>
          </div>
        </div>
      `;
    }
  } catch (error) {
    weeklyHTML = `
      <div class="error_message">
        <p style="color: red;">⚠️ Failed to load weekly forecast. Please try again later.</p>
      </div>
    `;
  }

  weeklyContainer.innerHTML = weeklyHTML;
}

async function drawAreaChart(modelName) {
  const canvas = document.getElementById("AreaChart");
  const ctx = canvas.getContext("2d");

  // Clear previous chart if it exists
  if (window.currentAreaChart) {
    window.currentAreaChart.destroy();
  }

  try {
    const response = await fetch(
      `/api/predict_next_7_days_stats?model_name=${modelName}`
    );
    const result = await response.json();

    if (result.status !== 200 || !Array.isArray(result.predictions)) {
      throw new Error("Invalid response format");
    }

    const data = result.predictions;

    // Extract labels (dates) and datasets (min and max temperatures)
    const labels = data.map((entry) => moment(entry.date).format("MM-DD"));
    const minTemps = data.map((entry) => entry.min_temp);
    const maxTemps = data.map((entry) => entry.max_temp);

    const chartData = {
      labels: labels,
      datasets: [
        {
          label: "Min Temperature (°C)",
          data: minTemps,
          borderColor: "blue",
          backgroundColor: "rgba(0, 123, 255, 0.2)",
          fill: "+1",
          tension: 0.4,
        },
        {
          label: "Max Temperature (°C)",
          data: maxTemps,
          borderColor: "red",
          backgroundColor: "rgba(255, 0, 0, 0.2)",
          fill: true,
          tension: 0.4,
        },
      ],
    };

    window.currentAreaChart = new Chart(ctx, {
      type: "line", // Area chart
      data: chartData,
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: `Min & Max Temperatures - 7 Days (${modelName.toUpperCase()})`,
            font: {
              size: 22,
            },
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Date",
              font: { size: 14 },
            },
          },
          y: {
            title: {
              display: true,
              text: "Temperature (°C)",
              font: { size: 14 },
            },
            beginAtZero: false,
            min: 15,
            max: 45,
          },
        },
      },
    });
  } catch (error) {
    console.error("Failed to render area chart:", error);
    canvas.insertAdjacentHTML(
      "afterend",
      `<div class="error_message" style="
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: red;
        background: rgba(255,255,255,0.8);
        padding: 10px 16px;
        border-radius: 8px;
        z-index: 10;
        pointer-events: none;">
        ⚠️ Failed to load area chart. Please try again later.
      </div>`
    );
  }
}

async function drawLineChart(modelName) {
  const canvas = document.getElementById("LineChart");
  const ctx = canvas.getContext("2d");
  canvas.width = 800;

  // Clear old chart if needed
  if (window.currentLineChart) {
    window.currentLineChart.destroy();
  }

  let labels = [];
  let temp = [];
  let time = [];

  try {
    const response = await fetch(
      `/api/predict_next_7_days?model_name=${modelName}`
    );
    const result = await response.json();

    if (result.status !== 200 || !Array.isArray(result.predictions)) {
      throw new Error("Invalid response format");
    }

    const data = result.predictions;

    data.forEach((entry) => {
      const datetime = moment(entry.datetime);
      labels.push(datetime.format("MM-DD"));
      temp.push(entry.temperature);
      time.push(datetime.format("HH:mm"));
    });

    const chartData = {
      labels: labels,
      datasets: [
        {
          label: "Temperature Forecast (°C)",
          data: temp,
          borderColor: "blue",
          backgroundColor: "rgba(0, 0, 255, 0.2)",
          fill: false,
          tension: 0.4,
        },
      ],
    };

    window.currentLineChart = new Chart(ctx, {
      type: "line",
      data: chartData,
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: `7-Day Temperature Forecast (${modelName.toUpperCase()})`,
            font: {
              size: 24,
            },
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const index = context.dataIndex;
                return `Date: ${labels[index]}, Time: ${
                  time[index]
                }, Temp: ${Math.round(temp[index])}°C`;
              },
            },
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Date",
              font: {
                size: 14,
              },
            },
          },
          y: {
            title: {
              display: true,
              text: "Temperature (°C)",
              font: {
                size: 14,
              },
            },
            beginAtZero: false,
            min: 15,
            max: 45,
          },
        },
      },
    });
  } catch (error) {
    console.error("Error drawing chart:", error);
    canvas.insertAdjacentHTML(
      "afterend",
      `<div class="error_message" style="
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: red;
        background: rgba(255,255,255,0.8);
        padding: 10px 16px;
        border-radius: 8px;
        z-index: 10;
        pointer-events: none;">
        ⚠️ Failed to load area chart. Please try again later.
      </div>`
    );
  }
}

function leftScroll() {
  const scrollCards = document.querySelector(".hourly_forecast_cards");
  scrollCards.scrollBy({
    left: -205,
    behavior: "smooth",
  });
}

function rightScroll() {
  const scrollCards = document.querySelector(".hourly_forecast_cards");
  scrollCards.scrollBy({
    left: 205,
    behavior: "smooth",
  });
}

function leftScrollDlinear() {
  const scrollCards = document.querySelector(".hourly_forecast_cards_dlinear");
  scrollCards.scrollBy({
    left: -205,
    behavior: "smooth",
  });
}

function rightScrollDlinear() {
  const scrollCards = document.querySelector(".hourly_forecast_cards_dlinear");
  scrollCards.scrollBy({
    left: 205,
    behavior: "smooth",
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const scrollCards = document.querySelector(".hourly_forecast_cards");
  const scrollCardsDlinear = document.querySelector(
    ".hourly_forecast_cards_dlinear"
  );
  const scrollLength = scrollCards.scrollWidth - scrollCards.clientWidth;
  const scrollLengthDlinear = scrollCardsDlinear
    ? scrollCardsDlinear.scrollWidth - scrollCardsDlinear.clientWidth
    : 0;
  const leftButton = document.querySelector(".left");
  const rightButton = document.querySelector(".right");
  const leftButtonDlinear = document.querySelector(".left_dlinear");
  const rightButtonDlinear = document.querySelector(".right_dlinear");

  if (!scrollCards || !leftButton || !rightButton) {
    console.error("Required elements are missing in the DOM.");
    return;
  }
  if (!scrollCardsDlinear || !leftButtonDlinear || !rightButtonDlinear) {
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

    const currentScrollDlinear = scrollCardsDlinear.scrollLeft;
    if (currentScrollDlinear === 0) {
      leftButtonDlinear.setAttribute("disabled", "true");
      rightButtonDlinear.removeAttribute("disabled");
    } else if (currentScrollDlinear === scrollLengthDlinear) {
      rightButtonDlinear.setAttribute("disabled", "true");
      leftButtonDlinear.removeAttribute("disabled");
    } else {
      leftButtonDlinear.removeAttribute("disabled");
      rightButtonDlinear.removeAttribute("disabled");
    }
  }

  scrollCards.addEventListener("scroll", checkScroll);
  scrollCardsDlinear.addEventListener("scroll", checkScroll);
  scrollCards.addEventListener("wheel", function (event) {
    event.preventDefault();
    if (event.deltaY > 0) {
      rightScroll();
    } else {
      leftScroll();
    }
  });

  scrollCardsDlinear.addEventListener("wheel", function (event) {
    event.preventDefault();
    if (event.deltaY > 0) {
      rightScrollDlinear();
    } else {
      leftScrollDlinear();
    }
  });
  window.addEventListener("resize", checkScroll);
  checkScroll();

  leftButton.addEventListener("click", leftScroll);
  rightButton.addEventListener("click", rightScroll);
  leftButtonDlinear.addEventListener("click", leftScrollDlinear);
  rightButtonDlinear.addEventListener("click", rightScrollDlinear);
});
