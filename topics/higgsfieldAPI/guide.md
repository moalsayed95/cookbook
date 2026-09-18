# Build Your Own AI Marketing Intern

Turn a product photo into campaign visuals with a 3D intern like Milo.

**Start with my Higgsfield link:**
https://higgsfield.ai/s/gpt-6-astra-ig-sayed.developer-lwKUde

**Why Higgsfield API?** One integration gives your app access to image and video models. Generate or edit product visuals, try different campaign directions, and bring results directly into your own workflow. Higgsfield handles the media generation; you build the experience.

## Six Steps

1. **Get API access.** Open the [Higgsfield API Console](https://console.higgsfield.ai), create a key ID and secret, and check your API balance and model pricing. My link opens the ChatGPT integration; the custom app uses the API Console instead.

2. **Ask GPT-6 Astra to build Milo.** Use a coding environment that can create files and run the app. Give it this prompt:

```text
Build a private Next.js app with a centered 3D intern named Milo,
a green shirt, glasses, and a light background. Use React Three Fiber.
Add Character, Tools, Brief, and Review steps, product-photo upload,
brand details, image/video toggles, plan approval, and result downloads.
Use OpenAI for campaign planning and Higgsfield for media generation.
Follow https://docs.higgsfield.ai for the server-side integration.
Upload references, save request IDs, poll status, and show real results.
Keep keys server-side. Require approval before paid calls.
Do not automatically retry uncertain submissions. Run and test locally.
```

3. **Connect your keys privately.** Configure `HF_API_KEY_ID` and `HF_API_KEY_SECRET` on the server. Add `OPENAI_API_KEY` for runtime planning. Never paste secrets into chat or browser code. Check each provider's billing separately.

4. **Start with one image.** Select Higgsfield's [Marketing Studio Image](https://console.higgsfield.ai/models/marketing-studio%2Fimage/api-reference). Enable image generation only, upload a product photo, and enter your product facts and audience.

5. **Give Milo a task.** Try: "Create a premium studio campaign image. Preserve the product's shape and label. Remove the original background. No invented branding." Review the plan and approve one generation.

6. **Review, download, then expand.** Wait for completion, inspect product details, and download the result. Once images work, add a video model from the API Console. Each new generation can incur a charge.

**The takeaway:** GPT helps build and plan. Higgsfield turns the approved creative direction into media.

Sources checked 2026-09-18: [API overview](https://docs.higgsfield.ai/) and [request lifecycle](https://docs.higgsfield.ai/docs/concepts/requests.md).
