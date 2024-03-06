// Set the countdown date and time
var countdownDate = "2024-06-29";
var countdownTime = "23:59:59";
// Calculate the remaining time
var countdownDateTime = new Date(countdownDate + "T" + countdownTime + "Z");
var countdown = setInterval(function () {
  var now = new Date().getTime();
  var distance = countdownDateTime - now;
  // Calculate days, hours, minutes, and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
  // Update the countdown display
  document.getElementById("countdown").innerHTML =
    days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
  // Stop the countdown when the timer ends
  if (distance < 0) {
    clearInterval(countdown);
    document.getElementById("countdown").innerHTML = "EXPIRED";
  }
}, 1000); // Update the countdown every second

// Function to change the font family
function changeFont() {
  var fontSelector = document.getElementById("font-selector");
  var font = fontSelector.options[fontSelector.selectedIndex].value;
  document.getElementById("countdown").style.fontFamily = font;
}
