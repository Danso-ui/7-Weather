document.addEventListener("DOMContentLoaded", () => {
  const locationBtn = document.querySelector(".location-btn");

  // This is the function that does the heavy lifting
  function getLocationAndSubmit() {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }

    // Change text to show it is working
    const originalText = locationBtn.innerHTML;
    locationBtn.innerHTML = "Locating...";

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        // Dynamically create a hidden form and submit it to Flask
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
        // If the user denies permission, silently reset the button
        console.warn("Location access denied or failed.");
        locationBtn.innerHTML = originalText;
      },
    );
  }

  // 1. Allow manual clicks just in case they want to refresh their location
  if (locationBtn) {
    locationBtn.addEventListener("click", getLocationAndSubmit);
  }

  // 2. AUTO-RUN LOGIC
  // We check if the '.city-name' div exists. If it DOES NOT exist,
  // it means the user just opened the app, so we run the location function.
  const weatherDataExists = document.querySelector(".city-name");
  if (!weatherDataExists) {
    getLocationAndSubmit();
  }
});
