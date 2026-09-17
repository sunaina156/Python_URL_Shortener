//  This JavaScript connects your frontend to your current FastAPI endpoint:


/* =================================
   API CONFIGURATION
================================= */

const API_BASE_URL = "http://127.0.0.1:8000";


/* =================================
   GET HTML ELEMENTS
================================= */

const shortenForm = document.getElementById("shorten-form");

const urlInput = document.getElementById("url-input");

const shortenButton = document.getElementById("shorten-button");

const message = document.getElementById("message");

const resultContainer = document.getElementById("result-container");

const shortUrlElement = document.getElementById("short-url");

const copyButton = document.getElementById("copy-button");


/* =================================
   FORM SUBMISSION
================================= */

shortenForm.addEventListener("submit", async function (event) {

    // Prevent the browser from refreshing the page.
    event.preventDefault();


    // Get the URL entered by the user.
    const originalUrl = urlInput.value.trim();


    // Clear previous messages and results.
    message.textContent = "";

    message.className = "message";

    resultContainer.classList.add("hidden");


    // Basic frontend validation.
    if (!originalUrl) {

        showError("Please enter a URL.");

        return;

    }


    // Disable the button while the request is running.
    shortenButton.disabled = true;

    shortenButton.textContent = "Shortening...";


    try {

        /*
            Send a POST request to FastAPI.

            The backend expects:
            {
                "original_url": "https://example.com"
            }
        */

        const response = await fetch(
            `${API_BASE_URL}/urls`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    original_url: originalUrl
                })
            }
        );


        // Read the response from FastAPI.
        const data = await response.json();


        // Handle backend errors.
        if (!response.ok) {

            const errorMessage =
                data.detail || "Unable to shorten the URL.";

            throw new Error(errorMessage);

        }


        /*
            Your current FastAPI endpoint returns:

            {
                "id": ...,
                "short_code": "...",
                "original_url": "...",
                "user_id": ...,
                "created_at": ...
            }
        */


        const shortCode = data.short_code;


        /*
            Build the short URL.

            Example:
            http://127.0.0.1:8000/abc123
        */

        const shortUrl = `${API_BASE_URL}/${shortCode}`;


        // Display the generated short URL.
        shortUrlElement.textContent = shortUrl;

        shortUrlElement.href = shortUrl;


        // Show the result container.
        resultContainer.classList.remove("hidden");


        // Show success message.
        showSuccess("Your URL was shortened successfully!");


    } catch (error) {

        console.error("Error:", error);

        showError(error.message || "Something went wrong.");

    } finally {

        // Enable the button again.
        shortenButton.disabled = false;

        shortenButton.textContent = "Shorten URL";

    }

});


/* =================================
   COPY SHORT URL
================================= */

copyButton.addEventListener("click", async function () {

    const shortUrl = shortUrlElement.textContent;


    if (!shortUrl) {

        return;

    }


    try {

        await navigator.clipboard.writeText(shortUrl);

        copyButton.textContent = "Copied!";


        // Restore button text after a short delay.
        setTimeout(function () {

            copyButton.textContent = "Copy";

        }, 2000);


    } catch (error) {

        console.error("Copy failed:", error);

        showError("Unable to copy the URL. Please copy it manually.");

    }

});


/* =================================
   DISPLAY SUCCESS MESSAGE
================================= */

function showSuccess(text) {

    message.textContent = text;

    message.className = "message success";

}


/* =================================
   DISPLAY ERROR MESSAGE
================================= */

function showError(text) {

    message.textContent = text;

    message.className = "message error";

}
