import { NextResponse } from "next/server"; // next.js utility for API responses
import { put } from "@vercel/blob";
import crypto from "crypto";

// handles POST requests to this endport
export async function POST(request: Request) {
  try {
    const body = await request.json(); // extracts json data from frontend
    const { text } = body; // pulls out text property from the request body

    // TODO: Call your Image Generation API here
    // For now, we'll just echo back the text
    console.log("API key from env (length):", process.env.API_KEY?.length);
    console.log("API key from env (value):", process.env.API_KEY);

    const url = new URL(
      "https://alexwang409--sd-demo-model-generate.modal.run"
    );

    url.searchParams.set("prompt", text); // security reasons

    console.log("Requesting URl:", url.toString());

    // console.log("AKI Key:", process.env.API_KEY);

    // create a fetch request
    const response = await fetch(url.toString(), {
      method: "GET",
      headers: {
        "X-API-Key": process.env.API_KEY ?? "",
        Accept: "image/jpeg",
      },
    });

    // basic error handling
    if (!response.ok) {
      const errorText = await response.text();
      console.error("API Response:", errorText);
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${errorText}`
      );
    }

    // api request was successful
    // read data from api - asynchornous, we need to await response from frontend
    const imageBuffer = await response.arrayBuffer();

    const filename = `${crypto.randomUUID()}.jpg`; // todo: implement way to stop malicious names

    // uploading to vercel blob storage
    const blob = await put(filename, imageBuffer, {
      access: "public",
      contentType: "image/jpeg",
    });

    return NextResponse.json({
      success: true,
      imageUrl: blob.url,
    });

    // TODO IMPLEMENT: i need to store prompt and image url in a database
  } catch (error) {
    console.error("Error generating image:", error);
    return NextResponse.json(
      { success: false, error: "Failed to generate image" },
      { status: 500 }
    );
  }
}
