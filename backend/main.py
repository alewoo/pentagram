import modal
import io
from fastapi import Response, HTTPException, Query, Request # modal is fastapi under the hood
from datetime import datetime, timezone
import requests # requests to endpoints
import os # need access to env variables

def download_model():
    from diffusers import AutoPipelineForText2Image
    import torch # pytorch: used for ML capabilities

    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-turbo", 
        torch_dtype=torch.float16,
        variant="fp16" # can lower precision to make faster, but 8 bit is a little worse quality
    )

# debian slim is a Linux distribution (containirzed applications)
# spinnning up a docker container running Linux
# standalone executable package
image = (modal.Image.debian_slim().pip_install(
    "fastapi[standard]",
    "diffusers",
    "transformers",
    "accelerate",
    "requests"
    ).run_function(download_model))

# now we set up Modal app
app = modal.App("sd-demo", image=image)

# specify a decorator
@app.cls(
    image=image,
    gpu="T4", # can also use A10G
    container_idle_timeout=300,
    secrets=[modal.Secret.from_name("custom-secret")]
)

class Model:

    @modal.build()
    @modal.enter() # need to be called when the container is building and is starting
    def load_weights(self):
        from diffusers import AutoPipelineForText2Image
        import torch

        self.pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", 
            torch_dtype=torch.float16,
            variant="fp16"
        )
        self.pipe.to("cuda") #nvidia cuda is their software stack
        self.API_KEY = os.environ["API_KEY"]
        print("Loaded API Key:", self.API_KEY)

    # create our modal endpoint (api endpoint that we query from our nextjs app in the backend)
    @modal.web_endpoint()
    def generate(self, request: Request, prompt: str = Query(..., description="The prompt for image generation")):
        api_key = request.headers.get("X-API-Key")

        # securing the api key
        if api_key != self.API_KEY:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )
        
        image = self.pipe(prompt, num_inference_steps=1, guidance_scale=0.0).images[0] # increasing steps will increase quality but increase latency as well
        # create a buffer - more efficient than saving to disk

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")

        return Response(content=buffer.getvalue(), media_type="image/jpeg") 
    
        # we should always have some sort of validation on our backend to verify that the datatype that we're receiving is of an image type

    # our container doesn't spin down. keeps container and warm and doesn't shut down
    @modal.web_endpoint()
    def health(self):
        """Lightweight endpoint for keeping the container warm"""
        return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# Warm-keeping function that runs every 5 minutes
@app.function(
    schedule=modal.Cron("*/5 * * * *"),
    secrets=[modal.Secret.from_name("custom-secret")]
)
def keep_warm():
    health_url = "https://alexwang409--sd-demo-model-health.modal.run"
    generate_url = "https://alexwang409--sd-demo-model-generate.modal.run"

    # First check health endpoint (no API key needed)
    health_response = requests.get(health_url)
    print(f"Health check at: {health_response.json()['timestamp']}")

    # Then make a test request to generate endpoint with API key
    headers = {"X-API-Key": os.environ["API_KEY"]}
    generate_response = requests.get(generate_url, headers=headers, params={"prompt": "test"})
    print(f"Generate endpoint tested successfully at: {datetime.now(timezone.utc).isoformat()}")