const generatingMessages = [
    "🚀 Launching creativity boosters... <span class='dots'></span> Your copy is almost ready! 🌟",
    "🧠 AI brainpower at work... <span class='dots'></span> Crafting your perfect copy! 📝",
    "🎨 Painting words with AI magic... <span class='dots'></span> Get ready for your masterpiece! 🖼️",
    "🔮 Gazing into the AI crystal ball... <span class='dots'></span> Unveiling your copy's future! ✨",
    "🕺 AI is dancing on the keyboard... <span class='dots'></span> Your groovy copy is coming right up! 💃"
];

function getRandomMessage() {
    const index = Math.floor(Math.random() * generatingMessages.length);
    return generatingMessages[index];
}

function animateDots() {
    const dots = document.querySelector(".dots");
    let dotCount = 0;

    setInterval(() => {
        dots.textContent = ".".repeat(dotCount);
        dotCount = (dotCount + 1) % 4;
    }, 500);
}

document.addEventListener("DOMContentLoaded", () => {
    animateDots();
});

document.querySelector("#questionnaire-form").addEventListener("submit", async (event) => {
    // Prevent the form from submitting
    event.preventDefault();

    // Set a random message
    document.querySelector("#generating-text").innerHTML = getRandomMessage();

    // Show the generating message
    document.querySelector("#generating-message").style.display = "block";

    // Hide the custom form
    document.querySelector("#custom-form").style.display = "none";

    // Collect answers from input fields
    const formData = new FormData(event.target);
    const answers = Object.fromEntries(formData.entries());

    // Send a POST request to your server
    const response = await fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(answers),
    });

    // After the copy is generated, hide the generating message and process the response
    document.querySelector("#generating-message").style.display = "none";

// Process the response from the server (e.g., display the generated copy)
const responseData = await response.json();

// Add <strong> tags around "Subject:"
const formattedText = responseData.generated_copy.replace("Subject:", "<strong>Subject:</strong>");

// Replace newline characters with <br> for single line breaks
const formattedTextWithLineBreaks = formattedText.replace(/\n/g, "<br>");

// Insert the formatted text into the #generated-copy-content element
document.querySelector("#generated-copy-content").innerHTML = formattedTextWithLineBreaks;
    
// Display the generated copy
document.querySelector("#generated-copy").style.display = "block";
});

document.querySelector("#copy-to-clipboard-btn").addEventListener("click", () => {
const generatedCopy = document.querySelector("#generated-copy-content").textContent;
navigator.clipboard.writeText(generatedCopy).then(() => {
alert("Copy successful!");
}, () => {
alert("Copy failed!");
});
});


