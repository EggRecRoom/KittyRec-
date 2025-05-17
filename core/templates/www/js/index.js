const apiUri = "https://api-dev.oldrecroom.com/";

function getToken() {
  return fetch('api/auth/session')
    .then(response => {
      if (!response.ok) {
        throw new Error(`Failed to get session: ${response.status}`);
      }
      return response.json();
    })
    .then(sessionData => {
      if ('accessToken' in sessionData) {
        return sessionData.accessToken; // Return the token
      } else {
        return null;
      }
    })
    .catch(error => {
      console.error("Error getting token:", error);
      throw error;
    });
}

function get(api) {
  return getToken() // Call getToken() to get the promise
    .then(accessToken => {
      return fetch(apiUri + api, {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Failed to get data: ${response.status}`);
      }
      return response.json();
    });
}

// Example usage:
getToken().then(token => console.log("Token:", token)); // Log the token when it's available

get('api/howToVideo/v2/random')
  .then(data => console.log("Data:", data))
  .catch(error => console.error("Error fetching data:", error));