const accessToken = undefined;
const apiUri = "https://api-dev.oldrecroom.com/"

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
        accessToken = sessionData.accessToken;
        return accessToken;
      } else {
        return null;
      }
    })
    .catch(error => {
      console.error("Error getting token:", error);
      throw error;
    });
}

getToken()

function get(api) {
    return fetch(apiUri + api, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Failed to get data: ${response.status}`);
      }
      return response.json();
    });
  }

console.log(accessToken)