# Setup notes for managing API keys and secrets for Agent MCP Tools

Do not hardcode API keys and tokens directly into `mcp.json` files. Instead, parameterize the configuration with environment variables and storing the secrets in the Apple Keychain.

**IMPORTANT:** Storing secrets in `mcp.json` exposes them to the LLM model and any memory systems integrated into agent harnesses. You must rotate these secrets either before or after moving them into the keychain.

Store secrets on the Apple Keychain:

```
security add-generic-password -s "myapp" -a "OPENAI_API_KEY" -w "sk-proj-abc123def456"
```

Verify you can retrieve the secret:

```
security find-generic-password -s "myapp" -a "OPENAI_API_KEY" -w
sk-proj-abc123def456
```

Add retrieval logic to your shell environment. Edit `~/.zshrc` with your preferred editor and add the following lines:

```
# Load keychain secret into an environment variable
export OPENAI_API_KEY=$(security find-generic-password -s "myapp" -a "OPENAI_API_KEY" -w)
```

After saving the changes to `.zshrc`, refresh your terminal session:

```
source ~/.zshrc
```

If a short-lived token is required, such as the Oauth token for the Google Cloud Resource Manager MCP server, add the env export command to the cron scheduler:

```
crontab -e
```

Then in the `crontab` editor, add the following line:

```

```

Reference: [Blog: macOS Keychain Tutorial for Developers — Store API Keys the Right Way](https://noboxdev.com/blog/macos-keychain-tutorial-for-developers)
