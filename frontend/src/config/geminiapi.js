async function runChat(query, page) {
  const API_BASE_URL = "http://3.110.50.190:8050/users";

  // Determine the endpoint based on the page
  let endpoint;
  switch (page) {
    case "text":
      endpoint = `${API_BASE_URL}/text`;
      break;
    case "summary":
      endpoint = `${API_BASE_URL}/summarizer`;
      break;
    case "images":
      endpoint = `${API_BASE_URL}/images`;
      break;
    case "memes":
      endpoint = `${API_BASE_URL}/memes`;
      break;
    case "videos":
      endpoint = `${API_BASE_URL}/video`; // Adjust if the actual endpoint differs
      break;
    default:
      throw new Error("Invalid page type");
  }

  try {
    const response = await fetch(endpoint, {
      method: "POST", // Changed to POST
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }), // Send the query in the body
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log(data)
    return data || "No response from server"; // Adjust based on API response format
  } catch (error) {
    console.error("Error in runChat:", error);
    throw error;
  }
}
export default runChat

// runChat("Create a LinkedIn Profile description", "summary")
//   .then((result) => {
//     console.log("API Response:", result);
//   })
//   .catch((error) => {
//     console.error("Error:", error);
//   });
