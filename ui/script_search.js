const domain = "https://weather-forecast-app-b74b.onrender.com/api/historical";
async function fetchHistoryMonthly(year, month, day) {
  const url =
    day && day !== ""
      ? `${domain}?month=${month}&year=${year}&date=${day}`
      : `${domain}?month=${month}&year=${year}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  const data = await response.json();
  return data.data;
}

async function getHistoryMonthly() {
  const historyMonthlyHtml = document.querySelector(
    ".history_monthly_container"
  );
  try {
    // Get the month selection value

    const yearSelect = document.getElementById("year_select");
    const monthSelect = document.getElementById("month_select");
    const daySelect = document.getElementById("day_select");
    const historyMonthly = await fetchHistoryMonthly(
      yearSelect.value,
      monthSelect.value,
      daySelect.value
    );
    // Add event listener for search button
    const searchBtn = document.getElementById("search_button");
    if (searchBtn) {
      searchBtn.addEventListener("click", async () => {
        console.log(
          `Searching for month: ${monthSelect.value}, year: ${yearSelect.value}`
        );
        // Refresh data with current selections
        await getHistoryMonthly();
      });
    }

    //onchange month
    monthSelect.addEventListener("change", async () => {
      const month = monthSelect.value;
      const year = yearSelect.value;
      console.log(`Selected month: ${month}, year: ${year}`);
    });
    // Helper function to get weather icon based on time and cloud coverage
    const getWeatherIcon = (time, cloud) => {
      const hour = parseInt(time.split(":")[0]);
      // Daytime is roughly between 6am and 6pm
      const isDaytime = hour >= 6 && hour < 18;

      if (cloud > 70) {
        return isDaytime
          ? "https://www.awxcdn.com/adc-assets/images/weathericons/26.svg"
          : "https://www.awxcdn.com/adc-assets/images/weathericons/38.svg"; // Changed from 27 to 38
      } else if (cloud > 30) {
        return isDaytime
          ? "https://www.awxcdn.com/adc-assets/images/weathericons/30.svg"
          : "https://www.awxcdn.com/adc-assets/images/weathericons/29.svg"; // Changed from 28 to 30
      } else {
        return isDaytime
          ? "https://www.awxcdn.com/adc-assets/images/weathericons/1.svg"
          : "https://www.awxcdn.com/adc-assets/images/weathericons/33.svg";
      }
    };

    // Create a container for the forecast timeline
    let timelineHTML = `
            <div class="forecast-timeline">
                <button class="left" onclick="leftScroll()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="white" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-chevron-left-icon lucide-chevron-left">
                        <path d="m15 18-6-6 6-6" />
                    </svg>
                </button>
                <div class="timeline-days">
        `;

    // Group data by day for the timeline
    const dayGroups = {};
    historyMonthly.forEach((entry) => {
      // Parse datetime
      const dateTime = entry.datetime.split(" ");
      const date = dateTime[0];
      const time = dateTime[1].substring(0, 5); // Extract HH:MM

      const dateObj = new Date(date);
      const dayKey = dateObj.toLocaleDateString("en-US", {
        weekday: "short",
        day: "numeric",
        month: "short",
      });

      if (!dayGroups[dayKey]) {
        dayGroups[dayKey] = {
          entries: [],
          minTemp: Infinity,
          maxTemp: -Infinity,
        };
      }

      // Add entry to day's data
      dayGroups[dayKey].entries.push({
        time,
        temperature: entry.temperature,
        icon: getWeatherIcon(time, entry.cloud),
        cloud: entry.cloud,
        rain: entry.rain,
        pressure: entry.pressure,
        wind: entry.wind,
      });

      // Update min/max temperature
      if (entry.temperature < dayGroups[dayKey].minTemp) {
        dayGroups[dayKey].minTemp = entry.temperature;
      }
      if (entry.temperature > dayGroups[dayKey].maxTemp) {
        dayGroups[dayKey].maxTemp = entry.temperature;
      }
    });

    // Create columns for each day
    Object.entries(dayGroups).forEach(([day, data], dayIndex) => {
      const { entries, minTemp, maxTemp } = data;

      timelineHTML += `
                <div class="day-column" id="day-column-${dayIndex}">
                    <div class="day-header">${day}</div>
                    <div class="day-data" style="position: relative;">
                        <svg class="temperature-line-svg" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 4;">
                            <path class="temp-path" fill="none" stroke="#ff0000" stroke-width="3" d="${generatePathData(
                              entries
                            )}"/>
                        </svg>
            `;

      // Create time slots
      entries.forEach((entry) => {
        timelineHTML += `
                    <div class="time-slot">
                        <div class="time">${entry.time}</div>
                        <div class="temp-line"
                             data-time="${entry.time}"
                             data-temp="${entry.temperature}"
                             style="
                                position: absolute;
                                width: 8px;
                                height: 8px;
                                background-color: #ff7300;
                                border-radius: 50%;
                                left: 50%;
                                transform: translateX(-50%);
                                top: ${215 - entry.temperature * 3}px;
                                z-index: 5;
                                box-shadow: 0 0 3px rgba(0,0,0,0.3);
                                cursor: pointer;
                             "
                        >
                            <div style="
                                position: absolute;
                                top: -20px;
                                left: 50%;
                                transform: translateX(-50%);
                                background-color: rgba(255, 115, 0, 0.8);
                                color: white;
                                padding: 2px 4px;
                                border-radius: 3px;
                                font-size: 10px;
                                white-space: nowrap;
                                z-index: 10;
                            ">${entry.temperature.toFixed(1)}°C</div>
                        </div>
                        <div class="weather-icon">
                            <img src="${entry.icon}" alt="Weather">
                        </div>
                        <div class="temperature">
                            <div class="rain">🌧️${entry.rain} mm</div>
                            <div class="pressure">${entry.pressure} hPa</div>
                        </div>
                    </div>
                `;
      });

      timelineHTML += `
                    </div>
                </div>
            `;
    });

    // Helper function to generate SVG path data for temperature line
    function generatePathData(entries) {
      if (!entries || entries.length === 0) return "";

      let pathData = "";
      const timeSlotWidth = 63; // Approximate width of each time slot

      entries.forEach((entry, index) => {
        const x = index * timeSlotWidth + timeSlotWidth / 2;
        const y = 220 - entry.temperature * 3;

        if (index === 0) {
          pathData += `M ${x} ${y}`;
        } else {
          pathData += ` L ${x} ${y}`;
        }
      });

      return pathData;
    }

    timelineHTML += `
                </div>
                <button class="right" onclick="rightScroll()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="white" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-chevron-right-icon lucide-chevron-right">
                        <path d="m9 18 6-6-6-6" />
                    </svg>
                </button>
            </div>
        `;

    historyMonthlyHtml.innerHTML = timelineHTML;

    // Initialize scrolling after the content is loaded
    setTimeout(initializeScrolling, 100);
  } catch (error) {
    console.error("Error fetching or displaying weather data:", error);
    historyMonthlyHtml.innerHTML = "<p>Error loading weather data</p>";
  }
}

// Function to draw lines connecting temperature points
function drawTemperatureLines(dayGroups) {
  Object.entries(dayGroups).forEach(([day, entries]) => {
    // Find all day headers
    const dayHeaders = document.querySelectorAll(".day-column .day-header");
    let dayColumn = null;

    // Loop through headers to find the one containing the day text
    for (const header of dayHeaders) {
      if (header.textContent.includes(day)) {
        dayColumn = header.closest(".day-column");
        break;
      }
    }

    if (!dayColumn) return;

    // Create SVG element for the lines
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute(
      "style",
      "position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;"
    );

    // Sort entries by time for correct line connection
    entries.sort((a, b) => {
      const timeA = parseInt(a.time.split(":")[0]);
      const timeB = parseInt(b.time.split(":")[0]);
      return timeA - timeB;
    });

    // Create path element
    let path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", "#ff7300");
    path.setAttribute("stroke-width", "2");

    // Build the SVG path data
    let pathData = "";

    entries.forEach((entry, index) => {
      const tempDot = dayColumn.querySelector(
        `[data-time="${entry.time}"][data-temp="${entry.temperature}"]`
      );

      if (tempDot) {
        const rect = tempDot.getBoundingClientRect();
        const columnRect = dayColumn.getBoundingClientRect();
        const x = rect.left + rect.width / 2 - columnRect.left;
        const y = rect.top + rect.height / 2 - columnRect.top;

        if (index === 0) {
          pathData += `M ${x} ${y}`;
        } else {
          pathData += ` L ${x} ${y}`;
        }
      }
    });

    path.setAttribute("d", pathData);
    svg.appendChild(path);
    dayColumn.appendChild(svg);
  });
}
// Wait for DOM to be fully loaded before executing
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded and parsed");
  selectMonth();
  getHistoryMonthly();
});

function leftScroll() {
  console.log("leftScroll");
  const scrollCards = document.querySelector(".timeline-days");
  scrollCards.scrollBy({
    left: -63,
    behavior: "smooth",
  });
}

function rightScroll() {
  console.log("rightScroll");
  const scrollCards = document.querySelector(".timeline-days");
  scrollCards.scrollBy({
    left: 63,
    behavior: "smooth",
  });
}
// Move scroll initialization to a separate function
function initializeScrolling() {
  const scrollCards = document.querySelector(".timeline-days");
  if (!scrollCards) {
    console.error("scrollCards element not found");
    return;
  }

  const scrollLength = scrollCards.scrollWidth - scrollCards.clientWidth;
  const leftButton = document.querySelector(".left");
  const rightButton = document.querySelector(".right");

  if (!leftButton || !rightButton) {
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
}

function selectMonth() {
  const currentDate = new Date();
  const currentYear = currentDate.getFullYear();
  const yearOptions = [];
  const monthOptions = [];
  const dayOptions = [];
  for (let i = currentYear; i >= 2010; i--) {
    yearOptions.push(i);
  }
  for (let i = 1; i <= 12; i++) {
    monthOptions.push(i);
  }
  for (let i = 1; i <= 31; i++) {
    dayOptions.push(i);
  }

  const yearSelect = document.getElementById("year_select");
  const monthSelect = document.getElementById("month_select");
  const daySelect = document.getElementById("day_select");

  daySelect.innerHTML = "";
  monthSelect.innerHTML = "";
  yearSelect.innerHTML = "";

  monthOptions.forEach((month) => {
    const option = document.createElement("option");
    option.value = month;
    option.textContent = month;
    monthSelect.appendChild(option);
  });
  yearOptions.forEach((year) => {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
  });

  const emptyOption = document.createElement("option");
  emptyOption.value = "";
  emptyOption.textContent = "all";
  daySelect.appendChild(emptyOption);

  dayOptions.forEach((day) => {
    const option = document.createElement("option");
    option.value = day;
    option.textContent = day;
    daySelect.appendChild(option);
  });
}
