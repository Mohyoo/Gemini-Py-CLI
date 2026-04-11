*In the name of Allah, the Entirely Merciful, the Especially Merciful*

## Privacy Summary
* If you want to help future visitors about privacy concerns, please help fulfill this page: [Gemini Terms](https://tosdr.org/en/service/7887).

* From this program's side, there is no data collection, or any anti-privacy matter (malware, adware, spyware...), but from Google's side:

1. Data Collection:
    + Default Use (Free Tier): Google can use your prompts & AI responses to develop, improve, and train its models and services.
    + Your Data is Not Private by Default: If you are using the free Google AI Studio key, you have no guarantee that your data won't be used for training.
    + Data Ownership: You retain ownership of the content you create, but you grant Google a license to use it to operate the service.
    + No Code Opt-Out: You cannot configure Google API's python library to stop data collection or training usage for standard API keys.

2. Solution:
    + Vertex AI: The only guaranteed way to ensure your data is not used is to switch to Google Cloud Vertex AI. This is a feature of their enterprise/paid service tier.
    + Data Retention: Data is generally retained for a limited period for safety monitoring and debugging, regardless of the training policy.

## Usage Advices
1. If you cancel a sent prompt earlier, Google will not receive it at all.
2. If you have a very slow internet that even browsers don't respond with:
    + Break your prompt into parts (< 100 characters).
    + Make sure the AI response will be short or broken into parts.
    + Periodically, restart both your network adapter & chat session.
    + And **BANG!** you are a network hacker!
3. The lower you set options (e.g: small history file size, simpler typing effect), the better performance & network latency you get.

## Advanced Usage Advices
1. For old consoles (e.g: Windows CMD), some features must be OFF for the program to function correctly (e.g: colors, ANSI codes, console width < 80).
2. Using /raw command can be more efficient than /upload command for short text files, because Gemini gives a higher priority to the prompt text than uploaded files.
3. Before using /upload command with text-based files (e.g: SRT, RTF, CPP, etc), change their extension to '.txt' to avoid server rejection (it's very strict). Otherwise, you can send me your preferred file types and I'll deal with them.
4. If you get API limit errors, use /switch command to update your chat temporarily & quickly; hence change your API key if you have another account, or just change the AI model; this can really help.

## Problems
+ API is genuinely limited, you are not free to write too long texts, or upload too much files, everything you do is counted.
+ Uploading feature is limited by Google (not by me); for now they support standard files like text, images, PDF, etc... but I don't know about other file types; however, you can upload up to 2GB (That doesn't mean Gemini will analyze a 2Gb file, as it contains billions of tokens; but i'll stay in Google server).
+ The command `/raw` is a fallback in case `/upload` fails, where the file content is sent as-is without uploading & saving it to google servers; but it's limited to only 20MB.
+ Gemini responses are a bit limited; for example it can send tables, but if the console is too narrow, they might look chaotic.
+ No image generation for the free tier; 'gemini-2.0-flash-preview-image-generation' was the only free image generation model, but it was removed recently.
