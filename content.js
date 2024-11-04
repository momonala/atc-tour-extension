// Function to remove the header background image
function removeHeaderImage() {
  const styleElement = document.createElement('style');
  styleElement.type = 'text/css';
  // Add CSS rules to override the background image and remove space
  styleElement.innerHTML = `
    .header-holder:after {
      background-image: none !important;
    }
    .header-holder {
      height: 0 !important;
      padding: 0 !important;
      margin: 0 !important;
      overflow: hidden;
    }
  `;
  // Append the style element to the head
  document.head.appendChild(styleElement);
  console.log("Header background image removed and space adjusted.");
}

// Function to filter rows and apply discount
function filterRowsAndApplyDiscount(countriesToExclude, discountPercentage) {
  const listViewButton = document.getElementById("compact_view");
  const visualViewButton = document.getElementById("visual_view");
  const containerCompact = document.getElementById("container-compact");
  const containerPretty = document.getElementById("container-pretty");

  if (listViewButton && visualViewButton && containerCompact && containerPretty) {
    console.log("Elements found: switching to List view.");

    if (!listViewButton.checked) {
      visualViewButton.checked = false;
      listViewButton.checked = true;
      listViewButton.dispatchEvent(new Event("change", { bubbles: true }));
      listViewButton.click();

      containerCompact.style.display = "block";
      containerPretty.style.display = "none";
      console.log("Switched to List view programmatically.");

      const listItems = containerCompact.querySelectorAll(".table tbody .tour-row");

      listItems.forEach((item) => {
        const itemText = item.textContent || item.innerText;

        // Hide items based on excluded countries
        if (countriesToExclude.some((country) => itemText.includes(country))) {
          item.style.display = "none";
          console.log(`Filtered out item: ${itemText.trim()}`);
        } else {
          // Apply discount to price if not excluded
          const priceCell = item.querySelector("td:nth-child(3)");
          if (priceCell) {
            const originalPriceText = priceCell.textContent.trim();
            const originalPrice = parseFloat(originalPriceText.replace(/[^0-9.-]+/g, ""));
            const discountedPrice = (originalPrice * (1 - discountPercentage / 100)).toFixed(2);
            priceCell.textContent = `${originalPriceText} (€${discountedPrice})`;
            console.log(`Updated price: ${originalPriceText} -> (€${discountedPrice})`);
          }
        }
      });
    } else {
      console.log("List view is already selected.");
    }
  }
}

// Mutation observer to detect when elements load
const observer = new MutationObserver((mutations, observerInstance) => {
  if (document.querySelector(".header-holder")) {
    removeHeaderImage();
  }

  chrome.storage.sync.get(["excludedCountries", "discountPercentage"], (data) => {
    const countriesToExclude = data.excludedCountries || [];
    const discountPercentage = data.discountPercentage || 0; // Default to 0% if not set
    filterRowsAndApplyDiscount(countriesToExclude, discountPercentage);
  });

  observerInstance.disconnect(); // Stop observing after switching views and filtering
});

// Start observing the body for added nodes
observer.observe(document.body, { childList: true, subtree: true });
