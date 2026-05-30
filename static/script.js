document.addEventListener("DOMContentLoaded", () => {
  const locationBtn = document.querySelector(".location-btn");

  // ==========================================
  // 1. TEMPERATURE TOGGLE LOGIC
  // ==========================================
  const unitToggleBtn = document.getElementById("unit-toggle");
  let isCelsius = true;

  if (unitToggleBtn) {
    unitToggleBtn.addEventListener("click", () => {
      isCelsius = !isCelsius; // Flip the true/false state

      // Update Main Temperature
      const mainTemp = document.querySelector(".temp-display");
      if (mainTemp) {
        const cVal = parseFloat(mainTemp.getAttribute("data-celsius"));
        const displayVal = isCelsius ? Math.round(cVal) : Math.round((cVal * 9/5) + 32);
        mainTemp.innerHTML = `${displayVal}<sup>${isCelsius ? '°C' : '°F'}</sup>`;
      }

      // Update Feels Like Temperature
      const feelsLine = document.querySelector(".feels-line");
      if (feelsLine) {
        const cVal = parseFloat(feelsLine.getAttribute("data-celsius"));
        const displayVal = isCelsius ? Math.round(cVal) : Math.round((cVal * 9/5) + 32);
        feelsLine.innerHTML = `Feels like ${displayVal}${isCelsius ? '°C' : '°F'}`;
      }

      // Update 6-Day Forecast List Temperatures
      const forecastTemps = document.querySelectorAll(".forecast-temp");
      forecastTemps.forEach(el => {
        const cVal = parseFloat(el.getAttribute("data-celsius"));
        const displayVal = isCelsius ? Math.round(cVal) : Math.round((cVal * 9/5) + 32);
        el.innerHTML = `${displayVal}°`;
      });
    });
  }

  // ==========================================
  // 2. GEOLOCATION LOCATION LOGIC
  // ==========================================
  function getLocationAndSubmit() {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }

    const originalText = locationBtn.innerHTML;
    locationBtn.innerHTML = "Locating...";

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        const form = document.createElement("form");
        form.method = "POST";
        form.action = "/";

        const latInput = document.createElement("input");
        latInput.type = "hidden";
        latInput.name = "lat";
        latInput.value = lat;

        const lonInput = document.createElement("input");
        lonInput.type = "hidden";
        lonInput.name = "lon";
        lonInput.value = lon;

        form.appendChild(latInput);
        form.appendChild(lonInput);
        document.body.appendChild(form);

        form.submit();
      },
      (error) => {
        // Mobile alert helper
        alert("Location error: " + error.message + "\n\nPlease check your phone's browser settings to allow location access for this site.");
        locationBtn.innerHTML = originalText;
      }
    );
  }

  // Attach click listener to the location button
  if (locationBtn) {
    locationBtn.addEventListener("click", getLocationAndSubmit);
  }

  // Auto-run if opening the app fresh without a city loaded
  const weatherDataExists = document.querySelector(".city-name");
  if (!weatherDataExists) {
    getLocationAndSubmit();
  }
});