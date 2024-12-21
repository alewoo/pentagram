// purpose of this function is to hide the api endpoint from the client side
"use server";

export async function generateImage(text: string) {
  try {
    const response = await fetch("/api/generate-image", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-SECRET": process.env.API_SECRET || "",
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error("HTTP error! status: ${response.status}");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Server Error: ", error);
    return {
      success: false,
      error:
        error instanceof Error ? error.message : "Failed to generate image",
    };
  }
}
