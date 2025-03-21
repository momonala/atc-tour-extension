document.addEventListener("DOMContentLoaded", () => {
  // Load saved countries and discount from storage
  chrome.storage.sync.get(["excludedCountries", "discountPercentage"], (data) => {
    const countries = data.excludedCountries || [];
    const discount = data.discountPercentage ?? 10; // Default to 10% if not set
    document.getElementById("countries").value = countries.join(", ");
    document.getElementById("discount").value = discount;
  });
});

document.getElementById("save").addEventListener("click", () => {
  const countries = document.getElementById("countries").value
    .split(",")
    .map((c) => c.trim())
    .filter((c) => c);

  const discount = parseFloat(document.getElementById("discount").value) || 0;

  chrome.storage.sync.set({ excludedCountries: countries, discountPercentage: discount }, () => {
    console.log("Settings saved:", { excludedCountries: countries, discountPercentage: discount });

    // Show the "✔ Saved" message
    const confirmation = document.getElementById("confirmation");
    confirmation.style.visibility = "visible";
    setTimeout(() => {
      confirmation.style.visibility = "hidden";
    }, 1500); // Hide the message after 1.5 seconds
  });
});
