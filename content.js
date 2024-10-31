console.log("Content script loaded.");

// Function to remove the header background image
function removeHeaderImage() {
  const styleElement = document.createElement('style');
  styleElement.type = 'text/css';
  // Add CSS rules to override the background image and remove space
  styleElement.innerHTML = `
    .header-holder:after {
      background-image: none !important; /* Remove the background image */
    }
    .header-holder {
      height: 0 !important; /* Set height to 0 */
      padding: 0 !important; /* Remove padding */
      margin: 0 !important; /* Remove margin */
      overflow: hidden; /* Prevent overflow */
    }
  `;
  // Append the style element to the head
  document.head.appendChild(styleElement);
  console.log("Header background image removed and space adjusted.");
}

// Mutation observer to detect when the elements load
const observer = new MutationObserver((mutations, observerInstance) => {
  if (document.querySelector(".header-holder")) {
    removeHeaderImage();
  }

  const listViewButton = document.getElementById("compact_view");
  const visualViewButton = document.getElementById("visual_view");
  const containerCompact = document.getElementById("container-compact");
  const containerPretty = document.getElementById("container-pretty");

  if (listViewButton && visualViewButton && containerCompact && containerPretty) {
    console.log("Elements found: switching to List view.");

    // If List view is not selected, toggle it
    if (!listViewButton.checked) {
      visualViewButton.checked = false;
      listViewButton.checked = true;
      listViewButton.dispatchEvent(new Event("change", { bubbles: true }));
      listViewButton.click();

      containerCompact.style.display = "block";
      containerPretty.style.display = "none";
      console.log("Switched to List view programmatically.");

      // Filter out items containing specific countries
      const countriesToExclude = ["Syria", "Iraq", "Mauritania", "Venezuela", "Eritrea", "Somaliland"];
      const listItems = containerCompact.querySelectorAll(".table tbody tr");

      listItems.forEach((item) => {
        const itemText = item.textContent || item.innerText;
        if (countriesToExclude.some((country) => itemText.includes(country))) {
          item.style.display = "none"; // Hide the item if it contains the specified countries
          console.log(`Filtered out item: ${itemText.trim()}`);
        }
      });
    } else {
      console.log("List view is already selected.");
    }

    observerInstance.disconnect(); // Stop observing after switching views and filtering
  }
});

// Start observing the body for added nodes
observer.observe(document.body, { childList: true, subtree: true });
