// ------------- Helper Functions -------------
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken'); // Get CSRF token globally

// ------------- User Management -------------
async function fetchUserData() {
    try {
        const response = await fetch('zaban/api/get_user_data/', { // Use the correct URL
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken, // Use the global csrftoken
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching user data:', error);
        return null; // Return null on error
    }
}

async function updateUserData(updatedData) {
    try {
        const response = await fetch('zaban/api/update_user_data/', { // Use the correct URL
            method: 'POST', // Use POST, not PUT
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken, // Use the global csrftoken
            },
            body: JSON.stringify(updatedData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error updating user data:', error);
        return null; // Return null on error
    }
}

// ------------- Initialization -------------
async function initializeUser() {
    // Prevent repeated reloads (if needed, keep this part)
    if (window.location.search.includes('no-reload')) {
        window.history.replaceState({}, document.title, window.location.pathname);
        return;
    }

    // Initial data loading (only if not already in sessionStorage)
    if (!sessionStorage.getItem("user-info")) {
        const userData = await fetchUserData();
        if (userData) {
            sessionStorage.setItem("user-info", JSON.stringify(userData));
        }
    }

    // --- Lesson Progress Logic (Moved inside initializeUser) ---
    await handleLessonProgress();
}

// ------------- Lesson Progress Logic -------------
async function handleLessonProgress() {
  const xpFromLesson = parseInt(localStorage.getItem("xpCount")) || -2; // Default to -2
  const newHearts = parseInt(localStorage.getItem("hearts")) || 0;

  // If no new lesson is completed, return early.
  if (xpFromLesson < 0) {
      return;
  }

  try {
    let userData = JSON.parse(sessionStorage.getItem("user-info"));
    // Fetch user data if it's not in sessionStorage
    if (!userData) {
        userData = await fetchUserData();
        if (!userData) { // Check if fetchUserData was successful
            console.error("Failed to fetch user data. Cannot proceed.");
            return;
        }
    }

    // Calculate changes (prepare the data to send)
    const updatedData = {
        xpFromLesson: xpFromLesson,  // Send xpFromLesson and newHearts
        newHearts: newHearts,
    };

    // Send update to server
    const newUserData = await updateUserData(updatedData);
    if (!newUserData) {
        console.error("Failed to update user data on the server.");
        return; // Stop if the update failed
    }

    // Clear local storage AFTER successful server update
    localStorage.removeItem("xpCount");
    localStorage.removeItem("hearts");

    // Update user data in sessionStorage *with the server's response*
    sessionStorage.setItem("user-info", JSON.stringify(newUserData.userData)); // Use newUserData.userData

    // Reload the page only if needed, and prevent infinite reloads
    if (xpFromLesson > 0 && !window.location.search.includes('no-reload')) {
        setTimeout(() => {
            // Use replaceState to prevent adding to history
            window.location.replace(window.location.pathname + '?no-reload=true');
        }, 300);
    }
  } catch (error) {
      console.error("Error processing lesson:", error);
  }
}


// ------------- Run the program -------------
document.addEventListener('DOMContentLoaded', initializeUser);
